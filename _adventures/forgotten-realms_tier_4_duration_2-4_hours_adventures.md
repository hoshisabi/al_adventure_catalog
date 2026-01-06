---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 4, 2-4 Hours
adventures:
  - product_id: 433917
    full_title: "A Grim and Ravenous Arrival"
    authors: ["Andy Dempz", "Gamehole Con"]
    campaign: ["Forgotten Realms"]
    code: PO-BK-02-10
    date_created: 20230414
    hours: 2-4
    tiers: 4
    url: https://www.dmsguild.com/product/433917/?affiliate_id=171040
  - product_id: 496426
    full_title: "And Then They Attacked"
    authors: ["Death 101010"]
    campaign: ["Forgotten Realms"]
    code: PS-DC-ELEMENT-DEATH-02
    date_created: 20240924
    hours: 2-4
    tiers: 4
    url: https://www.dmsguild.com/product/496426/?affiliate_id=171040
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
