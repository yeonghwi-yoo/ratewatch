---
title: "적금 금리 비교"
permalink: /saving/
layout: single
author_profile: false
sidebar:
  nav: "main"
toc: true
toc_label: "바로가기"
---

은행·저축은행의 적금 금리를 12개월(1년) 만기 기준, 최고우대금리가 높은 순으로 비교합니다.
데이터는 금융감독원 「금융상품통합비교공시」 오픈API에서 매일 아침 자동 갱신됩니다.

적금의 우대금리는 급여이체·카드실적·자동이체 등 조건이 붙는 경우가 많으니
가입 전 우대조건 충족 가능 여부를 반드시 확인하세요.

## 은행 적금

{% include rate-table.html rows=site.data.saving.bank %}

## 저축은행 적금

{% include rate-table.html rows=site.data.saving.savings_bank %}

{% include rate-notice.html data=site.data.saving %}
