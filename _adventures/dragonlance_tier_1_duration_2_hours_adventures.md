---
layout: adventure_list
title: Adventures in Dragonlance, Tier 1, 2 Hours
adventures:
  - product_id: Greenshield-DL-DC-SDCC-01
    full_title: Greenshield (DL-DC-SDCC-01)
    authors: ['Belinda Baldwin']
    campaign: Dragonlance
    code: DL-DC-SDCC-01
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445922/Greenshield-DLDCSDCC01?filters=45470_0_0_0_0_0
  - product_id: Knight-Fall-DL-DC-SDCC-03
    full_title: Knight Fall (DL-DC-SDCC-03)
    authors: ['JD McComb']
    campaign: Dragonlance
    code: DL-DC-SDCC-03
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445912/Knight-Fall-DLDCSDCC03?filters=0_0_100057_0_0_0_0_0
  - product_id: The-Dog-Days-of-Solamnia-DL-DC-SDCC-02
    full_title: The Dog Days of Solamnia (DL-DC-SDCC-02)
    authors: ['Belinda Baldwin']
    campaign: Dragonlance
    code: DL-DC-SDCC-02
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445925/The-Dog-Days-of-Solamnia-DLDCSDCC02?filters=45470_0_0_0_0_0
  - product_id: The-Inn-of-Forgotten-Melodies-DL-DC-SDCC-04
    full_title: The Inn of Forgotten Melodies (DL-DC-SDCC-04)
    authors: ['JD McComb']
    campaign: Dragonlance
    code: DL-DC-SDCC-04
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445923/The-Inn-of-Forgotten-Melodies-DLDCSDCC04?filters=0_0_100057_0_0_0_0_0
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
