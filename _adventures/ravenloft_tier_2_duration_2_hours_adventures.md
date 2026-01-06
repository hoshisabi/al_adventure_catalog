---
layout: adventure_list
title: Adventures in Ravenloft, Tier 2, 2 Hours
adventures:
  - product_id: 182771
    full_title: "The Broken One"
    authors: ["Joshua Kelly"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-08
    date_created: 20160510
    hours: 2
    tiers: 2
    url: https://www.dmsguild.com/product/182771/?affiliate_id=171040
  - product_id: 184342
    full_title: "The Tempter"
    authors: ["M. Sean Molley"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-09
    date_created: 20160607
    hours: 2
    tiers: 2
    url: https://www.dmsguild.com/product/184342/?affiliate_id=171040
  - product_id: 186783
    full_title: "The Raven"
    authors: ["Matt Hudson"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-12
    date_created: 20160705
    hours: 2
    tiers: 2
    url: https://www.dmsguild.com/product/186783/?affiliate_id=171040
  - product_id: 186786
    full_title: "The Horseman"
    authors: ["Daniel Helmick"]
    campaign: ["Forgotten Realms", "Ravenloft"]
    code: DDAL04-13
    date_created: 20160705
    hours: 2
    tiers: 2
    url: https://www.dmsguild.com/product/186786/?affiliate_id=171040
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
