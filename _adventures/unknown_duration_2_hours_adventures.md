---
layout: adventure_list
title: Adventures in UNKNOWN, 2 Hours
adventures:
  - product_id: Githzerai-Glitch-PS-DC-NOS-01
    full_title: Githzerai Glitch (PS-DC-NOS-01)
    authors: ['Lex Winter']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240211
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/470680/Githzerai-Glitch-PSDCNOS01?filters=0_0_100057_0_0_0_0_0
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
