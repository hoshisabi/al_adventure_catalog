---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 2, 4-6 Hours
adventures:
  - product_id: 273777
    full_title: "Breaking Umberlee's Resolve"
    authors: ["Ashley Warren"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-01
    date_created: 20190706
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/273777/?affiliate_id=171040
  - product_id: 282024
    full_title: "Blood in the Water"
    authors: ["Ashley Warren"]
    campaign: ["Forgotten Realms"]
    code: DDAL-DRW-02
    date_created: 20190706
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/282024/?affiliate_id=171040
  - product_id: 290246
    full_title: "Faces of Fortune: the Story of Fai Chen"
    authors: ["Ted Atkinson"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-05
    date_created: 20190930
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/290246/?affiliate_id=171040
  - product_id: 290898
    full_title: "Infernal Insurgency"
    authors: ["The GM Tim"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-06
    date_created: 20191007
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/290898/?affiliate_id=171040
  - product_id: 291677
    full_title: "The Diabolical Dive"
    authors: ["James J. Haeck"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-07
    date_created: 20191014
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/291677/?affiliate_id=171040
  - product_id: 295211
    full_title: "In the Garden of Evil"
    authors: ["Cameron Blair"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-08
    date_created: 20191118
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/295211/?affiliate_id=171040
  - product_id: 295212
    full_title: "Ruined Prospects"
    authors: ["Cat Evans"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-09
    date_created: 20191118
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/295212/?affiliate_id=171040
  - product_id: 295328
    full_title: "Tipping the Scales"
    authors: ["Mellanie Black"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-10
    date_created: 20191119
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/295328/?affiliate_id=171040
  - product_id: 296738
    full_title: "Losing Fai"
    authors: ["James Introcaso"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-11
    date_created: 20200204
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/296738/?affiliate_id=171040
  - product_id: 312580
    full_title: "A Small Trifle"
    authors: ["Jonathan Connor Self"]
    campaign: ["Forgotten Realms"]
    code: CCC-VOTE-01-01
    date_created: 20200508
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/312580/?affiliate_id=171040
  - product_id: 321118
    full_title: "Facades Undone"
    authors: ["Blake Jones"]
    campaign: ["Forgotten Realms"]
    code: CCC-TAROT-02-10
    date_created: 20200803
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/321118/?affiliate_id=171040
  - product_id: 322754
    full_title: "One Last Job"
    authors: ["Jonathan Connor Self", "Eric Weberg"]
    campaign: ["Forgotten Realms"]
    code: CCC-DES-01-06
    date_created: 20200821
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/322754/?affiliate_id=171040
  - product_id: 334716
    full_title: "A Hell of a Party"
    authors: ["Iam Pace"]
    campaign: ["Forgotten Realms"]
    code: CCC-DES-04-02
    date_created: 20201109
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/334716/?affiliate_id=171040
  - product_id: 392794
    full_title: "Autumn Burns Red"
    authors: ["Marcello De Velazquez", "Gamehole Con"]
    campaign: ["Forgotten Realms"]
    code: PO-BK-1-01
    date_created: 20220408
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/392794/?affiliate_id=171040
  - product_id: 392801
    full_title: "Trust No One"
    authors: ["Ruth Imhoff", "Gamehole Con"]
    campaign: ["Forgotten Realms"]
    code: PO-BK-1-02
    date_created: 20220408
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/392801/?affiliate_id=171040
  - product_id: 392803
    full_title: "Red Masks"
    authors: ["Andrew Bishkinskyi", "Gamehole Con"]
    campaign: ["Forgotten Realms"]
    code: PO-BK-1-03
    date_created: 20220408
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/392803/?affiliate_id=171040
  - product_id: 490910
    full_title: "The Hidden Sanctum"
    authors: ["Elijah Vince Aguila"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-PHP-INFRN01-01-
    date_created: 20240807
    hours: 4-6
    tiers: 2
    url: https://www.dmsguild.com/product/490910/?affiliate_id=171040
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
