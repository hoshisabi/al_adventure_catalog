---
layout: adventure_list
title: Adventures of 4-5 Hours
adventures:
  - product_id: 308079
    full_title: "Gulgo-13"
    authors: ["Christian Eichhorn"]
    campaign: ["Eberron"]
    code: EB-SM-GULGO-13
    date_created: 20200330
    hours: 4-5
    tiers: 1
    url: https://www.dmsguild.com/product/308079/?affiliate_id=171040
  - product_id: 465635
    full_title: "The Eternals"
    authors: ["JWei\u4f1f"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-PANDORA-JWEI-06
    date_created: 20240101
    hours: 4-5
    tiers: 3
    url: https://www.dmsguild.com/product/465635/?affiliate_id=171040
  - product_id: 475039
    full_title: "Samsareal"
    authors: ["JWei\u4f1f"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-PANDORA-JWEI-07
    date_created: 20240325
    hours: 4-5
    tiers: 3
    url: https://www.dmsguild.com/product/475039/?affiliate_id=171040
  - product_id: 475042
    full_title: "Echthra"
    authors: ["JWei\u4f1f"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-PANDORA-JWEI-09
    date_created: 20240325
    hours: 4-5
    tiers: 3
    url: https://www.dmsguild.com/product/475042/?affiliate_id=171040
  - product_id: 488844
    full_title: "Rocky Road"
    authors: ["Death 101010"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-ELEMENT-DEATH-01
    date_created: 20240725
    hours: 4-5
    tiers: 4
    url: https://www.dmsguild.com/product/488844/?affiliate_id=171040
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
