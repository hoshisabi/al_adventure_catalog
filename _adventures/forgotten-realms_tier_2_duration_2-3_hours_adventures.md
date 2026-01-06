---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 2, 2-3 Hours
adventures:
  - product_id: 350135
    full_title: "Failing You"
    authors: ["Addy Tortosa", "Big Mike"]
    campaign: ["Forgotten Realms"]
    code: DC-POA-HAG-SF4
    date_created: 20210314
    hours: 2-3
    tiers: 2
    url: https://www.dmsguild.com/product/350135/?affiliate_id=171040
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
