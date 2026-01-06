---
layout: adventure_list
title: Adventures in Eberron, 2 Hours
adventures:
  - product_id: 332476
    full_title: "Wrongs and Punishment An Eberron Salvage Mission"
    authors: ["Nicol\u00e1s Carrillo"]
    campaign: ["Eberron"]
    code: EB-SM-WRONGS
    date_created: 20201016
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/332476/?affiliate_id=171040
  - product_id: 425292
    full_title: "Daughter of Khyber"
    authors: ["Integral Game Conglomerate LLC"]
    campaign: ["Eberron"]
    code: EB-SALVAGE-RSM-T4.4
    date_created: 20230131
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/425292/?affiliate_id=171040
  - product_id: 427667
    full_title: "Off the Books"
    authors: ["Chris Wilson"]
    campaign: ["Eberron"]
    code: EB-DC-COG-01
    date_created: 20230221
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/427667/EBDCCOG01-Off-the-Books?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 519554
    full_title: "Tavern Rats"
    authors: ["Steven Truong"]
    campaign: ["Eberron"]
    code: EB-DC-CLASSIC-01
    date_created: 20250422
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/519554/?affiliate_id=171040
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
