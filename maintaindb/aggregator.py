import pathlib
import os
import logging
import sys
import json
import glob
from collections import defaultdict

from adventure import DC_CAMPAIGNS
import glob

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_path = os.path.join(root, '_dc')
output_path = os.path.join(root, '..', 'assets', 'data')

all_adventures = []

def __add_to_map(data, aggregated_by_dc_code):
    if 'code' not in data or data['code'] is None:
        logger.info(f">> {data.get('full_title', 'UNKNOWN TITLE')} missing DC code")
        return

    dc_code = None
    for code in DC_CAMPAIGNS:
        if data['code'].upper().startswith(code.upper()):
            dc_code = code
            break

    if dc_code:
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
                if "url" in data and data["url"] and "affiliate_id" not in data["url"]:
                    data["url"] += "&affiliate_id=171040"
                __add_to_map(data, aggregated_by_dc_code)
                all_adventures.append(data)
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
        json.dump(all_adventures, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    aggregate()
    # crawl_dc_listings(page_number=2, max_results=15)
