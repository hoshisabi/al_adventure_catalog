import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import datetime
import json
import os

from adventure import DungeonCraft, sanitize_filename, extract_data_from_html

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def parse_dmsguild_rss(url, affiliate_id="171040", filters="45470_0_0_0_0_0_0_0_0"):
    try:

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        items = root.findall('.//item')
        
        dungeon_craft_products = []
        for item in items:
            full_title = item.find('title').text
            product_url = item.find('link').text
            description_html = item.find('description').text
            pub_date_str = item.find('pubDate').text

            # Extract product_id from URL
            product_id_match = re.search(r'/product/(\d+)/', product_url)
            product_id = product_id_match.group(1) if product_id_match else None

            # Authors are not available from RSS feed, so we'll use an empty list
            authors = [] 

            dungeon_craft_products.append((product_id, full_title, authors, description_html, pub_date_str, product_url))
            
        return dungeon_craft_products

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing XML from {url}: {e}")
        return []


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-?", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite of existing JSON files.")
    parser.add_argument("--url", type=str, default="https://www.dmsguild.com/rss.php?affiliate_id=171040&filters=45470_0_0_0_0_0_0_0_0", help="The full RSS feed URL to parse.")
    parser.add_argument("-o", "--output-dir", type=str, default="_dc", help="The directory to save the JSON files to.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Fetch products from the specified URL
    print(f"Fetching products from {args.url}...")
    products = parse_dmsguild_rss(args.url)
    print(f"Found {len(products)} products.")
    for product_id, full_title, authors, description_html, pub_date_str, product_url in products:
        filename = sanitize_filename(full_title) 
        file_path = os.path.join(args.output_dir, filename)

        # Parse date
        # Remove timezone abbreviation (e.g., CDT) as strptime might not recognize all of them
        pub_date_str_no_tz = ' '.join(pub_date_str.split(' ')[:-1])
        date_created = datetime.datetime.strptime(pub_date_str_no_tz, '%a, %d %b %Y %H:%M:%S').date()

        soup = BeautifulSoup(description_html, 'html.parser')

        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

        data = extract_data_from_html(soup, product_id, existing_data=existing_data, force_overwrite=args.force)

        dc_product = DungeonCraft(product_id, full_title, authors, data.get("code"), date_created, str(data.get("hours")) if data.get("hours") is not None else None, data.get("tiers"), data.get("apl"), data.get("level_range"), product_url, data.get("campaigns"), data.get("season"), data.get("is_adventure"), data.get("price"))

        data_to_save = dc_product.to_json()

        file_exists = os.path.exists(file_path)

        if file_exists:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data_from_file = json.load(f)

            if existing_data_from_file == data_to_save and not args.force:
                print(f"(CACHED) Left alone {filename}")
                continue # Skip writing if content is identical and not forced
            else:
                print(f"(MODIFIED) {filename}")
        else:
            print(f"Saved {filename}")

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, sort_keys=True)
        except IOError as e:
            print(f"Error saving {filename}: {e}")