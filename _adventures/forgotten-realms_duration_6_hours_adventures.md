---
layout: adventure_list
title: Adventures in Forgotten Realms, 6 Hours
adventures:
  - product_id: 298232
    full_title: "House of Moonlight"
    authors: ["Andrew Bishkinskyi"]
    campaign: ["Forgotten Realms"]
    code: CCC-UNITE-05
    date_created: 20200102
    hours: 6
    tiers: 2
    url: https://www.dmsguild.com/product/298232/?affiliate_id=171040
  - product_id: 309290
    full_title: "Blood of the Covenent"
    authors: ["Jia Jian Tin"]
    campaign: ["Forgotten Realms"]
    code: CCC-ELF-04
    date_created: 20200429
    hours: 6
    tiers: 3
    url: https://www.dmsguild.com/product/309290/?affiliate_id=171040
  - product_id: 326717
    full_title: "Foreign Affairs"
    authors: ["Ginny Loveday"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-04
    date_created: 20200831
    hours: 6
    tiers: 3
    url: https://www.dmsguild.com/product/326717/?affiliate_id=171040
  - product_id: 330203
    full_title: "Uncertain Scrutiny"
    authors: ["Ben Heisler"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-05
    date_created: 20200928
    hours: 6
    tiers: 3
    url: https://www.dmsguild.com/product/330203/?affiliate_id=171040
  - product_id: 333727
    full_title: "Thimblerigging"
    authors: ["M.T. Black"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-06
    date_created: 20201028
    hours: 6
    tiers: 3
    url: https://www.dmsguild.com/product/333727/?affiliate_id=171040
  - product_id: 334208
    full_title: "Hints at Imbalance: Rumors of Moloch"
    authors: ["Trevor Duston"]
    campaign: ["Forgotten Realms"]
    code: CCC-PFF-03-01
    date_created: 20201102
    hours: 6
    tiers: 3
    url: https://www.dmsguild.com/product/334208/?affiliate_id=171040
  - product_id: 341614
    full_title: "Stygia A Refuge In the Cold"
    authors: ["Paul Duggan"]
    campaign: ["Forgotten Realms"]
    code: CCC-SAF02-01
    date_created: 20201230
    hours: 6
    tiers: 2
    url: https://www.dmsguild.com/product/341614/?affiliate_id=171040
  - product_id: 344671
    full_title: "Moment of Peace"
    authors: ["Toni Winslow-Brill"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-07
    date_created: 20210125
    hours: 6
    tiers: 3
    url: https://www.dmsguild.com/product/344671/?affiliate_id=171040
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
