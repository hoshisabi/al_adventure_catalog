---
layout: adventure_list
title: Adventures in Eberron, Tier 4
adventures:
  - product_id: 363337
    full_title: "The Final Tribute"
    authors: ["Richard Green", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-17
    date_created: 20210706
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/363337/?affiliate_id=171040
  - product_id: 368629
    full_title: "Scales of War"
    authors: ["Alan Patrick", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-18
    date_created: 20210824
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/368629/?affiliate_id=171040
  - product_id: 372377
    full_title: "Back to the Mud"
    authors: ["Andy Dempz", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-19
    date_created: 20210930
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/372377/?affiliate_id=171040
  - product_id: 379297
    full_title: "The Last War"
    authors: ["Will Doyle", "Laura Thompson", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-EP-04
    date_created: 20211207
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/379297/?affiliate_id=171040
  - product_id: 384724
    full_title: "Old Scores"
    authors: ["Will Doyle", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-20
    date_created: 20220127
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/384724/?affiliate_id=171040
  - product_id: 425292
    full_title: "Daughter of Khyber"
    authors: ["Integral Game Conglomerate LLC"]
    campaign: ["Eberron"]
    code: EB-SALVAGE-RSM-T4.4
    date_created: 20230131
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/425292/?affiliate_id=171040
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
