---
layout: adventure_list
title: Adventures Tier 1, 1-5 Hours
adventures:
  - product_id: 170384
    full_title: "Defiance in Phlan"
    authors: ["Shawn Merwin", "Claire Hoffman", "Chris Tulach", "Travis Woodall"]
    campaign: ["Forgotten Realms"]
    code: DDEX01-01
    date_created: 20160111
    hours: 1-5
    tiers: 1
    url: https://www.dmsguild.com/product/170384/?affiliate_id=171040
  - product_id: 170386
    full_title: "City of Danger"
    authors: ["Shawn Merwin", "Claire Hoffman", "Chris Tulach", "Travis Woodall"]
    campaign: ["Forgotten Realms"]
    code: DDEX02-01
    date_created: 20160111
    hours: 1-5
    tiers: 1
    url: https://www.dmsguild.com/product/170386/?affiliate_id=171040
  - product_id: 214058
    full_title: "A City on the Edge"
    authors: ["Rich Lescouflair"]
    campaign: ["Forgotten Realms"]
    code: DDAL07-01
    date_created: 20170905
    hours: 1-5
    tiers: 1
    url: https://www.dmsguild.com/product/214058/?affiliate_id=171040
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
