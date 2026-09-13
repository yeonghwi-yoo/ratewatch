# 예적금연구소 (RateWatch)

매일 갱신되는 예·적금 금리 비교 사이트.
금융감독원 「금융상품통합비교공시(금융상품 한눈에)」 오픈API 데이터를 GitHub Actions가
매일 받아 GitHub Pages(Jekyll)로 자동 배포합니다.

- 배포 주소: <https://savinglab.org/> (커스텀 도메인, 루트 `CNAME` 파일로 연결 · 옛 주소 yeonghwi-yoo.github.io/ratewatch 는 자동 리다이렉트)
- 테마: [minimal-mistakes](https://github.com/mmistakes/minimal-mistakes) 4.26.2 (remote_theme)

## 구조

```
├── _config.yml                  # Jekyll 설정 (url/baseurl, 테마, 플러그인)
├── _data/
│   ├── navigation.yml           # 상단 내비게이션
│   ├── deposit.json             # 정기예금 (은행/저축은행, 12개월 + by_term 만기별 6/12/24/36)
│   ├── saving.json              # 적금 (동일 구조)
│   ├── terms.yml                # 만기 탭 정의
│   ├── ui-text.yml              # 테마 UI 문자열 한국어
│   ├── mortgage.json            # 주택담보대출
│   ├── rent_loan.json           # 전세자금대출
│   ├── credit_loan.json         # 개인신용대출 (신용점수 구간별)
│   └── rate_history.json        # 일별 요약 지표 누적 (금리 추이용)
├── _includes/
│   ├── head/custom.html         # GA4·파비콘·RSS·애드센스·서치콘솔·네이버 메타
│   ├── rate-table.html          # 예·적금 표 include
│   ├── term-page.html / term-tabs.html  # 만기별 비교 페이지 본문·탭
│   ├── page__related.html       # 글 하단 관련 글(topics 기반) + 비교 페이지 링크
│   ├── analytics.html           # 비워 둠 (테마의 body 끝 삽입을 끄고 head 에서 삽입)
│   ├── topic-guides.html        # 비교 페이지 하단 관련 가이드 카드
│   ├── loan-table-*.html        # 대출 표 include (담보대출/신용대출)
│   ├── loan-stat-cards.html     # 대출 최저금리 요약 카드
│   └── *-notice.html            # 데이터 출처 고지문
├── _pages/                      # 정기예금·적금(12개월 + 6/24/36개월)·대출(허브+3종)·가이드·소개·개인정보처리방침·404
├── assets/images/               # 파비콘·OG 공유 이미지
├── _posts/                      # 금융 가이드 글
├── index.md                     # 홈 (TOP5)
├── sitemap.xml                  # 직접 작성한 사이트맵 (lastmod 포함)
├── rss.xml                      # RSS 2.0 피드 (네이버 서치어드바이저 제출용)
├── scripts/fetch_rates.py       # 금감원 오픈API → _data/*.json 갱신 스크립트
└── .github/workflows/
    ├── pages.yml                # main → gh-pages 미러링 (배포 트리거)
    └── update-rates.yml         # 매일 21:00 UTC(KST 06:00) 자동 갱신
```

`_data/*.json` 은 처음에는 **샘플 데이터**로 커밋되어 있으며(`is_sample: true`),
API 키를 등록하면 다음 자동 실행부터 실데이터로 교체됩니다(`is_sample: false`).
필드명은 금감원 API의 `baseList`/`optionList` 필드를 그대로 따릅니다
(`kor_co_nm`, `fin_prdt_nm`, `intr_rate`, `intr_rate2`, `dcls_month` 등).
`bank`/`savings_bank` 는 12개월 기준 목록이고, `by_term["6"|"12"|"24"|"36"]` 에 만기별 목록이 함께 저장됩니다.

`sitemap.xml` 은 직접 작성한 템플릿입니다(jekyll-sitemap 은 소스에 파일이 있으면 생성을 건너뜁니다).
`<lastmod>` 는 페이지 front matter 의 `lastmod_data` 가 가리키는 `_data` 파일의 `content_changed_at`
값을 씁니다. 이 값은 `fetch_rates.py` 가 **금리 내용이 실제로 바뀐 날에만** 갱신하므로,
매일 재실행돼도 내용이 같으면 수정일이 그대로 유지됩니다.

검색엔진 제출 현황: 구글 서치콘솔·네이버 서치어드바이저에 `sitemap.xml` 제출 완료.
네이버는 `rss.xml` 을 "요청 → RSS 제출"에 함께 등록합니다. 테마가 만드는 `/feed.xml` 은
Atom 형식이라 네이버용으로는 RSS 2.0 인 `/rss.xml` 을 따로 둡니다.

글(`_posts`)의 front matter `topics: [deposit, saving, loan, tax, youth, basics]` 는
글 하단 관련 글 추천과 비교 페이지의 관련 가이드 카드에 사용됩니다. 새 글에도 반드시 넣으세요.

대출 3종(`mortgage`, `rent_loan`, `credit_loan`)은 `pending: true` 상태로 시작하며 첫 워크플로 실행 시
실데이터로 채워집니다. 대출 수집이 실패해도 예·적금 갱신은 계속되고 해당 파일은 이전 값을 유지합니다.
`rate_history.json`에는 매 실행마다 하루 한 줄(최고금리·상위5 평균·대출 최저금리 등)이 누적되어
추후 금리 추이 차트에 사용합니다.

## FSS_API_KEY 발급 및 등록

1. **인증키 신청**: [finlife.fss.or.kr](https://finlife.fss.or.kr) → 오픈API → 인증키 신청.
   이메일로 인증키를 발급받습니다.
2. **Secret 등록**: 이 리포지토리 → **Settings → Secrets and variables → Actions →
   New repository secret** → Name: `FSS_API_KEY`, Value: 발급받은 인증키.
3. **수동 실행으로 확인**: **Actions → update-rates → Run workflow** 를 실행하면
   `_data/deposit.json`, `_data/saving.json` 이 실데이터로 갱신·커밋되고,
   푸시에 의해 GitHub Pages가 자동 재배포됩니다.
   - Secret 미등록 상태에서는 안내 메시지를 출력하고 정상 종료합니다.

이후에는 매일 21:00 UTC(한국 시간 오전 6시)에 자동으로 갱신됩니다.

## 로컬 미리보기 (선택)

```bash
gem install bundler jekyll
bundle init && bundle add github-pages --group jekyll_plugins
bundle exec jekyll serve
```

### 배포 방식

- 개발·콘텐츠 작업은 모두 **main** 브랜치에서 합니다.
- main에 푸시하면 `sync-to-pages` 워크플로가 main을 배포 브랜치 **gh-pages**로 미러링하고,
  GitHub Pages가 gh-pages를 소스로 기본 Jekyll 빌드(`pages build and deployment`)를 실행해
  사이트를 배포합니다. gh-pages에는 직접 커밋하지 마세요.
- 이렇게 구성한 이유: 브랜치 방식 Pages 활성화는 저장소 관리자 권한이 필요해
  워크플로 토큰으로 설정할 수 없고, gh-pages 브랜치 생성 시 Pages가 자동 활성화되는
  동작을 이용했습니다. 원하면 Settings → Pages에서 소스를 main으로 바꾸고
  `pages.yml`(sync-to-pages)을 삭제해 단순화할 수 있습니다.

## 애드센스 체크리스트

- [x] 콘텐츠 준비: 가이드 34편(10/31까지 예약 발행), 비교 페이지 13개에 표 아래 설명 본문 1,000자 이상
- [ ] 필수 페이지: 소개(`/about/`), 개인정보처리방침(`/privacy/`) — 포함됨
- [x] 애드센스 스크립트(`ca-pub-7635369920244942`) 전 페이지 head 삽입, 루트 `ads.txt` 배포
- [ ] [Google Search Console](https://search.google.com/search-console) 등록 +
      사이트맵 제출(`https://savinglab.org/sitemap.xml`), 소유 확인 메타 태그는 `head/custom.html` 주석 해제
- [x] [네이버 서치어드바이저](https://searchadvisor.naver.com) 등록 + 사이트맵·RSS(`/rss.xml`) 제출
- [x] 구글 애널리틱스(GA4) 연동 완료. 측정 ID는 `_config.yml` 의
      `analytics.google.tracking_id` 한 곳에서 관리하며, 비우면 스크립트가 삽입되지 않음
- [ ] 애드센스 가입 → 사이트 추가 → 심사 요청 → 승인 후 광고 코드 활성화

## 고지

본 사이트의 데이터는 금융감독원 금융상품통합비교공시 기준이며,
실제 가입 조건·금리는 각 금융회사에서 확인해야 합니다.
모든 콘텐츠는 정보 제공 목적이며 투자·금융 자문이 아닙니다.
