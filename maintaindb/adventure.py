import datetime
import json
import logging
import os
import re
from dataclasses import dataclass, field
from typing import Any

import unicodedata
from dotenv import load_dotenv
from word2number import w2n


@dataclass
class DungeonCraft:
    product_id: str
    full_title: str | None = None
    title: str | None = None
    authors: list[str] = field(default_factory=list)
    date_created: datetime.date | None = None
    hours: str | None = None
    tiers: str | None = None
    apl: str | None = None
    level_range: str | None = None
    url: str | None = None
    campaigns: list[str] = field(default_factory=list)
    season: str | None = None
    is_adventure: bool = True
    price: float | None = None

    def to_json(self) -> dict[str, Any]:
        # keep your new None-safe date handling
        ...


load_dotenv()
logger = logging.getLogger()

DC_CAMPAIGNS = {
    'DL-DC': 'Dragonlance',
    'EB-DC': 'Eberron',
    'EB-SM': 'Eberron',
    'FR-DC': 'Forgotten Realms',
    'PS-DC': 'Forgotten Realms',  # Changed from Planescape
    'SJ-DC': 'Forgotten Realms',  # Changed from Spelljammer
    'WBW-DC': 'Forgotten Realms',  # Changed from The Wild Beyond the Witchlight
    'DC-POA': 'Forgotten Realms',  # Changed from Icewind Dale: Rime of the Frostmaiden
    'PO-BK': 'Forgotten Realms',
    'BMG-DRW': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
    'BMG-MOON': 'Forgotten Realms',
    'CCC-': 'Forgotten Realms',
    'RV-DC': 'Ravenloft',
}

DDAL_CAMPAIGN = {
    'RMH': ['Ravenloft'],
    'DDAL4': ['Forgotten Realms', 'Ravenloft'],
    'DDAL04': ['Forgotten Realms', 'Ravenloft'],
    'DDEX1': ['Forgotten Realms'],
    'DDEX01': ['Forgotten Realms'],
    'DDEX2': ['Forgotten Realms'],
    'DDEX02': ['Forgotten Realms'],
    'DDEX3': ['Forgotten Realms'],
    'DDEX03': ['Forgotten Realms'],
    'DDAL5': ['Forgotten Realms'],
    'DDAL05': ['Forgotten Realms'],
    'DDAL6': ['Forgotten Realms'],
    'DDAL06': ['Forgotten Realms'],
    'DDAL7': ['Forgotten Realms'],
    'DDAL07': ['Forgotten Realms'],
    'DDAL8': ['Forgotten Realms'],
    'DDAL08': ['Forgotten Realms'],
    'DDAL9': ['Forgotten Realms'],
    'DDAL09': ['Forgotten Realms'],
    'DDAL10': ['Forgotten Realms'],
    'DDAL00': ['Forgotten Realms'],
    'DDAL-DRW': ['Forgotten Realms'],
    'DDEP': ['Forgotten Realms'],
    'DDAL-ELW': ['Eberron'],
    'EB': ['Eberron'],
}

SEASONS = {
    # Post-season named programs and hardback tie-ins (non-numeric seasons)
    'WBW-DC': "The Wild Beyond the Witchlight",
    'SJ-DC': "Spelljammer",
    'PS-DC': "Planescape",
    'DC-POA': "Icewind Dale",
}
# Human-friendly labels for numeric seasons (1-10)
SEASON_LABELS = {
    1: "Tyranny of Dragons",
    2: "Elemental Evil",
    3: "Rage of Demons",
    4: "Curse of Strahd",
    5: "Storm King's Thunder",
    6: "Tales From the Yawning Portal",
    7: "Tomb of Annihilation",
    8: "Waterdeep",
    9: "Avernus Rising",
    10: "Plague of Ancients",
}

# --- add somewhere near the top of adventure.py ---
def _collect_text_for_regexes(parsed_html) -> str:
    """Gather text from places both legacy and new pages use, plus simple test fixtures."""
    blocks: list[str] = []

    # 1) meta description (present on both old and new)
    md = parsed_html.find("meta", {"name": "description"})
    if md and md.get("content"):
        blocks.append(md["content"])

    # 2) legacy block
    legacy = parsed_html.find("div", {"class": "grid_11 alpha omega prod-content-content"})
    if legacy:
        blocks.append(legacy.get_text(" ", strip=True))

    # 3) generic prod-content variants (covers your test fixtures)
    for el in parsed_html.select("div.prod-content, div.prod-content-content, div.alpha.omega.prod-content"):
        t = el.get_text(" ", strip=True)
        if t and t not in blocks:
            blocks.append(t)

    # 4) any div whose class string contains "prod-content"
    for el in parsed_html.find_all("div", class_=lambda c: isinstance(c, str) and "prod-content" in c):
        t = el.get_text(" ", strip=True)
        if t and t not in blocks:
            blocks.append(t)

    # 5) absolute fallback: whole doc text
    if not blocks:
        t = parsed_html.get_text(" ", strip=True)
        if t:
            blocks.append(t)

    return " ".join(blocks)

def get_season(code):
    if not code:
        return None
    code_u = str(code).upper()
    # First: named seasons based on explicit prefixes (WBW-DC, SJ-DC, PS-DC, DC-POA)
    for prefix, season in SEASONS.items():
        if code_u.startswith(prefix) if isinstance(prefix, str) else False:
            return season
    # Next: infer numeric season from DD Adventurers League code families
    # Examples: DDEX1-01, DDEX01-01, DDAL5-01, DDAL05-01
    m = re.match(r"^(DDEX|DDAL)0?(\d+)", code_u)
    if m:
        try:
            return int(m.group(2))
        except Exception:
            pass
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

    def __init__(self, product_id, title, authors, code, date_created, hours, tiers, apl, level_range, url, campaigns,
                 season=None, is_adventure=None, price=None) -> None:
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
        self.campaigns = campaigns  # This will now be a list of strings
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
        # Remove explicit (5e) marker and any remaining standalone '5e' tokens (commonly at end)
        t = re.sub(r"\(\s*5e\s*\)", "", str(title), flags=re.IGNORECASE)
        # Remove DC trailing code fragments like FR-DC-XXX in the visible short title
        regex = r'[A-Z]{2,}-DC-([A-Z]{2,})([^\s]+)'
        # Also strip colons; keep parentheses removal after (5e) handled to avoid leaving '5e'
        t = t.replace(':', '')
        # Remove parentheses contents gently (except we've already removed (5e))
        t = t.replace('(', '').replace(')', '')
        result = re.sub(regex, '', t)
        # Remove any trailing '- 5e' or ' 5e'
        result = re.sub(r"[\s-]*\b5e\b[\s-]*$", "", result, flags=re.IGNORECASE)
        return result.strip()

    def __str__(self) -> str:
        return json.dumps(self.to_json(), sort_keys=True, indent=2, )

    def to_json(self):
        # --- safe date normalization for JSON ---
        def _fmt_date_yyyymmdd(d):
            if d is None:
                return None
            # already a date/datetime
            if isinstance(d, (datetime.date, datetime.datetime)):
                return d.strftime('%Y%m%d')
            # strings we accept: YYYYMMDD or YYYY-MM-DD
            if isinstance(d, str):
                s = d.strip()
                m = re.match(r'^(\d{4})-?(\d{2})-?(\d{2})$', s)
                if m:
                    return f"{m.group(1)}{m.group(2)}{m.group(3)}"
            # unknown shape, punt
            return None

        result = dict(
            product_id=self.product_id,
            full_title=self.full_title,
            title=self.title,
            authors=self.authors,
            code=self.code,
            date_created=_fmt_date_yyyymmdd(self.date_created),  # <-- was strftime() directly
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
    if value is None:
        return None

    # Try direct integer conversion first
    try:
        return int(value)
    except ValueError:
        pass  # Not a simple integer string, try word to number

    # Try word to number conversion
    try:
        return w2n.word_to_num(value)
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
                existing_value = str(int(existing_value))  # Convert to string, handle floats like 5.0

            if careful_mode:
                if not is_existing_value_empty:  # If existing is not empty, keep it
                    merged_data[key] = existing_value
                elif not is_new_value_empty:  # If existing is empty, and new is not, use new
                    merged_data[key] = new_value
                else:  # Both are empty, keep new (which is empty)
                    merged_data[key] = new_value
            else:  # Original behavior (not careful, not force)
                if not is_new_value_empty:
                    if is_existing_value_empty or existing_value != new_value:
                        merged_data[key] = new_value
                elif not is_existing_value_empty:  # If new is empty, but existing is not, keep existing
                    merged_data[key] = existing_value
    return merged_data


def _extract_raw_data_from_html(parsed_html, product_id):
    raw_data = {
        "module_name": None,
        "authors": [],
        "date_created": None,
        "hours_raw": None,
        "tiers_raw": None,
        "apl_raw": None,
        "level_range_raw": None,
        "price_raw": None,
        # Pay What You Want markers (raw)
        "pwyw_flag_raw": False,
        "suggested_price_raw": None,
    }

    # ---------- LEGACY PAGE (existing selectors) ----------
    product_title = parsed_html.find("div", {"class": "grid_12 product-title"})
    if product_title:
        children = product_title.findChildren("span", {"itemprop": "name"}, recursive=True)
        for child in children:
            raw_data["module_name"] = child.text
            break

    product_from = parsed_html.find("div", {"class": "grid_12 product-from"})
    if product_from:
        children = product_from.findChildren("a", recursive=True)
        for child in children:
            raw_data["authors"].append(child.text)

    children = parsed_html.find_all("div", {"class": "widget-information-item-content"})
    key = 'This title was added to our catalog on '
    for child in children:
        if key in child.text:
            date_str = child.text.replace(key, '').replace('.', '')
            raw_data["date_created"] = datetime.datetime.strptime(date_str.strip(), "%B %d, %Y").date()
            break

    product_content_div = parsed_html.find("div", {"class": "grid_11 alpha omega prod-content-content"})
    text = ""
    if product_content_div:
        text = product_content_div.get_text(separator=" ", strip=True)

    # Meta description (works for both old and new)
    meta_description_tag = parsed_html.find("meta", {"name": "description"})
    meta_description_text = meta_description_tag["content"] if meta_description_tag and "content" in meta_description_tag.attrs else ""
    combined_text = _collect_text_for_regexes(parsed_html)

    # ---------- NEW FORMAT FALLBACKS ----------
    # Title from og:title or <title> if legacy <div.product-title> missing
    if not raw_data["module_name"]:
        og_title = parsed_html.find("meta", {"property": "og:title"})
        if og_title and og_title.get("content"):
            # Example: "Una chiave Maledetta - Dungeon Masters Guild | Dungeon Masters Guild"
            title_txt = og_title["content"]
            title_txt = re.sub(r'\s*-\s*Dungeon Masters Guild.*$', '', title_txt, flags=re.IGNORECASE)
            raw_data["module_name"] = title_txt.strip()

    if not raw_data["module_name"]:
        title_tag = parsed_html.find("title")
        if title_tag and title_tag.text:
            title_txt = re.sub(r'\s*-\s*Dungeon Masters Guild.*$', '', title_tag.text, flags=re.IGNORECASE)
            raw_data["module_name"] = title_txt.strip()

    # JSON-LD (Angular site embeds structured data with price, sometimes date/author)
    # Look for one or more <script type="application/ld+json"> blocks
    try:
        for script in parsed_html.find_all("script", attrs={"type": "application/ld+json"}):
            if not script.string:
                continue
            try:
                blob = json.loads(script.string)
            except Exception:
                continue

            # Normalize to list
            nodes = blob if isinstance(blob, list) else [blob]
            for node in nodes:
                if not isinstance(node, dict):
                    continue

                # Try price from offers
                if raw_data["price_raw"] is None:
                    offers = node.get("offers")
                    if isinstance(offers, dict):
                        price = offers.get("price")
                        if price is None and isinstance(offers.get("priceSpecification"), dict):
                            price = offers["priceSpecification"].get("price")
                        if price is not None:
                            try:
                                raw_data["price_raw"] = float(price)
                            except Exception:
                                pass  # leave as None if it can't convert

                # Optional: try date published
                if raw_data["date_created"] is None:
                    dp = node.get("datePublished") or node.get("dateCreated")
                    # Common ISO formats; be permissive
                    if isinstance(dp, str):
                        for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
                            try:
                                dt = datetime.datetime.strptime(dp[:len(fmt)], fmt).date()
                                raw_data["date_created"] = dt
                                break
                            except Exception:
                                pass

                # Optional: try authors list if available
                if not raw_data["authors"]:
                    auth = node.get("author") or node.get("creator")
                    # Could be dict, list, or string
                    def _coerce_authors(a):
                        if isinstance(a, str):
                            return [a]
                        if isinstance(a, dict):
                            # Schema.org Person/Organization
                            n = a.get("name")
                            return [n] if n else []
                        if isinstance(a, list):
                            out = []
                            for item in a:
                                if isinstance(item, str):
                                    out.append(item)
                                elif isinstance(item, dict) and item.get("name"):
                                    out.append(item["name"])
                            return out
                        return []
                    raw_data["authors"] = _coerce_authors(auth) or raw_data["authors"]
    except Exception:
        # If JSON-LD parse fails, ignore silently and continue with other signals
        pass

    # ---------- Regex pulls (yours) over combined_text ----------
    # --- replace the current hours_match handling in _extract_raw_data_from_html ---
    # Hours: handle numeric and word forms, with optional hyphenated "two-to-four-hour" and spaced "two to four hour"
    hours_match = re.search(
        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)'
        r'(?:\s*(?:-|/|to|-?to-?)\s*(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty))?'
        r'(?:\s*(?:-|\s)*\s*)?'
        r'(?:hour|hours|hr)\b',
        combined_text,
        re.IGNORECASE
    )
    if hours_match:
        # Prefer ranges when both ends are present; otherwise accept single
        start = str_to_int(hours_match.group(1))
        end = str_to_int(hours_match.group(2)) if hours_match.group(2) else None
        if start is not None and end is not None:
            raw_data["hours_raw"] = f"{start}-{end}"
        elif start is not None and raw_data.get("hours_raw") is None:
            # Only set single-hour if we haven't already captured a range elsewhere
            raw_data["hours_raw"] = str(start)

    if not raw_data.get("hours_raw"):
        hours_match_alt = re.search(r'(\d+)(?:[-/](\d+))?\s*[-h]*(?:hour|hours|hr)', combined_text, re.IGNORECASE)
        if hours_match_alt:
            raw_data["hours_raw"] = f"{hours_match_alt.group(1)}-{hours_match_alt.group(2)}" if hours_match_alt.group(
                2) else hours_match_alt.group(1)

    raw_data["apl_raw"]        = get_patt_first_matching_group(r"(?:APL|Average Party Level)\s*(?:\(APL\))?\s*(\d+)", combined_text)
    raw_data["tiers_raw"]      = get_patt_first_matching_group(r"Tier ?([1-4])", combined_text)
    raw_data["level_range_raw"]= get_patt_first_matching_group(r"(?i)Level(?:s)?\s*([\d-]+)", combined_text)
    # If not captured, try ordinal style like '1st-4th level'
    if not raw_data["level_range_raw"]:
        m_levels = re.search(r"(?i)(\d+)(?:st|nd|rd|th)?\s*[-to]+\s*(\d+)(?:st|nd|rd|th)?\s*level", combined_text)
        if m_levels:
            try:
                start = int(m_levels.group(1))
                end = int(m_levels.group(2))
                raw_data["level_range_raw"] = f"{start}-{end}"
            except Exception:
                pass

    if not raw_data["hours_raw"]:
        hours_match_alt = re.search(r'(\d+)(?:[-/](\d+))?\s*[-h]*(?:hour|hours|hr)', combined_text, re.IGNORECASE)
        if hours_match_alt:
            raw_data["hours_raw"] = f"{hours_match_alt.group(1)}-{hours_match_alt.group(2)}" if hours_match_alt.group(2) else hours_match_alt.group(1)

    # ---------- Price extraction precedence ----------
    # Prefer JSON-LD offers (set above), then meta[itemprop=price], then the CURRENT displayed price (div.price),
    # and only fall back to historical/original prices (price-old, product-price-strike).
    if raw_data["price_raw"] is None:
        meta_price = parsed_html.find("meta", attrs={"itemprop": "price"})
        if meta_price and meta_price.get("content"):
            try:
                content_val = meta_price.get("content").strip()
                # Some pages include a leading $ in the meta content; strip non-numeric chars
                m = re.search(r"([0-9]+(?:\.[0-9]+)?)", content_val)
                if m:
                    raw_data["price_raw"] = float(m.group(1))
            except Exception:
                pass

    if raw_data["price_raw"] is None:
        current_price_div = parsed_html.find("div", class_="price")
        if current_price_div:
            price_text = current_price_div.get_text(strip=True)
            price_value = re.search(r'\$([\d\.]+)', price_text)
            if price_value:
                raw_data["price_raw"] = float(price_value.group(1))

    # --- Pay What You Want detection & suggested price extraction ---
    # Heuristics:
    #  - presence of input name="pwyw_price" indicates PWYW
    #  - elements with attributes like pwyw_average or classes pwyw_* also indicate PWYW
    try:
        # Detect PWYW via explicit input field
        if parsed_html.find(attrs={"name": "pwyw_price"}):
            raw_data["pwyw_flag_raw"] = True
        # Detect PWYW via classes starting with 'pwyw_'
        if not raw_data["pwyw_flag_raw"]:
            any_pwyw_class = parsed_html.find(class_=re.compile(r"^pwyw_"))
            if any_pwyw_class:
                raw_data["pwyw_flag_raw"] = True

        # Suggested price from attribute pwyw_average
        if raw_data["suggested_price_raw"] is None:
            for el in parsed_html.find_all(True):  # all tags
                if hasattr(el, 'attrs') and 'pwyw_average' in el.attrs:
                    val = el.attrs.get('pwyw_average')
                    if isinstance(val, str) and val.strip():
                        try:
                            raw_data["suggested_price_raw"] = float(val)
                            break
                        except Exception:
                            pass

        # Suggested price from visible text e.g., "Suggested Price $1.00"
        if raw_data["suggested_price_raw"] is None:
            full_text = parsed_html.get_text(" ", strip=True)
            m = re.search(r"Suggested\s+Price\s*\$([\d\.]+)", full_text, flags=re.IGNORECASE)
            if m:
                try:
                    raw_data["suggested_price_raw"] = float(m.group(1))
                except Exception:
                    pass
    except Exception:
        # Be conservative; do not let PWYW parsing break the pipeline
        pass

    if raw_data["price_raw"] is None:
        original_price_old_match = parsed_html.find("div", class_="price-old")
        if original_price_old_match:
            price_text = original_price_old_match.get_text(strip=True)
            price_value = re.search(r'\$([\d\.]+)', price_text)
            if price_value:
                raw_data["price_raw"] = float(price_value.group(1))

    if raw_data["price_raw"] is None:
        original_price_strike_match = parsed_html.find("div", class_="product-price-strike")
        if original_price_strike_match:
            price_text = original_price_strike_match.get_text(strip=True)
            price_value = re.search(r'\$([\d\.]+)', price_text)
            if price_value:
                raw_data["price_raw"] = float(price_value.group(1))


    return raw_data


def _normalize_and_convert_data(raw_data):
    processed_data = {
        "module_name": raw_data["module_name"],
        "authors": raw_data["authors"],
        "code": None,
        "date_created": raw_data["date_created"],
        "hours": None,
        "tiers": None,
        "apl": None,
        "level_range": None,
        "campaigns": [],
        "season": None,
        "is_adventure": False,
        "price": raw_data["price_raw"],
        # New normalized fields for Pay What You Want
        "payWhatYouWant": bool(raw_data.get("pwyw_flag_raw", False)),
        "suggestedPrice": raw_data.get("suggested_price_raw")
    }

    if processed_data["module_name"]:
        result = get_dc_code_and_campaign(processed_data["module_name"])
        if result is not None:
            processed_data["code"] = result[0]
            processed_data["campaigns"] = result[1]
            processed_data["season"] = get_season(processed_data["code"])

    # Hours conversion
    if raw_data["hours_raw"]:
        extracted_range_str = raw_data["hours_raw"]
        if '-' in extracted_range_str or 'to' in extracted_range_str.lower():
            # It's a range
            parts = re.split(r'\s*(?:-|to)\s*', extracted_range_str, flags=re.IGNORECASE)
            start_int = str_to_int(parts[0])
            end_int = str_to_int(parts[-1])  # Take the last part for the end of the range
            if start_int is not None and end_int is not None:
                processed_data["hours"] = f"{start_int}-{end_int}"
            else:
                processed_data["hours"] = None
        else:
            # It's a single value
            single_int = str_to_int(extracted_range_str)
            if single_int is not None:
                processed_data["hours"] = str(single_int)
            else:
                processed_data["hours"] = None

    # APL and Tiers conversion
    processed_data["apl"] = str_to_int(raw_data["apl_raw"])
    processed_data["tiers"] = str_to_int(raw_data["tiers_raw"])
    processed_data["level_range"] = raw_data["level_range_raw"]

    return processed_data


def _infer_missing_adventure_data(data):
    # Derive Tier from APL if Tier is None
    if data["tiers"] is None and data["apl"] is not None:
        if 1 <= data["apl"] <= 4:
            data["tiers"] = 1
        elif 5 <= data["apl"] <= 10:
            data["tiers"] = 2
        elif 11 <= data["apl"] <= 16:
            data["tiers"] = 3
        elif 17 <= data["apl"] <= 20:
            data["tiers"] = 4
    # Derive Tier from Level Range if Tier and APL are None
    elif data["tiers"] is None and data["level_range"] is not None:
        if isinstance(data["level_range"], str) and '-' in data["level_range"]:
            start_level = int(data["level_range"].split('-')[0])
            if 1 <= start_level <= 4:
                data["tiers"] = 1
            elif 5 <= start_level <= 10:
                data["tiers"] = 2
            elif 11 <= start_level <= 16:
                data["tiers"] = 3
            elif 17 <= start_level <= 20:
                data["tiers"] = 4

    # Derive Level Range from Tier if Level Range is None or not a valid range
    derived_level_range = None
    if data["tiers"] is not None:
        if data["tiers"] == 1:
            derived_level_range = "1-4"
        elif data["tiers"] == 2:
            derived_level_range = "5-10"
        elif data["tiers"] == 3:
            derived_level_range = "11-16"
        elif data["tiers"] == 4:
            derived_level_range = "17-20"

    if data["level_range"] is None or not re.match(r"\d+-\d+", str(data["level_range"])):
        data["level_range"] = derived_level_range

    # Determine if it's an adventure
    lower_full_title = data["module_name"].lower() if data["module_name"] else ""
    is_bundle = 'bundle' in lower_full_title
    is_roll20 = 'roll20' in lower_full_title
    is_fg = 'fantasy grounds' in lower_full_title

    if data["code"] and not is_bundle and not is_roll20 and not is_fg:
        data["is_adventure"] = True
    else:
        data["is_adventure"] = False

    return data


def extract_data_from_html(parsed_html, product_id, product_alt=None, existing_data=None, force_overwrite=False,
                           careful_mode=False):
    raw_data = _extract_raw_data_from_html(parsed_html, product_id)
    normalized_data = _normalize_and_convert_data(raw_data)
    new_data = _infer_missing_adventure_data(normalized_data)

    return merge_adventure_data(existing_data, new_data, force_overwrite, careful_mode)


if __name__ == "__main__":
    ## Extract data from a JSON if a JSON is specified on the comnmand line and display
    pass



def get_season_label(value):
    """
    Resolve a human-friendly label for a season value.
    - If value is an int and present in SEASON_LABELS, return that label.
    - If value is a string (named program), return as-is.
    - Otherwise, return None.
    """
    if isinstance(value, int):
        return SEASON_LABELS.get(value)
    if isinstance(value, str):
        return value
    return None
