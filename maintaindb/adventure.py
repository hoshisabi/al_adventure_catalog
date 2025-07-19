import datetime
import json
import re
import unicodedata
from word2number import w2n
import requests
from bs4 import BeautifulSoup
import logging
import sys
import os

logger = logging.getLogger()

DC_CAMPAIGNS = {
    'DL-DC': 'Dragonlance',
    'EB-DC': 'Eberron',
    'EB-SM': 'Eberron',
    'FR-DC': 'Forgotten Realms',
    'PS-DC': 'Planescape',
    'SJ-DC': 'Spelljammer',
    'WBW-DC': 'The Wild Beyond the Witchlight',
    'DC-POA': 'Icewind Dale: Rime of the Frostmaiden',
    'PO-BK': 'Forgotten Realms',
    'BMG-DRW': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
    'BMG-MOON': 'Forgotten Realms',
    'CCC-': 'Forgotten Realms',
    'RV-DC': 'Ravenloft',
}

DDAL_CAMPAIGN = {
    'RMH':    ['Ravenloft'],
    'DDAL4':  ['Forgotten Realms', 'Ravenloft'],
    'DDAL04': ['Forgotten Realms', 'Ravenloft'],
    'DDEX1':  ['Forgotten Realms'],
    'DDEX01': ['Forgotten Realms'],
    'DDEX2':  ['Forgotten Realms'],
    'DDEX02': ['Forgotten Realms'],
    'DDEX3':  ['Forgotten Realms'],
    'DDEX03': ['Forgotten Realms'],
    'DDAL5':  ['Forgotten Realms'],
    'DDAL05': ['Forgotten Realms'],
    'DDAL6':  ['Forgotten Realms'],
    'DDAL06': ['Forgotten Realms'],
    'DDAL7':  ['Forgotten Realms'],
    'DDAL07': ['Forgotten Realms'],
    'DDAL8':  ['Forgotten Realms'],
    'DDAL08': ['Forgotten Realms'],
    'DDAL9':  ['Forgotten Realms'],
    'DDAL09': ['Forgotten Realms'],
    'DDAL10': ['Forgotten Realms'],
    'DDAL00': ['Forgotten Realms'],
    'DDAL-DRW': ['Forgotten Realms'],
    'DDEP': ['Forgotten Realms'],
    'DDAL-ELW': ['Eberron'],
    'EB': ['Eberron'],
}

SEASONS = {
    'WBW-DC': 'The Wild Beyond the Witchlight',
    'SJ-DC': 'Spelljammer',
    'PS-DC': 'Planescape',
    'DC-POA': 'Icewind Dale',
}

def get_season(code):
    if not code:
        return None
    for prefix, season in SEASONS.items():
        if code.startswith(prefix):
            return season
    return None

def sanitize_filename(filename):
    """
    Normalizes and sanitizes a string to be a valid filename.
    """
    # Normalize unicode characters
    normalized_filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')

    # Split into base name and original extension
    base_name, _ = os.path.splitext(normalized_filename)

    # Replace all periods in the base name with dashes
    base_name_with_dashes = base_name.replace('.', '-')
    
    # Replace non-alphanumeric characters (excluding the period for extension) with a dash
    # This regex will replace any character that is NOT a letter, number, underscore, or hyphen with a dash.
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '-', base_name_with_dashes)
    
    # Replace multiple dashes with a single dash
    sanitized_name = re.sub(r'-+', '-', sanitized_name)
    
    # Remove leading and trailing dashes from the name
    sanitized_name = sanitized_name.strip('-')
    
    # Always append .json as the extension
    sanitized_filename = f"{sanitized_name}.json"
    
    return sanitized_filename


class DungeonCraft:

    def __init__(self, product_id, title, authors, code, date_created, hours, tiers, apl, level_range, url, campaigns, season=None, is_adventure=None, price=None) -> None:
        self.product_id = product_id
        self.full_title = title
        self.title = self.__get_short_title(title).strip()
        self.authors = authors
        self.code = code
        self.date_created = date_created
        if hours is not None and hours != '':
            self.hours = str(hours)
        else:
            self.hours = None
        self.tiers = tiers
        self.apl = apl
        self.level_range = level_range
        self.url = url
        self.campaigns = campaigns # This will now be a list of strings
        self.season = season
        self.is_adventure = is_adventure
        self.price = price

    def is_tier(self, tier):
        if self.tiers is not None:
            return self.tiers == tier
        return False

    def is_tier_unknown(self):
        if self.tiers is None:
            return True
        return False

    def is_hour(self, hour):
        if self.hours is not None:
            # Parse the hours string (e.g., "1-2", "4", "1,2,3")
            hours_list = []
            for part in str(self.hours).split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    hours_list.extend(range(start, end + 1))
                else:
                    hours_list.append(int(part))
            return hour in hours_list
        return False

    def is_hour_unknown(self):
        if self.hours is None or self.hours == '':
            return True
        return False

    def is_campaign(self, campaign_name):
        if self.campaigns is not None:
            return campaign_name in self.campaigns
        return False

    def is_campaign_unknown(self):
        if self.campaigns is None or not self.campaigns:
            return True
        return False

    def __get_short_title(self, title):
        regex = r'[A-Z]{2,}-DC-([A-Z]{2,})([^\s]+)'
        new_title = title.replace('(', '').replace(')', '').replace(':', '')
        result = re.sub(regex, '', new_title)
        return result.strip()

    def __str__(self) -> str:
        return json.dumps(self.to_json(),  sort_keys=True, indent=2,)

    def to_json(self):
        result = dict(
            product_id=self.product_id,
            full_title=self.full_title,
            title=self.title,
            authors=self.authors,
            code=self.code,
            date_created=self.date_created.strftime('%Y%m%d'),
            hours=self.hours,
            tiers=self.tiers,
            apl=self.apl,
            level_range=self.level_range,
            url=self.url,
            campaigns=self.campaigns,
            season=self.season,
            is_adventure=self.is_adventure,
            price=self.price
        )
        return result

    def convert_date_to_readable_str(self):
        if self.date_created is not None:
            # Ensure date_created is a datetime object before formatting
            if isinstance(self.date_created, datetime.date):
                date_obj = self.date_created
            else:
                date_obj = datetime.datetime.strptime(self.date_created, "%Y%m%d").date()
            return date_obj.strftime("%Y, %b")
        return 'Unknown'

def str_to_int(value):
    if not value:
        return None

    try:
        number = int(value)
        return number
    except ValueError:
        try:
            number = w2n.word_to_num(value)
            return number
        except Exception:
            return None
    except Exception:
        return None

def get_patt_first_matching_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        for group in matches.groups():
            if group:
                return group
    return None

def get_dc_code_and_campaign(product_title):
    content = str(product_title).upper().split()
    for text in content:
        text = text.replace(',', '').replace(
            '(', '').replace(')', '').replace("'", '').replace(':', '-')
        text = text.strip()
        if text:
            for code in DC_CAMPAIGNS:
                if text.startswith(code):
                    campaign_val = DC_CAMPAIGNS.get(code)
                    return (text, [campaign_val] if not isinstance(campaign_val, list) else campaign_val)
            for code in DDAL_CAMPAIGN:
                if text.startswith(code):
                    campaign_val = DDAL_CAMPAIGN.get(code)
                    return (text, [campaign_val] if not isinstance(campaign_val, list) else campaign_val)
    return None

def merge_adventure_data(existing_data, new_data, force_overwrite=False, careful_mode=False):
    merged_data = new_data.copy()  # Start with all keys from new_data

    if force_overwrite:
        return new_data

    if existing_data:
        for key, existing_value in existing_data.items():
            is_existing_value_empty = existing_value is None or existing_value == "" or existing_value == [] or existing_value == {}
            new_value = new_data.get(key)
            is_new_value_empty = new_value is None or new_value == "" or new_value == [] or new_value == {}

            if key == "hours" and isinstance(existing_value, (int, float)):
                existing_value = str(int(existing_value)) # Convert to string, handle floats like 5.0

            if key == "hours" and isinstance(existing_value, (int, float)):
                existing_value = str(int(existing_value)) # Convert to string, handle floats like 5.0

            if key == "hours" and isinstance(existing_value, (int, float)):
                existing_value = str(int(existing_value)) # Convert to string, handle floats like 5.0

            if careful_mode:
                if not is_existing_value_empty: # If existing is not empty, keep it
                    merged_data[key] = existing_value
                elif not is_new_value_empty: # If existing is empty, and new is not, use new
                    merged_data[key] = new_value
                else: # Both are empty, keep new (which is empty)
                    merged_data[key] = new_value
            else: # Original behavior (not careful, not force)
                if not is_new_value_empty:
                    if is_existing_value_empty or existing_value != new_value:
                        merged_data[key] = new_value
                elif not is_existing_value_empty: # If new is empty, but existing is not, keep existing
                    merged_data[key] = existing_value
    return merged_data

def extract_data_from_html(parsed_html, product_id, product_alt=None, existing_data=None, force_overwrite=False, careful_mode=False):
    new_data = {
        "module_name": None,
        "authors": [],
        "code": None,
        "date_created": None,
        "hours": None,
        "tiers": None,
        "apl": None,
        "level_range": None,
        "campaigns": None, # Changed to campaigns (plural)
        "season": None,
        "is_adventure": False,
        "price": None
    }

    product_title = parsed_html.find(
        "div", {"class": "grid_12 product-title"})
    if product_title:
        children = product_title.findChildren(
            "span", {"itemprop": "name"}, recursive=True)
        for child in children:
            new_data["module_name"] = child.text
            break

    authors = []
    product_from = parsed_html.find(
        "div", {"class": "grid_12 product-from"})
    if product_from:
        children = product_from.findChildren("a", recursive=True)
        for child in children:
            new_data["authors"].append(child.text)

    date_created = None
    children = parsed_html.find_all(
        "div", {"class": "widget-information-item-content"})
    key = 'This title was added to our catalog on '
    for child in children:
        if key in child.text:
            date_str = child.text.replace(key, '').replace('.', '')
            new_data["date_created"] = datetime.datetime.strptime(
                date_str.strip(), "%B %d, %Y").date()
            break

    product_content = parsed_html.find(
        "div", {"class": "alpha omega prod-content"})
    text = ""
    if product_content:
        text = product_content.text

    if new_data["module_name"]:
        result = get_dc_code_and_campaign(new_data["module_name"])
        if result is not None:
            new_data["code"] = result[0]
            new_data["campaigns"] = result[1] # campaigns is already a list from get_dc_code_and_campaign
            new_data["season"] = get_season(new_data["code"])

    # Check for EB- series adventures
    if new_data["code"] and new_data["code"].startswith("EB-"):
        new_data["hours"] = "4"
    else:
        # Try to find "X hour(s)" or "X-Y hour(s)"
        # This regex will find all occurrences of single numbers or ranges followed by 'hour(s)' or 'hr'
        hours_matches = re.findall(r'([\d\w]+)(?:[ -]([\d\w]+))?[-\s\xa0]*(?:hour|hours|hr)', text, re.IGNORECASE)
        
        extracted_hours = []
        for match in hours_matches:
            start_hour = str_to_int(match[0])
            end_hour = str_to_int(match[1]) if match[1] else None

            if start_hour is not None:
                if end_hour is not None and end_hour > start_hour:
                    extracted_hours.append(f"{start_hour}-{end_hour}")
                else:
                    extracted_hours.append(str(start_hour))
        
        if extracted_hours:
            new_data["hours"] = ",".join(map(str, extracted_hours))
        else:
            new_data["hours"] = None

    new_data["tiers"] = str_to_int(get_patt_first_matching_group(r"Tier ?([1-4])", text))
    new_data["apl"] = str_to_int(get_patt_first_matching_group(r"APL ?(\d+)", text))

    level_range_match = get_patt_first_matching_group(r"(?i)(?:levels? )?(\d+)(?:(?:[ -]|(?: to ))(\d+))?", text)
    if level_range_match:
        if isinstance(level_range_match, tuple):
            new_data["level_range"] = f"{level_range_match[0]}-{level_range_match[1]}"
        else:
            new_data["level_range"] = str(level_range_match)

    # Derive Tier from APL if Tier is None
    if new_data["tiers"] is None and new_data["apl"] is not None:
        if 1 <= new_data["apl"] <= 4: new_data["tiers"] = 1
        elif 5 <= new_data["apl"] <= 10: new_data["tiers"] = 2
        elif 11 <= new_data["apl"] <= 16: new_data["tiers"] = 3
        elif 17 <= new_data["apl"] <= 20: new_data["tiers"] = 4
    
    # Derive Level Range from Tier if Level Range is None or not a valid range
    derived_level_range = None
    if new_data["tiers"] is not None:
        if new_data["tiers"] == 1: derived_level_range = "1-4"
        elif new_data["tiers"] == 2: derived_level_range = "5-10"
        elif new_data["tiers"] == 3: derived_level_range = "11-16"
        elif new_data["tiers"] == 4: derived_level_range = "17-20"

    # Use derived level range if extracted is not a range or is None
    if new_data["level_range"] is None or not re.match(r"\d+-\d+", str(new_data["level_range"])):
        new_data["level_range"] = derived_level_range

    # Determine if it's an adventure
    lower_full_title = new_data["module_name"].lower() if new_data["module_name"] else ""
    is_bundle = 'bundle' in lower_full_title
    is_roll20 = 'roll20' in lower_full_title
    is_fg = 'fantasy grounds' in lower_full_title

    if new_data["code"] and not is_bundle and not is_roll20 and not is_fg:
        new_data["is_adventure"] = True
    else:
        new_data["is_adventure"] = False

    # Price extraction
    # Prioritize product-price-strike for original price
    original_price_strike_match = parsed_html.find("div", class_="product-price-strike")
    if original_price_strike_match:
        price_text = original_price_strike_match.get_text(strip=True)
        price_value = re.search(r'\$([\d\.]+)', price_text)
        if price_value:
            new_data["price"] = float(price_value.group(1))
    
    if new_data["price"] is None:
        # Then try price-old
        original_price_old_match = parsed_html.find("div", class_="price-old")
        if original_price_old_match:
            price_text = original_price_old_match.get_text(strip=True)
            price_value = re.search(r'\$([\d\.]+)', price_text)
            if price_value:
                new_data["price"] = float(price_value.group(1))
    
    if new_data["price"] is None:
        # Fallback to general price
        price_match = parsed_html.find("div", class_="price")
        if price_match:
            price_text = price_match.get_text(strip=True)
            price_value = re.search(r'\$([\d\.]+)', price_text)
            if price_value:
                new_data["price"] = float(price_value.group(1))

    return merge_adventure_data(existing_data, new_data, force_overwrite, careful_mode)
