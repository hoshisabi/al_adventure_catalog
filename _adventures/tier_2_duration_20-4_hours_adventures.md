---
layout: adventure_list
title: Adventures Tier 2, 20-4 Hours
adventures:
  - product_id: 418922
    full_title: "Mutiny The Ballad of Blunderbuss Bill"
    authors: ["Ethan Stanhope", "Te\u00e4n Stanhope", "James Twigg"]
    campaign: ["Forgotten Realms"]
    code: SJ-DC-BBB-01
    date_created: 20221205
    hours: 20-4
    tiers: 2
    url: https://www.dmsguild.com/product/418922/?affiliate_id=171040
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
