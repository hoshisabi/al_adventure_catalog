---
layout: adventure_list
title: Adventures in Eberron, 3-4 Hours
adventures:
  - product_id: 326052
    full_title: "Dino World"
    authors: ["Celeste Conowitch"]
    campaign: ["Eberron"]
    code: EB-SM-DINO
    date_created: 20200827
    hours: 3-4
    tiers: 2
    url: https://www.dmsguild.com/product/326052/?affiliate_id=171040
  - product_id: 334451
    full_title: "Last Stand at Copper Canyon"
    authors: ["Stacey Allan"]
    campaign: ["Eberron"]
    code: EB-SM-COPPER
    date_created: 20201102
    hours: 3-4
    tiers: 2
    url: https://www.dmsguild.com/product/334451/?affiliate_id=171040
  - product_id: 355475
    full_title: "The Curious Incident of the Dog in the Night Land"
    authors: ["Tan Lou Ee"]
    campaign: ["Eberron"]
    code: EB-SM-CURIOUS
    date_created: 20210429
    hours: 3-4
    tiers: 2
    url: https://www.dmsguild.com/product/355475/?affiliate_id=171040
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
