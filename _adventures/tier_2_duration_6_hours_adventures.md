---
layout: adventure_list
title: Adventures Tier 2, 6 Hours
adventures:
  - product_id: 298232
    full_title: "House of Moonlight"
    authors: ["Andrew Bishkinskyi"]
    campaign: ["Forgotten Realms"]
    code: CCC-UNITE-05
    date_created: 20200102
    hours: 6
    tiers: 2
    url: https://www.dmsguild.com/product/298232/?affiliate_id=171040
  - product_id: 341614
    full_title: "Stygia A Refuge In the Cold"
    authors: ["Paul Duggan"]
    campaign: ["Forgotten Realms"]
    code: CCC-SAF02-01
    date_created: 20201230
    hours: 6
    tiers: 2
    url: https://www.dmsguild.com/product/341614/?affiliate_id=171040
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
