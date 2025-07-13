---
layout: adventure_list
title: Adventures in Forgotten Realms, 13 Hours
adventures:
  - product_id: Kobold-Kings-Labyrinth-WBW-DC-LAB-01
    full_title: Kobold King's Labyrinth (WBW-DC-LAB-01)
    authors: ['Jason Lee']
    campaign: Forgotten Realms
    code: WBW-DC-LAB-01
    date_created: 20220814
    hours: 13
    tiers: 1
    url: https://www.dmsguild.com/product/406494/Kobold-Kings-Labyrinth-WBWDCLAB01?filters=0_0_100057_0_0_0_0_0
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
