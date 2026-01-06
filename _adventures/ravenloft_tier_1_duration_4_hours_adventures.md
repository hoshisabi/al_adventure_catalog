---
layout: adventure_list
title: Adventures in Ravenloft, Tier 1, 4 Hours
adventures:
  - product_id: 178795
    full_title: "The Marionette"
    authors: ["Robert Alaniz"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-04
    date_created: 20160405
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/178795/?affiliate_id=171040
  - product_id: 182769
    full_title: "The Ghost"
    authors: ["Ken Hart"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-06
    date_created: 20160510
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/182769/?affiliate_id=171040
  - product_id: 367198
    full_title: "RMH-01 The Final Curtain"
    authors: ["D&D Adventurers League"]
    campaign: ["Ravenloft"]
    code: RMH-01
    date_created: 20210810
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/367198/?affiliate_id=171040
  - product_id: 367294
    full_title: "RMH-EP-01 The Grand Masquerade"
    authors: ["Amy Lynn Dzura", "Ma\u2019at Crook"]
    campaign: ["Ravenloft"]
    code: RMH-EP-01
    date_created: 20210810
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/367294/?affiliate_id=171040
  - product_id: 367527
    full_title: "And Then There Was a Murder"
    authors: ["Raymond Holding"]
    campaign: ["Ravenloft"]
    code: RV-DC-DBH-01
    date_created: 20210813
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/367527/RVDCDBH01-And-Then-There-Was-a-Murder?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 370754
    full_title: "RMH-02 Back to the Front"
    authors: ["D&D Adventurers League"]
    campaign: ["Ravenloft"]
    code: RMH-02
    date_created: 20210914
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/370754/?affiliate_id=171040
  - product_id: 511921
    full_title: "Inheritance"
    authors: ["David Sklenicka", "Davestar Gaming"]
    campaign: ["Ravenloft"]
    code: RV-DC-HH-01
    date_created: 20250210
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/511921/?affiliate_id=171040
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
