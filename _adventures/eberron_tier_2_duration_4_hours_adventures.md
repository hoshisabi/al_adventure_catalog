---
layout: adventure_list
title: Adventures in Eberron, Tier 2, 4 Hours
adventures:
  - product_id: None
    full_title: A Whisper In Your Mind
    authors: ['Bruce Wood']
    campaign: Eberron
    code: EB-SM-WHISPER
    date_created: 20200511
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/313252/A-Whisper-In-Your-Mind?filters=1000043_0_0_0_0_0_0_0
  - product_id: Deep-Space-Vine
    full_title: Deep Space Vine
    authors: ['Christopher Bagg']
    campaign: Eberron
    code: EB-SM-VINE
    date_created: 20211206
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/379308/Deep-Space-Vine
  - product_id: EB-05-A-Century-of-Ashes
    full_title: EB-05 A Century of Ashes
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-05
    date_created: 20200504
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/312336/EB05-A-Century-of-Ashes?filters=1000043_0_0_0_0_0_0_0
  - product_id: EB-06-The-Last-Word
    full_title: EB-06 The Last Word
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-06
    date_created: 20200603
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/316059/EB06-The-Last-Word?filters=1000043_0_0_0_0_0_0_0
  - product_id: EB-07-Song-of-the-Sky
    full_title: EB-07 Song of the Sky
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-07
    date_created: 20200706
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/319657/EB07-Song-of-the-Sky?filters=1000043_0_0_0_0_0_0_0
  - product_id: EB-08-Parliament-of-Gears
    full_title: EB-08 Parliament of Gears
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-08
    date_created: 20200803
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/322749/EB08-Parliament-of-Gears?filters=1000043_0_0_0_0_0_0_0
  - product_id: EB-09-Lord-Bucket
    full_title: EB-09 Lord Bucket
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-09
    date_created: 20200901
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/326339/EB09-Lord-Bucket?filters=1000043_0_0_0_0_0_0_0
  - product_id: EB-10-Judgment-of-Iron
    full_title: EB-10 Judgment of Iron
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-10
    date_created: 20201006
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/331083/EB10-Judgment-of-Iron?filters=1000043_0_0_0_0_0_0_0
  - product_id: EB-EP-02-Rolling-Thunder
    full_title: EB-EP-02 Rolling Thunder
    authors: ['D&D Adventurers League']
    campaign: ['Eberron']
    code: EB-EP-02
    date_created: 20201110
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/335587/EBEP02-Rolling-Thunder?filters=1000043_0_0_0_0_0_0_0
  - product_id: Eberron--The-Ruin-of-Grave-Metallus
    full_title: Eberron: The Ruin of Grave Metallus
    authors: ['Jon Christian', 'Zac Goins', 'Troy Sandlin']
    campaign: ['Eberron']
    code: EB-SM-METALLUS
    date_created: 20230314
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/430378/Eberron-The-Ruin-of-Grave-Metallus
  - product_id: None
    full_title: Ghost Town
    authors: ['Gregory Hallenbeck']
    campaign: Eberron
    code: EB-SM-GHOST
    date_created: 20200318
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/306912/Ghost-Town?filters=1000043_0_0_0_0_0_0_0
  - product_id: Seaside-Salvage--Eberron-Salvage-Mission-Anthology
    full_title: Seaside Salvage: Eberron Salvage Mission Anthology
    authors: ['Bum Lee']
    campaign: ['Eberron']
    code: EB-SM-SEASIDE
    date_created: 20210308
    hours: 4
    tiers: 2
    url: https://www.dmsguild.com/product/349569/Seaside-Salvage-Eberron-Salvage-Mission-Anthology?filters=1000043_0_0_0_0_0_0_0
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
