---
layout: adventure_list
title: Adventures in Eberron, 3-6 Hours
adventures:
  - product_id: 310611
    full_title: "The Cannith Schematica"
    authors: ["M.T. Black"]
    campaign: ["Eberron"]
    code: EB-SM-CANNITH
    date_created: 20200420
    hours: 3-6
    tiers: 1
    url: https://www.dmsguild.com/product/310611/The-Cannith-Schematica?filters=1000043_0_0_0_0_0_0_0&affiliate_id=171040
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
