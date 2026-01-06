---
layout: adventure_list
title: Adventures in Forgotten Realms, Tier 1, 3 Hours
adventures:
  - product_id: 340333
    full_title: "The Great Knucklehead Rally"
    authors: ["Celeste Conowitch", "Shawn Merwin"]
    campaign: ["Forgotten Realms"]
    code: DDEP10-00
    date_created: 20201217
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/340333/?affiliate_id=171040
  - product_id: 517244
    full_title: "The Secret in Sanctuary"
    authors: ["Greg Wright"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-SSG-FAI-01
    date_created: 20250401
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/517244/?affiliate_id=171040
  - product_id: 545526
    full_title: "The Communion of Laughter"
    authors: ["Greg Wright"]
    campaign: ["Forgotten Realms"]
    code: FR-DC-SSG-FAI-02-
    date_created: 20251111
    hours: 3
    tiers: 1
    url: https://www.dmsguild.com/product/545526/?affiliate_id=171040
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
