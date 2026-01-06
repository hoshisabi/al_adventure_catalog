---
layout: adventure_list
title: Adventures of 2-6 Hours
adventures:
  - product_id: 262080
    full_title: "Moonshae Treasure Hunt"
    authors: ["Baldman Games", "Shawn Merwin", "Robert Alaniz", "Krishna Simonse", "Cindy Moore"]
    campaign: ["Forgotten Realms"]
    code: CCC-BMG-MOON1-1
    date_created: 20181220
    hours: 2-6
    tiers: 3
    url: https://www.dmsguild.com/product/262080/?affiliate_id=171040
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
