---
layout: adventure_list
title: Adventures in Eberron, Tier 1, 3 Hours
adventures:
  - product_id: Murder-in-Salvation--A-3-hour-Tier-1-Salvage-Mission
    full_title: Murder in Salvation: A 3 hour Tier 1 Salvage Mission
    authors: ['Fynn Headen']
    campaign: Eberron
    code: EB-SM-MURDER
    date_created: 20200418
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/310332/Murder-in-Salvation-A-3-hour-Tier-1-Salvage-Mission?filters=1000043_0_0_0_0_0_0_0
  - product_id: The-Cannith-Schematica
    full_title: The Cannith Schematica
    authors: ['M.T. Black']
    campaign: ['Eberron']
    code: EB-SM-CANNITH
    date_created: 20200420
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/310611/The-Cannith-Schematica?filters=1000043_0_0_0_0_0_0_0
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
