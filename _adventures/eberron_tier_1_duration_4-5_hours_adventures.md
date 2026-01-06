---
layout: adventure_list
title: Adventures in Eberron, Tier 1, 4-5 Hours
adventures:
  - product_id: 308079
    full_title: "Gulgo-13"
    authors: ["Christian Eichhorn"]
    campaign: ["Eberron"]
    code: EB-SM-GULGO-13
    date_created: 20200330
    hours: 4-5
    tiers: 1
    url: https://www.dmsguild.com/product/308079/?affiliate_id=171040
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
