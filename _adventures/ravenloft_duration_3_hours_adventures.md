---
layout: adventure_list
title: Adventures in Ravenloft, 3 Hours
adventures:
  - product_id: None
    full_title: A Cursed Key
    authors: ['Stefan Tomaschitz']
    campaign: Ravenloft
    code: RV-DC-SDG-01
    date_created: 20240811
    hours: 3
    tiers: None
    url: https://www.dmsguild.com/product/491254/A-Cursed-Key?filters=45470_0_0_0_0_0
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
