---
layout: adventure_list
title: Adventures in Dragonlance, 4 Hours
adventures:
  - product_id: 438248
    full_title: "Dragons of Destruction"
    authors: ["Jeremey Arnold", "Krishna Simonse"]
    campaign: ["Dragonlance"]
    code: BMG-DLEP-VOTU-1
    date_created: 20230518
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/438248/?affiliate_id=171040
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
  - product_id: 463522
    full_title: "A Mother's Love: A Dragonlance Adventures Experience"
    authors: ["Marcello De Velazquez"]
    campaign: ["Dragonlance"]
    code: DL-DC-MDV-01
    date_created: 20231211
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/463522/?affiliate_id=171040
  - product_id: 463661
    full_title: "Dragons of Treachery"
    authors: ["Janine Hempy", "Jon Christian"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-03
    date_created: 20231213
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/463661/?affiliate_id=171040
  - product_id: 473696
    full_title: "Split or Fuse"
    authors: ["George Sanders"]
    campaign: ["Dragonlance"]
    code: DL-DC-SF-01
    date_created: 20240311
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/473696/?affiliate_id=171040
  - product_id: 487856
    full_title: "Dragonlance Echoes of war"
    authors: ["Alexander Klement"]
    campaign: ["Dragonlance"]
    code: DL-DC-SOTH-01
    date_created: 20240714
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/487856/?affiliate_id=171040
  - product_id: 491735
    full_title: "Dragons of Heresy"
    authors: ["D&D Adventurers League"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-04
    date_created: 20240815
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/491735/?affiliate_id=171040
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
  - product_id: 508960
    full_title: "Dragons of Affliction"
    authors: ["Jon Christian,", "Zac Goins"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-05
    date_created: 20250116
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/508960/?affiliate_id=171040
  - product_id: 515257
    full_title: "Dragons of Future Past"
    authors: ["D&D Adventurers League"]
    campaign: ["Dragonlance"]
    code: BMG-DLEP-VOTU-02
    date_created: 20250313
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/515257/?affiliate_id=171040
  - product_id: 522732
    full_title: "Wulfgar's Champion"
    authors: ["George Sanders"]
    campaign: ["Dragonlance"]
    code: DL-DC-SF-02
    date_created: 20250519
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/522732/?affiliate_id=171040
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
