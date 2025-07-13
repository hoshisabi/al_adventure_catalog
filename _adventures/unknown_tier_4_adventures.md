---
layout: adventure_list
title: Adventures in UNKNOWN, Tier 4
adventures:
  - product_id: Broken-Yet-Unbowed-PS-DC-NOS-02
    full_title: Broken Yet Unbowed (PS-DC-NOS-02)
    authors: ['Lex Winter']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240317
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/474512/Broken-Yet-Unbowed-PSDCNOS02?filters=0_0_100057_0_0_0_0_0
  - product_id: Duke-Ravengard-Gets-Sent-to-Hell-Again-PS-DC-RAVENGARD-V
    full_title: Duke Ravengard Gets Sent to Hell (Again) (PS-DC-RAVENGARD-V)
    authors: ['Jeremy Cheong']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240430
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/479242/Duke-Ravengard-Gets-Sent-to-Hell-Again-PSDCRAVENGARDV?filters=0_0_100057_0_0_0_0_0
  - product_id: Githzerai-Glitch-PS-DC-NOS-01
    full_title: Githzerai Glitch (PS-DC-NOS-01)
    authors: ['Lex Winter']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240211
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/470680/Githzerai-Glitch-PSDCNOS01?filters=0_0_100057_0_0_0_0_0
  - product_id: PS-DC-AUG-02-The-Dark-Sun
    full_title: PS-DC-AUG-02 The Dark Sun
    authors: ['Johnny Smith']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240531
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/483044/PSDCAUG02-The-Dark-Sun?filters=0_0_100057_0_0_0_0_0
  - product_id: PS-DC-POP-01-Pillars-of-Peril
    full_title: PS-DC-POP-01 Pillars of Peril
    authors: ['Briarwall Press', 'Hunter Sinclair']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240301
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/472724/PSDCPOP01-Pillars-of-Peril?filters=0_0_100057_0_0_0_0_0
  - product_id: PS-DC-STRAT-UNDEAD-05-Return-of-the-Dragon
    full_title: PS-DC-STRAT-UNDEAD-05 Return of the Dragon
    authors: ['Nguyen Le']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240524
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/482253/PSDCSTRATUNDEAD05-Return-of-the-Dragon?filters=0_0_100057_0_0_0_0_0
  - product_id: Soul-and-Shadow-PS-DC-SS
    full_title: Soul and Shadow (PS-DC-SS)
    authors: ['Brian Balagot']
    campaign: UNKNOWN
    code: UNKNOWN
    date_created: 20240311
    hours: 4
    tiers: 4
    url: https://www.dmsguild.com/product/473735/Soul-and-Shadow-PSDCSS?filters=0_0_100057_0_0_0_0_0
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
