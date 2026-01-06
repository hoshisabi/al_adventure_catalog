---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 1, 4-Hour Hours
adventures:
  - product_id: 406782
    full_title: "Spectacle at Shrineholt"
    authors: ["Sonja Dunbar", "Matthew Rihan"]
    campaign: ["Forgotten Realms"]
    code: WBW-DC-LUN-01
    date_created: 20220816
    hours: 4-Hour
    tiers: 1
    url: https://www.dmsguild.com/product/406782/?affiliate_id=171040
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
