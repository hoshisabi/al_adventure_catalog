---
layout: adventure_list
title: Adventures in Dragonlance, Tier 1, 2 Hours
adventures:
  - product_id: 432961
    full_title: "Dragons of Divinity"
    authors: ["Jon Christian", "Alan Patrick"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-00
    date_created: 20230405
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/432961/?affiliate_id=171040
  - product_id: 445912
    full_title: "Knight Fall"
    authors: ["JD McComb"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-03
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445912/?affiliate_id=171040
  - product_id: 445922
    full_title: "Greenshield"
    authors: ["Belinda Baldwin"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-01
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445922/?affiliate_id=171040
  - product_id: 445923
    full_title: "The Inn of Forgotten Melodies"
    authors: ["JD McComb"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-04
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445923/?affiliate_id=171040
  - product_id: 445925
    full_title: "The Dog Days of Solamnia"
    authors: ["Belinda Baldwin"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-02
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445925/?affiliate_id=171040
  - product_id: 519557
    full_title: "Tavern Rats"
    authors: ["Steven Truong"]
    campaign: ["Dragonlance"]
    code: DL-DC-CLASSIC-01
    date_created: 20250422
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/519557/?affiliate_id=171040
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
