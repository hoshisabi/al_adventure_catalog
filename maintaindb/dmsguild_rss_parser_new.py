# dmsguild_rss_parser_new.py
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import datetime
import json
import os
import argparse
import logging
import sys

# IMPORTS
from typing import List, Dict, Any
from adventure_model import Adventure
# from adventure_extractors import AdventureHTMLExtractor # <--- REMOVED THIS
from adventure_normalizers import AdventureDataNormalizer
from adventure_utils import sanitize_filename # Use shared utils
# from adventure_utils import parse_date_string # No longer needed directly here, normalizer handles it

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def parse_dmsguild_rss(url: str) -> List[Dict[str, Any]]:
    """
    Parses the DMsGuild RSS feed and returns a list of dictionaries
    with raw product info.
    """
    products_from_rss = []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        root = ET.fromstring(response.text)
        items = root.findall('.//item')
        
        for item in items:
            full_title = item.find('title').text
            product_url = item.find('link').text
            description_html = item.find('description').text # This is just a snippet
            pub_date_str = item.find('pubDate').text

            # Extract product_id from URL
            product_id_match = re.search(r'/product/(\d+)/', product_url)
            product_id = product_id_match.group(1) if product_id_match else None

            if product_id and full_title and product_url and description_html and pub_date_str:
                products_from_rss.append({
                    "product_id": product_id,
                    "full_title_raw": full_title,
                    "url_raw": product_url,
                    "description_html_raw": description_html, # Store the snippet for now, but not for extraction
                    "pub_date_str_raw": pub_date_str
                })
            else:
                logger.warning(f"Skipping RSS item due to missing data: ID={product_id}, Title={full_title}")
            
        return products_from_rss

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return []
    except ET.ParseError as e:
        logger.error(f"Error parsing XML from {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred during RSS parsing: {e}", exc_info=True)
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-?", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite of existing JSON files.")
    parser.add_argument("--url", type=str, default="https://www.dmsguild.com/rss.php?affiliate_id=171040&filters=45470_0_0_0_0_0_0_0_0", help="The full RSS feed URL to parse.")
    parser.add_argument("-o", "--output-dir", type=str, default="_dc", help="The directory to save the JSON files to.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # html_extractor = AdventureHTMLExtractor() # <--- REMOVED THIS
    data_normalizer = AdventureDataNormalizer() # Initialize normalizer

    logger.info(f"Fetching products from {args.url}...")
    products = parse_dmsguild_rss(args.url)
    logger.info(f"Found {len(products)} products in RSS feed.")

    for product_raw_rss_data in products:
        product_id = product_raw_rss_data["product_id"]
        full_title_from_rss = product_raw_rss_data["full_title_raw"]
        product_url = product_raw_rss_data["url_raw"]
        pub_date_str_raw = product_raw_rss_data["pub_date_str_raw"]

        # --- Construct extracted_data directly from RSS fields ---
        # Fields not present in RSS will be None or empty lists
        extracted_data = {
            "product_id": product_id,
            "full_title_raw": full_title_from_rss,
            "url_raw": product_url,
            "date_created_raw": pub_date_str_raw, # Pass the raw string from RSS
            "authors_raw": [], # Not available in RSS, will be populated by HTML extraction
            "price_raw": None, # Not available in RSS
            "page_count_raw": None, # Not available in RSS
            "apl_raw": None, # Not available in RSS
            "tiers_raw": None, # Not available in RSS
            "level_range_raw": None, # Not available in RSS
            "hours_raw": [], # Not available in RSS
            # Keep description_html_raw if you want to store the RSS snippet, but it won't be "extracted"
            "description_html_raw": product_raw_rss_data["description_html_raw"]
        }

        # No call to html_extractor.extract(soup) here, as soup is just the snippet.
        
        normalized_data = data_normalizer.normalize(extracted_data)

        # The 'is_adventure' flag logic needs to be careful here, as we have limited data
        # For RSS, we can only roughly guess based on code existence from title
        is_adventure_flag = True if normalized_data.get("code") else False
        
        adventure_data_for_obj = {
            k: v for k, v in normalized_data.items() if k in Adventure.__dataclass_fields__
        }
        adventure_data_for_obj['is_adventure'] = is_adventure_flag
        # Crucially, set needs_review to True as these entries are incomplete from RSS alone.
        adventure_data_for_obj['needs_review'] = True 

        adventure_obj = Adventure(**adventure_data_for_obj)
        data_to_save = adventure_obj.to_json()

        filename_base = adventure_obj.full_title or adventure_obj.title or product_id
        file_path = os.path.join(args.output_dir, sanitize_filename(filename_base))

        file_exists = os.path.exists(file_path)

        should_write = True
        if file_exists:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data_from_file = json.load(f)
                    if json.dumps(existing_data_from_file, sort_keys=True, default=str) == \
                       json.dumps(data_to_save, sort_keys=True, default=str) and not args.force:
                        logger.info(f"(CACHED) Left alone {os.path.basename(file_path)}")
                        should_write = False
                    elif not args.force:
                        logger.info(f"(CHANGED) Will overwrite {os.path.basename(file_path)} as it's from RSS and not forced to skip.")
                except json.JSONDecodeError:
                    logger.warning(f"Error decoding existing JSON from {os.path.basename(file_path)}. Will overwrite.")
            
        if should_write:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, indent=4, sort_keys=True)
                logger.info(f"Saved {os.path.basename(file_path)}")
            except IOError as e:
                logger.error(f"Error saving {os.path.basename(file_path)}: {e}")