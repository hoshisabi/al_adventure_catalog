import pathlib
import os
import logging
import sys
import json
import datetime
from collections import defaultdict

from adventure import DungeonCraft
import glob

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
stats_output_path = os.path.join(root, '..', 'assets', 'data', 'stats.json')
adventures_input_path = os.path.join(root, '..', 'assets', 'data', 'all_adventures.json')

def _parse_hours_string(hours_str):
    if not hours_str:
        return []
    hours_list = []
    for part in hours_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            hours_list.extend(range(start, end + 1))
        else:
            hours_list.append(int(part))
    return hours_list

def generate_stats():
    with open(adventures_input_path) as f:
        raw_data = json.load(f)
        data = []
        for d in raw_data:
            d['title'] = d.pop('full_title')
            d['date_created'] = datetime.datetime.strptime(d['date_created'], "%Y%m%d").date()
            d['season'] = d.get('season')

            # Handle the transition from 'campaign' (singular) to 'campaigns' (plural)
            # Ensure 'campaigns' is always a list
            if 'campaign' in d:
                campaign_value = d.pop('campaign') # Remove the old 'campaign' key
                if isinstance(campaign_value, list):
                    d['campaigns'] = campaign_value
                else:
                    d['campaigns'] = [campaign_value]
            else:
                d['campaigns'] = [] # Default to empty list if no campaign data

            data.append(DungeonCraft(**d))

    stats = {
        'tier': defaultdict(int),
        'duration': defaultdict(int),
        'campaign': defaultdict(int),
        'season': defaultdict(int)
    }

    for adventure in data:
        if adventure.tiers:
            stats['tier'][f'Tier {adventure.tiers}'] += 1
        else:
            stats['tier']['Unknown'] += 1

        if adventure.hours:
            for hour in _parse_hours_string(adventure.hours):
                stats['duration'][f'{hour} Hours'] += 1
        else:
            stats['duration']['Unknown'] += 1
        
        if adventure.campaigns:
            for campaign_name in adventure.campaigns:
                stats['campaign'][campaign_name] += 1
        else:
            stats['campaign']['Unknown'] += 1
        
        if adventure.season:
            stats['season'][adventure.season] += 1
        else:
            stats['season']['Unknown'] += 1
            
    with open(stats_output_path, 'w') as f:
        json.dump(stats, f, indent=4)
    
    logger.info(f"Stats generated and saved to {stats_output_path}")


if __name__ == '__main__':
    generate_stats()