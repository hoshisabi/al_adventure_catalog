---
layout: adventure_list
title: Adventures in Ravenloft, Tier 2, 3 Hours
adventures:
  - product_id: 380627
    full_title: "Unexpected Hospitality"
    authors: ["Casper Kirketerp-Helenius"]
    campaign: ["Ravenloft"]
    code: RMH-05
    date_created: 20211214
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/380627/?affiliate_id=171040
  - product_id: 380630
    full_title: "RMH-06 Amber Reclamation"
    authors: ["Ayanna Jones-Lightsy"]
    campaign: ["Ravenloft"]
    code: RMH-06
    date_created: 20211214
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/380630/?affiliate_id=171040
  - product_id: 383265
    full_title: "RMH-07 The City of Dreams"
    authors: ["Jay Africa"]
    campaign: ["Ravenloft"]
    code: RMH-07
    date_created: 20220112
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/383265/?affiliate_id=171040
  - product_id: 383275
    full_title: "RMH-08 The Palace of Bones"
    authors: ["Kat Kruger"]
    campaign: ["Ravenloft"]
    code: RMH-08
    date_created: 20220112
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/383275/?affiliate_id=171040
  - product_id: 386609
    full_title: "RMH-09 The Deadliest Game"
    authors: ["The GM Tim"]
    campaign: ["Ravenloft"]
    code: RMH-09
    date_created: 20220211
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/386609/?affiliate_id=171040
  - product_id: 387334
    full_title: "RMH-10 Scion of Darkness"
    authors: ["Marcello De Velazquez"]
    campaign: ["Ravenloft"]
    code: RMH-10
    date_created: 20220218
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/387334/?affiliate_id=171040
  - product_id: 389773
    full_title: "RMH-11 Calling Upon the Dead"
    authors: ["Gabrielle Harbowy"]
    campaign: ["Ravenloft"]
    code: RMH-11
    date_created: 20220310
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/389773/?affiliate_id=171040
  - product_id: 389775
    full_title: "RMH-12 Beneath the New Star"
    authors: ["Steffie de Vaan"]
    campaign: ["Ravenloft"]
    code: RMH-12
    date_created: 20220314
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/389775/?affiliate_id=171040
  - product_id: 390632
    full_title: "RMH-EP-02 A Darklord's Denouement"
    authors: ["Ginny Loveday", "Jeremy Forbing"]
    campaign: ["Ravenloft"]
    code: RMH-EP-02
    date_created: 20220318
    hours: 3
    tiers: 2
    url: https://www.dmsguild.com/product/390632/?affiliate_id=171040
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
