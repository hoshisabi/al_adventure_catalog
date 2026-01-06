---
layout: adventure_list
title: Adventures in Eberron, Tier 3
adventures:
  - product_id: 337947
    full_title: "My Undying Heart"
    authors: ["Tom \"Evhelm\" Donovan", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-11
    date_created: 20201201
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/337947/?affiliate_id=171040
  - product_id: 341110
    full_title: "A Crimson Carol"
    authors: ["Bum Lee"]
    campaign: ["Eberron"]
    code: EB-SM-CRIMSON
    date_created: 20201224
    hours: 3
    tiers: 3
    url: https://www.dmsguild.com/product/341110/?affiliate_id=171040
  - product_id: 342451
    full_title: "The Waiting Game"
    authors: ["Shawn Merwin", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-12
    date_created: 20210105
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/342451/?affiliate_id=171040
  - product_id: 344584
    full_title: "Stonefire"
    authors: ["Rich Lescouflair", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-13
    date_created: 20210125
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/344584/?affiliate_id=171040
  - product_id: 349212
    full_title: "Happy-Go-Lucky"
    authors: ["Scott Moore"]
    campaign: ["Eberron"]
    code: EB-SM-HAPPY
    date_created: 20210305
    hours: 3
    tiers: 3
    url: https://www.dmsguild.com/product/349212/?affiliate_id=171040
  - product_id: 349669
    full_title: "From Dust"
    authors: ["Andy Dempz", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-14
    date_created: 20210309
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/349669/?affiliate_id=171040
  - product_id: 352879
    full_title: "Dream Eater"
    authors: ["D&D Adventurers League", "Celeste Conowitch"]
    campaign: ["Eberron"]
    code: EB-15
    date_created: 20210406
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/352879/?affiliate_id=171040
  - product_id: 356496
    full_title: "The Dragon Below"
    authors: ["Bianca Bickford", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-16
    date_created: 20210503
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/356496/?affiliate_id=171040
  - product_id: 360228
    full_title: "Chrome On The Range"
    authors: ["Christopher Bagg"]
    campaign: ["Eberron"]
    code: EB-SM-CHROME
    date_created: 20210608
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/360228/?affiliate_id=171040
  - product_id: 361712
    full_title: "The Rising City"
    authors: ["Will Doyle", "Tony Porteous", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-EP-03
    date_created: 20210621
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/361712/?affiliate_id=171040
  - product_id: 379308
    full_title: "Deep Space Vine"
    authors: ["Christopher Bagg"]
    campaign: ["Eberron"]
    code: EB-SM-VINE
    date_created: 20211206
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/379308/?affiliate_id=171040
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
