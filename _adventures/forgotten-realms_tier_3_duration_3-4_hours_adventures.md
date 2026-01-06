---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 3, 3-4 Hours
adventures:
  - product_id: 253212
    full_title: "Winds of Rot"
    authors: ["Jeremy Hochhalter"]
    campaign: ["Forgotten Realms"]
    code: CCC-GOC01-03
    date_created: 20180924
    hours: 3-4
    tiers: 3
    url: https://www.dmsguild.com/product/253212/?affiliate_id=171040
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
