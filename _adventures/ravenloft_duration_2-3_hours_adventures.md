---
layout: adventure_list
title: Adventures in Ravenloft, 2-3 Hours
adventures:
  - product_id: 536025
    full_title: "Una chiave Maledetta"
    authors: ["Stefan Tomaschitz"]
    campaign: ["Ravenloft"]
    code: DC-RV-IC-SDG-01
    date_created: 20250906
    hours: 2-3
    tiers: 1
    url: https://www.dmsguild.com/product/536025/?affiliate_id=171040
  - product_id: 548946
    full_title: "Uma Chave Amaldiçoada"
    authors: ["Stefan Tomaschitz"]
    campaign: ["Ravenloft"]
    code: Uma Chave Amaldiçoada
    date_created: 20251210
    hours: 2-3
    tiers: 1
    url: https://www.dmsguild.com/product/548946/?affiliate_id=171040
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
