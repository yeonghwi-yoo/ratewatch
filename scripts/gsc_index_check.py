#!/usr/bin/env python3
"""구글 서치콘솔 URL 검사 API로 최근 글·수정 페이지의 색인 상태를 점검한다.

- 최근 30일 안에 공개된 글 + 최근 21일 안에 수정된 글·페이지를 조사한다
- 색인이 안 됐거나, 수정 뒤 아직 재크롤링되지 않은 URL 을 "조치 필요"로 분류한다
- 구글 색인 생성 요청은 API 가 없어 자동화할 수 없다. 이 스크립트는 사람이 눌러야 할
  URL 목록을 만드는 용도다.

환경변수
  GA_KEY_FILE : 서비스 계정 키(JSON) 경로. 키는 리포에 두지 않는다.
옵션
  --days-new N   : 공개 후 N일이 지나도 색인이 없으면 조치 (기본 4)
  --days-mod N   : 수정 후 N일이 지나도 재크롤링이 없으면 조치 (기본 5)
  --json PATH    : 결과를 JSON 으로도 저장
"""
import glob
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

SITE = "https://savinglab.org"
KST = timezone(timedelta(hours=9))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def arg(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def permalink_of(path):
    try:
        head = open(os.path.join(ROOT, path), encoding="utf-8").read(4000)
    except OSError:
        return None
    m = re.search(r"^permalink:\s*(\S+)", head, re.M)
    if m:
        return m.group(1).strip("\"'")
    return "/" if path == "index.md" else None


def collect_targets():
    """{url: {"published": date|None, "changed": datetime|None}}"""
    now = datetime.now(KST)
    today = now.date()
    targets = {}

    for f in glob.glob(os.path.join(ROOT, "_posts", "*.md")):
        rel = os.path.relpath(f, ROOT)
        m = re.search(r"_posts/(\d{4}-\d{2}-\d{2})-", rel)
        if not m:
            continue
        d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        if d <= today and (today - d).days <= 30:
            u = permalink_of(rel)
            if u:
                targets.setdefault(u, {"published": d, "changed": None})

    try:
        log = subprocess.check_output(
            ["git", "log", "--since=21.days", "--name-only", "--format=@%ct"],
            cwd=ROOT, text=True)
    except subprocess.CalledProcessError:
        log = ""
    ts = None
    for line in log.splitlines():
        if line.startswith("@"):
            ts = datetime.fromtimestamp(int(line[1:]), KST)
            continue
        p = line.strip()
        if not p:
            continue
        if p.startswith("_posts/") or p.startswith("_pages/") or p == "index.md":
            u = permalink_of(p)
            if not u or u.endswith("404.html"):
                continue
            pub = None
            m = re.search(r"_posts/(\d{4}-\d{2}-\d{2})-", p)
            if m:
                pub = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                if pub > today:
                    continue  # 아직 공개 안 된 예약 글
            t = targets.setdefault(u, {"published": pub, "changed": None})
            if t["changed"] is None or ts > t["changed"]:
                t["changed"] = ts
    return targets


def inspect_all(targets):
    from google.oauth2 import service_account
    import google.auth.transport.requests as gtr
    c = service_account.Credentials.from_service_account_file(
        os.environ["GA_KEY_FILE"], scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    c.refresh(gtr.Request())
    H = {"Authorization": f"Bearer {c.token}", "Content-Type": "application/json"}

    def call(u, p=None):
        r = urllib.request.Request(u, data=json.dumps(p).encode() if p else None, headers=H)
        try:
            return json.load(urllib.request.urlopen(r, timeout=60))
        except urllib.error.HTTPError as e:
            return {"__error": e.code, "body": e.read().decode()[:200]}

    sites = call("https://searchconsole.googleapis.com/webmasters/v3/sites").get("siteEntry", [])
    prop = next((s["siteUrl"] for s in sites if "savinglab" in s["siteUrl"]), None)
    if not prop:
        sys.exit("서치콘솔에 savinglab 속성이 없습니다(서비스 계정 권한 확인).")

    out = []
    for path, meta in sorted(targets.items()):
        r = call("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                 {"inspectionUrl": SITE + path, "siteUrl": prop, "languageCode": "ko"})
        if "__error" in r:
            out.append({"path": path, "error": f"{r['__error']} {r['body'][:80]}"})
            continue
        ir = r["inspectionResult"]["indexStatusResult"]
        crawl = ir.get("lastCrawlTime")
        out.append({
            "path": path,
            "verdict": ir.get("verdict"),
            "coverage": ir.get("coverageState", ""),
            "last_crawl": crawl,
            "published": str(meta["published"]) if meta["published"] else None,
            "changed": meta["changed"].isoformat() if meta["changed"] else None,
        })
    return out


def classify(rows, days_new, days_mod):
    now = datetime.now(KST)
    for r in rows:
        if "error" in r:
            r["action"] = "오류"
            continue
        crawl = datetime.fromisoformat(r["last_crawl"].replace("Z", "+00:00")) if r.get("last_crawl") else None
        changed = datetime.fromisoformat(r["changed"]) if r.get("changed") else None
        published = datetime.strptime(r["published"], "%Y-%m-%d").replace(tzinfo=KST) if r.get("published") else None
        ref = max([d for d in (changed, published) if d] or [now])
        age = (now - ref).days
        if r["verdict"] != "PASS":
            r["action"] = "색인 요청" if age >= days_new else f"대기 ({age}일차)"
        elif changed and crawl and crawl < changed and age >= days_mod:
            r["action"] = "재크롤링 요청"
        elif changed and crawl and crawl < changed:
            r["action"] = f"대기 (수정 {age}일차)"
        else:
            r["action"] = "정상"
    return rows


def main():
    days_new = int(arg("--days-new", 4))
    days_mod = int(arg("--days-mod", 5))
    targets = collect_targets()
    if not targets:
        print("점검 대상 URL 없음")
        return 0
    rows = classify(inspect_all(targets), days_new, days_mod)

    print(f"{'경로':36} {'색인':8} {'마지막 크롤링':12} 판정")
    for r in rows:
        crawl = (r.get("last_crawl") or "-")[:10]
        print(f"{r['path']:36} {str(r.get('verdict','-')):8} {crawl:12} {r['action']}")

    todo = [r for r in rows if r["action"] in ("색인 요청", "재크롤링 요청")]
    print()
    if todo:
        print("서치콘솔에서 '색인 생성 요청'을 눌러야 할 URL:")
        for r in todo:
            print(f"  {SITE}{r['path']}   ({r['action']})")
    else:
        print("조치가 필요한 URL 없음")

    if "--json" in sys.argv:
        with open(arg("--json", "gsc_index.json"), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
