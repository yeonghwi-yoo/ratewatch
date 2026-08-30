# 예적금연구소 (RateWatch)

매일 갱신되는 예·적금 금리 비교 사이트.
금융감독원 「금융상품통합비교공시(금융상품 한눈에)」 오픈API 데이터를 GitHub Actions가
매일 받아 GitHub Pages(Jekyll)로 자동 배포합니다.

- 배포 주소: <https://yeonghwi-yoo.github.io/ratewatch/>
- 테마: [minimal-mistakes](https://github.com/mmistakes/minimal-mistakes) 4.26.2 (remote_theme)

## 구조

```
├── _config.yml                  # Jekyll 설정 (url/baseurl, 테마, 플러그인)
├── _data/
│   ├── navigation.yml           # 상단 내비게이션
│   ├── deposit.json             # 정기예금 데이터 (은행/저축은행)
│   └── saving.json              # 적금 데이터 (은행/저축은행)
├── _includes/
│   ├── head/custom.html         # 애드센스·서치콘솔·네이버 메타 태그 자리
│   ├── rate-table.html          # 금리 표 렌더링 include
│   └── rate-notice.html         # 데이터 출처 고지문
├── _pages/                      # 정기예금·적금·가이드·소개·개인정보처리방침·404
├── _posts/                      # 금융 가이드 글
├── index.md                     # 홈 (TOP5)
├── scripts/fetch_rates.py       # 금감원 오픈API → _data/*.json 갱신 스크립트
└── .github/workflows/
    ├── pages.yml                # main → gh-pages 미러링 (배포 트리거)
    └── update-rates.yml         # 매일 21:00 UTC(KST 06:00) 자동 갱신
```

`_data/*.json` 은 처음에는 **샘플 데이터**로 커밋되어 있으며(`is_sample: true`),
API 키를 등록하면 다음 자동 실행부터 실데이터로 교체됩니다(`is_sample: false`).
필드명은 금감원 API의 `baseList`/`optionList` 필드를 그대로 따릅니다
(`kor_co_nm`, `fin_prdt_nm`, `intr_rate`, `intr_rate2`, `dcls_month` 등).

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
bundle exec jekyll serve --baseurl /ratewatch
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

- [ ] 콘텐츠 준비: 가이드 글 확충(최소 15~20개 권장), 각 글 충분한 분량·독창성
- [ ] 필수 페이지: 소개(`/about/`), 개인정보처리방침(`/privacy/`) — 포함됨
- [ ] `_includes/head/custom.html` 의 애드센스 스크립트 주석 해제 후
      `ca-pub-XXXXXXXXXXXXXXXX` 를 본인 게시자 ID로 교체
- [ ] [Google Search Console](https://search.google.com/search-console) 등록 +
      사이트맵 제출(`/ratewatch/sitemap.xml`), 소유 확인 메타 태그는 `head/custom.html` 주석 해제
- [ ] [네이버 서치어드바이저](https://searchadvisor.naver.com) 등록(메타 태그 동일 위치)
- [ ] 애드센스 가입 → 사이트 추가 → 심사 요청 → 승인 후 광고 코드 활성화
- [ ] `ads.txt` 필요 시 루트에 추가 (승인 후 애드센스가 안내하는 내용대로)

## 고지

본 사이트의 데이터는 금융감독원 금융상품통합비교공시 기준이며,
실제 가입 조건·금리는 각 금융회사에서 확인해야 합니다.
모든 콘텐츠는 정보 제공 목적이며 투자·금융 자문이 아닙니다.
