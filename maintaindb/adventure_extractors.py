# adventure_extractors.py
import re
import datetime
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional

# Assuming get_patt_first_matching_group and parse_date_string are in adventure_utils
from adventure_utils import get_patt_first_matching_group, parse_date_string


class AdventureHTMLExtractor:
    """
    Extracts raw data fields from DMsGuild HTML content using BeautifulSoup.
    This stage aims to get the data as it appears in the HTML, with minimal processing.
    """

    def extract(self, soup: BeautifulSoup) -> Dict[str, Any]:
        raw_data: Dict[str, Any] = {
            "full_title_raw": None,
            "authors_raw": [],
            "code_raw": None, # This will be set by the inferer, not extracted raw directly
            "date_created_raw": None,
            "hours_raw": None,
            "tiers_raw": None,
            "apl_raw": None,
            "level_range_raw": None,
            "price_raw": None
            # product_id and url_raw will be added by the caller (process_downloads_new.py)
        }

        # --- Title ---
        product_title_div = soup.find("div", {"class": "grid_12 product-title"})
        if product_title_div:
            # Get the direct text content, ignoring child spans for now
            raw_data["full_title_raw"] = product_title_div.get_text(strip=True)

        # --- Authors ---
        product_from_div = soup.find("div", {"class": "grid_12 product-from"})
        if product_from_div:
            author_links = product_from_div.find_all("a")
            raw_data["authors_raw"] = [link.get_text(strip=True) for link in author_links]

        # --- Date Created ---
        info_items = soup.find_all("div", {"class": "widget-information-item-content"})
        date_key = 'This title was added to our catalog on '
        for item in info_items:
            if date_key in item.get_text():
                date_str = item.get_text().replace(date_key, '').replace('.', '').strip()
                raw_data["date_created_raw"] = date_str
                break

        # --- Combined Text for Regex Extraction (Description + Meta Description) ---
        product_content_div = soup.find("div", {"class": "alpha omega prod-content"})
        description_text = product_content_div.get_text(separator=" ", strip=True) if product_content_div else ""

        meta_description_tag = soup.find("meta", {"name": "description"})
        meta_description_text = meta_description_tag["content"] if meta_description_tag and "content" in meta_description_tag.attrs else ""

        combined_text = (description_text + " " + meta_description_text).strip()

        # --- Raw Hours ---
        # The regex now captures the entire hour phrase, including "X-Y hours" or "X hours"
        hours_match = re.search(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)(?:\s*(?:-|to)\s*(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty))?[-\s\xa0]*(?:hour|hours|hr)\b', combined_text, re.IGNORECASE)
        if hours_match:
            raw_data["hours_raw"] = hours_match.group(0).strip() # Capture the full matched string

        # --- Raw Tiers, APL, Level Range ---
        # These are still simple patterns that grab a single value/range string
        raw_data["tiers_raw"] = get_patt_first_matching_group(r"Tier(?:s)?\s*(?:[1-4]|one|two|three|four)(?:\s*-\s*(?:[1-4]|one|two|three|four))?", combined_text)
        raw_data["apl_raw"] = get_patt_first_matching_group(r"(?:APL|Average Party Level)\s*(?:\(APL\))?\s*(\d+)", combined_text)
        raw_data["level_range_raw"] = get_patt_first_matching_group(r"(?i)Level(?:s)?\s*([\d-]+(?:\s*,\s*[\d-]+)*)", combined_text) # Capture multiple ranges like "1-4, 5-10"

        # --- Price Extraction (complex as it can be in different divs) ---
        price_value = None
        # Priority 1: product-price-strike (original price, often higher)
        original_price_strike_match = soup.find("div", class_="product-price-strike")
        if original_price_strike_match:
            price_text = original_price_strike_match.get_text(strip=True)
            price_match = re.search(r'\$([\d\.]+)', price_text)
            if price_match:
                price_value = float(price_match.group(1))
        
        # Priority 2: price-old
        if price_value is None:
            original_price_old_match = soup.find("div", class_="price-old")
            if original_price_old_match:
                price_text = original_price_old_match.get_text(strip=True)
                price_match = re.search(r'\$([\d\.]+)', price_text)
                if price_match:
                    price_value = float(price_match.group(1))
        
        # Priority 3: main price (current price, could be sale or regular)
        if price_value is None:
            price_match_div = soup.find("div", class_="price")
            if price_match_div:
                price_text = price_match_div.get_text(strip=True)
                price_match = re.search(r'\$([\d\.]+)', price_text)
                if price_match:
                    price_value = float(price_match.group(1))

        raw_data["price_raw"] = price_value

        return raw_data