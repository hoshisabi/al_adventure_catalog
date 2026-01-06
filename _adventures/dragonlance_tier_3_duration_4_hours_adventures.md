---
layout: adventure_list
title: Adventures in Dragonlance, Tier 3, 4 Hours
adventures:
  - product_id: 473696
    full_title: "Split or Fuse"
    authors: ["George Sanders"]
    campaign: ["Dragonlance"]
    code: DL-DC-SF-01
    date_created: 20240311
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/473696/?affiliate_id=171040
  - product_id: 522732
    full_title: "Wulfgar's Champion"
    authors: ["George Sanders"]
    campaign: ["Dragonlance"]
    code: DL-DC-SF-02
    date_created: 20250519
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/522732/?affiliate_id=171040
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
