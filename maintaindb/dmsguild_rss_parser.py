import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import datetime
import json
import os



def parse_dmsguild_rss(url, affiliate_id="171040", filters="45470_0_0_0_0_0_0_0_0"):
    try:

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
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

            price_match = re.search(r'<b>Price</b>: \$([\d\.]+)', description_html)
            price = float(price_match.group(1)) if price_match else None

            # Extract product_id from URL
            product_id_match = re.search(r'/product/(\d+)/', product_url)
            product_id = product_id_match.group(1) if product_id_match else None

            # Parse date
            # Remove timezone abbreviation (e.g., CDT) as strptime might not recognize all of them
            pub_date_str_no_tz = ' '.join(pub_date_str.split(' ')[:-1])
            date_created = datetime.datetime.strptime(pub_date_str_no_tz, '%a, %d %b %Y %H:%M:%S').date()

            soup = BeautifulSoup(description_html, 'html.parser')
            description_text = soup.get_text()

            # Filtering logic
            lower_full_title = full_title.lower()
            lower_description_text = description_text.lower()

            from adventure import DungeonCraft, sanitize_filename, get_patt_first_matching_group, str_to_int, get_dc_code_and_campaign
            code, campaign = get_dc_code_and_campaign(full_title) or (None, None)
            has_code = code is not None
            is_bundle = 'bundle' in lower_full_title
            is_roll20 = 'roll20' in lower_full_title
            is_fg = 'fantasy grounds' in lower_full_title

            if has_code and not is_bundle and not is_roll20 and not is_fg:
                is_adventure = True
            else:
                is_adventure = False

            hours = get_patt_first_matching_group(r"(?i)(two|four|\d)+(?:hour|to|through|\+|-|\s+)*(?:(\d|two|four|eight|\s)+)*Hour", description_text)
            hours = str_to_int(hours)
            
            tier = get_patt_first_matching_group(r"Tier ?([1-4])", description_text)
            tier = str_to_int(tier)
            
            apl = get_patt_first_matching_group(r"APL ?(\d+)", description_text)
            apl = str_to_int(apl)
            
            level_range_match = get_patt_first_matching_group(r"(?i)(?:levels? )?(\d+)(?:(?:[ -]|(?: to ))(\d+))?", description_text)
            level_range = None
            if level_range_match:
                if isinstance(level_range_match, tuple):
                    level_range = f"{level_range_match[0]}-{level_range_match[1]}"
                else:
                    level_range = str(level_range_match)

            # Derive Tier from APL if Tier is None
            if tier is None and apl is not None:
                if 1 <= apl <= 4: tier = 1
                elif 5 <= apl <= 10: tier = 2
                elif 11 <= apl <= 16: tier = 3
                elif 17 <= apl <= 20: tier = 4
            
            # Derive Level Range from Tier if Level Range is None or not a valid range
            derived_level_range = None
            if tier is not None:
                if tier == 1: derived_level_range = "1-4"
                elif tier == 2: derived_level_range = "5-10"
                elif tier == 3: derived_level_range = "11-16"
                elif tier == 4: derived_level_range = "17-20"

            # Use derived level range if extracted is not a range or is None
            if level_range is None or not re.match(r"\d+-\d+", str(level_range)):
                level_range = derived_level_range

            # Authors are not available from RSS feed
            authors = [] 

            dc_product = DungeonCraft(product_id, full_title, authors, code, date_created, hours, tier, apl, level_range, product_url, campaign, is_adventure, price)
            dungeon_craft_products.append(dc_product)
            
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
    for product in products:
        filename = sanitize_filename(product.full_title) + ".json"
        file_path = os.path.join(args.output_dir, filename)
        
        if not args.force and os.path.exists(file_path):
            print(f"Skipping {filename}, already exists.")
            continue
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(product.to_json(), f, indent=4, sort_keys=True)
            print(f"Saved {filename}")
        except IOError as e:
            print(f"Error saving {filename}: {e}")