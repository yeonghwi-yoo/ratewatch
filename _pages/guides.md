---
title: "금융 가이드"
permalink: /guides/
layout: single
author_profile: false
classes: wide
lastmod_from_posts: true
---

예·적금 고르는 법, 청년·정부지원 상품, 세금과 우대금리, 대출까지 돈을 모으고 빌릴 때 알아야 할 내용을
주제별로 정리한 글 모음입니다. 글마다 기준일을 적어 두었고, 수치가 바뀌는 내용은 확인 방법을 함께 안내합니다.
새 글은 주 2~3회 추가됩니다.

**처음이라면 이 순서로 읽는 것을 권합니다.** ① 기초 편에서 통장 구조와 이자 계산을 익히고 → ② 예금·적금 편에서 상품 고르는 기준을 잡은 뒤 → ③ 세금 편으로 실수령액을 계산하고 → ④ 청년이라면 정부지원 편을, 대출이 필요하면 대출 편을 보면 됩니다. 각 글 하단에는 관련 비교 페이지와 함께 읽을 글이 연결되어 있습니다.

{% assign matched = site.posts | where_exp: "p", "p.topics.first == 'basics'" %}
{% if matched.size > 0 %}
<div class="section-head" markdown="0">
  <h2 id="topic-basics">기초: 통장과 이자의 구조</h2>
</div>

파킹통장·CMA·예금의 차이, 적금 이자가 생각보다 적은 이유, 비상금과 통장 쪼개기, 첫 월급 관리처럼 저축을 시작하기 전에 알아야 할 구조를 다룹니다. 금융 상품을 고르기 전에 "돈이 어떻게 굴러가는지"를 먼저 이해하면 이후 선택이 쉬워집니다.

<div class="guide-cards" markdown="0">
  {% for post in matched %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
    <div class="guide-card__meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: site.date_format }}</time></div>
  </a>
  {% endfor %}
</div>
{% endif %}

{% assign matched = site.posts | where_exp: "p", "p.topics.first == 'deposit'" %}
{% if matched.size > 0 %}
<div class="section-head" markdown="0">
  <h2 id="topic-deposit">예금: 목돈 굴리기</h2>
</div>

정기예금 고르는 기준, 만기 선택, 특판 잡는 법, 저축은행 고르기, 예금자보호, 만기 후 관리와 중도해지 대응까지 목돈을 굴릴 때 필요한 판단을 정리했습니다. 실제 금리는 [정기예금 비교]({{ "/deposit/" | relative_url }})에서 매일 갱신되며, 6·24·36개월 만기는 만기 탭에서 볼 수 있습니다.

<div class="guide-cards" markdown="0">
  {% for post in matched %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
    <div class="guide-card__meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: site.date_format }}</time></div>
  </a>
  {% endfor %}
</div>
{% endif %}

{% assign matched = site.posts | where_exp: "p", "p.topics.first == 'saving'" %}
{% if matched.size > 0 %}
<div class="section-head" markdown="0">
  <h2 id="topic-saving">적금: 매달 모으기</h2>
</div>

적금 이자 계산 구조, 예금과 적금의 역할 차이, 풍차돌리기의 실제 효과, 자동이체 설계처럼 매달 돈을 모으는 사람에게 필요한 내용입니다. 상품별 금리는 [적금 비교]({{ "/saving/" | relative_url }})에서 확인하세요.

<div class="guide-cards" markdown="0">
  {% for post in matched %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
    <div class="guide-card__meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: site.date_format }}</time></div>
  </a>
  {% endfor %}
</div>
{% endif %}

{% assign matched = site.posts | where_exp: "p", "p.topics.first == 'youth'" %}
{% if matched.size > 0 %}
<div class="section-head" markdown="0">
  <h2 id="topic-youth">청년·정부지원 상품</h2>
</div>

청년미래적금, 주택청약, ISA처럼 정부 기여금이나 세제혜택이 붙는 상품은 일반 예·적금보다 실효 수익률이 높아 우선순위가 앞섭니다. 자격 요건, 신청 시기, 중복 가입 제한, 놓치기 쉬운 실수를 정리했습니다.

<div class="guide-cards" markdown="0">
  {% for post in matched %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
    <div class="guide-card__meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: site.date_format }}</time></div>
  </a>
  {% endfor %}
</div>
{% endif %}

{% assign matched = site.posts | where_exp: "p", "p.topics.first == 'tax'" %}
{% if matched.size > 0 %}
<div class="section-head" markdown="0">
  <h2 id="topic-tax">세금과 연말정산</h2>
</div>

이자소득세 15.4%의 구조와 세후 환산법, 비과세 저축, 연금저축·IRP 세액공제, 신용카드·체크카드 소득공제처럼 실수령액과 환급액을 바꾸는 세금 이야기입니다. 금리 0.1%p보다 세금 구조를 아는 것이 실수령액에 더 큰 차이를 만드는 경우가 많습니다.

<div class="guide-cards" markdown="0">
  {% for post in matched %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
    <div class="guide-card__meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: site.date_format }}</time></div>
  </a>
  {% endfor %}
</div>
{% endif %}

{% assign matched = site.posts | where_exp: "p", "p.topics.first == 'loan'" %}
{% if matched.size > 0 %}
<div class="section-head" markdown="0">
  <h2 id="topic-loan">대출</h2>
</div>

주택담보대출·전세자금대출·신용대출의 금리 결정 구조, DSR 한도 계산, 고정·변동 선택, 대환 손익, 마이너스통장과 리볼빙의 위험, 금리인하요구권까지 빌리는 쪽의 판단을 다룹니다. 금리 비교는 [대출 금리 비교]({{ "/loans/" | relative_url }})에서 볼 수 있습니다.

<div class="guide-cards" markdown="0">
  {% for post in matched %}
  <a class="guide-card" href="{{ post.url | relative_url }}">
    <div class="guide-card__title">{{ post.title }}</div>
    <div class="guide-card__desc">{{ post.excerpt | strip_html | truncate: 80 }}</div>
    <div class="guide-card__meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: site.date_format }}</time></div>
  </a>
  {% endfor %}
</div>
{% endif %}

## 이 가이드를 읽을 때

- 금리·한도·세율처럼 시점에 따라 바뀌는 숫자는 글 상단의 **기준일** 시점 값입니다. 결정 전에는 해당 기관의 최신 안내를 확인하세요.
- 모든 글은 일반적인 정보 제공 목적이며 특정 상품 가입을 권하거나 수익을 보장하지 않습니다.
- 글은 주제별로 묶여 있고 각 묶음 안에서는 최신 글이 앞에 옵니다. 같은 주제의 글은 서로 이어지도록 썼으니, 한 편을 읽은 뒤 글 하단의 "함께 읽을 글"을 따라가면 자연스럽게 다음 내용으로 넘어갑니다.
- 비교표의 숫자는 매일 아침 갱신되지만 글의 숫자는 기준일 시점 값입니다. 글에서 본 금리와 표의 금리가 다르다면 표가 최신입니다.
- 오류를 발견했거나 다뤘으면 하는 주제가 있다면 [소개 페이지]({{ "/about/" | relative_url }})의 문의 메일로 알려주세요.
