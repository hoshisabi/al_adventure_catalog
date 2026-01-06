---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 2, 3 Hours
adventures:
  - product_id: 334520
    full_title: "Finding Linric"
    authors: ["Martine Lassen"]
    campaign: ["Forgotten Realms"]
    code: CCC-CONMAR01-02
    date_created: 20201103
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/334520/?affiliate_id=171040
  - product_id: 370744
    full_title: "Song of Spears"
    authors: ["Rich Lescouflair", "Jeff C. Stevens"]
    campaign: ["Forgotten Realms"]
    code: DDEP10-02
    date_created: 20210914
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/370744/?affiliate_id=171040
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
