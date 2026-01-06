---
layout: adventure_list
title: Adventures Tier 4, 4-5 Hours
adventures:
  - product_id: 488844
    full_title: "Rocky Road"
    authors: ["Death 101010"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-ELEMENT-DEATH-01
    date_created: 20240725
    hours: 4-5
    tiers: 4
    url: https://www.dmsguild.com/product/488844/?affiliate_id=171040
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
