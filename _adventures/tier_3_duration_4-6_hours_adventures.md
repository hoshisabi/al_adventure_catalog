---
layout: adventure_list
title: Adventures Tier 3, 4-6 Hours
adventures:
  - product_id: 242840
    full_title: "To Wake The Leviathan"
    authors: ["Rich Lescouflair"]
    campaign: ["Forgotten Realms"]
    code: DDHC-MORD-03
    date_created: 20180524
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/242840/?affiliate_id=171040
  - product_id: 254694
    full_title: "Red War: Housekeeping"
    authors: ["Garrett Col\u00f3n"]
    campaign: ["Forgotten Realms"]
    code: CCC-OCC-01
    date_created: 20181011
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/254694/?affiliate_id=171040
  - product_id: 285151
    full_title: "Saving Silverbeard"
    authors: ["Ashley Warren"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-03
    date_created: 20190926
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/285151/?affiliate_id=171040
  - product_id: 301019
    full_title: "The Breath of Life"
    authors: ["Jared Fegan"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-12
    date_created: 20200120
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/301019/?affiliate_id=171040
  - product_id: 301020
    full_title: "The Swarmed Heart"
    authors: ["Bianca Bickford"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-13
    date_created: 20200120
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/301020/?affiliate_id=171040
  - product_id: 301021
    full_title: "The Vast Emptiness of Grace"
    authors: ["Travis Woodall"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-14
    date_created: 20200120
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/301021/?affiliate_id=171040
  - product_id: 306935
    full_title: "Maddening Screams"
    authors: ["Jessica Ross"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-15
    date_created: 20200428
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/306935/?affiliate_id=171040
  - product_id: 306937
    full_title: "Honors Unforseen"
    authors: ["Deridre Donlon"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-16
    date_created: 20200428
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/306937/?affiliate_id=171040
  - product_id: 306938
    full_title: "In the Hand"
    authors: ["Ben Heisler", "Paige Leitman"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-17
    date_created: 20200428
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/306938/?affiliate_id=171040
  - product_id: 318834
    full_title: "Consequences of Choice"
    authors: ["Claire Hoffman"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-18
    date_created: 20200628
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/318834/?affiliate_id=171040
  - product_id: 322760
    full_title: "A Snip Here, a Stitch There"
    authors: ["Noah Grand", "Ayanna Jones-Lightsy"]
    campaign: ["Forgotten Realms"]
    code: CCC-DES-03-01
    date_created: 20200821
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/322760/?affiliate_id=171040
  - product_id: 334414
    full_title: "Fenaria's Gambit"
    authors: ["Jason Koh"]
    campaign: ["Forgotten Realms"]
    code: CCC-RPSG-03
    date_created: 20201103
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/334414/?affiliate_id=171040
  - product_id: 335799
    full_title: "For The Greater Good"
    authors: ["Bruce Wood"]
    campaign: ["Forgotten Realms"]
    code: CCC-FC3-04
    date_created: 20201111
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/335799/?affiliate_id=171040
  - product_id: 336854
    full_title: "Maladomini Unleashed"
    authors: ["Paul Gabat"]
    campaign: ["Forgotten Realms"]
    code: CCC-GSP02-03
    date_created: 20201123
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/336854/?affiliate_id=171040
  - product_id: 341252
    full_title: "King Obould's Fist"
    authors: ["Jonathan Connor Self"]
    campaign: ["Forgotten Realms"]
    code: CCC-MAYDAYS-02-01
    date_created: 20201230
    hours: 4-6
    tiers: 3
    url: https://www.dmsguild.com/product/341252/?affiliate_id=171040
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
