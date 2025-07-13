---
layout: adventure_list
title: Adventures in Eberron, Tier 2, 3 Hours
adventures:
  - product_id: Dino-World
    full_title: Dino World
    authors: ['Celeste Conowitch']
    campaign: Eberron
    code: EB-SM-DINO
    date_created: 20200827
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/326052/Dino-World
  - product_id: Last-Stand-at-Copper-Canyon
    full_title: Last Stand at Copper Canyon
    authors: ['Stacey Allan']
    campaign: ['Eberron']
    code: EB-SM-COPPER
    date_created: 20201102
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/334451/Last-Stand-at-Copper-Canyon?filters=1000043_0_0_0_0_0_0_0
  - product_id: None
    full_title: The Curious Incident of the Dog in the Night Land
    authors: ['Tan Lou Ee']
    campaign: Eberron
    code: EB-SM-CURIOUS
    date_created: 20210429
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/355475/The-Curious-Incident-of-the-Dog-in-the-Night-Land?filters=1000043_0_0_0_0_0_0_0
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
      <td>{{ adventure.campaign }}</td>
      <td>{{ adventure.code }}</td>
      <td>{{ adventure.date_created }}</td>
      <td>{{ adventure.hours }}</td>
      <td>{{ adventure.tiers }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
