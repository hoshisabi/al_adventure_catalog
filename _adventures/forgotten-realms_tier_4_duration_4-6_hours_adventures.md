---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 4, 4-6 Hours
adventures:
  - product_id: 268517
    full_title: "A Change of Address"
    authors: ["Rob Steiner"]
    campaign: ["Forgotten Realms"]
    code: DDAL08-16
    date_created: 20190305
    hours: 4-6
    tiers: 4
    url: https://www.dmsguild.com/product/268517/?affiliate_id=171040
  - product_id: 268520
    full_title: "Moving Day"
    authors: ["Lysa Chen"]
    campaign: ["Forgotten Realms"]
    code: DDAL08-18
    date_created: 20190305
    hours: 4-6
    tiers: 4
    url: https://www.dmsguild.com/product/268520/?affiliate_id=171040
  - product_id: 321063
    full_title: "Fang and Claw"
    authors: ["Will Doyle"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-19
    date_created: 20200721
    hours: 4-6
    tiers: 4
    url: https://www.dmsguild.com/product/321063/?affiliate_id=171040
  - product_id: 321069
    full_title: "Where Devils Fear to Tread"
    authors: ["Greg Marks"]
    campaign: ["Forgotten Realms"]
    code: DDAL09-20
    date_created: 20200721
    hours: 4-6
    tiers: 4
    url: https://www.dmsguild.com/product/321069/?affiliate_id=171040
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
