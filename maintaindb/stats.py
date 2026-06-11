import pathlib
import os
import logging
import sys
import json
import datetime
from collections import defaultdict

try:
    from .adventure import DungeonCraft
    from .adventure_utils import normalize_season_display, CAMPAIGN_BITMASK, resolve_al_season
    from .paths import STATS_JSON, CATALOG_JSON
except (ImportError, ValueError):
    from adventure import DungeonCraft
    from adventure_utils import normalize_season_display, CAMPAIGN_BITMASK, resolve_al_season
    from paths import STATS_JSON, CATALOG_JSON
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


def _tier_label(tier):
    """Return a canonical stats label for a tier value, or None if unknown."""
    if tier in (1, 2, 3, 4):
        return f'Tier {tier}'
    return None


def _duration_label(hour):
    return f'{hour} Hours'


def normalize_tier_stats(raw):
    """
    Normalize tier counts to canonical 'Tier 1'..'Tier 4' + 'Unknown' keys.
    Accepts legacy numeric-key stats (0-indexed or 1-indexed).
    """
    normalized = {f'Tier {i}': 0 for i in range(1, 5)}
    normalized['Unknown'] = 0

    if any(k.startswith('Tier ') for k in raw):
        for key, count in raw.items():
            if key in normalized:
                normalized[key] += count
            elif key == 'Unknown':
                normalized['Unknown'] += count
        return normalized

    numeric_keys = [int(k) for k in raw if str(k).isdigit()]
    if not numeric_keys:
        normalized['Unknown'] = raw.get('Unknown', 0)
        return normalized

    zero_indexed = 0 in numeric_keys

    for key, count in raw.items():
        if not str(key).isdigit():
            if key == 'Unknown':
                normalized['Unknown'] += count
            continue
        n = int(key)
        if zero_indexed:
            if 0 <= n <= 3:
                normalized[f'Tier {n + 1}'] += count
            else:
                normalized['Unknown'] += count
        elif 1 <= n <= 4:
            normalized[f'Tier {n}'] += count
        else:
            normalized['Unknown'] += count

    return normalized


def normalize_duration_stats(raw):
    """
    Normalize duration counts to canonical 'N Hours' keys (+ All Others, Unknown).
    Accepts legacy bare numeric keys ('1' instead of '1 Hours').
    """
    normalized = defaultdict(int)
    for key, count in raw.items():
        if key in ('All Others', 'Unknown'):
            normalized[key] += count
            continue
        if isinstance(key, str) and key.endswith(' Hours'):
            normalized[key] += count
            continue
        if str(key).isdigit():
            normalized[_duration_label(int(key))] += count
            continue
        normalized[key] += count
    return dict(normalized)

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
        return True, '10 - Icewind Dale (Plague of Ancients)'
    if 'WBW' in code_upper or code_upper.startswith('WBW-DC') or code_upper.startswith('DC-WBW'):
        return True, 'Wild Beyond the Witchlight (WBW-DC)'
    if code_upper.startswith('SJ-DC') or code_upper.startswith('DC-SJ'):
        return True, 'Spelljammer (SJ-DC)'
    return False, None

def catalog_entry_to_dungeoncraft_params(entry):
    """
    Maps a minified catalog entry back to parameters for DungeonCraft.
    """
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

    # Map abbreviated keys back to DungeonCraft param names
    d = {key_map[k]: v for k, v in entry.items() if k in key_map}

    # 't' is omitted from the catalog entry when tiers is None (see aggregator.py)
    d.setdefault('tiers', None)

    # Decode campaign bitmask if necessary
    if 'campaigns' in d and isinstance(d['campaigns'], int):
        bitmask = d['campaigns']
        d['campaigns'] = [name for name, bit in CAMPAIGN_BITMASK.items() if bitmask & bit]
    
    # Safely parse date_created (YYYYMMDD)
    date_created_str = d.get('date_created')
    if date_created_str:
        try:
            d['date_created'] = datetime.datetime.strptime(date_created_str, "%Y%m%d").date()
        except (ValueError, TypeError):
            d['date_created'] = None
    else:
        d['date_created'] = None
        
    return d

def generate_stats():
    with open(adventures_input_path, 'r', encoding='utf-8') as f:
        catalog_data = json.load(f)
        
        if isinstance(catalog_data, dict):
            raw_catalog = catalog_data.get('adventures', [])
        else:
            raw_catalog = catalog_data
            
        data = []
        for entry in raw_catalog:
            d = catalog_entry_to_dungeoncraft_params(entry)
            data.append((DungeonCraft(**d), entry))

    stats = {
        'tier': defaultdict(int),
        'duration': defaultdict(int),
        'campaign': defaultdict(int),
        'season': defaultdict(int),
        'ai_assisted': defaultdict(int),
        'seed_by_season': defaultdict(lambda: defaultdict(int))
    }

    # Standard duration hours we want to track separately
    standard_durations = {1, 2, 4, 6, 8}

    for adventure, entry in data:
        tier_label = _tier_label(adventure.tiers)
        if tier_label:
            stats['tier'][tier_label] += 1
        else:
            stats['tier']['Unknown'] += 1

        ac = entry.get('ac')
        if ac == 2:
            stats['ai_assisted']['AI assisted'] += 1
        elif ac == 1:
            stats['ai_assisted']['Human-created (disclosed)'] += 1
        else:
            stats['ai_assisted']['Not disclosed'] += 1

        if adventure.hours:
            parsed_hours = _parse_hours_string(adventure.hours)
            if parsed_hours:
                for hour in parsed_hours:
                    if hour in standard_durations:
                        stats['duration'][_duration_label(hour)] += 1
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
        
        al_season = resolve_al_season(season=adventure.season, code=adventure.code)
        if al_season:
            stats['season'][al_season] += 1
        
        # Collect seed statistics for POA/WBW/SJ campaigns
        if adventure.code:
            is_required, season_name = is_seed_required_code(adventure.code)
            if is_required and hasattr(adventure, 'seed') and adventure.seed:
                # Normalize seed name to handle variations (e.g., "St. Argol's Fire" vs "Saint Argol's Fire")
                normalized_seed = normalize_seed_name(adventure.seed)
                stats['seed_by_season'][season_name][normalized_seed] += 1
    
    # Convert nested defaultdicts to regular dicts for JSON serialization
    stats['tier'] = normalize_tier_stats(dict(stats['tier']))
    stats['duration'] = normalize_duration_stats(dict(stats['duration']))
    stats['ai_assisted'] = dict(stats['ai_assisted'])
    stats['seed_by_season'] = {
        season: dict(seed_counts) 
        for season, seed_counts in stats['seed_by_season'].items()
    }
    
    # Add timestamp for cache busting
    stats['timestamp'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            
    with open(stats_output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    
    logger.info(f"Stats generated and saved to {stats_output_path}")


if __name__ == '__main__':
    generate_stats()