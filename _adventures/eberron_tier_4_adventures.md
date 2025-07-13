---
layout: adventure_list
title: Adventures in Eberron, Tier 4
adventures:
  - product_id: Salvage-Mission--The-Mabar-Conspiracy
    full_title: Salvage Mission: The Mabar Conspiracy
    authors: ['Nicholas Reed']
    campaign: ['Eberron']
    code: EB-SM-MABAR
    date_created: 20210816
    hours: None
    tiers: 4
    url: https://www.dmsguild.com/product/367908/Salvage-Mission-The-Mabar-Conspiracy?filters=1000043_0_0_0_0_0_0_0
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
