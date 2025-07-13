import json
import os
import re

def slugify(text):
    text = str(text).strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+', '', text)
    text = re.sub(r'-+$', '', text)
    return text

def generate_markdown_page(filename, title, adventures):
    content = f"""---
layout: adventure_list
title: {title}
adventures:
"""
    for adventure in adventures:
        content += f"""  - product_id: {adventure.get('product_id')}
    full_title: {adventure.get('full_title')}
    authors: {adventure.get('authors')}
    campaign: {adventure.get('campaign')}
    code: {adventure.get('code')}
    date_created: {adventure.get('date_created')}
    hours: {adventure.get('hours')}
    tiers: {adventure.get('tiers')}
    url: {adventure.get('url')}
"""
    content += """---

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
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, '..', '_data', 'all_adventures.json')
    adventures_dir = os.path.join(script_dir, '..', '_adventures')

    with open(data_file, 'r', encoding='utf-8') as f:
        adventures_data = json.load(f)

    # Create a directory for the generated pages
    os.makedirs(adventures_dir, exist_ok=True)

    # Generate all adventures page
    generate_markdown_page(os.path.join(adventures_dir, 'all_adventures.md'), 'All Adventures', adventures_data)

    # Get unique values for filtering
    campaigns = sorted(list(set(','.join(a['campaign']) if isinstance(a.get('campaign'), list) else a.get('campaign') for a in adventures_data if a.get('campaign'))))
    hours = sorted(list(set(a['hours'] for a in adventures_data if a.get('hours'))))
    tiers = sorted(list(set(a['tiers'] for a in adventures_data if a.get('tiers'))))

    # Generate pages for each campaign
    for campaign in campaigns:
        filtered_adventures = [a for a in adventures_data if (isinstance(a.get('campaign'), list) and campaign in a.get('campaign')) or (isinstance(a.get('campaign'), str) and a.get('campaign') == campaign)]
        generate_markdown_page(os.path.join(adventures_dir, f'{slugify(campaign)}_adventures.md'), f'Adventures in {campaign}', filtered_adventures)

    # Generate pages for each tier
    for tier in tiers:
        filtered_adventures = [a for a in adventures_data if a.get('tiers') == tier]
        generate_markdown_page(os.path.join(adventures_dir, f'tier_{slugify(tier)}_adventures.md'), f'Adventures Tier {tier}', filtered_adventures)

    # Generate pages for each duration (hours)
    for hour in hours:
        filtered_adventures = [a for a in adventures_data if a.get('hours') == hour]
        generate_markdown_page(os.path.join(adventures_dir, f'duration_{slugify(hour)}_hours_adventures.md'), f'Adventures of {hour} Hours', filtered_adventures)

    # Generate pages for campaign and tier combinations
    for campaign in campaigns:
        for tier in tiers:
            filtered_adventures = [a for a in adventures_data if ((isinstance(a.get('campaign'), list) and campaign in a.get('campaign')) or (isinstance(a.get('campaign'), str) and a.get('campaign') == campaign)) and a.get('tiers') == tier]
            if filtered_adventures:
                generate_markdown_page(os.path.join(adventures_dir, f'{slugify(campaign)}_tier_{slugify(tier)}_adventures.md'), f'Adventures in {campaign}, Tier {tier}', filtered_adventures)

    # Generate pages for campaign and hours combinations
    for campaign in campaigns:
        for hour in hours:
            filtered_adventures = [a for a in adventures_data if ((isinstance(a.get('campaign'), list) and campaign in a.get('campaign')) or (isinstance(a.get('campaign'), str) and a.get('campaign') == campaign)) and a.get('hours') == hour]
            if filtered_adventures:
                generate_markdown_page(os.path.join(adventures_dir, f'{slugify(campaign)}_duration_{slugify(hour)}_hours_adventures.md'), f'Adventures in {campaign}, {hour} Hours', filtered_adventures)

    # Generate pages for tier and hours combinations
    for tier in tiers:
        for hour in hours:
            filtered_adventures = [a for a in adventures_data if a.get('tiers') == tier and a.get('hours') == hour]
            if filtered_adventures:
                generate_markdown_page(os.path.join(adventures_dir, f'tier_{slugify(tier)}_duration_{slugify(hour)}_hours_adventures.md'), f'Adventures Tier {tier}, {hour} Hours', filtered_adventures)

    # Generate pages for campaign, tier, and hours combinations
    for campaign in campaigns:
        for tier in tiers:
            for hour in hours:
                filtered_adventures = [a for a in adventures_data if ((isinstance(a.get('campaign'), list) and campaign in a.get('campaign')) or (isinstance(a.get('campaign'), str) and a.get('campaign') == campaign)) and a.get('tiers') == tier and a.get('hours') == hour]
                if filtered_adventures:
                    generate_markdown_page(os.path.join(adventures_dir, f'{slugify(campaign)}_tier_{slugify(tier)}_duration_{slugify(hour)}_hours_adventures.md'), f'Adventures in {campaign}, Tier {tier}, {hour} Hours', filtered_adventures)

if __name__ == '__main__':
    main()
