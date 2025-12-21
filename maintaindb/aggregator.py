import pathlib
import os
import logging
import sys
import json
import glob
from collections import defaultdict

from .adventure import DC_CAMPAIGNS, DDAL_CAMPAIGN, get_dc_code_and_campaign
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

    # Check if code matches DC_CAMPAIGNS
    dc_code = None
    for code in DC_CAMPAIGNS:
        if data['code'].upper().startswith(code.upper()):
            dc_code = code
            break

    # If not found in DC_CAMPAIGNS, check DDAL_CAMPAIGN (for DDEX, DDAL, CCC, etc.)
    if not dc_code:
        for code in DDAL_CAMPAIGN:
            if data['code'].upper().startswith(code.upper()):
                # For AL codes, we still add to all_adventures_map but don't categorize by DC code
                # We'll use a generic "AL" category or the code prefix itself
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
    if dc_code:
        # Ensure the category exists in aggregated_by_dc_code
        if dc_code.upper() not in aggregated_by_dc_code:
            aggregated_by_dc_code[dc_code.upper()] = []
        aggregated_by_dc_code[dc_code.upper()].append(data)

def aggregate():
    aggregated_by_dc_code = defaultdict(list)
    for code in DC_CAMPAIGNS:
        aggregated_by_dc_code[code.upper()] = []

    logger.info(f'Reading all files at: {input_path}')
    input_full_path = f"{str(input_path)}/*.json"
    for file in glob.glob(input_full_path):
        with open(file, 'r') as _input:
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
        with open(output_full_path, 'w') as f:
            json.dump(dc_list, f, indent=4, sort_keys=True)

    output_full_path = f"{str(output_path)}/all_adventures.json"
    with open(output_full_path, 'w') as f:
        json.dump(list(all_adventures_map.values()), f, indent=4, sort_keys=True)


if __name__ == '__main__':
    aggregate()
    # crawl_dc_listings(page_number=2, max_results=15)
