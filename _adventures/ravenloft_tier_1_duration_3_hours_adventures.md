---
layout: adventure_list
title: Adventures in Ravenloft, Tier 1, 3 Hours
adventures:
  - product_id: 373816
    full_title: "RMH-03 The Amber Dirge"
    authors: ["Claire Hoffman"]
    campaign: ["Ravenloft"]
    code: RMH-03
    date_created: 20211013
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/373816/?affiliate_id=171040
  - product_id: 377048
    full_title: "RMH-04 The Amber Secret"
    authors: ["D&D Adventurers League"]
    campaign: ["Ravenloft"]
    code: RMH-04
    date_created: 20211110
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/377048/RMH04-The-Amber-Secret?filters=45470_0_0_0_0_0_0_0&affiliate_id=171040
  - product_id: 472632
    full_title: "Ein verfluchter Schlüssel"
    authors: ["Stefan Tomaschitz"]
    campaign: ["Ravenloft"]
    code: RV-DC-SDG-01
    date_created: 20240301
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/472632/Ein-verfluchter-Schlussel?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 491254
    full_title: "A Cursed Key"
    authors: ["Stefan Tomaschitz"]
    campaign: ["Ravenloft"]
    code: RV-DC-SDG-01
    date_created: 20240811
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/491254/?affiliate_id=171040
  - product_id: 499970
    full_title: "The Horrors of Uninhabited Places"
    authors: ["Miguel Luis de Jesus"]
    campaign: ["Ravenloft"]
    code: RV-DC-LAGIM-02
    date_created: 20241025
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/499970/?affiliate_id=171040
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
