import pathlib
import os
import logging
import sys
import json
import datetime
from collections import defaultdict

from .adventure import DungeonCraft
from .paths import STATS_JSON, CATALOG_JSON
import glob

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

# Use centralized path configuration
stats_output_path = str(STATS_JSON)
adventures_input_path = str(CATALOG_JSON)

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

def normalize_seed_name(seed):
    """
    Normalize seed names to handle variations and inconsistencies.
    For example, "St. Argol's Fire", "Saint Argol's Fire", "Saint Argols Fire" should all map to the same canonical name.
    """
    if not seed:
        return seed
    
    seed_lower = seed.lower().strip()
    
    # Normalize "St. Argol's Fire" variations
    # Handle variations: "st. argol's fire", "saint argol's fire", "saint argols fire", "st argol's fire", etc.
    if 'argol' in seed_lower and 'fire' in seed_lower:
        # Normalize to "St. Argol's Fire" (canonical form)
        # This handles: "St. Argol's Fire", "Saint Argol's Fire", "Saint Argols Fire", "St Argol's Fire", etc.
        return "St. Argol's Fire"
    
    # Add more normalization rules here as needed for other seed name variations
    # For now, return the original seed if no normalization rule matches
    return seed

def is_seed_required_code(code):
    """Check if code belongs to POA, WBW, or SJ campaigns that require seeds.
    Returns (is_required, season_name) tuple."""
    if not code:
        return False, None
    code_upper = code.upper()
    if 'POA' in code_upper or code_upper.startswith('DC-POA') or code_upper.startswith('DDAL10'):
        return True, 'Icewind Dale (Plague of Ancients)'
    if 'WBW' in code_upper or code_upper.startswith('WBW-DC') or code_upper.startswith('DC-WBW'):
        return True, 'Wild Beyond the Witchlight (WBW-DC)'
    if code_upper.startswith('SJ-DC') or code_upper.startswith('DC-SJ'):
        return True, 'Spelljammer (SJ-DC)'
    return False, None

def generate_stats():
    with open(adventures_input_path, 'r', encoding='utf-8') as f:
        catalog_data = json.load(f)
        
        if isinstance(catalog_data, dict):
            raw_catalog = catalog_data.get('adventures', [])
        else:
            raw_catalog = catalog_data
            
        data = []
        
        # Mapping from minified keys to DungeonCraft parameters
        key_map = {
            'i': 'product_id',
            'n': 'title',
            'a': 'authors',
            'c': 'code',
            'd': 'date_created',
            'h': 'hours',
            't': 'tiers',
            'p': 'campaigns',
            's': 'season',
            'u': 'url',
            'e': 'seed'
        }
        
        for entry in raw_catalog:
            # Map abbreviated keys back to DungeonCraft param names
            d = {key_map[k]: v for k, v in entry.items() if k in key_map}
            
            # Safely parse date_created (YYYYMMDD)
            date_created_str = d.get('date_created')
            if date_created_str:
                try:
                    d['date_created'] = datetime.datetime.strptime(date_created_str, "%Y%m%d").date()
                except (ValueError, TypeError):
                    d['date_created'] = None
            else:
                d['date_created'] = None
            
            # Tiers in catalog are already int or range string, but DungeonCraft might expect specific format
            # Let's ensure it's passed correctly.
            
            # Campaigns are already a list in catalog.json
            
            data.append(DungeonCraft(**d))

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
                # Normalize seed name to handle variations (e.g., "St. Argol's Fire" vs "Saint Argol's Fire")
                normalized_seed = normalize_seed_name(adventure.seed)
                stats['seed_by_season'][season_name][normalized_seed] += 1
    
    # Convert nested defaultdicts to regular dicts for JSON serialization
    stats['seed_by_season'] = {
        season: dict(seed_counts) 
        for season, seed_counts in stats['seed_by_season'].items()
    }
            
    with open(stats_output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    
    logger.info(f"Stats generated and saved to {stats_output_path}")


if __name__ == '__main__':
    generate_stats()