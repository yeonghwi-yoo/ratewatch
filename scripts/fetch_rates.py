#!/usr/bin/env python3
"""금융감독원 금융상품통합비교공시(금융상품 한눈에) 오픈API에서
예·적금과 대출 금리를 받아 _data/*.json 으로 저장한다.

- 표준 라이브러리만 사용 (urllib, json)
- 예·적금: 12개월(save_trm == "12") 옵션 기준, 최고우대금리(intr_rate2) 내림차순
  + 만기별(6/12/24/36개월) 목록을 by_term 에 함께 저장 (만기별 비교 페이지용)
- 주택담보대출·전세자금대출: 옵션(담보/상환/금리유형)별 행, 최저금리 오름차순
- 개인신용대출: 신용점수 구간별 대출금리(crdt_lend_rate_type == "A"), 평균금리 오름차순
- 권역: 020000(은행) → "bank", 030300(저축은행) → "savings_bank"
- 매 실행마다 요약 지표를 _data/rate_history.json 에 하루 한 줄 누적 (금리 추이용)
- 인증키: 환경변수 FSS_API_KEY

대출 수집이 실패해도 예·적금 갱신은 계속되며, 실패한 대출 파일은 이전 값을 유지한다.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

API_BASE = "https://finlife.fss.or.kr/finlifeapi"

# 예·적금 (필수 — 실패 시 종료 코드 1)
PRODUCTS = {
    "deposit": "depositProductsSearch.json",
    "saving": "savingProductsSearch.json",
}

# 대출 (선택 — 실패 시 경고만 출력하고 계속)
LOAN_PRODUCTS = {
    "mortgage": "mortgageLoanProductsSearch.json",      # 주택담보대출
    "rent_loan": "rentHouseLoanProductsSearch.json",    # 전세자금대출
    "credit_loan": "creditLoanProductsSearch.json",     # 개인신용대출
}

FIN_GROUPS = {
    "bank": "020000",          # 은행
    "savings_bank": "030300",  # 저축은행
}

TARGET_TERM = "12"  # 예·적금 12개월 기준
TERMS = ("6", "12", "24", "36")  # 만기별 비교 페이지에 쓰는 만기(개월)

KST = timezone(timedelta(hours=9))

# 신용대출 신용점수 구간 필드 (API 필드명 → 표시 라벨)
CREDIT_GRADE_FIELDS = [
    ("crdt_grad_1", "900점 초과"),
    ("crdt_grad_4", "801~900점"),
    ("crdt_grad_5", "701~800점"),
    ("crdt_grad_6", "601~700점"),
    ("crdt_grad_10", "501~600점"),
    ("crdt_grad_11", "401~500점"),
    ("crdt_grad_12", "301~400점"),
    ("crdt_grad_13", "300점 이하"),
]


# ---------------------------------------------------------------------------
# API 호출
# ---------------------------------------------------------------------------

def fetch_page(endpoint: str, auth_key: str, fin_grp: str, page_no: int) -> dict:
    params = urllib.parse.urlencode({
        "auth": auth_key,
        "topFinGrpNo": fin_grp,
        "pageNo": page_no,
    })
    url = f"{API_BASE}/{endpoint}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "ratewatch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    data = json.loads(body)
    result = data.get("result")
    if not result:
        raise RuntimeError(f"API 응답에 result가 없습니다: {body[:300]}")
    err_cd = result.get("err_cd")
    if err_cd != "000":
        raise RuntimeError(
            f"API 오류 (err_cd={err_cd}): {result.get('err_msg')}"
        )
    return result


def fetch_all(endpoint: str, auth_key: str, fin_grp: str):
    """모든 페이지의 baseList / optionList 를 합쳐서 반환한다."""
    base_list, option_list = [], []
    page_no = 1
    while True:
        result = fetch_page(endpoint, auth_key, fin_grp, page_no)
        base_list.extend(result.get("baseList") or [])
        option_list.extend(result.get("optionList") or [])
        max_page = int(result.get("max_page_no") or 1)
        if page_no >= max_page:
            break
        page_no += 1
    return base_list, option_list


# ---------------------------------------------------------------------------
# 공통 유틸
# ---------------------------------------------------------------------------

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def base_index(base_list):
    return {(b.get("fin_co_no"), b.get("fin_prdt_cd")): b for b in base_list}


def sort_key_asc(value):
    """None(미공시)을 뒤로 보내는 오름차순 정렬 키."""
    return (value is None, value if value is not None else 0.0)


# ---------------------------------------------------------------------------
# 예·적금
# ---------------------------------------------------------------------------

def build_rows(base_list, option_list, term=TARGET_TERM):
    """baseList와 optionList를 상품 단위로 합쳐 해당 만기(term)의 최고우대금리 순으로 정렬한다."""
    base_by_key = base_index(base_list)

    best_option = {}
    for opt in option_list:
        if str(opt.get("save_trm")) != str(term):
            continue
        rate2 = to_float(opt.get("intr_rate2"))
        if rate2 is None:
            continue
        key = (opt.get("fin_co_no"), opt.get("fin_prdt_cd"))
        current = best_option.get(key)
        if current is None or rate2 > to_float(current.get("intr_rate2")):
            best_option[key] = opt

    rows = []
    for key, opt in best_option.items():
        base = base_by_key.get(key)
        if base is None:
            continue
        row = {
            "dcls_month": base.get("dcls_month"),
            "kor_co_nm": base.get("kor_co_nm"),
            "fin_prdt_cd": base.get("fin_prdt_cd"),
            "fin_prdt_nm": base.get("fin_prdt_nm"),
            "intr_rate_type_nm": opt.get("intr_rate_type_nm"),
            "save_trm": str(opt.get("save_trm")),
            "intr_rate": to_float(opt.get("intr_rate")),
            "intr_rate2": to_float(opt.get("intr_rate2")),
            "spcl_cnd": base.get("spcl_cnd"),
            "join_way": base.get("join_way"),
            "max_limit": base.get("max_limit"),
        }
        if opt.get("rsrv_type_nm"):
            row["rsrv_type_nm"] = opt.get("rsrv_type_nm")
        rows.append(row)

    rows.sort(key=lambda r: (r["intr_rate2"] or 0.0), reverse=True)
    return rows


# ---------------------------------------------------------------------------
# 대출
# ---------------------------------------------------------------------------

def build_secured_loan_rows(base_list, option_list):
    """주택담보대출·전세자금대출: 옵션(담보유형/상환방식/금리유형)별 한 행.
    최저금리(lend_rate_min) → 평균금리 오름차순."""
    base_by_key = base_index(base_list)
    rows = []
    for opt in option_list:
        key = (opt.get("fin_co_no"), opt.get("fin_prdt_cd"))
        base = base_by_key.get(key)
        if base is None:
            continue
        rows.append({
            "dcls_month": base.get("dcls_month"),
            "kor_co_nm": base.get("kor_co_nm"),
            "fin_prdt_cd": base.get("fin_prdt_cd"),
            "fin_prdt_nm": base.get("fin_prdt_nm"),
            "mrtg_type_nm": opt.get("mrtg_type_nm"),          # 주담대만 (아파트/아파트외)
            "rpay_type_nm": opt.get("rpay_type_nm"),          # 분할상환/만기일시상환
            "lend_rate_type_nm": opt.get("lend_rate_type_nm"),  # 고정/변동
            "lend_rate_min": to_float(opt.get("lend_rate_min")),
            "lend_rate_max": to_float(opt.get("lend_rate_max")),
            "lend_rate_avg": to_float(opt.get("lend_rate_avg")),  # 전월 취급 평균
            "loan_lmt": base.get("loan_lmt"),
            "erly_rpay_fee": base.get("erly_rpay_fee"),
            "dly_rate": base.get("dly_rate"),
            "join_way": base.get("join_way"),
        })
    rows.sort(key=lambda r: (sort_key_asc(r["lend_rate_min"]), sort_key_asc(r["lend_rate_avg"])))
    return rows


def build_credit_loan_rows(base_list, option_list):
    """개인신용대출: 상품별 '대출금리'(crdt_lend_rate_type == "A") 옵션 한 행.
    신용점수 구간별 금리 + 평균금리, 평균금리 오름차순."""
    base_by_key = base_index(base_list)
    rows = []
    for opt in option_list:
        rate_type = opt.get("crdt_lend_rate_type")
        if rate_type is not None and rate_type != "A":
            continue  # 기준금리/가산금리/가감조정금리는 제외, 대출금리만
        key = (opt.get("fin_co_no"), opt.get("fin_prdt_cd"))
        base = base_by_key.get(key)
        if base is None:
            continue
        row = {
            "dcls_month": base.get("dcls_month"),
            "kor_co_nm": base.get("kor_co_nm"),
            "fin_prdt_cd": base.get("fin_prdt_cd"),
            "fin_prdt_nm": base.get("fin_prdt_nm"),
            "crdt_prdt_type_nm": base.get("crdt_prdt_type_nm") or opt.get("crdt_prdt_type_nm"),
            "cb_name": base.get("cb_name"),
            "join_way": base.get("join_way"),
            "crdt_grad_avg": to_float(opt.get("crdt_grad_avg")),
        }
        for field, _label in CREDIT_GRADE_FIELDS:
            row[field] = to_float(opt.get(field))
        rows.append(row)
    rows.sort(key=lambda r: sort_key_asc(r["crdt_grad_avg"]))
    return rows


LOAN_BUILDERS = {
    "mortgage": build_secured_loan_rows,
    "rent_loan": build_secured_loan_rows,
    "credit_loan": build_credit_loan_rows,
}


# ---------------------------------------------------------------------------
# 금리 추이 누적
# ---------------------------------------------------------------------------

def _min_field(rows, field):
    vals = [r[field] for r in rows if r.get(field) is not None]
    return min(vals) if vals else None


def _top_avg(rows, field, n=5):
    vals = [r[field] for r in rows[:n] if r.get(field) is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


def append_history(out_dir, today, dcls_month, payloads):
    """하루 한 줄 요약 지표를 _data/rate_history.json 에 누적한다."""
    path = os.path.join(out_dir, "rate_history.json")
    history = []
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                history = json.load(f)
        except (OSError, ValueError):
            history = []
    if history and history[-1].get("date") == today:
        print("금리 추이: 오늘 항목이 이미 있어 건너뜁니다.")
        return

    dep = payloads.get("deposit") or {}
    sav = payloads.get("saving") or {}
    mort = payloads.get("mortgage") or {}
    rent = payloads.get("rent_loan") or {}
    cred = payloads.get("credit_loan") or {}

    entry = {
        "date": today,
        "dcls_month": dcls_month,
        # 예·적금: 최고우대금리 최대값 / 상위5 평균 (rows는 내림차순 정렬 상태)
        "deposit_bank_max": (dep.get("bank") or [{}])[0].get("intr_rate2"),
        "deposit_bank_top5_avg": _top_avg(dep.get("bank") or [], "intr_rate2"),
        "deposit_sb_max": (dep.get("savings_bank") or [{}])[0].get("intr_rate2"),
        "deposit_sb_top5_avg": _top_avg(dep.get("savings_bank") or [], "intr_rate2"),
        "saving_bank_max": (sav.get("bank") or [{}])[0].get("intr_rate2"),
        "saving_sb_max": (sav.get("savings_bank") or [{}])[0].get("intr_rate2"),
        # 대출: 은행 기준 최저금리 / 신용대출 최저 평균금리
        "mortgage_bank_min": _min_field(mort.get("bank") or [], "lend_rate_min"),
        "rent_bank_min": _min_field(rent.get("bank") or [], "lend_rate_min"),
        "credit_bank_avg_min": _min_field(cred.get("bank") or [], "crdt_grad_avg"),
    }
    history.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"금리 추이 누적: {today} (총 {len(history)}일)")


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------

def collect(endpoint, auth_key, builder, label, by_term=False):
    """권역별로 API를 받아 builder로 행을 만든다.
    by_term=True 이면 TERMS 각각의 목록을 payload["by_term"][term][group] 에도 저장한다."""
    payload = {
        "is_sample": False,
        "pending": False,
        "generated_at": datetime.now(KST).isoformat(timespec="seconds"),
        "dcls_month": None,
    }
    if by_term:
        payload["by_term"] = {t: {} for t in TERMS}
    for group_key, fin_grp in FIN_GROUPS.items():
        base_list, option_list = fetch_all(endpoint, auth_key, fin_grp)
        rows = builder(base_list, option_list)
        payload[group_key] = rows
        if rows and not payload["dcls_month"]:
            payload["dcls_month"] = rows[0].get("dcls_month")
        print(f"{label}/{group_key}: {len(rows)}건")
        if by_term:
            for term in TERMS:
                term_rows = rows if term == TARGET_TERM else builder(base_list, option_list, term)
                payload["by_term"][term][group_key] = term_rows
                print(f"{label}/{group_key}/{term}개월: {len(term_rows)}건")
    return payload


def write_json(out_dir, name, payload):
    out_path = os.path.join(out_dir, f"{name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"저장 완료: {out_path}")


def main() -> int:
    auth_key = os.environ.get("FSS_API_KEY", "").strip()
    if not auth_key:
        print("FSS_API_KEY 환경변수가 설정되지 않았습니다.")
        print("finlife.fss.or.kr 에서 오픈API 인증키를 발급받아 등록하세요.")
        return 1

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data")
    os.makedirs(out_dir, exist_ok=True)
    payloads = {}

    # 1) 예·적금 (필수)
    for name, endpoint in PRODUCTS.items():
        payload = collect(endpoint, auth_key, build_rows, name, by_term=True)
        payload["save_trm"] = TARGET_TERM
        write_json(out_dir, name, payload)
        payloads[name] = payload

    # 2) 대출 (선택: 실패해도 계속)
    for name, endpoint in LOAN_PRODUCTS.items():
        try:
            payload = collect(endpoint, auth_key, LOAN_BUILDERS[name], name)
            write_json(out_dir, name, payload)
            payloads[name] = payload
        except Exception as exc:  # noqa: BLE001 — 대출 실패는 경고만
            print(f"::warning::{name} 수집 실패, 이전 데이터 유지: {exc}")

    # 3) 금리 추이 누적
    today = datetime.now(KST).strftime("%Y-%m-%d")
    dcls_month = payloads["deposit"].get("dcls_month")
    try:
        append_history(out_dir, today, dcls_month, payloads)
    except Exception as exc:  # noqa: BLE001
        print(f"::warning::금리 추이 누적 실패: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
