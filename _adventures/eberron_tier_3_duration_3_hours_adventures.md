---
layout: adventure_list
title: Adventures in Eberron, Tier 3, 3 Hours
adventures:
  - product_id: 341110
    full_title: "A Crimson Carol"
    authors: ["Bum Lee"]
    campaign: ["Eberron"]
    code: EB-SM-CRIMSON
    date_created: 20201224
    hours: 3
    tiers: 3
    url: https://www.dmsguild.com/product/341110/?affiliate_id=171040
  - product_id: 349212
    full_title: "Happy-Go-Lucky"
    authors: ["Scott Moore"]
    campaign: ["Eberron"]
    code: EB-SM-HAPPY
    date_created: 20210305
    hours: 3
    tiers: 3
    url: https://www.dmsguild.com/product/349212/?affiliate_id=171040
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
