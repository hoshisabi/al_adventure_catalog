---
layout: adventure_list
title: Adventures in Eberron, Tier 1, 4 Hours
adventures:
  - product_id: Arena-Troubles
    full_title: Arena Troubles
    authors: ['Nathan Bond']
    campaign: Eberron
    code: EB-SM-ARENA
    date_created: 20200612
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/317299/Arena-Troubles?filters=1000043_0_0_0_0_0_0_0
  - product_id: Estranged-Tower
    full_title: Estranged Tower
    authors: ['Nathan Bond']
    campaign: Eberron
    code: EB-SM-TOWER
    date_created: 20200515
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/313869/Estranged-Tower?filters=1000043_0_0_0_0_0_0_0
  - product_id: Finding-a-Home
    full_title: Finding a Home
    authors: ['Nathan Bond']
    campaign: Eberron
    code: EB-SM-HOME
    date_created: 20200416
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/310224/Finding-a-Home?filters=1000043_0_0_0_0_0_0_0
  - product_id: Gulgo-13--An-Eberron-Salvage-Mission-for-Oracle-of-War
    full_title: Gulgo-13 | An Eberron Salvage Mission for Oracle of War
    authors: ['Christian Eichhorn']
    campaign: ['Eberron']
    code: EB-SM-GULGO-13
    date_created: 20200330
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/308079/Gulgo13--An-Eberron-Salvage-Mission-for-Oracle-of-War
  - product_id: House-Hunting--A-4-hour-Tier-1-Salvage-Mission
    full_title: House Hunting: A 4 hour Tier 1 Salvage Mission
    authors: ['Fynn Headen']
    campaign: Eberron
    code: EB-SM-HOUSE
    date_created: 20200407
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/309087/House-Hunting-A-4-hour-Tier-1-Salvage-Mission?filters=1000043_0_0_0_0_0_0_0
  - product_id: Nightmares-of-Salvation--A-4-hour-Tier-1-Salvage-Mission
    full_title: Nightmares of Salvation: A 4 hour Tier 1 Salvage Mission
    authors: ['Fynn Headen']
    campaign: Eberron
    code: EB-SM-NIGHTMARES
    date_created: 20200430
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/311714/Nightmares-of-Salvation-A-4-hour-Tier-1-Salvage-Mission?filters=1000043_0_0_0_0_0_0_0
  - product_id: Salvation-Inspection--A-4-hour-Tier-1-Salvage-Mission
    full_title: Salvation Inspection: A 4 hour Tier 1 Salvage Mission
    authors: ['Fynn Headen']
    campaign: ['Eberron']
    code: EB-SM-INSPECTION
    date_created: 20200420
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/310606/Salvation-Inspection-A-4-hour-Tier-1-Salvage-Mission?filters=1000043_0_0_0_0_0_0_0
  - product_id: Surprise-Visitor
    full_title: Surprise Visitor
    authors: ['Nathan Bond']
    campaign: Eberron
    code: EB-SM-SURPRISE
    date_created: 20200427
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/311326/Surprise-Visitor?filters=1000043_0_0_0_0_0_0_0
  - product_id: The-Doll-House-EB-DC-THC-01
    full_title: The Doll House (EB-DC-THC-01)
    authors: ['Belinda Baldwin']
    campaign: Eberron
    code: EB-DC-THC-01
    date_created: 20230513
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/437675/The-Doll-House-EBDCTHC01?filters=45470_0_0_0_0_0
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
