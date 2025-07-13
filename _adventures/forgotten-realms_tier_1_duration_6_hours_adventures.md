---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 1, 6 Hours
adventures:
  - product_id: WBW-DC-Rook-1-4-The-Rookery--Long-Live-the-Goblins
    full_title: WBW-DC-Rook-1-4 The Rookery: Long Live the Goblins
    authors: ['Chris Valentine']
    campaign: Forgotten Realms
    code: WBW-DC-ROOK-1-4
    date_created: 20220621
    hours: 6
    tiers: 1
    url: https://www.dmsguild.com/product/400472/WBWDCRook14-The-Rookery-Long-Live-the-Goblins?filters=0_0_100057_0_0_0_0_0
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
