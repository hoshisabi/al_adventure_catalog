---
layout: adventure_list
title: Adventures in Ravenloft, Tier 2, 4 Hours
adventures:
  - product_id: 182770
    full_title: "The Innocent"
    authors: ["Michael E. Shea"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-07
    date_created: 20160510
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/182770/?affiliate_id=171040
  - product_id: 184341
    full_title: "The Artifact"
    authors: ["Teos Abadia"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-10
    date_created: 20160607
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/184341/?affiliate_id=171040
  - product_id: 184344
    full_title: "The Donjon"
    authors: ["Ash Law"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-11
    date_created: 20160607
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/184344/?affiliate_id=171040
  - product_id: 186787
    full_title: "The Darklord"
    authors: ["Greg Marks"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-14
    date_created: 20160705
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/186787/?affiliate_id=171040
  - product_id: 431307
    full_title: "Expedition Into The Desert"
    authors: ["Teddy Benson", "Paige Leitman"]
    campaign: ["Ravenloft"]
    code: RV-DC-GC15-01
    date_created: 20230322
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/431307/RVDCGC1501-Expedition-Into-The-Desert?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 431311
    full_title: "Domain Infringement"
    authors: ["Jay H Anderson", "Paige Leitman"]
    campaign: ["Ravenloft"]
    code: RV-DC-GC15-02
    date_created: 20230322
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/431311/RVDCGC1502-Domain-Infringement?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 431313
    full_title: "False Faces"
    authors: ["Paige Leitman", "Adrian Rhodes"]
    campaign: ["Ravenloft"]
    code: RV-DC-GC15-03
    date_created: 20230322
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/431313/RVDCGC1503-False-Faces?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 431316
    full_title: "Kingdom, Rise!"
    authors: ["Paige Leitmen", "Marcello De Velazquez"]
    campaign: ["Ravenloft"]
    code: RV-DC-GC15-04
    date_created: 20230322
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/431316/RVDCGC1504-Kingdom-Rise?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 434117
    full_title: "On That Fateful Day"
    authors: ["Miguel Luis de Jesus"]
    campaign: ["Ravenloft"]
    code: RV-DC-PHP-1313-01
    date_created: 20230416
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/434117/?affiliate_id=171040
  - product_id: 442290
    full_title: "Domains of Dread the Braska Roadhouse Chainsaw Massacre"
    authors: ["the illuminhaughti"]
    campaign: ["Ravenloft"]
    code: RV-DC-HBI-001
    date_created: 20230620
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/442290/?affiliate_id=171040
  - product_id: 446081
    full_title: "In the Mists of Keening"
    authors: ["Nicholas Reed"]
    campaign: ["Ravenloft"]
    code: RV-DC-OH01
    date_created: 20230718
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/446081/RVDCOH01-In-the-Mists-of-Keening?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 447852
    full_title: "Domains of Dread Doom Down in Boomtown"
    authors: ["the illuminhaughti"]
    campaign: ["Ravenloft"]
    code: RV-DC-HBI-002
    date_created: 20230731
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/447852/?affiliate_id=171040
  - product_id: 451012
    full_title: "Domains of Dread Terror in Tombstone"
    authors: ["the illuminhaughti"]
    campaign: ["Ravenloft"]
    code: RV-DC-HBI-003
    date_created: 20230912
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/451012/?affiliate_id=171040
  - product_id: 498757
    full_title: "A Peculiar Premiere"
    authors: ["Katriel Paige"]
    campaign: ["Ravenloft"]
    code: RV-DC-POE-01
    date_created: 20241013
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/498757/?affiliate_id=171040
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
