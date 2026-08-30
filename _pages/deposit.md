---
title: "정기예금 금리 비교"
permalink: /deposit/
layout: single
author_profile: false
sidebar:
  nav: "main"
toc: true
toc_label: "바로가기"
---

은행·저축은행의 정기예금 금리를 12개월(1년) 만기 기준, 최고우대금리가 높은 순으로 비교합니다.
데이터는 금융감독원 「금융상품통합비교공시」 오픈API에서 매일 아침 자동 갱신됩니다.

## 은행 정기예금

{% include rate-table.html rows=site.data.deposit.bank %}

## 저축은행 정기예금

저축은행 예금도 예금자보호 대상입니다(1인당 1개 금융회사 기준 원금+이자 합산 한도까지).
자세한 내용은 [예금자보호 제도 가이드]({{ "/guides/deposit-insurance/" | relative_url }})를 참고하세요.

{% include rate-table.html rows=site.data.deposit.savings_bank %}

{% include rate-notice.html data=site.data.deposit %}
