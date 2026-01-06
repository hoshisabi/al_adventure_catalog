"""
Aggregates individual adventure JSON files from `_dc/` into a minified `catalog.json`.

This script processes all JSON files in the `_dc/` directory, normalizes adventure data 
(codes, campaigns, tiers, hours, seasons), and generates a consolidated catalog 
used by the Jekyll site's filtering system.

Key features:
- Data normalization for consistent filtering (campaigns as lists, integer tiers, string hours).
- DDAL/DDEX code normalization (e.g., DDEX3 -> DDEX03).
- Intelligent season formatting (e.g., "11 - The Wild Beyond the Witchlight").
- Minified output payload with abbreviated keys to reduce file size.
- Automatic affiliate ID injection for DMsGuild URLs.

Output:
- `assets/data/catalog.json`: Minified JSON file with abbreviated keys.
"""
import pathlib
import os
import logging
import sys
import json
import glob
import re
from collections import defaultdict

from .adventure import DC_CAMPAIGNS, DDAL_CAMPAIGN, get_dc_code_and_campaign
from .adventure import DC_CAMPAIGNS, DDAL_CAMPAIGN, get_dc_code_and_campaign
from .adventure_utils import normalize_ddal_ddex_code, SEASONS
from .paths import DC_DIR, STATS_DIR

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

# Use centralized path configuration
input_path = str(DC_DIR)
output_path = str(STATS_DIR)

all_adventures_map = {}

def __add_to_map(data, aggregated_by_dc_code):
    if 'code' not in data or data['code'] is None:
        logger.info(f">> {data.get('full_title', 'UNKNOWN TITLE')} missing code")
        return

    # Normalize the code first (e.g., DDEX3 -> DDEX03) to ensure consistent grouping
    normalized_code = normalize_ddal_ddex_code(data['code'])
    # Update the code in data to the normalized version
    data['code'] = normalized_code

    # Extract the prefix for grouping (e.g., "DDEX03" from "DDEX03-01")
    # For DDAL/DDEX codes, extract the season prefix (DDEX03, DDAL05, etc.)
    code_prefix_match = re.match(r'^(DDEX|DDAL)(\d{2})', normalized_code.upper())
    if code_prefix_match:
        # Extract normalized prefix (e.g., DDEX03 from DDEX03-01)
        normalized_prefix = code_prefix_match.group(0)  # e.g., "DDEX03"
    else:
        # For other codes, try to match against known prefixes
        normalized_prefix = None

    # Check if code matches DC_CAMPAIGNS
    dc_code = None
    for code in DC_CAMPAIGNS:
        if normalized_code.upper().startswith(code.upper()):
            dc_code = code
            break

    # If not found in DC_CAMPAIGNS, check DDAL_CAMPAIGN (for DDEX, DDAL, CCC, etc.)
    if not dc_code:
        # If we extracted a normalized prefix, prefer matching that first
        if normalized_prefix and normalized_prefix in DDAL_CAMPAIGN:
            dc_code = normalized_prefix
        else:
            # Fall back to iterating through DDAL_CAMPAIGN, checking longer prefixes first
            # Sort by length descending to check longer prefixes first (e.g., DDEX03 before DDEX3)
            for code in sorted(DDAL_CAMPAIGN.keys(), key=lambda x: len(x), reverse=True):
                if normalized_code.upper().startswith(code.upper()):
                    dc_code = code
                    break

    # Use product_id for deduplication
    product_id = data.get('product_id')
    if product_id:
        key = product_id
    else:
        # Generate a fallback key if product_id is missing
        key = f"{data.get('full_title', 'UNKNOWN')}-{data.get('date_created', 'UNKNOWN')}"
        logger.warning(f"Using fallback key for '{data.get('full_title', 'UNKNOWN TITLE')}' due to missing product_id.")

    # Always add to all_adventures_map if it has a code (regardless of DC_CAMPAIGNS match)
    all_adventures_map[key] = data
    
    # Only add to aggregated_by_dc_code if it matches a DC code
    # Use normalized_prefix if we extracted one (for consistent grouping of DDAL/DDEX codes)
    grouping_key = normalized_prefix if normalized_prefix and normalized_prefix in DDAL_CAMPAIGN else dc_code
    if grouping_key:
        # Ensure the category exists in aggregated_by_dc_code
        if grouping_key.upper() not in aggregated_by_dc_code:
            aggregated_by_dc_code[grouping_key.upper()] = []
        aggregated_by_dc_code[grouping_key.upper()].append(data)

def aggregate():
    """
    Main aggregation function.
    
    1. Reads all .json files from DC_DIR.
    2. Filters for `is_adventure == True`.
    3. Normalizes fields: campaigns (list), tiers (int), hours (str).
    4. Formats seasons using SEASONS lookup and custom mappings.
    5. Maps data to abbreviated keys:
       - i: product_id
       - n: title
       - c: code
       - a: authors
       - p: campaigns
       - s: season
       - h: hours
       - t: tiers
       - u: url
       - d: date_created
    6. Writes minified JSON to `assets/data/catalog.json`.
    """
    aggregated_by_dc_code = defaultdict(list)
    for code in DC_CAMPAIGNS:
        aggregated_by_dc_code[code.upper()] = []

    logger.info(f'Reading all files at: {input_path}')
    input_full_path = f"{str(input_path)}/*.json"
    for file in glob.glob(input_full_path):
        with open(file, 'r', encoding='utf-8') as _input:
            try:
                data = json.load(_input)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to load JSON from {file}: {e}")
                continue

            is_adventure = data.get('is_adventure', True)
            if is_adventure:
                # Populate campaigns from product_title if not already present
                if not data.get('campaigns'):
                    _, campaigns_from_title = get_dc_code_and_campaign(data.get('full_title'))
                    if campaigns_from_title:
                        data['campaigns'] = campaigns_from_title

                if "url" in data and data["url"] and "affiliate_id" not in data["url"]:
                    data["url"] += "&affiliate_id=171040"
                
                # Normalize 'campaigns' to be a list
                if 'campaigns' in data:
                    if not isinstance(data['campaigns'], list):
                        data['campaigns'] = [data['campaigns']]
                elif 'campaign' in data: # Fallback to singular 'campaign' if 'campaigns' not found
                    if not isinstance(data['campaign'], list):
                        data['campaigns'] = [data['campaign']]
                    else:
                        data['campaigns'] = data['campaign']
                    del data['campaign'] # Remove the old singular key
                else:
                    data['campaigns'] = [] # Ensure it's always a list

                # Normalize 'tiers' to be an integer
                if 'tiers' in data and isinstance(data['tiers'], str) and '-' in data['tiers']:
                    data['tiers'] = int(data['tiers'].split('-')[0])
                elif 'tiers' in data and data['tiers'] is None:
                    data['tiers'] = 0 # Or some other default integer value

                # Ensure 'hours' is always a string
                if 'hours' in data and data['hours'] is None:
                    data['hours'] = ''
                elif 'hours' in data and not isinstance(data['hours'], str):
                    data['hours'] = str(data['hours'])
                
                __add_to_map(data, aggregated_by_dc_code)
            else:
                logger.info(f"Skipping '{data.get('full_title', 'UNKNOWN TITLE')}' as it is not an adventure.")
    
    logger.info("------")
    logger.info(f'Aggregated stats:')
    for dc_season, dc_list in aggregated_by_dc_code.items():
        logger.info(f'  {dc_season} :: {len(dc_list)} DCs')

    logger.info("------")
    # Use ASSETS_DATA_DIR logic or relative path
    assets_data_path = pathlib.Path(output_path).parent.parent / 'assets' / 'data'
    assets_data_path.mkdir(parents=True, exist_ok=True)
    logger.info(f'Writing consolidated catalog to: {assets_data_path}')

    # Pre-defined mappings for recent seasons
    CUSTOM_SEASON_MAPPINGS = {
        '0': 'Season Agnostic',
        '11': 'The Wild Beyond the Witchlight',
        '12': 'Spelljammer',
        '13': 'Planescape'
    }

    catalog = []

    for adventure in all_adventures_map.values():
        # Format Season: "N - Name"
        raw_season = adventure.get('season')
        formatted_season = raw_season
        
        if raw_season:
            r_str = str(raw_season)
            # 1. Check custom mappings (strings "0", "11", etc.)
            if r_str in CUSTOM_SEASON_MAPPINGS:
                formatted_season = f"{r_str} - {CUSTOM_SEASON_MAPPINGS[r_str]}"
            # 2. Check strict integers (e.g. from Derived logic)
            elif r_str.isdigit():
                 i_val = int(r_str)
                 if i_val in SEASONS:
                     formatted_season = f"{r_str} - {SEASONS[i_val]}"
                 else:
                     formatted_season = r_str
            # 3. Check if it is a Name (e.g. "Tyranny of Dragons") -> Reverse Lookup
            else:
                 # Try to find the Key (ID) for this Value (Name) in SEASONS
                 # SEASONS keys are mix of int and str
                 found_id = None
                 for k, v in SEASONS.items():
                     if v.lower() == r_str.lower():
                         found_id = k
                         break
                 
                 if found_id is not None:
                     formatted_season = f"{found_id} - {r_str}"
                 else:
                     # Leave as is
                     formatted_season = r_str
            
        # Minified Payload with Abbreviated Keys
        # i: product_id (was id)
        # n: title/full_title (was t)
        # c: code
        # a: authors
        # p: campaigns (was ca)
        # s: season
        # h: hours
        # t: tiers (was ti)
        # u: url
        # d: date_created
        
        entry = {
            'i': adventure.get('product_id'),
            'n': adventure.get('title') or adventure.get('full_title'),
            'c': adventure.get('code'),
            'a': adventure.get('authors'),
            'p': adventure.get('campaigns'),
            's': formatted_season, 
            'h': adventure.get('hours'),
            't': adventure.get('tiers'),
            'u': adventure.get('url'),
            'd': adventure.get('date_created')
        }
        catalog.append(entry)
        
    with open(assets_data_path / "catalog.json", 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=None, ensure_ascii=False)

    logger.info(f"Generated consolidated catalog: catalog.json ({len(catalog)} items)")


if __name__ == '__main__':
    aggregate()
    # crawl_dc_listings(page_number=2, max_results=15)
