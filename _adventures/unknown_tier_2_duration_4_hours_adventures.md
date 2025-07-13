---
layout: adventure_list
title: Adventures in UNKNOWN, Tier 2, 4 Hours
adventures:
  - product_id: PS-DC-BINGO-1-Lorem-Ipsum
    full_title: PS-DC-BINGO-1 Lorem Ipsum
    authors: ['Sean Ware']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240522
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/482067/PSDCBINGO1-Lorem-Ipsum?filters=0_0_100057_0_0_0_0_0
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
      <td>{{ adventure.campaign }}</td>
      <td>{{ adventure.code }}</td>
      <td>{{ adventure.date_created }}</td>
      <td>{{ adventure.hours }}</td>
      <td>{{ adventure.tiers }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
