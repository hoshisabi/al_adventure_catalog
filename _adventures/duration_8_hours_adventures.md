---
layout: adventure_list
title: Adventures of 8 Hours
adventures:
  - product_id: DDEX03-16-Assault-on-Maerimydra-5e
    full_title: DDEX03-16 Assault on Maerimydra (5e)
    authors: ['Wizards of the Coast']
    campaign: ['Forgotten Realms']
    code: DDEX03-16
    date_created: 20160322
    hours: 8
    tiers: None
    url: https://www.dmsguild.com/product/177572/DDEX0316-Assault-on-Maerimydra-5e
  - product_id: None
    full_title: CCC-6SWORDS-01 Six Swords Out of Hell
    authors: ['Andrew Bishkinskyi']
    campaign: Forgotten Realms
    code: CCC-6SWORDS-01
    date_created: 20200720
    hours: 8
    tiers: None
    url: https://www.dmsguild.com/product/313874/Six-Swords-Out-of-Hell?filters=45470_0_0_0_0_0_0_0
  - product_id: Tyches-Torment
    full_title: Tyche's Torment
    authors: ['Matthew Whitby', 'Ginny Loveday', 'Sadie Lowry']
    campaign: None
    code: None
    date_created: 20200911
    hours: 8
    tiers: None
    url: https://www.dmsguild.com/product/328075/Tyches-Torment
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
