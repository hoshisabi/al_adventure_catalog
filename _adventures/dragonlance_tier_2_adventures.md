---
layout: adventure_list
title: Adventures in Dragonlance, Tier 2
adventures:
  - product_id: DL-DC-MDV-01-A-Mothers-Love--A-Dragonlance-Adventures-Experience
    full_title: DL-DC-MDV-01 A Mother's Love: A Dragonlance Adventures Experience
    authors: ['Marcello De Velazquez']
    campaign: Dragonlance
    code: DL-DC-MDV-01
    date_created: 20231211
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/463522/DLDCMDV01-A-Mothers-Love-A-Dragonlance-Adventures-Experience?filters=45470_0_0_0_0_0_0_0
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
