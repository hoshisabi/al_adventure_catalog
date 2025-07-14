import datetime
import json
import re
import unicodedata
from word2number import w2n
import requests
from bs4 import BeautifulSoup
import logging
import sys

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
    # Replace non-alphanumeric characters with a dash
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '-', normalized_filename)
    # Replace multiple dashes with a single dash
    sanitized_filename = re.sub(r'-+', '-', sanitized_filename)
    # Remove leading and trailing dashes
    sanitized_filename = sanitized_filename.strip('-')
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

def get_patt_first_matching_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        for group in matches.groups():
            if group:
                return group
    return None

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

def _parse_html_to_dc_data(parsed_html, product_id, product_alt=None):
    module_name = None
    hours = None
    tier = None
    apl = None
    level_range = None
    code = None
    campaign = None
    price = None
    is_adventure = False

    product_title = parsed_html.body.find(
        "div", {"class": "grid_12 product-title"})
    children = product_title.findChildren(
        "span", {"itemprop": "name"}, recursive=True)
    for child in children:
        module_name = child.text
        break

    authors = []
    product_from = parsed_html.body.find(
        "div", {"class": "grid_12 product-from"})
    children = product_from.findChildren("a", recursive=True)
    for child in children:
        current_author = child.text
        authors.append(current_author)

    date_created = None
    children = parsed_html.body.find_all(
        "div", {"class": "widget-information-item-content"})
    key = 'This title was added to our catalog on '
    for child in children:
        if key in child.text:
            date_str = child.text.replace(key, '').replace('.', '')
            date_created = datetime.datetime.strptime(
                date_str.strip(), "%B %d, %Y").date()
            break

    product_content = parsed_html.body.find(
        "div", {"class": "alpha omega prod-content"})
    text = product_content.text

    hours = get_patt_first_matching_group(r"(?i)(two|four|\d)+(?:hour|to|through|\+|-|\s+)*(?:(\d|two|four|eight|\s)+)*Hour", text)
    hours = str_to_int(hours)
    tier = get_patt_first_matching_group(r"Tier ?([1-4])", text)
    tier = str_to_int(tier)
    apl = get_patt_first_matching_group(r"APL ?(\d+)", text)
    apl = str_to_int(apl)
    level_range = get_patt_first_matching_group(r"(?i)(?:levels ?)?(\d+)(?:nd|th)?(?:[ -]|through|to)*(\d+)(?:nd|th)?[- ](?:level)?", text)
    
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

    code = None
    campaign = None
    if module_name:
        result = get_dc_code_and_campaign(module_name)
        if result is not None: (code, campaign) = result

    # Extract price
    price_match = re.search(r'<b>Price</b>: \$([\d\.]+)', parsed_html.prettify())
    price = float(price_match.group(1)) if price_match else None

    # Determine is_adventure
    lower_module_name = module_name.lower() if module_name else ""
    is_bundle = 'bundle' in lower_module_name
    is_roll20 = 'roll20' in lower_module_name
    is_fg = 'fantasy grounds' in lower_module_name
    has_code = code is not None

    if has_code and not is_bundle and not is_roll20 and not is_fg:
        is_adventure = True
    else:
        is_adventure = False

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

def url_2_DC(input_url: str, product_id: str = None, product_alt=None) -> DungeonCraft:
    try:
        if "affiliate_id" not in input_url:
            input_url += "&affiliate_id=171040"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        parsed_html = BeautifulSoup(requests.get(
            input_url, headers=headers, timeout=60).text, features="html.parser")

        data = _parse_html_to_dc_data(parsed_html, product_id, product_alt)

        dc = DungeonCraft(product_id, data["module_name"], data["authors"],
                          data["code"], data["date_created"], data["hours"], data["tiers"], data["apl"], data["level_range"], input_url, data["campaign"])

        logger.info(f'>> {product_id} processed ({input_url})')
        return dc
    except Exception as ex:
        logger.error(f'Error processing {input_url}: {str(ex)}')
        return None