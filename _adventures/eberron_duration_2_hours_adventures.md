---
layout: adventure_list
title: Adventures in Eberron, 2 Hours
adventures:
  - product_id: EB-DC-COG-01-Off-the-Books
    full_title: EB-DC-COG-01 Off the Books
    authors: ['Chris Wilson']
    campaign: Eberron
    code: EB-DC-COG-01
    date_created: 20230221
    hours: 2
    tiers: None
    url: https://www.dmsguild.com/product/427667/EBDCCOG01-Off-the-Books?filters=0_0_100057_0_0_0_0_0
  - product_id: Wrongs-and-Punishment--An-Eberron-Salvage-Mission
    full_title: Wrongs and Punishment: An Eberron Salvage Mission
    authors: ['Nicolás Carrillo']
    campaign: ['Eberron']
    code: EB-SM-WRONGS
    date_created: 20201016
    hours: 2
    tiers: None
    url: https://www.dmsguild.com/product/332476/Wrongs-and-Punishment-An-Eberron-Salvage-Mission?filters=1000043_0_0_0_0_0_0_0
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
