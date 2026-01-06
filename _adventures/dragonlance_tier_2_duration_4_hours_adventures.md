---
layout: adventure_list
title: Adventures in Dragonlance, Tier 2, 4 Hours
adventures:
  - product_id: 463522
    full_title: "A Mother's Love: A Dragonlance Adventures Experience"
    authors: ["Marcello De Velazquez"]
    campaign: ["Dragonlance"]
    code: DL-DC-MDV-01
    date_created: 20231211
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/463522/?affiliate_id=171040
  - product_id: 491735
    full_title: "Dragons of Heresy"
    authors: ["D&D Adventurers League"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-04
    date_created: 20240815
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/491735/?affiliate_id=171040
  - product_id: 508960
    full_title: "Dragons of Affliction"
    authors: ["Jon Christian,", "Zac Goins"]
    campaign: ["Dragonlance"]
    code: BMG-DL-VOTU-05
    date_created: 20250116
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/508960/?affiliate_id=171040
  - product_id: 515257
    full_title: "Dragons of Future Past"
    authors: ["D&D Adventurers League"]
    campaign: ["Dragonlance"]
    code: BMG-DLEP-VOTU-02
    date_created: 20250313
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/515257/?affiliate_id=171040
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
