---
layout: adventure_list
title: Adventures of 7 Hours
adventures:
  - product_id: CCC-3MAGS-ONE-Vormestrands-Scroll
    full_title: CCC-3MAGS-ONE Vormestrand's Scroll
    authors: ['Travis Woodall', 'Peter Williams']
    campaign: Forgotten Realms
    code: CCC-3MAGS-ONE
    date_created: 20181202
    hours: 7
    tiers: None
    url: https://www.dmsguild.com/product/260364/CCC3MAGSONE-Vormestrands-Scroll?filters=45470_0_0_0_0_0_0_0
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
      <td>{{ adventure.campaign }}</td>
      <td>{{ adventure.code }}</td>
      <td>{{ adventure.date_created }}</td>
      <td>{{ adventure.hours }}</td>
      <td>{{ adventure.tiers }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
