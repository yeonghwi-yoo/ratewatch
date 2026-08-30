#!/usr/bin/env python3
"""금융감독원 금융상품통합비교공시(금융상품 한눈에) 오픈API에서
정기예금·적금 금리를 받아 _data/deposit.json, _data/saving.json 으로 저장한다.

- 표준 라이브러리만 사용 (urllib, json)
- 12개월(save_trm == "12") 옵션 기준, 최고우대금리(intr_rate2) 내림차순 정렬
- 권역: 020000(은행) → "bank", 030300(저축은행) → "savings_bank"
- 인증키: 환경변수 FSS_API_KEY
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

API_BASE = "https://finlife.fss.or.kr/finlifeapi"

PRODUCTS = {
    "deposit": "depositProductsSearch.json",
    "saving": "savingProductsSearch.json",
}

FIN_GROUPS = {
    "bank": "020000",          # 은행
    "savings_bank": "030300",  # 저축은행
}

TARGET_TERM = "12"  # 12개월 기준

KST = timezone(timedelta(hours=9))


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


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_rows(base_list, option_list):
    """baseList와 optionList를 상품 단위로 합쳐 12개월 최고우대금리 순으로 정렬한다."""
    base_by_key = {
        (b.get("fin_co_no"), b.get("fin_prdt_cd")): b for b in base_list
    }

    # 상품별로 12개월 옵션 중 최고우대금리가 가장 높은 옵션을 고른다
    best_option = {}
    for opt in option_list:
        if str(opt.get("save_trm")) != TARGET_TERM:
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
        if opt.get("rsrv_type_nm"):  # 적금만 있는 필드(정액/자유적립식)
            row["rsrv_type_nm"] = opt.get("rsrv_type_nm")
        rows.append(row)

    rows.sort(key=lambda r: (r["intr_rate2"] or 0.0), reverse=True)
    return rows


def main() -> int:
    auth_key = os.environ.get("FSS_API_KEY", "").strip()
    if not auth_key:
        print("FSS_API_KEY 환경변수가 설정되지 않았습니다.")
        print("finlife.fss.or.kr 에서 오픈API 인증키를 발급받아 등록하세요.")
        return 1

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data")
    os.makedirs(out_dir, exist_ok=True)

    for name, endpoint in PRODUCTS.items():
        payload = {
            "is_sample": False,
            "generated_at": datetime.now(KST).isoformat(timespec="seconds"),
            "dcls_month": None,
            "save_trm": TARGET_TERM,
        }
        for group_key, fin_grp in FIN_GROUPS.items():
            base_list, option_list = fetch_all(endpoint, auth_key, fin_grp)
            rows = build_rows(base_list, option_list)
            payload[group_key] = rows
            if rows and not payload["dcls_month"]:
                payload["dcls_month"] = rows[0].get("dcls_month")
            print(f"{name}/{group_key}: 상품 {len(rows)}건 (12개월 기준)")

        out_path = os.path.join(out_dir, f"{name}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"저장 완료: {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
