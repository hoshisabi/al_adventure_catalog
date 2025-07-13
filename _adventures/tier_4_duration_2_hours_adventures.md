---
layout: adventure_list
title: Adventures Tier 4, 2 Hours
adventures:
  - product_id: EB-SALVAGE-RSM-T44-Daughter-of-Khyber
    full_title: EB-SALVAGE-RSM-T4.4 Daughter of Khyber
    authors: ['Integral Game Conglomerate LLC']
    campaign: None
    code: EB-SM-RSM-T4.4
    date_created: 20230131
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/425292/EBSALVAGERSMT44-Daughter-of-Khyber?filters=45470_0_0_0_0_0
  - product_id: Githzerai-Glitch-PS-DC-NOS-01
    full_title: Githzerai Glitch (PS-DC-NOS-01)
    authors: ['Lex Winter']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240211
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/470680/Githzerai-Glitch-PSDCNOS01?filters=0_0_100057_0_0_0_0_0
  - product_id: Its-Always-Boring-in-Automata-PS-DC-NOS-03
    full_title: Its Always Boring in Automata (PS-DC-NOS-03)
    authors: ['Lex Winter']
    campaign: Forgotten Realms
    code: PS-DC-NOS-03
    date_created: 20240906
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/494242/Its-Always-Boring-in-Automata-PSDCNOS03?filters=45470_0_0_0_0_0_0_0
  - product_id: PS-DC-ELEMENT-DEATH-02-And-Then-They-Attacked
    full_title: PS-DC-ELEMENT-DEATH-02 And Then They Attacked
    authors: ['Death 101010']
    campaign: Forgotten Realms
    code: PS-DC-ELEMENT-DEATH-02
    date_created: 20240924
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/496426/PSDCELEMENTDEATH02-And-Then-They-Attacked?filters=45470_0_0_0_0_0
  - product_id: Snakes-on-a-Planescape-PS-DC-CEG-02
    full_title: Snakes on a Planescape (PS-DC-CEG-02)
    authors: ['Bennett Ellis', 'Dante Santos']
    campaign: Forgotten Realms
    code: PS-DC-CEG-02
    date_created: 20240427
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/478979/Snakes-on-a-Planescape-PSDCCEG02?filters=0_0_100057_0_0_0_0_0
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
