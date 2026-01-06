---
layout: adventure_list
title: Adventures in Dragonlance, Tier 1
adventures:
  - product_id: 432961
    full_title: "Dragons of Divinity"
    authors: ["Jon Christian", "Alan Patrick"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-00
    date_created: 20230405
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/432961/?affiliate_id=171040
  - product_id: 438248
    full_title: "Dragons of Destruction"
    authors: ["Jeremey Arnold", "Krishna Simonse"]
    campaign: ["Dragonlance"]
    code: BMG-DLEP-VOTU-1
    date_created: 20230518
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/438248/?affiliate_id=171040
  - product_id: 445912
    full_title: "Knight Fall"
    authors: ["JD McComb"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-03
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445912/?affiliate_id=171040
  - product_id: 445922
    full_title: "Greenshield"
    authors: ["Belinda Baldwin"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-01
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445922/?affiliate_id=171040
  - product_id: 445923
    full_title: "The Inn of Forgotten Melodies"
    authors: ["JD McComb"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-04
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445923/?affiliate_id=171040
  - product_id: 445925
    full_title: "The Dog Days of Solamnia"
    authors: ["Belinda Baldwin"]
    campaign: ["Dragonlance"]
    code: DL-DC-SDCC-02
    date_created: 20230717
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/445925/?affiliate_id=171040
  - product_id: 450331
    full_title: "Dragons of Revelation"
    authors: ["Jon Christian"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-01
    date_created: 20230822
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/450331/?affiliate_id=171040
  - product_id: 452943
    full_title: "Dragons of Sorrow"
    authors: ["Jon Christian"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-02
    date_created: 20230912
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/452943/?affiliate_id=171040
  - product_id: 463661
    full_title: "Dragons of Treachery"
    authors: ["Janine Hempy", "Jon Christian"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-03
    date_created: 20231213
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/463661/?affiliate_id=171040
  - product_id: 487856
    full_title: "Dragonlance Echoes of war"
    authors: ["Alexander Klement"]
    campaign: ["Dragonlance"]
    code: DL-DC-SOTH-01
    date_created: 20240714
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/487856/?affiliate_id=171040
  - product_id: 492361
    full_title: "A Silver Light"
    authors: ["Marcello De Velazquez", "Liga dos Aventureiros"]
    campaign: ["Dragonlance"]
    code: DL-DC-LIGA01
    date_created: 20240821
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/492361/?affiliate_id=171040
  - product_id: 495850
    full_title: "Wickedness over Dargaard"
    authors: ["DMGMorais", "Liga dos Aventureiros"]
    campaign: ["Dragonlance"]
    code: DL-DC-LIGA02
    date_created: 20240919
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/495850/?affiliate_id=171040
  - product_id: 500778
    full_title: "Firstwal under Siege"
    authors: ["Lu\u00eds Ricardo 'DM Corvo' da Costa", "Liga dos Aventureiros"]
    campaign: ["Dragonlance"]
    code: DL-DC-LIGA03
    date_created: 20241031
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/500778/?affiliate_id=171040
  - product_id: 519557
    full_title: "Tavern Rats"
    authors: ["Steven Truong"]
    campaign: ["Dragonlance"]
    code: DL-DC-CLASSIC-01
    date_created: 20250422
    hours: 2
    tiers: 1
    url: https://www.dmsguild.com/product/519557/?affiliate_id=171040
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
