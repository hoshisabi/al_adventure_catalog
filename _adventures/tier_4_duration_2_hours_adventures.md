---
layout: adventure_list
title: Adventures Tier 4, 2 Hours
adventures:
  - product_id: 213029
    full_title: "Crypt of the Death Giants"
    authors: ["Robert Adducci"]
    campaign: ["Forgotten Realms"]
    code: DDAL06-03
    date_created: 20170704
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/213029/?affiliate_id=171040
  - product_id: 247140-5
    full_title: "The Definition of Heroism (Lost Tales of Myth Drannor)"
    authors: ["Greg Marks", "Claire Hoffman", "Alan Patrick", "Travis Woodall", "Bill Benham", "Robert Adducci"]
    campaign: ["Forgotten Realms"]
    code: DDAL00-02f
    date_created: 20180713
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/247140/?affiliate_id=171040
  - product_id: 425292
    full_title: "Daughter of Khyber"
    authors: ["Integral Game Conglomerate LLC"]
    campaign: ["Eberron"]
    code: EB-SALVAGE-RSM-T4.4
    date_created: 20230131
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/425292/?affiliate_id=171040
  - product_id: 470680
    full_title: "Githzerai Glitch"
    authors: ["Lex Winter"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-NOS-01
    date_created: 20240212
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/470680/?affiliate_id=171040
  - product_id: 478979
    full_title: "Snakes on a Planescape"
    authors: ["Bennett Ellis", "Dante Santos"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-CEG-02
    date_created: 20240427
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/478979/Snakes-on-a-Planescape-PSDCCEG02?filters=0_0_100057_0_0_0_0_0&affiliate_id=171040
  - product_id: 494242
    full_title: "Its Always Boring in Automata"
    authors: ["Lex Winter"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-NOS-03
    date_created: 20240906
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/494242/?affiliate_id=171040
  - product_id: 539689-01
    full_title: "Vault of the Drow Risen"
    authors: ["Johnny Smith"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-RDP-01
    date_created: 20251007
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/539689/?affiliate_id=171040
  - product_id: 539689-02
    full_title: "The Great Fane of Lolth"
    authors: ["Johnny Smith"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-RDP-02
    date_created: 20251007
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/539689/?affiliate_id=171040
  - product_id: 547771-03
    full_title: "The Upper Demonweb"
    authors: ["Johnny Smith"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-RDP-03
    date_created: 20251130
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/547771/?affiliate_id=171040
  - product_id: 547771-04
    full_title: "The Lower Demonweb"
    authors: ["Johnny Smith"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-RDP-04
    date_created: 20251130
    hours: 2
    tiers: 4
    url: https://www.dmsguild.com/product/547771/?affiliate_id=171040
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
