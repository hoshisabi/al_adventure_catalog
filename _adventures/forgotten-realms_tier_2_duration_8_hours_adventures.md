---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 2, 8 Hours
adventures:
  - product_id: 170470
    full_title: "Dark Pyramid of Sorcerer’s Isle"
    authors: ["Claire Hoffman", "Chris Tulach", "Travis Woodall"]
    campaign: ["Forgotten Realms"]
    code: DDEX01-11
    date_created: 20160111
    hours: 8
    tiers: 2
    url: https://www.dmsguild.com/product/170470/?affiliate_id=171040
  - product_id: 170484
    full_title: "Eye of the Tempest"
    authors: ["Pieter Sleijpen", "Claire Hoffman", "Chris Tulach", "Travis Woodall"]
    campaign: ["Forgotten Realms"]
    code: DDEX02-09
    date_created: 20160111
    hours: 8
    tiers: 2
    url: https://www.dmsguild.com/product/170484/?affiliate_id=171040
  - product_id: 206459
    full_title: "Plots in Motion"
    authors: ["Jason Denton"]
    campaign: ["Forgotten Realms"]
    code: CCC-SFBAY-01-01
    date_created: 20170302
    hours: 8
    tiers: 2
    url: https://www.dmsguild.com/product/206459/?affiliate_id=171040
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
