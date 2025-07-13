---
layout: adventure_list
title: Adventures in Dragonlance, Tier 1, 4 Hours
adventures:
  - product_id: DL-DC-LIGA01---A-Silver-Light
    full_title: DL-DC-LIGA01 - A Silver Light
    authors: ['Marcello De Velazquez', 'Liga dos Aventureiros']
    campaign: Dragonlance
    code: DL-DC-LIGA01
    date_created: 20240821
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/492361/DLDCLIGA01--A-Silver-Light?filters=0_0_100057_0_0_0_0_0
  - product_id: DL-DC-LIGA02---Wickedness-over-Dargaard
    full_title: DL-DC-LIGA02 - Wickedness over Dargaard
    authors: ['DMGMorais', 'Liga dos Aventureiros']
    campaign: Dragonlance
    code: DL-DC-LIGA02
    date_created: 20240919
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/495850/DLDCLIGA02--Wickedness-over-Dargaard?filters=45470_0_0_0_0_0
  - product_id: Dragonlance--Echoes-of-war-DL-DC-SOTH-01
    full_title: Dragonlance: Echoes of war (DL-DC-SOTH-01)
    authors: ['Alexander Klement']
    campaign: Dragonlance
    code: DL-DC-SOTH-01
    date_created: 20240714
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/487856/Dragonlance-Echoes-of-war-DLDCSOTH01?filters=0_0_100057_0_0_0_0_0
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
