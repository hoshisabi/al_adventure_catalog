---
layout: adventure_list
title: Adventures Tier 3, 2-4 Hours
adventures:
  - product_id: 282991
    full_title: "The Scarlet Divide"
    authors: ["Scott Moore"]
    campaign: ["Forgotten Realms"]
    code: CCC-QCC2019-03
    date_created: 20190715
    hours: 2-4
    tiers: 3
    url: https://www.dmsguild.com/product/282991/?affiliate_id=171040
  - product_id: 358288
    full_title: "Nothing Is Sacred"
    authors: ["Baldman Games", "Toni Winslow-Brill", "Eric Menge"]
    campaign: ["Forgotten Realms"]
    code: CCC-BMG-MOON12-1
    date_created: 20210520
    hours: 2-4
    tiers: 3
    url: https://www.dmsguild.com/product/358288/?affiliate_id=171040
  - product_id: 358290
    full_title: "A Gift from the Queen"
    authors: ["Baldman Games", "Jeff C. Stevens"]
    campaign: ["Forgotten Realms"]
    code: CCC-BMG-MOON12-2
    date_created: 20210520
    hours: 2-4
    tiers: 3
    url: https://www.dmsguild.com/product/358290/?affiliate_id=171040
  - product_id: 358291
    full_title: "Tempest of Malice"
    authors: ["Baldman Games", "Ashley Warren"]
    campaign: ["Forgotten Realms"]
    code: CCC-BMG-MOON12-3
    date_created: 20210520
    hours: 2-4
    tiers: 3
    url: https://www.dmsguild.com/product/358291/?affiliate_id=171040
  - product_id: 433913
    full_title: "Straight Through the Heart"
    authors: ["Ted Atkinson", "Gamehole Con"]
    campaign: ["Forgotten Realms"]
    code: PO-BK-02-08
    date_created: 20230414
    hours: 2-4
    tiers: 3
    url: https://www.dmsguild.com/product/433913/?affiliate_id=171040
  - product_id: 438392
    full_title: "Thunderstorms & Wine"
    authors: ["Steven Truong"]
    campaign: ["Forgotten Realms"]
    code: SJ-DC-WINE-01
    date_created: 20230520
    hours: 2-4
    tiers: 3
    url: https://www.dmsguild.com/product/438392/?affiliate_id=171040
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
