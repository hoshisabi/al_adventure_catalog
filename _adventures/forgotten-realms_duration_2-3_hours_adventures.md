---
layout: adventure_list
title: Adventures in Forgotten Realms, 2-3 Hours
adventures:
  - product_id: 220572
    full_title: "Cellar of Death"
    authors: ["James Introcaso"]
    campaign: ["Forgotten Realms"]
    code: DDHC-TOA-4
    date_created: 20170908
    hours: 2-3
    tiers: 1
    url: https://www.dmsguild.com/product/220572/?affiliate_id=171040
  - product_id: 350135
    full_title: "Failing You"
    authors: ["Addy Tortosa", "Big Mike"]
    campaign: ["Forgotten Realms"]
    code: DC-POA-HAG-SF4
    date_created: 20210314
    hours: 2-3
    tiers: 2
    url: https://www.dmsguild.com/product/350135/?affiliate_id=171040
  - product_id: 452693
    full_title: "Leviathan"
    authors: ["Steven Truong"]
    campaign: ["Forgotten Realms"]
    code: SJ-DC-MONSTER-02
    date_created: 20230911
    hours: 2-3
    tiers: 3
    url: https://www.dmsguild.com/product/452693/SJDCMONSTER02-Leviathan?filters=45470_0_0_0_0_0_0_0&affiliate_id=171040
  - product_id: 456972
    full_title: "Astheneia"
    authors: ["JWei\u4f1f"]
    campaign: ["Forgotten Realms"]
    code: SJ-DC-PANDORA-JWEI-03A
    date_created: 20231017
    hours: 2-3
    tiers: 3
    url: https://www.dmsguild.com/product/456972/SJDCPANDORAJWEI03A-Astheneia?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 459410
    full_title: "Goblin's Gambit"
    authors: ["Steven Truong"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-GOBLIN-01
    date_created: 20231108
    hours: 2-3
    tiers: 1
    url: https://www.dmsguild.com/product/459410/Goblins-Gambit-FRDCGOBLIN01?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 461261
    full_title: "Chloe"
    authors: ["JWei\u4f1f"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-PANDORA-JWEI-05
    date_created: 20231122
    hours: 2-3
    tiers: 3
    url: https://www.dmsguild.com/product/461261/FRDCPANDORAJWEI05-Chloe?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 475044
    full_title: "Maya"
    authors: ["JWei\u4f1f"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-PANDORA-JWEI-11
    date_created: 20240325
    hours: 2-3
    tiers: 3
    url: https://www.dmsguild.com/product/475044/FRDCPANDORAJWEI11-Maya?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
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
