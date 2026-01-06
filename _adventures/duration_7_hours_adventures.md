---
layout: adventure_list
title: Adventures of 7 Hours
adventures:
  - product_id: 260364
    full_title: "Vormestrand's Scroll"
    authors: ["Travis Woodall", "Peter Williams"]
    campaign: ["Forgotten Realms"]
    code: CCC-3MAGS-ONE
    date_created: 20181202
    hours: 7
    tiers: 1
    url: https://www.dmsguild.com/product/260364/?affiliate_id=171040
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
