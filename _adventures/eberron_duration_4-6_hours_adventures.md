---
layout: adventure_list
title: Adventures in Eberron, 4-6 Hours
adventures:
  - product_id: 430378
    full_title: "Eberron The Ruin of Grave Metallus"
    authors: ["Jon Christian", "Zac Goins", "Troy Sandlin"]
    campaign: ["Eberron"]
    code: EB-SM-METALLUS
    date_created: 20230314
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/430378/?affiliate_id=171040
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
