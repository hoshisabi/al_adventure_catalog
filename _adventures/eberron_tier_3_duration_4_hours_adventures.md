---
layout: adventure_list
title: Adventures in Eberron, Tier 3, 4 Hours
adventures:
  - product_id: Chrome-On-The-Range
    full_title: Chrome On The Range
    authors: ['Christopher Bagg']
    campaign: Eberron
    code: EB-SM-CHROME
    date_created: 20210608
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/360228/Chrome-On-The-Range
  - product_id: EB-11-My-Undying-Heart
    full_title: EB-11 My Undying Heart
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-11
    date_created: 20201201
    hours: 4
    tiers: 3
    url: https://www.dmsguild.com/product/337947/EB11-My-Undying-Heart?filters=1000043_0_0_0_0_0_0_0
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
