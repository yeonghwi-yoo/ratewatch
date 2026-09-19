#!/usr/bin/env python3
"""IndexNow 제출 — 새로 공개된 글과 내용이 바뀐 페이지 URL을 네이버·빙 등 참여 검색엔진에 알린다.

구글은 IndexNow에 참여하지 않으므로 이 스크립트로는 반영되지 않는다(사이트맵으로 자동 발견).

사용법
  python3 scripts/indexnow.py --auto                 # 최근 커밋에서 바뀐 파일로 URL 추정
  python3 scripts/indexnow.py --urls /a/,/b/         # 지정한 경로만 제출
  옵션 --dry-run : 제출하지 않고 URL 목록만 출력
  환경변수 INDEXNOW_BEFORE : --auto 에서 비교할 이전 커밋 (기본 HEAD~1)

키 파일: 루트의 <32자 hex>.txt (IndexNow 규약상 공개 파일이며 비밀이 아니다)
"""
import glob
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

SITE = "https://savinglab.org"
HOST = "savinglab.org"
KST = timezone(timedelta(hours=9))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# _data 파일이 바뀌었을 때 내용이 달라지는 페이지
DATA_PAGES = {
    "deposit": ["/", "/deposit/", "/deposit/6m/", "/deposit/24m/", "/deposit/36m/"],
    "saving": ["/", "/saving/", "/saving/6m/", "/saving/24m/", "/saving/36m/"],
    "mortgage": ["/", "/loans/", "/loans/mortgage/"],
    "rent_loan": ["/", "/loans/", "/loans/rent/"],
    "credit_loan": ["/", "/loans/", "/loans/credit/"],
}


def find_key():
    files = [f for f in glob.glob(os.path.join(ROOT, "*.txt"))
             if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(f))]
    if not files:
        sys.exit("IndexNow 키 파일(<32자 hex>.txt)이 루트에 없습니다.")
    key = open(files[0], encoding="utf-8").read().strip()
    return key, os.path.basename(files[0])


def permalink_of(path):
    """마크다운 파일의 permalink 를 읽는다. 없으면 None."""
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            head = f.read(4000)
    except OSError:
        return None
    m = re.search(r"^permalink:\s*(\S+)", head, re.M)
    if m:
        return m.group(1).strip('"\'')
    return "/" if path == "index.md" else None


def post_date(path):
    m = re.search(r"_posts/(\d{4}-\d{2}-\d{2})-", path)
    return m.group(1) if m else None


def content_changed_today(name, today):
    try:
        with open(os.path.join(ROOT, "_data", f"{name}.json"), encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return False
    return str(d.get("content_changed_at", ""))[:10] == today


def auto_urls():
    today = datetime.now(KST).strftime("%Y-%m-%d")
    urls = []

    # 1) 오늘 날짜로 공개되는 글
    for f in glob.glob(os.path.join(ROOT, "_posts", f"{today}-*.md")):
        rel = os.path.relpath(f, ROOT)
        p = permalink_of(rel)
        if p:
            urls.append(p)

    # 2) 최근 커밋에서 바뀐 파일
    before = os.environ.get("INDEXNOW_BEFORE") or "HEAD~1"
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", f"{before}..HEAD"],
                                      cwd=ROOT, text=True)
    except subprocess.CalledProcessError:
        out = ""
    for path in out.split():
        if path.startswith("_posts/"):
            d = post_date(path)
            if d and d <= today:              # 예약 글(미래)은 제외
                p = permalink_of(path)
                if p:
                    urls.append(p)
        elif path.startswith("_pages/") or path == "index.md":
            p = permalink_of(path)
            if p and not p.endswith("404.html"):
                urls.append(p)
        elif path.startswith("_data/"):
            name = os.path.basename(path)[:-5]
            if name in DATA_PAGES and content_changed_today(name, today):
                urls.extend(DATA_PAGES[name])

    seen, result = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def submit(paths, dry_run=False):
    key, key_file = find_key()
    full = [SITE + p for p in paths]
    print(f"제출 대상 {len(full)}개:")
    for u in full:
        print("  ", u)
    if dry_run or not full:
        return 0
    body = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"{SITE}/{key_file}",
        "urlList": full,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body,
        headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow 응답: {resp.status}")
            return 0
    except urllib.error.HTTPError as e:
        print(f"::warning::IndexNow 오류 {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")
        return 0  # 제출 실패가 배포를 막지 않도록
    except Exception as e:  # noqa: BLE001
        print(f"::warning::IndexNow 요청 실패: {e}")
        return 0


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    if "--urls" in args:
        raw = args[args.index("--urls") + 1]
        paths = [p.strip() for p in raw.split(",") if p.strip()]
    elif "--auto" in args:
        paths = auto_urls()
    else:
        sys.exit(__doc__)
    if not paths:
        print("제출할 URL이 없습니다.")
        return 0
    return submit(paths, dry_run=dry)


if __name__ == "__main__":
    sys.exit(main())
