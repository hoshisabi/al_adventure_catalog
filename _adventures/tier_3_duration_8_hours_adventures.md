---
layout: adventure_list
title: Adventures Tier 3, 8 Hours
adventures:
  - product_id: 170497
    full_title: "It's All in the Blood"
    authors: ["Dave Olson"]
    campaign: ["Forgotten Realms"]
    code: DDEX03-04
    date_created: 20160111
    hours: 8
    tiers: 3
    url: https://www.dmsguild.com/product/170497/?affiliate_id=171040
  - product_id: 177572
    full_title: "Assault on Maerimydra"
    authors: ["Greg Marks"]
    campaign: ["Forgotten Realms"]
    code: DDEX03-16
    date_created: 20160322
    hours: 8
    tiers: 3
    url: https://www.dmsguild.com/product/177572/?affiliate_id=171040
  - product_id: 313874
    full_title: "Six Swords Out of Hell"
    authors: ["Andrew Bishkinskyi"]
    campaign: ["Forgotten Realms"]
    code: CCC-6SWORDS-01
    date_created: 20200720
    hours: 8
    tiers: 3
    url: https://www.dmsguild.com/product/313874/?affiliate_id=171040
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
