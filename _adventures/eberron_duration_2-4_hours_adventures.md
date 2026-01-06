---
layout: adventure_list
title: Adventures in Eberron, 2-4 Hours
adventures:
  - product_id: 248589
    full_title: "What's Past is Prologue"
    authors: ["Alan Patrick"]
    campaign: ["Eberron"]
    code: DDAL-ELW00
    date_created: 20180921
    hours: 2-4
    tiers: 0
    url: https://www.dmsguild.com/product/248589/?affiliate_id=171040
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
  - product_id: 257230
    full_title: "Against the Lightning"
    authors: ["Will Doyle"]
    campaign: ["Eberron"]
    code: DDAL-ELW05
    date_created: 20181026
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/257230/?affiliate_id=171040
  - product_id: 257741
    full_title: "A Holy Visit"
    authors: ["Ashley Warren"]
    campaign: ["Eberron"]
    code: DDAL-ELW06
    date_created: 20181101
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/257741/?affiliate_id=171040
  - product_id: 258975
    full_title: "Blades of Terror"
    authors: ["Lysa Chen"]
    campaign: ["Eberron"]
    code: DDAL-ELW07
    date_created: 20181116
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/258975/?affiliate_id=171040
  - product_id: 258976
    full_title: "The Kundarak Job"
    authors: ["Shawn Merwin"]
    campaign: ["Eberron"]
    code: DDAL-ELW08
    date_created: 20181116
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/258976/?affiliate_id=171040
  - product_id: 260064
    full_title: "Searching for Secrets"
    authors: ["Travis Woodall"]
    campaign: ["Eberron"]
    code: DDAL-ELW09
    date_created: 20181130
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/260064/?affiliate_id=171040
  - product_id: 260858
    full_title: "The Killing Blade"
    authors: ["Robert Adducci"]
    campaign: ["Eberron"]
    code: DDAL-ELW10
    date_created: 20181207
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/260858/?affiliate_id=171040
  - product_id: 261301
    full_title: "Secrets Below"
    authors: ["M.T. Black"]
    campaign: ["Eberron"]
    code: DDAL-ELW11
    date_created: 20181214
    hours: 2-4
    tiers: 2
    url: https://www.dmsguild.com/product/261301/?affiliate_id=171040
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
