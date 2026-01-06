---
layout: adventure_list
title: Adventures in Eberron, Tier 1, 4 Hours
adventures:
  - product_id: 296403
    full_title: "The Night Land"
    authors: ["Shawn Merwin", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-01
    date_created: 20191202
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/296403/?affiliate_id=171040
  - product_id: 299680
    full_title: "Voice in the Machine"
    authors: ["Will Doyle", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-02
    date_created: 20200107
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/299680/?affiliate_id=171040
  - product_id: 302373
    full_title: "Where the Dead Wait"
    authors: ["James Introcaso", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-03
    date_created: 20200204
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/302373/?affiliate_id=171040
  - product_id: 305024
    full_title: "The Third Protocol"
    authors: ["M.T. Black", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-04
    date_created: 20200301
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/305024/?affiliate_id=171040
  - product_id: 309087
    full_title: "House Hunting"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-HOUSE
    date_created: 20200407
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/309087/?affiliate_id=171040
  - product_id: 309600
    full_title: "Snail Tale"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-SNAIL
    date_created: 20200410
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/309600/?affiliate_id=171040
  - product_id: 310224
    full_title: "Finding a Home"
    authors: ["Nathan Bond"]
    campaign: ["Eberron"]
    code: EB-SM-HOME
    date_created: 20200416
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/310224/Finding-a-Home?filters=1000043_0_0_0_0_0_0_0&affiliate_id=171040
  - product_id: 310606
    full_title: "Salvation Inspection"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-SALVINSP
    date_created: 20200420
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/310606/?affiliate_id=171040
  - product_id: 310775
    full_title: "Visions of Salvation"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-VISIONS
    date_created: 20200422
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/310775/?affiliate_id=171040
  - product_id: 311326
    full_title: "Surprise Visitor"
    authors: ["Nathan Bond"]
    campaign: ["Eberron"]
    code: EB-SM-SURPRISE
    date_created: 20200427
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/311326/?affiliate_id=171040
  - product_id: 311419
    full_title: "Dreams of Salvation"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-DREAMS
    date_created: 20200428
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/311419/?affiliate_id=171040
  - product_id: 311714
    full_title: "Nightmares of Salvation A 4 hour Tier 1 Salvage Mission"
    authors: ["Fynn Headen"]
    campaign: ["Eberron"]
    code: EB-SM-NIGHTMARES
    date_created: 20200430
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/311714/?affiliate_id=171040
  - product_id: 313869
    full_title: "Estranged Tower"
    authors: ["Nathan Bond"]
    campaign: ["Eberron"]
    code: EB-SM-TOWER
    date_created: 20200515
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/313869/Estranged-Tower?filters=1000043_0_0_0_0_0_0_0&affiliate_id=171040
  - product_id: 317299
    full_title: "Arena Troubles"
    authors: ["Nathan Bond"]
    campaign: ["Eberron"]
    code: EB-SM-ARENA
    date_created: 20200612
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/317299/?affiliate_id=171040
  - product_id: 437675
    full_title: "The Doll House"
    authors: ["Belinda Baldwin"]
    campaign: ["Eberron"]
    code: EB-DC-THC-01
    date_created: 20230513
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/437675/The-Doll-House-EBDCTHC01?filters=45470_0_0_0_0_0&affiliate_id=171040
  - product_id: 549619
    full_title: "Mercy in the Mournland"
    authors: ["Death 101010"]
    campaign: ["Eberron"]
    code: EB-DC-MOURN-01
    date_created: 20251216
    hours: 4
    tiers: 1
    url: https://www.dmsguild.com/product/549619/?affiliate_id=171040
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
