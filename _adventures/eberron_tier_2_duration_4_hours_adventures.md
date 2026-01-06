---
layout: adventure_list
title: Adventures in Eberron, Tier 2, 4 Hours
adventures:
  - product_id: 306912
    full_title: "Ghost Town"
    authors: ["Gregory Hallenbeck"]
    campaign: ["Eberron"]
    code: EB-SM-GHOST
    date_created: 20200318
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/306912/Ghost-Town?filters=1000043_0_0_0_0_0_0_0&affiliate_id=171040
  - product_id: 312336
    full_title: "A Century of Ashes"
    authors: ["Bianca Bickford", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-05
    date_created: 20200504
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/312336/?affiliate_id=171040
  - product_id: 313252
    full_title: "A Whisper In Your Mind"
    authors: ["Bruce Wood"]
    campaign: ["Eberron"]
    code: EB-SM-WHISPER
    date_created: 20200511
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/313252/?affiliate_id=171040
  - product_id: 316059
    full_title: "The Last Word"
    authors: ["Anne Gregersen", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-06
    date_created: 20200603
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/316059/?affiliate_id=171040
  - product_id: 319657
    full_title: "Song of the Sky"
    authors: ["Stacey Allan", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-07
    date_created: 20200706
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/319657/?affiliate_id=171040
  - product_id: 322749
    full_title: "Parliament of Gears"
    authors: ["Ian Hawthorne", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-08
    date_created: 20200803
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/322749/?affiliate_id=171040
  - product_id: 326339
    full_title: "Lord Bucket"
    authors: ["Travis Woodall", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-09
    date_created: 20200901
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/326339/?affiliate_id=171040
  - product_id: 331083
    full_title: "Judgment of Iron"
    authors: ["Richard Green", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-10
    date_created: 20201006
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/331083/?affiliate_id=171040
  - product_id: 335587
    full_title: "Rolling Thunder"
    authors: ["Will Doyle", "Tony Porteous", "D&D Adventurers League"]
    campaign: ["Eberron"]
    code: EB-EP-02
    date_created: 20201110
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/335587/?affiliate_id=171040
  - product_id: 349569
    full_title: "Seaside Salvage"
    authors: ["Bum Lee"]
    campaign: ["Eberron"]
    code: EB-SM-SEASIDE
    date_created: 20210308
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/349569/?affiliate_id=171040
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
