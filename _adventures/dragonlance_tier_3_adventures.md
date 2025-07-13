---
layout: adventure_list
title: Adventures in Dragonlance, Tier 3
adventures:
  - product_id: DL-DC-SF-01-Split-or-Fuse
    full_title: DL-DC-SF-01 Split or Fuse
    authors: ['George Sanders']
    campaign: Dragonlance
    code: DL-DC-SF-01
    date_created: 20240311
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/473696/DLDCSF01-Split-or-Fuse?filters=0_0_100057_0_0_0_0_0
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
