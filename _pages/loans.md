---
title: "대출 금리 비교"
permalink: /loans/
layout: single
author_profile: false
classes: wide
---

은행·저축은행이 금융감독원에 공시한 **주택담보대출·전세자금대출·개인신용대출** 금리를
매일 아침 자동으로 받아 비교합니다. 광고나 제휴 없이 공시 데이터만으로 정렬하며,
본 사이트는 대출을 신청·중개하지 않습니다.

{% include loan-stat-cards.html %}

## 어떤 대출을 봐야 할까

<div class="type-cards" markdown="0">
  <a class="type-card" href="{{ '/loans/mortgage/' | relative_url }}">
    <div class="type-card__title">주택담보대출</div>
    <div class="type-card__desc">집을 사거나, 보유 주택을 담보로 큰 금액을 장기간 빌릴 때</div>
    <div class="type-card__tag">담보가 있어 금리가 가장 낮은 편</div>
    <div class="type-card__link">주담대 금리 비교 →</div>
  </a>
  <a class="type-card" href="{{ '/loans/rent/' | relative_url }}">
    <div class="type-card__title">전세자금대출</div>
    <div class="type-card__desc">전세 보증금이 부족할 때. 보증기관(HF·HUG·SGI) 보증으로 담보 없이 이용</div>
    <div class="type-card__tag">주담대와 비슷하거나 약간 높음</div>
    <div class="type-card__link">전세대출 금리 비교 →</div>
  </a>
  <a class="type-card" href="{{ '/loans/credit/' | relative_url }}">
    <div class="type-card__title">개인신용대출</div>
    <div class="type-card__desc">담보 없이 신용으로 빌릴 때. 마이너스통장 포함</div>
    <div class="type-card__tag">신용점수에 따라 차이가 큼</div>
    <div class="type-card__link">신용대출 금리 비교 →</div>
  </a>
</div>

## 대출 금리 표를 읽는 법

- **최저·최고**: 금융회사가 공시한 적용 가능 금리 구간입니다. 최저금리는 우대조건을 모두
  충족한 최고 신용자 기준이라, 대부분의 사람은 그보다 높은 금리를 받습니다.
- **평균**: 그 금융회사가 **전월에 실제로 취급한 대출의 평균금리**입니다. 내가 받을 금리를
  가늠하는 데는 최저금리보다 이 숫자가 훨씬 현실적입니다.
- **변동 vs 고정**: 변동금리는 기준금리(코픽스 등)에 따라 주기적으로 바뀌고, 고정금리는
  약정 기간 동안 유지됩니다. 금리 하락기엔 변동, 상승기엔 고정이 유리하다는 것이 일반론이지만
  예측은 누구도 못 하므로 상환 기간과 감내 가능한 변동 폭으로 판단하는 것이 안전합니다.
- **상환방식**: 분할상환(원리금균등·원금균등)은 매달 원금을 갚아 총이자가 적고,
  만기일시상환은 매달 이자만 내다 만기에 원금을 갚아 월 부담은 적지만 총이자가 큽니다.

## 대출 전 확인할 것

1. **DSR(총부채원리금상환비율) 한도** — 소득 대비 연간 원리금 상환액 비율 규제로,
   금리보다 먼저 "얼마까지 빌릴 수 있는지"를 정합니다.
2. **중도상환수수료** — 조기 상환 시 부담. 상품별로 다르며 일정 기간 후 면제되는 경우가 많습니다.
3. **우대금리 조건** — 급여이체·카드실적·자동이체 등. 최저금리는 이 조건을 전부 채웠을 때입니다.
4. **정책 상품 우선 확인** — 디딤돌·보금자리론(주택 구입), 버팀목(전세), 햇살론(저신용) 등
   정부 지원 대출은 요건이 맞으면 시중 상품보다 유리한 경우가 많습니다.

{% include loan-notice.html data=site.data.mortgage %}

{% include topic-guides.html topic="loan" %}
