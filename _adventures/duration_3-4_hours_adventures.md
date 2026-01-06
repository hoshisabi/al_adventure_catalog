---
layout: adventure_list
title: Adventures of 3-4 Hours
adventures:
  - product_id: 240322
    full_title: "Rats of Waterdeep"
    authors: ["Will Doyle", "Lysa Penrose"]
    campaign: ["Forgotten Realms"]
    code: DDHC-XGE-01
    date_created: 20180422
    hours: 3-4
    tiers: 1
    url: https://www.dmsguild.com/product/240322/?affiliate_id=171040
  - product_id: 249757
    full_title: "Pudding Faire"
    authors: ["Will Doyle", "Shawn Merwin", "Cindy Moore"]
    campaign: []
    code: Pudding Faire
    date_created: 20180813
    hours: 3-4
    tiers: 1
    url: https://www.dmsguild.com/product/249757/?affiliate_id=171040
  - product_id: 251922
    full_title: "Escape from Wheloon"
    authors: ["Alan Patrick"]
    campaign: ["Forgotten Realms"]
    code: DDHC-MORD-05
    date_created: 20180912
    hours: 3-4
    tiers: 1
    url: https://www.dmsguild.com/product/251922/?affiliate_id=171040
  - product_id: 252855
    full_title: "Blue Alley"
    authors: ["Alan Patrick", "M.T. Black"]
    campaign: ["Forgotten Realms"]
    code: DDHC-WDH-03
    date_created: 20180920
    hours: 3-4
    tiers: 1
    url: https://www.dmsguild.com/product/252855/?affiliate_id=171040
  - product_id: 253212
    full_title: "Winds of Rot"
    authors: ["Jeremy Hochhalter"]
    campaign: ["Forgotten Realms"]
    code: CCC-GOC01-03
    date_created: 20180924
    hours: 3-4
    tiers: 3
    url: https://www.dmsguild.com/product/253212/?affiliate_id=171040
  - product_id: 326052
    full_title: "Dino World"
    authors: ["Celeste Conowitch"]
    campaign: ["Eberron"]
    code: EB-SM-DINO
    date_created: 20200827
    hours: 3-4
    tiers: 2
    url: https://www.dmsguild.com/product/326052/?affiliate_id=171040
  - product_id: 334451
    full_title: "Last Stand at Copper Canyon"
    authors: ["Stacey Allan"]
    campaign: ["Eberron"]
    code: EB-SM-COPPER
    date_created: 20201102
    hours: 3-4
    tiers: 2
    url: https://www.dmsguild.com/product/334451/?affiliate_id=171040
  - product_id: 355475
    full_title: "The Curious Incident of the Dog in the Night Land"
    authors: ["Tan Lou Ee"]
    campaign: ["Eberron"]
    code: EB-SM-CURIOUS
    date_created: 20210429
    hours: 3-4
    tiers: 2
    url: https://www.dmsguild.com/product/355475/?affiliate_id=171040
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
