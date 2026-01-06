---
layout: adventure_list
title: Adventures in Eberron, Tier 1, 2-4 Hours
adventures:
  - product_id: 252925
    full_title: "Murder in Skyway"
    authors: ["Greg Marks"]
    campaign: ["Eberron"]
    code: DDAL-ELW01
    date_created: 20180920
    hours: 2-4
    tiers: 1
    url: https://www.dmsguild.com/product/252925/?affiliate_id=171040
  - product_id: 253783
    full_title: "Boromar Ball"
    authors: ["Bill Benham"]
    campaign: ["Eberron"]
    code: DDAL-ELW02
    date_created: 20181001
    hours: 2-4
    tiers: 1
    url: https://www.dmsguild.com/product/253783/?affiliate_id=171040
  - product_id: 254691
    full_title: "The Cannith Code"
    authors: ["James Haeck"]
    campaign: ["Eberron"]
    code: DDAL-ELW03
    date_created: 20181011
    hours: 2-4
    tiers: 1
    url: https://www.dmsguild.com/product/254691/?affiliate_id=171040
  - product_id: 256437
    full_title: "Jack of Daggers"
    authors: ["Ginny Loveday"]
    campaign: ["Eberron"]
    code: DDAL-ELW04
    date_created: 20181018
    hours: 2-4
    tiers: 1
    url: https://www.dmsguild.com/product/256437/?affiliate_id=171040
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
