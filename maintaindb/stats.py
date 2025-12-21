import pathlib
import os
import logging
import sys
import json
import datetime
from collections import defaultdict

from .adventure import DungeonCraft
from .paths import STATS_JSON, ALL_ADVENTURES_ASSETS
import glob

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

# Use centralized path configuration
stats_output_path = str(STATS_JSON)
adventures_input_path = str(ALL_ADVENTURES_ASSETS)

def _parse_hours_string(hours_str):
    """Parse hours string into a list of hour values. Handles ranges and single values."""
    if not hours_str:
        return []
    hours_list = []
    try:
        for part in hours_str.split(','):
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    hours_list.extend(range(start, end + 1))
                except (ValueError, IndexError):
                    # Skip malformed ranges
                    continue
            else:
                try:
                    hours_list.append(int(part))
                except ValueError:
                    # Skip non-numeric values
                    continue
    except (AttributeError, TypeError):
        # hours_str is not a string, return empty list
        return []
    return hours_list

def is_seed_required_code(code):
    """Check if code belongs to POA, WBW, or SJ campaigns that require seeds.
    Returns (is_required, season_name) tuple."""
    if not code:
        return False, None
    code_upper = code.upper()
    if 'POA' in code_upper or code_upper.startswith('DC-POA'):
        return True, 'Icewind Dale (DC-POA)'
    if 'WBW' in code_upper or code_upper.startswith('WBW-DC') or code_upper.startswith('DC-WBW'):
        return True, 'Wild Beyond the Witchlight (WBW-DC)'
    if code_upper.startswith('SJ-DC') or code_upper.startswith('DC-SJ'):
        return True, 'Spelljammer (SJ-DC)'
    return False, None

def generate_stats():
    with open(adventures_input_path) as f:
        raw_data = json.load(f)
        data = []
        # Define the expected parameters for DungeonCraft.__init__
        expected_params = {
            'product_id', 'title', 'authors', 'code', 'date_created', 'hours', 
            'tiers', 'apl', 'level_range', 'url', 'campaigns', 'season', 
            'is_adventure', 'price', 'payWhatYouWant', 'suggestedPrice', 'needs_review', 'seed'
        }
        
        for d in raw_data:
            # Skip non-adventures (bundles, Roll20, Fantasy Grounds)
            if not d.get('is_adventure', False):
                continue
            
            # Safely get full_title with fallback
            d['title'] = d.pop('full_title', d.get('title', ''))
            
            # Safely parse date_created
            date_created_str = d.get('date_created')
            if date_created_str:
                try:
                    d['date_created'] = datetime.datetime.strptime(date_created_str, "%Y%m%d").date()
                except (ValueError, TypeError):
                    # If date parsing fails, set to None
                    d['date_created'] = None
            else:
                d['date_created'] = None
            
            d['season'] = d.get('season')

            # Handle the transition from 'campaign' (singular) to 'campaigns' (plural)
            # Ensure 'campaigns' is always a list
            if 'campaign' in d:
                campaign_value = d.pop('campaign') # Remove the old 'campaign' key
                if isinstance(campaign_value, list):
                    d['campaigns'] = campaign_value
                else:
                    d['campaigns'] = [campaign_value] if campaign_value else []
            else:
                d['campaigns'] = d.get('campaigns', []) # Use existing campaigns or default to empty list

            # Filter out any unexpected keys (like 'id') before passing to DungeonCraft
            filtered_d = {k: v for k, v in d.items() if k in expected_params}
            data.append(DungeonCraft(**filtered_d))

    stats = {
        'tier': defaultdict(int),
        'duration': defaultdict(int),
        'campaign': defaultdict(int),
        'season': defaultdict(int),
        'seed_by_season': defaultdict(lambda: defaultdict(int))  # season -> seed -> count
    }

    # Standard duration hours we want to track separately
    standard_durations = {1, 2, 4, 6, 8}

    for adventure in data:
        if adventure.tiers:
            stats['tier'][f'Tier {adventure.tiers}'] += 1
        else:
            stats['tier']['Unknown'] += 1

        if adventure.hours:
            parsed_hours = _parse_hours_string(adventure.hours)
            if parsed_hours:
                # Count each hour separately (existing behavior)
                for hour in parsed_hours:
                    if hour in standard_durations:
                        stats['duration'][f'{hour} Hours'] += 1
                    else:
                        stats['duration']['All Others'] += 1
            else:
                stats['duration']['Unknown'] += 1
        else:
            stats['duration']['Unknown'] += 1
        
        if adventure.campaigns:
            for campaign_name in adventure.campaigns:
                # Handle null/None values as strings or actual None
                if campaign_name and campaign_name != 'null' and str(campaign_name).lower() != 'null':
                    stats['campaign'][campaign_name] += 1
                else:
                    stats['campaign']['Unknown'] += 1
        else:
            stats['campaign']['Unknown'] += 1
        
        if adventure.season:
            stats['season'][adventure.season] += 1
        else:
            stats['season']['Unknown'] += 1
        
        # Collect seed statistics for POA/WBW/SJ campaigns
        if adventure.code:
            is_required, season_name = is_seed_required_code(adventure.code)
            if is_required and hasattr(adventure, 'seed') and adventure.seed:
                stats['seed_by_season'][season_name][adventure.seed] += 1
    
    # Convert nested defaultdicts to regular dicts for JSON serialization
    stats['seed_by_season'] = {
        season: dict(seed_counts) 
        for season, seed_counts in stats['seed_by_season'].items()
    }
            
    with open(stats_output_path, 'w') as f:
        json.dump(stats, f, indent=4)
    
    logger.info(f"Stats generated and saved to {stats_output_path}")


if __name__ == '__main__':
    generate_stats()