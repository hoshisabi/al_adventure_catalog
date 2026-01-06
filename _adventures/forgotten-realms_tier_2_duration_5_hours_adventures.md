---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 2, 5 Hours
adventures:
  - product_id: 382223
    full_title: "What is Heroism"
    authors: ["Hariz HUSAINI"]
    campaign: ["Forgotten Realms"]
    code: WBW-DC-HH-01
    date_created: 20211231
    hours: 5
    tiers: 2
    url: https://www.dmsguild.com/product/382223/?affiliate_id=171040
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
