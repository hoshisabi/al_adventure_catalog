---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 1, 4-8 Hours
adventures:
  - product_id: 203580
    full_title: "In Volo's Wake"
    authors: ["Monica Valentinelli", "Shawn Merwin", "Rich Lescouflair"]
    campaign: ["Forgotten Realms"]
    code: DDIA-VOLO
    date_created: 20170131
    hours: 4-8
    tiers: 1
    url: https://www.dmsguild.com/product/203580/?affiliate_id=171040
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
