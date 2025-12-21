import pathlib
import os
import logging
import sys
import json
import glob
import re
from collections import defaultdict

from .adventure import DC_CAMPAIGNS, DDAL_CAMPAIGN, get_dc_code_and_campaign
from .adventure_utils import normalize_ddal_ddex_code
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
    logger.info(f'Writting aggregated data at: {output_path}')
    for dc_season, dc_list in aggregated_by_dc_code.items():
        output_full_path = f"{str(output_path)}/{dc_season}.json"
        with open(output_full_path, 'w', encoding='utf-8') as f:
            json.dump(dc_list, f, indent=4, sort_keys=True, ensure_ascii=False)

    output_full_path = f"{str(output_path)}/all_adventures.json"
    with open(output_full_path, 'w', encoding='utf-8') as f:
        json.dump(list(all_adventures_map.values()), f, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    aggregate()
    # crawl_dc_listings(page_number=2, max_results=15)
