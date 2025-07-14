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
    'PS-DC': 'Forgotten Realms',
    'SJ-DC': 'Forgotten Realms',
    'WBW-DC': 'Forgotten Realms',
    'DC-POA': 'Forgotten Realms',
    'PO-BK': 'Forgotten Realms',
    'BMG-DRW': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
    'BMG-MOON': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
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

def sanitize_filename(filename):
    """
    Normalizes and sanitizes a string to be a valid filename.
    """
    # Normalize unicode characters
    normalized_filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    
    # Split the filename into name and extension
    name, ext = os.path.splitext(normalized_filename)

    # Replace non-alphanumeric characters (excluding the period for extension) with a dash in the name part
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '-', name)
    
    # Replace multiple dashes with a single dash
    sanitized_name = re.sub(r'-+', '-', sanitized_name)
    
    # Remove leading and trailing dashes from the name
    sanitized_name = sanitized_name.strip('-')
    
    # Recombine the sanitized name and original extension
    sanitized_filename = f"{sanitized_name}{ext}"
    
    return sanitized_filename


class DungeonCraft:

    def __init__(self, product_id, title, authors, code, date_created, hours, tiers, apl, level_range, url, campaign, is_adventure=None, price=None) -> None:
        self.product_id = product_id
        self.full_title = title
        self.title = self.__get_short_title(title).strip()
        self.authors = authors
        self.code = code
        self.date_created = date_created
        self.hours = hours
        self.tiers = tiers
        self.apl = apl
        self.level_range = level_range
        self.url = url
        self.campaign = campaign
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
            return self.hours == hour
        return False

    def is_hour_unknown(self):
        if self.hours is None:
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
            campaign=self.campaign,
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
                    return (text, DC_CAMPAIGNS.get(code))
            for code in DDAL_CAMPAIGN:
                if text.startswith(code):
                    return (text, DDAL_CAMPAIGN.get(code))
    return None

def extract_data_from_html(parsed_html, product_id, product_alt=None):
    module_name = None
    hours = None
    tier = None
    apl = None
    level_range = None
    code = None
    campaign = None
    price = None
    is_adventure = False

    product_title = parsed_html.find(
        "div", {"class": "grid_12 product-title"})
    if product_title:
        children = product_title.findChildren(
            "span", {"itemprop": "name"}, recursive=True)
        for child in children:
            module_name = child.text
            break

    authors = []
    product_from = parsed_html.find(
        "div", {"class": "grid_12 product-from"})
    if product_from:
        children = product_from.findChildren("a", recursive=True)
        for child in children:
            current_author = child.text
            authors.append(current_author)

    date_created = None
    children = parsed_html.find_all(
        "div", {"class": "widget-information-item-content"})
    key = 'This title was added to our catalog on '
    for child in children:
        if key in child.text:
            date_str = child.text.replace(key, '').replace('.', '')
            date_created = datetime.datetime.strptime(
                date_str.strip(), "%B %d, %Y").date()
            break

    product_content = parsed_html.find(
        "div", {"class": "alpha omega prod-content"})
    text = ""
    if product_content:
        text = product_content.text

    code = None
    campaign = None
    if module_name:
        result = get_dc_code_and_campaign(module_name)
        if result is not None: (code, campaign) = result

    # Check for EB- series adventures
    if code and code.startswith("EB-"):
        hours = 4
    else:
        # Try to find "X hour(s)" or "X-Y hour(s)"
        hours_match = re.search(r'(\d+)(?:-(\d+))?\s*(?:hour|hours|hr)', text, re.IGNORECASE)
        if hours_match:
            if hours_match.group(2): # It's a range like "X-Y hours"
                start_hour = str_to_int(hours_match.group(1))
                end_hour = str_to_int(hours_match.group(2))
                if start_hour and end_hour:
                    hours = (start_hour + end_hour) / 2 # Take the average
            else: # It's a single number like "X hours"
                hours = str_to_int(hours_match.group(1))

    tier = get_patt_first_matching_group(r"Tier ?([1-4])", text)
    tier = str_to_int(tier)

    apl = get_patt_first_matching_group(r"APL ?(\d+)", text)
    apl = str_to_int(apl)

    level_range_match = get_patt_first_matching_group(r"(?i)(?:levels? )?(\d+)(?:(?:[ -]|(?: to ))(\d+))?", text)
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
    if level_range is None or not re.match(r"\\d+-\\d+", str(level_range)):
        level_range = derived_level_range

    # Determine if it's an adventure
    lower_full_title = module_name.lower() if module_name else ""
    is_bundle = 'bundle' in lower_full_title
    is_roll20 = 'roll20' in lower_full_title
    is_fg = 'fantasy grounds' in lower_full_title

    if code and not is_bundle and not is_roll20 and not is_fg:
        is_adventure = True
    else:
        is_adventure = False

    # Price extraction
    price = None
    # Prioritize product-price-strike for original price
    original_price_strike_match = parsed_html.find("div", class_="product-price-strike")
    if original_price_strike_match:
        price_text = original_price_strike_match.get_text(strip=True)
        price_value = re.search(r'\$([\\d\\.]+)', price_text)
        if price_value:
            price = float(price_value.group(1))
    
    if price is None:
        # Then try price-old
        original_price_old_match = parsed_html.find("div", class_="price-old")
        if original_price_old_match:
            price_text = original_price_old_match.get_text(strip=True)
            price_value = re.search(r'\$([\\d\\.]+)', price_text)
            if price_value:
                price = float(price_value.group(1))
    
    if price is None:
        # Fallback to general price
        price_match = parsed_html.find("div", class_="price")
        if price_match:
            price_text = price_match.get_text(strip=True)
            price_value = re.search(r'\$([\\d\\.]+)', price_text)
            if price_value:
                price = float(price_value.group(1))

    return {
        "module_name": module_name,
        "authors": authors,
        "code": code,
        "date_created": date_created,
        "hours": hours,
        "tiers": tier,
        "apl": apl,
        "level_range": level_range,
        "campaign": campaign,
        "is_adventure": is_adventure,
        "price": price
    }
