---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 1, 3-4 Hours
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
