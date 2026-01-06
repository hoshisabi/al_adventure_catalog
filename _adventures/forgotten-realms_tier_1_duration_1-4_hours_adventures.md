---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 1, 1-4 Hours
adventures:
  - product_id: 282281
    full_title: "A Rat's Tale"
    authors: ["Colby Savell", "Monkey Mind Tabletop"]
    campaign: ["Forgotten Realms"]
    code: CCC-GREY-01-01
    date_created: 20190716
    hours: 1-4
    tiers: 1
    url: https://www.dmsguild.com/product/282281/?affiliate_id=171040
  - product_id: 328476
    full_title: "Ice Road Trackers"
    authors: ["Shawn Merwin"]
    campaign: ["Forgotten Realms"]
    code: DDAL10-00
    date_created: 20200914
    hours: 1-4
    tiers: 1
    url: https://www.dmsguild.com/product/328476/?affiliate_id=171040
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
