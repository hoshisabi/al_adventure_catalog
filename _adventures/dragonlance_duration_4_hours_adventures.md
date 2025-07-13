---
layout: adventure_list
title: Adventures in Dragonlance, 4 Hours
adventures:
  - product_id: BMG-DL-VOTU-01-Dragons-of-Revelation
    full_title: BMG-DL-VOTU-01 Dragons of Revelation
    authors: ['Jon Christian']
    campaign: Dragonlance
    code: BMG-DL-VOTU-01
    date_created: 20230822
    hours: 4
    tiers: None
    url: https://www.dmsguild.com/product/450331/BMGDLVOTU01-Dragons-of-Revelation?filters=45470_0_0_0_0_0
  - product_id: BMG-DL-VOTU-02-Dragons-of-Sorrow
    full_title: BMG-DL-VOTU-02 Dragons of Sorrow
    authors: ['Jon Christian']
    campaign: Dragonlance
    code: BMG-DL-VOTU-02
    date_created: 20230912
    hours: 4
    tiers: None
    url: https://www.dmsguild.com/product/452943/BMGDLVOTU02-Dragons-of-Sorrow?filters=45470_0_0_0_0_0
  - product_id: BMG-DL-VOTU-03-Dragons-of-Treachery
    full_title: BMG-DL-VOTU-03 Dragons of Treachery
    authors: ['Janine Hempy', 'Jon Christian']
    campaign: Dragonlance
    code: BMG-DL-VOTU-03
    date_created: 20231213
    hours: 4
    tiers: None
    url: https://www.dmsguild.com/product/463661/BMGDLVOTU03-Dragons-of-Treachery?filters=45470_0_0_0_0_0
  - product_id: BMG-DL-VOTU-04-Dragons-of-Heresy
    full_title: BMG-DL-VOTU-04 Dragons of Heresy
    authors: ['D&D Adventurers League']
    campaign: Dragonlance
    code: BMG-DL-VOTU-04
    date_created: 20240815
    hours: 4
    tiers: None
    url: https://www.dmsguild.com/product/491735/BMGDLVOTU04-Dragons-of-Heresy?filters=45470_0_0_0_0_0
  - product_id: BMG-DLEP-VOTU-1-Dragons-of-Destruction
    full_title: BMG-DLEP-VOTU-1 Dragons of Destruction
    authors: ['Jeremey Arnold', 'Krishna Simonse']
    campaign: Dragonlance
    code: BMG-DLEP-VOTU-1
    date_created: 20230518
    hours: 4
    tiers: None
    url: https://www.dmsguild.com/product/438248/BMGDLEPVOTU1-Dragons-of-Destruction?filters=45470_0_0_0_0_0
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
  - product_id: DL-DC-MDV-01-A-Mothers-Love--A-Dragonlance-Adventures-Experience
    full_title: DL-DC-MDV-01 A Mother's Love: A Dragonlance Adventures Experience
    authors: ['Marcello De Velazquez']
    campaign: Dragonlance
    code: DL-DC-MDV-01
    date_created: 20231211
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/463522/DLDCMDV01-A-Mothers-Love-A-Dragonlance-Adventures-Experience?filters=45470_0_0_0_0_0_0_0
  - product_id: DL-DC-SF-01-Split-or-Fuse
    full_title: DL-DC-SF-01 Split or Fuse
    authors: ['George Sanders']
    campaign: Dragonlance
    code: DL-DC-SF-01
    date_created: 20240311
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/473696/DLDCSF01-Split-or-Fuse?filters=0_0_100057_0_0_0_0_0
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
