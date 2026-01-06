---
layout: adventure_list
title: Adventures in Ravenloft, Tier 1, 2 Hours
adventures:
  - product_id: 178793
    full_title: "The Beast"
    authors: ["Alan Patrick"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-02
    date_created: 20160405
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/178793/?affiliate_id=171040
  - product_id: 178794
    full_title: "The Executioner"
    authors: ["Jerry LeNeave"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-03
    date_created: 20160405
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/178794/?affiliate_id=171040
  - product_id: 178796
    full_title: "The Seer"
    authors: ["Ron Lundeen"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-05
    date_created: 20160405
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/178796/?affiliate_id=171040
  - product_id: 472637
    full_title: "Der Meister der Puppen"
    authors: ["Stefan Tomaschitz"]
    campaign: ["Ravenloft", "Forgotten Realms"]
    code: RV-DC-SDG-02
    date_created: 20240301
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/472637?affiliate_id=171040
  - product_id: 490715
    full_title: "Letting The Dead Rest"
    authors: ["Miguel Luis de Jesus"]
    campaign: ["Ravenloft"]
    code: RV-DC-LAGIM-01-
    date_created: 20240806
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/490715/?affiliate_id=171040
  - product_id: 519560
    full_title: "Tavern Rats"
    authors: ["Steven Truong"]
    campaign: ["Ravenloft"]
    code: RV-DC-CLASSIC-01
    date_created: 20250422
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/519560/?affiliate_id=171040
  - product_id: 541193
    full_title: "Hypnotic Pattern"
    authors: ["Jieying Ji"]
    campaign: ["Ravenloft"]
    code: RV-DC-FREAK-01
    date_created: 20251020
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/541193/?affiliate_id=171040
  - product_id: 547890
    full_title: "The Merchant"
    authors: ["Jonathan Bennett"]
    campaign: ["Ravenloft"]
    code: RV-DC-KEN-01
    date_created: 20251201
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/547890/?affiliate_id=171040
---

<h1 class="page-title">{{ page.title }}</h1>

<table class="adventure-table">
  <thead>
    <tr>
      <th>Title</th>
      <th>Authors</th>
      <th>Campaign</th>
      <th>Code</th>
      <th>Date</th>
      <th>Hours</th>
      <th>Tier</th>
    </tr>
  </thead>
  <tbody>
    {% for adventure in page.adventures %}
    <tr>
      <td><a href="{{ adventure.url }}">{{ adventure.full_title }}</a></td>
      <td>{{ adventure.authors | join: ", " }}</td>
      <td>{{ adventure.campaign | join: ", " }}</td>
      <td>{{ adventure.code }}</td>
      <td>{{ adventure.date_created }}</td>
      <td>{{ adventure.hours }}</td>
      <td>{{ adventure.tiers }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
