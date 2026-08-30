---
layout: single
title: "오늘의 예·적금 금리 TOP5"
author_profile: false
sidebar:
  nav: "main"
---

**레이트워치**는 금융감독원 「금융상품통합비교공시(금융상품 한눈에)」 오픈API 데이터를
매일 아침 자동으로 받아 은행·저축은행의 정기예금·적금 금리를 비교해 보여주는 사이트입니다.
아래 표는 12개월(1년) 만기 기준 최고우대금리 상위 5개 상품입니다.

## 🏦 은행 정기예금 TOP5

{% include rate-table.html rows=site.data.deposit.bank limit=5 %}

## 🏦 저축은행 정기예금 TOP5

{% include rate-table.html rows=site.data.deposit.savings_bank limit=5 %}

[👉 정기예금 전체 금리 비교 보기]({{ "/deposit/" | relative_url }})

## 💰 은행 적금 TOP5

{% include rate-table.html rows=site.data.saving.bank limit=5 %}

## 💰 저축은행 적금 TOP5

{% include rate-table.html rows=site.data.saving.savings_bank limit=5 %}

[👉 적금 전체 금리 비교 보기]({{ "/saving/" | relative_url }})

{% include rate-notice.html data=site.data.deposit %}

---

## 📚 금융 가이드

- [신용점수 올리는 방법 — 실제 평가에 반영되는 것만 정리]({{ "/guides/credit-score/" | relative_url }})
- [예금자보호 제도 정확히 이해하기 — 저축은행 고금리, 안전할까]({{ "/guides/deposit-insurance/" | relative_url }})
- [정기예금 vs 파킹통장 vs CMA — 구조부터 다른 세 가지 통장]({{ "/guides/deposit-parking-cma/" | relative_url }})

<small>본 사이트의 모든 정보는 참고용이며 투자·금융 자문이 아닙니다.</small>
