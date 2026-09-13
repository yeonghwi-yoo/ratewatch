---
layout: single
title: "오늘의 예·적금 금리 비교 — 은행·저축은행 TOP5"
author_profile: false
classes:
  - wide
  - home
lastmod_data: deposit   # sitemap lastmod 기준 데이터
---

<div class="hero" markdown="0">
  <h1>오늘의 예·적금 금리,<br><span class="accent">한눈에</span> 비교하세요</h1>
  <p>금융감독원 공시 데이터를 매일 아침 자동으로 받아 은행·저축은행의 정기예금·적금 금리를 비교합니다.</p>
  <div class="hero-chips">
    <span class="chip chip--blue">공시월 {{ site.data.deposit.dcls_month | slice: 0, 4 }}.{{ site.data.deposit.dcls_month | slice: 4, 2 }}</span>
    <span class="chip">12개월 만기 기준</span>
    <span class="chip">최고우대금리순</span>
    <span class="chip">매일 오전 6시 갱신</span>
  </div>
</div>

<div class="section-head" markdown="0">
  <h2>은행 정기예금 TOP5</h2>
  <a class="more-link" href="{{ '/deposit/' | relative_url }}">전체 보기 →</a>
</div>

{% include rate-table.html rows=site.data.deposit.bank limit=5 %}

<div class="section-head" markdown="0">
  <h2>저축은행 정기예금 TOP5</h2>
  <a class="more-link" href="{{ '/deposit/' | relative_url }}">전체 보기 →</a>
</div>

{% include rate-table.html rows=site.data.deposit.savings_bank limit=5 %}

<div class="section-head" markdown="0">
  <h2>은행 적금 TOP5</h2>
  <a class="more-link" href="{{ '/saving/' | relative_url }}">전체 보기 →</a>
</div>

{% include rate-table.html rows=site.data.saving.bank limit=5 %}

<div class="section-head" markdown="0">
  <h2>저축은행 적금 TOP5</h2>
  <a class="more-link" href="{{ '/saving/' | relative_url }}">전체 보기 →</a>
</div>

{% include rate-table.html rows=site.data.saving.savings_bank limit=5 %}

<div class="section-head" markdown="0">
  <h2>대출 금리 한눈에</h2>
  <a class="more-link" href="{{ '/loans/' | relative_url }}">전체 보기 →</a>
</div>

{% include loan-stat-cards.html %}

{% include rate-notice.html data=site.data.deposit %}

<div class="home-intro" markdown="1">

## 이 사이트를 보는 법

위 표는 금융감독원 금융상품통합비교공시에 올라온 은행과 저축은행의 예·적금을 **12개월 만기, 최고우대금리 순**으로 정렬한 것입니다. 매일 아침 6시에 자동으로 갱신되며, 상위 5개만 여기 보이고 전체 목록은 각 "전체 보기"에서 확인할 수 있습니다. 6개월이나 24·36개월 만기는 [정기예금]({{ "/deposit/" | relative_url }})과 [적금]({{ "/saving/" | relative_url }}) 페이지의 만기 탭에서 따로 볼 수 있습니다.

**최고우대금리**는 은행이 내건 조건(급여이체, 카드 실적, 첫 거래, 비대면 가입 등)을 전부 채웠을 때의 금리입니다. 조건 없이 받는 금리는 **기본금리** 열에 있습니다. 두 숫자 차이가 크면 조건부 금리이니 기본금리를 먼저 보세요. 표의 금리는 세전이며, 이자소득세 15.4%를 떼면 실수령액은 "이자 × 0.846"입니다.

**저축은행**은 은행보다 금리가 높은 대신 규모가 작습니다. 다만 예금자보호는 은행과 동일하게 1인당 한 금융회사 기준 원금과 이자 합산 1억원까지 적용되므로, 그 한도 안이라면 금리가 높은 곳을 고르는 것이 합리적입니다.

**적금 금리는 예금과 다르게 읽어야 합니다.** 매달 넣는 구조라 첫 달 돈만 12개월치 이자를 받습니다. 월 50만원 12개월 연 4% 적금의 이자는 24만원이 아니라 13만원(세전)입니다. 표 상단의 6~7%대 적금은 월 납입 한도가 작거나 우대조건이 여러 개 겹치는 경우가 대부분입니다.

**대출 금리 한눈에** 카드는 주택담보대출·전세자금대출·신용대출 각각에서 은행권 최저금리(신용대출은 평균금리)를 뽑은 것입니다. 최저금리는 우대조건을 모두 충족한 최고 신용자 기준이라 대부분은 그보다 높게 받으며, 실제 적용 금리는 개인의 신용·소득·담보에 따라 달라집니다. 각 대출 페이지에는 신용점수 구간별 평균금리와 상환방식별 비교, 월 상환액 예시가 있습니다.

처음 방문했다면 [금융 가이드]({{ "/guides/" | relative_url }})의 기초 편부터 읽는 것을 권합니다. 통장 구조와 이자 계산을 알고 나면 표의 숫자가 다르게 보입니다.

이 사이트는 광고나 제휴 없이 공시 데이터만으로 정렬하며, 금융상품을 판매하거나 중개하지 않습니다. 공시와 실제 판매 조건에는 시차가 있을 수 있으니 가입 전 각 금융회사에서 확인하세요.

</div>

<div class="section-head" markdown="0">
  <h2>금융 가이드</h2>
  <a class="more-link" href="{{ '/guides/' | relative_url }}">전체 보기 →</a>
</div>

{% include guide-cards.html limit=6 %}
