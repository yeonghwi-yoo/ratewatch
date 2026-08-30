---
layout: single
title: "오늘의 예·적금 금리 비교 — 은행·저축은행 TOP5"
author_profile: false
classes:
  - wide
  - home
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

{% include rate-notice.html data=site.data.deposit %}

<div class="section-head" markdown="0">
  <h2>금융 가이드</h2>
  <a class="more-link" href="{{ '/guides/' | relative_url }}">전체 보기 →</a>
</div>

<div class="guide-cards" markdown="0">
  {% for post in site.posts limit: 6 %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
  </a>
  {% endfor %}
</div>
