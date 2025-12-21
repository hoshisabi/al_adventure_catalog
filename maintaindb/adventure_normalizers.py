# adventure_normalizers.py
import re
import datetime
from decimal import Decimal
from typing import Dict, Any, List, Optional

from adventure_utils import (
    get_patt_first_matching_group,
    parse_number_string_to_int,
    parse_date_string,
    parse_rss_date_string, # <--- NEW IMPORT
    get_adventure_code_and_campaigns,
    get_season
)

class AdventureDataNormalizer:
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized_data = {}

        # Product ID
        normalized_data["product_id"] = raw_data.get("product_id")

        # Full Title
        normalized_data["full_title"] = raw_data.get("full_title_raw")

        # URL
        normalized_data["url"] = raw_data.get("url_raw")

        # Code and Campaigns
        code, campaigns = get_adventure_code_and_campaigns(normalized_data["full_title"]) or (None, [])
        normalized_data["code"] = code
        normalized_data["campaigns"] = campaigns
        normalized_data["season"] = get_season(code)

        # Title
        title = get_patt_first_matching_group(r"(?:^[A-Z]{2,}-\s?[A-Z]{2,}\d{1,}-\d{1,}\s?)(.*?)(?:\s+PDF|\s*\|\s*DMsGuild)?$", normalized_data["full_title"])
        if not title:
            title = get_patt_first_matching_group(r"^(.*?)(?:\s+PDF|\s*\|\s*DMsGuild)?$", normalized_data["full_title"])
        normalized_data["title"] = title if title else normalized_data["full_title"] # Fallback to full title if no specific title found

        # Date Created
        # Try parsing as RSS date first, then as standard date
        date_created_raw = raw_data.get("date_created_raw")
        parsed_date = parse_rss_date_string(date_created_raw)
        if parsed_date:
            normalized_data["date_created"] = parsed_date
        else:
            normalized_data["date_created"] = parse_date_string(date_created_raw)


        # Authors
        raw_authors = raw_data.get("authors_raw", [])
        # Strip whitespace and trailing commas from author names
        normalized_data["authors"] = [author.strip().rstrip(',') for author in raw_authors if author.strip()] if raw_authors else []

        # Price
        raw_price = raw_data.get("price_raw")
        if isinstance(raw_price, str) and raw_price.startswith("$"):
            try:
                normalized_data["price"] = Decimal(raw_price[1:])
            except Exception:
                normalized_data["price"] = None
        else:
            normalized_data["price"] = None # Ensure it's None if not a valid string or not starting with $

        # Page Count
        raw_page_count = raw_data.get("page_count_raw")
        normalized_data["page_count"] = parse_number_string_to_int(raw_page_count)

        # APL
        normalized_data["apl"] = parse_number_string_to_int(raw_data.get("apl_raw"))

        # Tiers and Level Range
        raw_level_range = raw_data.get("level_range_raw")
        raw_tiers = raw_data.get("tiers_raw")

        # Try to derive levels from range
        start_level, end_level = None, None
        if raw_level_range and re.match(r"^\d+-\d+$", raw_level_range):
            try:
                s, e = map(int, raw_level_range.split('-'))
                start_level, end_level = s, e
            except ValueError:
                pass # Continue if parsing fails

        # Derive tiers from parsed levels
        derived_tiers = None
        if start_level is not None and end_level is not None:
            if 1 <= start_level <= 4: derived_tiers = 1
            elif 5 <= start_level <= 10: derived_tiers = 2
            elif 11 <= start_level <= 16: derived_tiers = 3
            elif 17 <= start_level <= 20: derived_tiers = 4
        
        normalized_data["tiers"] = parse_number_string_to_int(raw_tiers) if raw_tiers else derived_tiers
        
        # If tiers is still None, try to derive from APL
        if normalized_data["tiers"] is None and normalized_data["apl"] is not None:
            if 1 <= normalized_data["apl"] <= 4: normalized_data["tiers"] = 1
            elif 5 <= normalized_data["apl"] <= 10: normalized_data["tiers"] = 2
            elif 11 <= normalized_data["apl"] <= 16: normalized_data["tiers"] = 3
            elif 17 <= normalized_data["apl"] <= 20: normalized_data["tiers"] = 4

        # If Level Range is None or not a valid range, derive from Tier
        derived_level_range = None
        if normalized_data["tiers"] is not None:
            if normalized_data["tiers"] == 1: derived_level_range = "1-4"
            elif normalized_data["tiers"] == 2: derived_level_range = "5-10"
            elif normalized_data["tiers"] == 3: derived_level_range = "11-16"
            elif normalized_data["tiers"] == 4: derived_level_range = "17-20"
        
        normalized_data["level_range"] = raw_level_range if (raw_level_range and re.match(r"^\d+-\d+$", raw_level_range)) else derived_level_range


        # Hours
        raw_hours = raw_data.get("hours_raw")
        normalized_hours = []
        if isinstance(raw_hours, list):
            for h in raw_hours:
                # Assuming 'h' could be '2-4 hours', '2 hours', '4 hours', 'variable'
                # Extract numbers or 'variable'
                match_range = re.search(r'(\d+-\d+)\s*hours?', h, re.IGNORECASE)
                match_single = re.search(r'(\d+)\s*hours?', h, re.IGNORECASE)
                match_variable = re.search(r'variable', h, re.IGNORECASE)

                if match_range:
                    normalized_hours.append(match_range.group(1))
                elif match_single:
                    normalized_hours.append(match_single.group(1))
                elif match_variable:
                    normalized_hours.append("variable")
                # If no specific pattern, just append the original cleaned string if it's meaningful
                elif h and h.strip().lower() not in ["", "none", "n/a"]: # Avoid adding empty/meaningless strings
                     normalized_hours.append(h.strip())
        elif isinstance(raw_hours, str): # Handle case where it might be a single string from older data
             match_range = re.search(r'(\d+-\d+)\s*hours?', raw_hours, re.IGNORECASE)
             match_single = re.search(r'(\d+)\s*hours?', raw_hours, re.IGNORECASE)
             match_variable = re.search(r'variable', raw_hours, re.IGNORECASE)
             if match_range:
                 normalized_hours.append(match_range.group(1))
             elif match_single:
                 normalized_hours.append(match_single.group(1))
             elif match_variable:
                 normalized_hours.append("variable")
             elif raw_hours and raw_hours.strip().lower() not in ["", "none", "n/a"]:
                 normalized_hours.append(raw_hours.strip())
        
        # Remove duplicates and ensure unique values, preserving order as much as possible for common cases
        # Convert to set and back to list for uniqueness, then sort if desirable (alphanumeric for hours like "10", "2-4")
        # For simplicity, let's just make it unique and keep order.
        unique_hours = []
        seen = set()
        for x in normalized_hours:
            if x not in seen:
                unique_hours.append(x)
                seen.add(x)
        normalized_data["hours"] = unique_hours


        # Is Adventure (boolean) - for consistency, let's derive it here based on normalized data
        # This logic determines if the product is an adventure suitable for the catalog.
        # It's an adventure if it has a code AND is not a bundle/Roll20/Fantasy Grounds product.
        is_adventure_flag = False
        if normalized_data["code"]:
            lower_full_title = normalized_data["full_title"].lower() if normalized_data["full_title"] else ""
            is_bundle = 'bundle' in lower_full_title or 'compendium' in lower_full_title
            is_roll20 = 'roll20' in lower_full_title
            is_fg = 'fantasy grounds' in lower_full_title
            if not is_bundle and not is_roll20 and not is_fg:
                is_adventure_flag = True
        normalized_data["is_adventure"] = is_adventure_flag

        # Needs Review - for initial processing, set to True if critical data is missing
        # This flag can be updated by a separate fixup script
        normalized_data["needs_review"] = False # Default to False, will be updated by process_downloads_new.py more thoroughly
        if not normalized_data["code"] or \
           not normalized_data["level_range"] or \
           not normalized_data["tiers"] or \
           not normalized_data["hours"]: # Checks if the list is empty
            normalized_data["needs_review"] = True

        return normalized_data