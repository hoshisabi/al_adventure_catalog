---
layout: adventure_list
title: Adventures in Eberron, Tier 1, 3 Hours
adventures:
  - product_id: 308553
    full_title: "The Iron Titan"
    authors: ["Will Doyle", "James Introcaso", "Shawn Merwin", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-EP-01
    date_created: 20200407
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/308553/?affiliate_id=171040
  - product_id: 310332
    full_title: "Murder in Salvation A 3 hour Tier 1 Salvage Mission"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-MURDER
    date_created: 20200418
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/310332/?affiliate_id=171040
  - product_id: 323626
    full_title: "The Khyber Heart A Salvage Mission"
    authors: ["Nors"]
    campaign: ["Eberron"]
    code: EB-SM-KHYBER
    date_created: 20200809
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/323626/The-Khyber-Heart-A-Salvage-Mission?filters=1000043_0_45418_0_0_0_0_0&affiliate_id=171040
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
