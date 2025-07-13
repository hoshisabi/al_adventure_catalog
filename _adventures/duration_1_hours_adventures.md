---
layout: adventure_list
title: Adventures of 1 Hours
adventures:
  - product_id: CCC-AN-02-The-Wrathful-Deity-of-Khurovogo
    full_title: CCC-AN-02 The Wrathful Deity of Khurovogo
    authors: ['Garrett Crowe']
    campaign: Forgotten Realms
    code: CCC-AN-02
    date_created: 20180816
    hours: 1
    tiers: 1
    url: https://www.dmsguild.com/product/250006/CCCAN02-The-Wrathful-Deity-of-Khurovogo?filters=45470_0_0_0_0_0_0_0
  - product_id: CCC-MAG01-01-Mischief-at-the-Festival
    full_title: CCC-MAG01-01 Mischief at the Festival
    authors: ['Y. Michael Zhang']
    campaign: Forgotten Realms
    code: CCC-MAG01-01
    date_created: 20200803
    hours: 1
    tiers: 1
    url: https://www.dmsguild.com/product/318581/CCCMAG0101-Mischief-at-the-Festival?filters=45470_0_0_0_0_0_0_0
  - product_id: DDAL10-00-Ice-Road-Trackers
    full_title: DDAL10-00 Ice Road Trackers
    authors: ['D&D Adventurers League']
    campaign: ['Forgotten Realms']
    code: DDAL10-00
    date_created: 20200914
    hours: 1
    tiers: None
    url: https://www.dmsguild.com/product/328476/DDAL1000-Ice-Road-Trackers
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
