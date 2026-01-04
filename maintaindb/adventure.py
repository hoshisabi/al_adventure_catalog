"""
Adventure data model and HTML parsing utilities for DMsGuild adventure catalog.

This module provides:
- DungeonCraft class for representing adventure data
- HTML extraction and normalization functions
- Utility functions for filename sanitization, season/campaign mapping, etc.
"""

import datetime
import json
import logging
import os
import re
from typing import Any

import unicodedata
from dotenv import load_dotenv
from word2number import w2n


# ============================================================================
# INITIALIZATION
# ============================================================================

load_dotenv()
logger = logging.getLogger()


# ============================================================================
# CONSTANTS
# ============================================================================

# Import constants from adventure_utils to avoid duplication
# Re-export them here for backward compatibility with existing imports
from .adventure_utils import DC_CAMPAIGNS, DDAL_CAMPAIGN, SEASONS, get_campaigns_from_code, get_adventure_code_and_campaigns, normalize_ddal_ddex_code

# SEASON_LABELS is kept for backward compatibility with get_season_label() function
# It's derived from SEASONS for numeric seasons (1-10)
SEASON_LABELS = {k: v for k, v in SEASONS.items() if isinstance(k, int)}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def sanitize_filename(filename):
    """
    Normalizes and sanitizes a string to be a valid filename.
    
    Args:
        filename: The string to sanitize
        
    Returns:
        A sanitized filename string ending with .json
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


def generate_warhorn_slug(title):
    """
    Generates a Warhorn-style slug from a given title.
    Converts to lowercase and replaces spaces/non-alphanumeric characters with hyphens.
    
    Args:
        title: The title string to convert to a slug
        
    Returns:
        A slug string suitable for Warhorn URLs
    """
    if not title:
        return ""
    # Convert to lowercase
    slug = title.lower()
    # Replace spaces and non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def str_to_int(value):
    """
    Converts a value to an integer, handling both numeric strings and number words.
    
    Args:
        value: A value that might be an int, numeric string, or word (e.g., "one", "two")
        
    Returns:
        An integer if conversion succeeds, None otherwise
    """
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
    """
    Returns the first matching group from a regex pattern in text.
    If no groups are defined, returns the full match.
    
    Args:
        regex: Regular expression pattern string
        text: Text to search in
        
    Returns:
        The first matching group or full match, or None if no match
    """
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        for group in matches.groups():
            if group:
                return group
    return None


# ============================================================================
# DATA MODEL
# ============================================================================

class DungeonCraft:

    def __init__(self, product_id, title, authors, code, date_created, hours, tiers, apl, level_range, url, campaigns,
                 season=None, is_adventure=None, price=None, payWhatYouWant=None, suggestedPrice=None, needs_review=None, seed=None) -> None:
        self.product_id = product_id
        self.full_title = title
        self.title = self.__get_short_title(title, code).strip()
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
        self.payWhatYouWant = payWhatYouWant
        self.suggestedPrice = suggestedPrice
        self.needs_review = needs_review
        self.seed = seed

    def is_tier(self, tier):
        """Check if this adventure is for the specified tier."""
        if self.tiers is not None:
            return self.tiers == tier
        return False

    def is_tier_unknown(self):
        """Check if the tier is unknown."""
        if self.tiers is None:
            return True
        return False

    def is_hour(self, hour):
        """
        Check if this adventure matches the specified hour.
        Handles ranges (e.g., "1-2") and comma-separated lists (e.g., "1,2,3").
        """
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
        """Check if the hours are unknown."""
        if self.hours is None or self.hours == '':
            return True
        return False

    def is_campaign(self, campaign_name):
        """Check if this adventure belongs to the specified campaign."""
        if self.campaigns is not None:
            return campaign_name in self.campaigns
        return False

    def is_campaign_unknown(self):
        """Check if the campaign is unknown."""
        if self.campaigns is None or not self.campaigns:
            return True
        return False

    def __get_short_title(self, title, code=None):
        """Extract a short title by removing code fragments and formatting markers."""
        t = str(title)
        original_title = t  # Keep original for fallback
        
        # Normalize Unicode dash variants to standard hyphen-minus for code matching
        # U+2010 HYPHEN, U+2011 NON-BREAKING HYPHEN, U+2012 FIGURE DASH, 
        # U+2013 EN DASH, U+2014 EM DASH, U+2015 HORIZONTAL BAR, U+2212 MINUS SIGN
        dash_variants = ['\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2212']
        normalized_t = t
        for dash_char in dash_variants:
            normalized_t = normalized_t.replace(dash_char, '-')
        
        # Strip code prefix if code is provided and title starts with it
        if code:
            code_str = str(code)
            # Try case-insensitive matching for code removal using normalized title
            normalized_t_lower = normalized_t.lower()
            code_lower = code_str.lower()
            # Try to remove code with various possible separators (space, dash, or nothing)
            code_removed = False
            for separator in [' ', '-', '']:
                code_prefix_lower = code_lower + separator
                if normalized_t_lower.startswith(code_prefix_lower):
                    # Find the actual length to remove (preserving original case)
                    code_prefix_len = len(code_str + separator)
                    # Check if removing the code would leave us with an empty string
                    remaining = t[code_prefix_len:].strip()
                    if remaining:  # Only remove if there's something left
                        t = remaining
                        normalized_t = normalized_t[code_prefix_len:].strip()
                        code_removed = True
                    break
            # If code is at the start but no separator matched, remove it directly
            if not code_removed and normalized_t_lower.startswith(code_lower):
                remaining = t[len(code_str):].strip()
                if remaining:  # Only remove if there's something left
                    t = remaining
                    normalized_t = normalized_t[len(code_str):].strip()
        
        # Remove explicit (5e) marker and any remaining standalone '5e' tokens (commonly at end)
        t = re.sub(r"\(\s*5e\s*\)", "", t, flags=re.IGNORECASE)
        
        # Strip common metadata patterns that appear after " - " or " |"
        # Patterns like: " - Wizards of the Coast | D&D 5th Edition | Dungeon Masters Guild"
        t = re.sub(r'\s*-\s*(Wizards of the Coast|D&D 5th Edition|Dungeon Masters Guild).*$', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s*\|\s*(D&D 5th Edition|Dungeon Masters Guild).*$', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s*-\s*Dungeon Masters Guild.*$', '', t, flags=re.IGNORECASE)
        # Strip "D&D Adventurers League" pattern (appears after " - ")
        t = re.sub(r'\s*-\s*D&D Adventurers League.*$', '', t, flags=re.IGNORECASE)
        
        # Remove DC trailing code fragments like FR-DC-XXX in the visible short title
        regex = r'[A-Z]{2,}-DC-([A-Z]{2,})([^\s]+)'
        # Also strip colons; keep parentheses removal after (5e) handled to avoid leaving '5e'
        t = t.replace(':', '')
        # Remove parentheses contents gently (except we've already removed (5e))
        t = t.replace('(', '').replace(')', '')
        result = re.sub(regex, '', t)
        # Remove any trailing '- 5e' or ' 5e'
        result = re.sub(r"[\s-]*\b5e\b[\s-]*$", "", result, flags=re.IGNORECASE)
        # Clean up any remaining double spaces
        result = re.sub(r'\s+', ' ', result)
        result = result.strip()
        # If we ended up with an empty string, fall back to the original title
        # (This handles cases where the title was just the code)
        if not result:
            result = original_title.strip()
        return result

    def __str__(self) -> str:
        return json.dumps(self.to_json(), sort_keys=True, indent=2, )

    def to_json(self):
        """Convert the DungeonCraft object to a JSON-serializable dictionary."""
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
        # Add PWYW fields if they exist
        if self.payWhatYouWant is not None:
            result["payWhatYouWant"] = self.payWhatYouWant
        if self.suggestedPrice is not None:
            result["suggestedPrice"] = self.suggestedPrice
        # Add needs_review if it exists (set by inference logic or RSS parser)
        if self.needs_review is not None:
            result["needs_review"] = self.needs_review
        # Add seed if it exists
        if self.seed is not None:
            result["seed"] = self.seed
        return result

    def convert_date_to_readable_str(self):
        """Convert date_created to a human-readable string format."""
        if self.date_created is not None:
            # Ensure date_created is a datetime object before formatting
            if isinstance(self.date_created, datetime.date):
                date_obj = self.date_created
            else:
                date_obj = datetime.datetime.strptime(self.date_created, "%Y%m%d").date()
            return date_obj.strftime("%Y, %b")
        return 'Unknown'


# ============================================================================
# HTML EXTRACTION FUNCTIONS
# ============================================================================

def _clean_title_metadata(title):
    """
    Remove common metadata patterns from extracted titles.
    Strips patterns like " - Publisher | Edition | Platform" and edition markers.
    
    Args:
        title: Raw title string from HTML
        
    Returns:
        Cleaned title string
    """
    if not title:
        return title
    
    # Strip common metadata patterns that appear after " - " or " |"
    # Patterns like: " - Wizards of the Coast | D&D 5th Edition | Dungeon Masters Guild"
    # Also handle variations with just " - Publisher | Platform"
    title = re.sub(r'\s*-\s*(Wizards of the Coast|D&D 5th Edition|Dungeon Masters Guild).*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*\|\s*(D&D 5th Edition|Dungeon Masters Guild).*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*-\s*Dungeon Masters Guild.*$', '', title, flags=re.IGNORECASE)
    # Strip "D&D Adventurers League" pattern (appears after " - ")
    title = re.sub(r'\s*-\s*D&D Adventurers League.*$', '', title, flags=re.IGNORECASE)
    
    # Strip edition markers like "(5e)", "(5th Edition)", etc.
    title = re.sub(r'\(\s*5e\s*\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(\s*5th\s+Edition\s*\)', '', title, flags=re.IGNORECASE)
    
    # Clean up any remaining double spaces or trailing/leading whitespace
    title = re.sub(r'\s+', ' ', title)
    title = title.strip()
    
    return title


def _extract_title_from_html(parsed_html):
    """
    Extract product title from HTML using multiple fallback strategies.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        Title string or None if not found
    """
    title_result = None
    
    # Try legacy format first
    product_title = parsed_html.find("div", {"class": "grid_12 product-title"})
    if product_title:
        children = product_title.findChildren("span", {"itemprop": "name"}, recursive=True)
        for child in children:
            title_result = child.text
            break
    
    # Try og:title meta tag
    if not title_result:
        og_title = parsed_html.find("meta", {"property": "og:title"})
        if og_title and og_title.get("content"):
            title_result = og_title["content"]
    
    # Try h1 tag (for newer Angular format)
    if not title_result:
        h1_tag = parsed_html.find("h1")
        if h1_tag and h1_tag.text:
            title_result = h1_tag.text.strip()
    
    # Try <title> tag as last resort
    if not title_result:
        title_tag = parsed_html.find("title")
        if title_tag and title_tag.text:
            title_result = title_tag.text
    
    # Clean metadata from extracted title
    if title_result:
        title_result = _clean_title_metadata(title_result)
    
    return title_result


def _extract_authors_from_html(parsed_html):
    """
    Extract authors from HTML using legacy format, new Angular format, and JSON-LD fallback.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        List of author names (may be empty)
    """
    authors = []
    
    # Try legacy format
    product_from = parsed_html.find("div", {"class": "grid_12 product-from"})
    if product_from:
        children = product_from.findChildren("a", recursive=True)
        for child in children:
            authors.append(child.text)
    
    # If no authors found, try new Angular format (table with obs-publisher-or-creators)
    if not authors:
        # Look for the "Author(s)" label in a table
        authors_label = parsed_html.find("p", {"data-codeid": "authors"})
        if authors_label:
            # Find the parent table row
            tr = authors_label.find_parent("tr")
            if tr:
                # Get all td elements in this row
                tds = tr.find_all("td")
                if len(tds) > 1:
                    # The second td should contain the obs-publisher-or-creators component
                    obs_component = tds[1].find("obs-publisher-or-creators")
                    if obs_component:
                        # Extract author links from within the component
                        author_links = obs_component.find_all("a")
                        for link in author_links:
                            author_text = link.get_text(strip=True)
                            if author_text:
                                authors.append(author_text)
    
    # If no authors found, try JSON-LD
    if not authors:
        try:
            for script in parsed_html.find_all("script", attrs={"type": "application/ld+json"}):
                if not script.string:
                    continue
                try:
                    blob = json.loads(script.string)
                except Exception:
                    continue
                
                nodes = blob if isinstance(blob, list) else [blob]
                for node in nodes:
                    if not isinstance(node, dict):
                        continue
                    
                    auth = node.get("author") or node.get("creator")
                    if auth:
                        def _coerce_authors(a):
                            if isinstance(a, str):
                                return [a]
                            if isinstance(a, dict):
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
                        authors = _coerce_authors(auth)
                        if authors:
                            break
                    if authors:
                        break
                if authors:
                    break
        except Exception:
            pass
    
    return authors


def _extract_date_from_html(parsed_html):
    """
    Extract creation date from HTML using legacy format, new Angular format, and JSON-LD fallback.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        datetime.date object or None if not found
    """
    # Try legacy format first
    children = parsed_html.find_all("div", {"class": "widget-information-item-content"})
    key = 'This title was added to our catalog on '
    for child in children:
        if key in child.text:
            date_str = child.text.replace(key, '').replace('.', '')
            try:
                return datetime.datetime.strptime(date_str.strip(), "%B %d, %Y").date()
            except Exception:
                pass
    
    # Try new Angular format: "Added to Catalog" followed by date
    try:
        # Find all <p> tags
        all_ps = parsed_html.find_all("p")
        for i, p_tag in enumerate(all_ps):
            # Check if this <p> contains "Added to Catalog"
            if p_tag.text and "Added to Catalog" in p_tag.text:
                # Look for the next few <p> tags that might contain a date
                for j in range(i + 1, min(i + 10, len(all_ps))):  # Check next several <p> tags
                    next_p = all_ps[j]
                    date_text = next_p.get_text(strip=True)
                    
                    # First, try the clean format: "Nov 14, 2025" or "November 14, 2025"
                    for date_format in ["%b %d, %Y", "%B %d, %Y"]:
                        try:
                            dt = datetime.datetime.strptime(date_text, date_format)
                            return dt.date()
                        except ValueError:
                            pass
                    
                    # Fallback: try MM/DD/YY or MM/DD/YYYY format (in u-text-bold class)
                    if next_p.get("class") and "u-text-bold" in next_p.get("class", []):
                        date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', date_text)
                        if date_match:
                            month, day, year = date_match.groups()
                            # Normalize year: if 2 digits, assume 20XX for years 00-99
                            if len(year) == 2:
                                year_int = int(year)
                                # Assume years 00-25 are 2000-2025, 26-99 are 1926-1999
                                year = f"20{year}" if year_int <= 25 else f"19{year}"
                            # Try parsing with normalized format
                            try:
                                date_str = f"{month}/{day}/{year}"
                                dt = datetime.datetime.strptime(date_str, "%m/%d/%Y")
                                return dt.date()
                            except ValueError:
                                pass
    except Exception:
        pass
    
    # Try JSON-LD if other formats didn't work
    try:
        for script in parsed_html.find_all("script", attrs={"type": "application/ld+json"}):
            if not script.string:
                continue
            try:
                blob = json.loads(script.string)
            except Exception:
                continue
            
            nodes = blob if isinstance(blob, list) else [blob]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                
                dp = node.get("datePublished") or node.get("dateCreated")
                if isinstance(dp, str):
                    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
                        try:
                            dt = datetime.datetime.strptime(dp[:len(fmt)], fmt).date()
                            return dt
                        except Exception:
                            pass
    except Exception:
        pass
    
    return None


def _extract_hours_from_text(text):
    """
    Extract hours information from combined text using regex patterns.
    
    Args:
        text: Combined text string to search
        
    Returns:
        Hours string (e.g., "2-4", "4") or None if not found
    """
    # Primary pattern: handle numeric and word forms with ranges
    hours_match = re.search(
        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)'
        r'(?:\s*(?:-|/|to|-?to-?)\s*(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty))?'
        r'(?:\s*(?:-|\s)*\s*)?'
        r'(?:hour|hours|hr)\b',
        text,
        re.IGNORECASE
    )
    if hours_match:
        start = str_to_int(hours_match.group(1))
        end = str_to_int(hours_match.group(2)) if hours_match.group(2) else None
        if start is not None and end is not None:
            return f"{start}-{end}"
        elif start is not None:
            return str(start)
    
    # Fallback pattern: simpler numeric pattern
    hours_match_alt = re.search(r'(\d+)(?:[-/](\d+))?\s*[-h]*(?:hour|hours|hr)', text, re.IGNORECASE)
    if hours_match_alt:
        if hours_match_alt.group(2):
            return f"{hours_match_alt.group(1)}-{hours_match_alt.group(2)}"
        else:
            return hours_match_alt.group(1)
    
    return None


def _extract_game_stats_from_text(text):
    """
    Extract game statistics (APL, tiers, level_range) from combined text.
    
    Args:
        text: Combined text string to search
        
    Returns:
        Dictionary with keys: apl_raw, tiers_raw, level_range_raw
    """
    stats = {
        "apl_raw": None,
        "tiers_raw": None,
        "level_range_raw": None,
    }
    
    # APL pattern: Handle variations like "APL 3", "APL: 3", "APL - 3", "APL (3)", "(APL) 3", "Average Party Level 3", "average party level (APL) of 2", etc.
    stats["apl_raw"] = get_patt_first_matching_group(r"(?:APL|Average Party Level|average party level)\s*(?:\(APL\))?\s*(?:of|is|:|-)?\s*(\d+)", text)
    
    # If APL not found, try "optimized for Xth level" pattern (e.g., "optimized for 13th level")
    if not stats["apl_raw"]:
        stats["apl_raw"] = get_patt_first_matching_group(r"(?i)optimized\s+for\s+(\d+)(?:st|nd|rd|th)?\s*level", text)
    
    stats["tiers_raw"] = get_patt_first_matching_group(r"Tier ?([1-4])", text)
    
    # Level range pattern: Handle "Level Range: 11-16", "Levels 11-16", "Level 11-16", etc.
    stats["level_range_raw"] = get_patt_first_matching_group(r"(?i)Level(?:s)?\s+Range\s*:?\s*([\d-]+)", text)
    
    # If not found with "Range", try simpler pattern "Level(s) 11-16"
    if not stats["level_range_raw"]:
        stats["level_range_raw"] = get_patt_first_matching_group(r"(?i)Level(?:s)?\s*([\d-]+)", text)
    
    # If level_range not captured, try ordinal style like '1st-4th level' or '11th through 16th Level'
    if not stats["level_range_raw"]:
        # Pattern 1: Ordinal numbers with "through", "to", or "-" before "Level" (e.g., "11th through 16th Level")
        # Allow optional text after "level" (e.g., "Level Characters")
        m_levels = re.search(r"(?i)(\d+)(?:st|nd|rd|th)?\s*(?:through|to|-)\s*(\d+)(?:st|nd|rd|th)?\s*level\b", text)
        if m_levels:
            try:
                start = int(m_levels.group(1))
                end = int(m_levels.group(2))
                stats["level_range_raw"] = f"{start}-{end}"
            except Exception:
                pass
        # Pattern 2: "for Xth through Yth Level" (e.g., "for 11th through 16th Level Characters")
        # Allow optional text after "level" (e.g., "Level Characters")
        if not stats["level_range_raw"]:
            m_levels = re.search(r"(?i)for\s+(\d+)(?:st|nd|rd|th)?\s*(?:through|to|-)\s*(\d+)(?:st|nd|rd|th)?\s*level\b", text)
            if m_levels:
                try:
                    start = int(m_levels.group(1))
                    end = int(m_levels.group(2))
                    stats["level_range_raw"] = f"{start}-{end}"
                except Exception:
                    pass
    
    return stats


def _extract_price_from_html(parsed_html):
    """
    Extract price from HTML using multiple strategies with precedence order.
    
    Precedence:
    1. JSON-LD offers (handled in _extract_jsonld_data)
    2. meta[itemprop=price]
    3. div.price (current price)
    4. div.price-old (historical price)
    5. div.product-price-strike (original price)
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        Price as float or None if not found
    """
    # Try meta[itemprop=price]
    meta_price = parsed_html.find("meta", attrs={"itemprop": "price"})
    if meta_price and meta_price.get("content"):
        try:
            content_val = meta_price.get("content").strip()
            m = re.search(r"([0-9]+(?:\.[0-9]+)?)", content_val)
            if m:
                return float(m.group(1))
        except Exception:
            pass
    
    # Try div.price (current price)
    current_price_div = parsed_html.find("div", class_="price")
    if current_price_div:
        price_text = current_price_div.get_text(strip=True)
        price_value = re.search(r'\$([\d\.]+)', price_text)
        if price_value:
            try:
                return float(price_value.group(1))
            except Exception:
                pass
    
    # Try div.price-old (historical price)
    original_price_old_match = parsed_html.find("div", class_="price-old")
    if original_price_old_match:
        price_text = original_price_old_match.get_text(strip=True)
        price_value = re.search(r'\$([\d\.]+)', price_text)
        if price_value:
            try:
                return float(price_value.group(1))
            except Exception:
                pass
    
    # Try div.product-price-strike (original price)
    original_price_strike_match = parsed_html.find("div", class_="product-price-strike")
    if original_price_strike_match:
        price_text = original_price_strike_match.get_text(strip=True)
        price_value = re.search(r'\$([\d\.]+)', price_text)
        if price_value:
            try:
                return float(price_value.group(1))
            except Exception:
                pass
    
    return None


def _extract_jsonld_price(parsed_html):
    """
    Extract price from JSON-LD structured data.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        Price as float or None if not found
    """
    try:
        for script in parsed_html.find_all("script", attrs={"type": "application/ld+json"}):
            if not script.string:
                continue
            try:
                blob = json.loads(script.string)
            except Exception:
                continue
            
            nodes = blob if isinstance(blob, list) else [blob]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                
                offers = node.get("offers")
                if isinstance(offers, dict):
                    # Prioritize ListPrice (original/regular price) over sale price
                    price = None
                    price_spec = offers.get("priceSpecification")
                    if isinstance(price_spec, dict):
                        # Check if it's a ListPrice (regular price, not sale price)
                        price_type = price_spec.get("priceType", "")
                        if "ListPrice" in str(price_type):
                            price = price_spec.get("price")
                    
                    # Fall back to offers.price only if ListPrice not found
                    if price is None:
                        price = offers.get("price")
                    
                    if price is not None:
                        try:
                            return float(price)
                        except Exception:
                            pass
    except Exception:
        pass
    
    return None


def _extract_seed_from_text(text):
    """
    Extract seed name from adventure description text.
    Looks for patterns like "Seed used: [name]" or "Seed: [name]"
    
    Args:
        text: Combined text from HTML description
        
    Returns:
        Seed name string or None if not found
    """
    if not text:
        return None
    
    # Pattern 1: "Seed used: [name]" or "Seed: [name]"
    # The seed name is typically followed by "Content Warnings:" or end of line
    patterns = [
        r'[Ss]eed\s+(?:used\s*:)?\s*([^\.\n]+?)(?:Content\s+Warnings|$)',
        r'[Ss]eed\s*:\s*([^\.\n]+?)(?:Content\s+Warnings|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            seed = match.group(1).strip()
            # Clean up common artifacts
            seed = re.sub(r'^used\s*:\s*', '', seed, flags=re.IGNORECASE)
            seed = seed.strip()
            if seed:
                return seed
    
    return None


def _extract_pwyw_info_from_html(parsed_html):
    """
    Extract Pay What You Want (PWYW) information from HTML.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        Dictionary with keys: pwyw_flag_raw (bool), suggested_price_raw (float or None)
    """
    pwyw_info = {
        "pwyw_flag_raw": False,
        "suggested_price_raw": None,
    }
    
    try:
        full_text = parsed_html.get_text(" ", strip=True)
        
        # Detect PWYW via explicit input field
        if parsed_html.find(attrs={"name": "pwyw_price"}):
            pwyw_info["pwyw_flag_raw"] = True
        
        # Detect PWYW via classes starting with 'pwyw_'
        if not pwyw_info["pwyw_flag_raw"]:
            any_pwyw_class = parsed_html.find(class_=re.compile(r"^pwyw_"))
            if any_pwyw_class:
                pwyw_info["pwyw_flag_raw"] = True
        
        # Detect PWYW via "Select Price Below" text (new Angular format)
        if not pwyw_info["pwyw_flag_raw"]:
            if re.search(r"Select\s+Price\s+Below", full_text, re.IGNORECASE):
                pwyw_info["pwyw_flag_raw"] = True
        
        # Detect PWYW via "Support the creator by paying" text
        if not pwyw_info["pwyw_flag_raw"]:
            if re.search(r"Support\s+the\s+creator\s+by\s+paying", full_text, re.IGNORECASE):
                pwyw_info["pwyw_flag_raw"] = True
        
        # Suggested price from attribute pwyw_average
        for el in parsed_html.find_all(True):  # all tags
            if hasattr(el, 'attrs') and 'pwyw_average' in el.attrs:
                val = el.attrs.get('pwyw_average')
                if isinstance(val, str) and val.strip():
                    try:
                        pwyw_info["suggested_price_raw"] = float(val)
                        break
                    except Exception:
                        pass
        
        # Suggested price from visible text e.g., "Suggested Price $1.00"
        if pwyw_info["suggested_price_raw"] is None:
            m = re.search(r"Suggested\s+Price\s*\$([\d\.]+)", full_text, flags=re.IGNORECASE)
            if m:
                try:
                    pwyw_info["suggested_price_raw"] = float(m.group(1))
                except Exception:
                    pass
        
        # If PWYW is detected but no suggested price found, try to find the lowest price button
        # This handles cases where the suggested price is shown as a button (e.g., "$0.50")
        if pwyw_info["pwyw_flag_raw"] and pwyw_info["suggested_price_raw"] is None:
            # Look for price patterns like "$0.50", "$1.00" etc. and take the lowest one as suggested
            price_matches = re.findall(r'\$(\d+\.?\d*)', full_text)
            if price_matches:
                try:
                    prices = [float(p) for p in price_matches if float(p) > 0]
                    if prices:
                        # Take the lowest non-zero price as the suggested price
                        pwyw_info["suggested_price_raw"] = min(prices)
                except Exception:
                    pass
    except Exception:
        # Be conservative; do not let PWYW parsing break the pipeline
        pass
    
    return pwyw_info


def _collect_text_for_regexes(parsed_html) -> str:
    """
    Gather text from places both legacy and new pages use, plus simple test fixtures.
    Collects text from meta description, legacy content divs, product description areas, and falls back to full document.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        
    Returns:
        Combined text string from various sources
    """
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

    # 5) product-description-control (newer page format)
    desc_control = parsed_html.find("div", {"class": "product-description-control"})
    if desc_control:
        t = desc_control.get_text(" ", strip=True)
        if t and t not in blocks:
            blocks.append(t)

    # 6) any div whose class contains "description" (catch other description variants)
    for el in parsed_html.find_all("div", class_=lambda c: isinstance(c, str) and "description" in c.lower()):
        t = el.get_text(" ", strip=True)
        if t and t not in blocks and len(t) > 50:  # Only include substantial text blocks
            blocks.append(t)

    # 7) absolute fallback: whole doc text
    if not blocks:
        t = parsed_html.get_text(" ", strip=True)
        if t:
            blocks.append(t)

    return " ".join(blocks)


def _extract_raw_data_from_html(parsed_html, product_id):
    """
    Extract raw data fields from DMsGuild HTML content.
    This function handles both legacy and new page formats.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        product_id: Product ID string
        
    Returns:
        Dictionary of raw extracted data with keys like module_name, authors, hours_raw, etc.
    """
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

    # Extract basic fields using helper functions
    raw_data["module_name"] = _extract_title_from_html(parsed_html)
    raw_data["authors"] = _extract_authors_from_html(parsed_html)
    raw_data["date_created"] = _extract_date_from_html(parsed_html)
    
    # Extract price from JSON-LD first (highest precedence)
    raw_data["price_raw"] = _extract_jsonld_price(parsed_html)
    
    # Get combined text for regex-based extraction
    combined_text = _collect_text_for_regexes(parsed_html)
    # Store description text for code extraction fallback
    raw_data["description_text"] = combined_text
    
    # Extract hours from text
    raw_data["hours_raw"] = _extract_hours_from_text(combined_text)
    
    # Extract game statistics (APL, tiers, level_range) from text
    game_stats = _extract_game_stats_from_text(combined_text)
    raw_data["apl_raw"] = game_stats["apl_raw"]
    raw_data["tiers_raw"] = game_stats["tiers_raw"]
    raw_data["level_range_raw"] = game_stats["level_range_raw"]
    
    # Extract price from HTML (fallback if JSON-LD didn't work)
    if raw_data["price_raw"] is None:
        raw_data["price_raw"] = _extract_price_from_html(parsed_html)
    
    # Extract PWYW information
    pwyw_info = _extract_pwyw_info_from_html(parsed_html)
    raw_data["pwyw_flag_raw"] = pwyw_info["pwyw_flag_raw"]
    raw_data["suggested_price_raw"] = pwyw_info["suggested_price_raw"]
    
    # Extract seed information
    raw_data["seed_raw"] = _extract_seed_from_text(combined_text)

    return raw_data


# ============================================================================
# NORMALIZATION FUNCTIONS
# ============================================================================

def _normalize_and_convert_data(raw_data):
    """
    Normalize and convert raw extracted data into processed format.
    
    Args:
        raw_data: Dictionary of raw extracted data from HTML
        
    Returns:
        Dictionary of normalized/processed data
    """
    # Normalize authors: strip whitespace and trailing commas
    authors = raw_data.get("authors", [])
    if authors:
        processed_authors = [author.strip().rstrip(',') for author in authors if author and author.strip()]
    else:
        processed_authors = []
    
    processed_data = {
        "module_name": raw_data["module_name"],
        "authors": processed_authors,
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
        "suggestedPrice": raw_data.get("suggested_price_raw"),
        # Seed field (only for POA, WBW, SJ campaigns)
        "seed": raw_data.get("seed_raw")
    }
    
    # If suggestedPrice is found but PWYW flag wasn't set, infer that it's PWYW
    # (suggestedPrice is a strong indicator of PWYW)
    if processed_data["suggestedPrice"] is not None and not processed_data["payWhatYouWant"]:
        processed_data["payWhatYouWant"] = True
    
    # For PWYW adventures, if price is None but suggestedPrice is set, use suggestedPrice as price
    # This ensures the price field has a value for filtering/searching while payWhatYouWant flag indicates it's PWYW
    if processed_data["payWhatYouWant"] and processed_data["price"] is None and processed_data["suggestedPrice"] is not None:
        processed_data["price"] = processed_data["suggestedPrice"]

    if processed_data["module_name"]:
        # Use get_adventure_code_and_campaigns for better pattern matching
        code_from_title, campaigns_from_title = get_adventure_code_and_campaigns(processed_data["module_name"])
        if code_from_title:
            # Normalize code to all uppercase
            processed_data["code"] = code_from_title.upper()
            processed_data["campaigns"] = campaigns_from_title
            processed_data["season"] = get_season(processed_data["code"])
    
    # Fallback: if code not found in title, search in description text
    if not processed_data["code"] and raw_data.get("description_text"):
        result = _extract_code_from_description(raw_data["description_text"])
        if result is not None:
            # Normalize code to all uppercase
            processed_data["code"] = result[0].upper()
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
    
    # Also set full_title to match module_name for compatibility
    processed_data["full_title"] = processed_data["module_name"]

    return processed_data


def _infer_missing_adventure_data(data):
    """
    Infer missing adventure data from available fields.
    Derives tier from APL or level range, level range from tier, and determines if it's an adventure.
    
    Args:
        data: Dictionary of processed adventure data (may be modified in place)
        
    Returns:
        Dictionary with inferred fields filled in
    """
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

    # Derive Level Range from Tier if Level Range is None, empty, or not a valid range
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

    # Set level_range if it's missing, empty, or invalid, and we have a derived value
    current_level_range = data.get("level_range")
    if derived_level_range is not None:
        if current_level_range is None or current_level_range == "" or not re.match(r"^\d+-\d+$", str(current_level_range).strip()):
            data["level_range"] = derived_level_range

    # Determine if it's an adventure
    # Check both module_name and full_title (for compatibility with different data structures)
    title_for_check = data.get("module_name") or data.get("full_title") or ""
    if not title_for_check:
        # If no title at all, can't determine if it's an adventure
        data["is_adventure"] = False
        return data
    
    lower_full_title = title_for_check.lower()
    is_bundle = 'bundle' in lower_full_title or 'compendium' in lower_full_title
    is_roll20 = 'roll20' in lower_full_title
    is_fg = 'fantasy grounds' in lower_full_title

    # It's an adventure if it has a code AND is not excluded by keywords
    code = data.get("code")
    # Debug: Check if code is truthy (not None, not empty string)
    if code and code.strip() if isinstance(code, str) else code:
        if not is_bundle and not is_roll20 and not is_fg:
            data["is_adventure"] = True
        else:
            data["is_adventure"] = False
    else:
        data["is_adventure"] = False
    
    # Flag for human review if title (module_name) couldn't be extracted
    # This indicates the title wasn't in the HTML and may need manual entry
    # (e.g., title might only be visible in thumbnail images)
    module_name = data.get("module_name")
    if not module_name or module_name.strip() == "":
        data["needs_review"] = True
        # Try to use code as a fallback title if available, but still flag for review
        if data.get("code"):
            data["module_name"] = data["code"]
            # Note: title will be derived from module_name by DungeonCraft.__get_short_title()
        else:
            # If we don't even have a code, use product_id as absolute fallback
            if data.get("product_id"):
                data["module_name"] = f"Product {data['product_id']}"

    return data


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

def get_season(code):
    """
    Get the season name for a given adventure code.
    
    Args:
        code: Adventure code string (e.g., "DDAL09-01", "WBW-DC-01")
        
    Returns:
        Season name string or None if not found
    """
    if not code:
        return None
    code_u = str(code).upper()
    # First: named seasons based on explicit prefixes (WBW-DC, SJ-DC, PS-DC, DC-POA)
    for prefix, season in SEASONS.items():
        if isinstance(prefix, str) and code_u.startswith(prefix):
            return season
    # Next: infer numeric season from DD Adventurers League code families and map to descriptive label
    # Examples: DDEX1-01, DDEX01-01, DDAL5-01, DDAL05-01
    m = re.match(r"^(DDEX|DDAL)0?(\d+)", code_u)
    if m:
        try:
            season_num = int(m.group(2))
            # Use SEASONS dict which now includes numeric seasons
            return SEASONS.get(season_num, season_num)
        except Exception:
            pass
    return None


def get_season_label(value):
    """
    Resolve a human-friendly label for a season value.
    - If value is an int and present in SEASON_LABELS, return that label.
    - If value is a string (named program), return as-is.
    - Otherwise, return None.
    
    Args:
        value: Season value (int or string)
        
    Returns:
        Human-friendly season label or None
    """
    if isinstance(value, int):
        return SEASON_LABELS.get(value)
    if isinstance(value, str):
        return value
    return None


def _extract_code_from_description(description_text):
    """
    Extract adventure code from description text when it's not found in the title.
    Searches for code patterns anywhere in the text (not just at the start).
    
    Args:
        description_text: Description text string from HTML
        
    Returns:
        Tuple of (code, campaigns_list) or None if no code found
    """
    if not description_text:
        return None
    
    # Normalize Unicode dash variants to standard hyphen-minus for regex matching
    # U+2010 HYPHEN, U+2011 NON-BREAKING HYPHEN, U+2012 FIGURE DASH, 
    # U+2013 EN DASH, U+2014 EM DASH, U+2015 HORIZONTAL BAR, U+2212 MINUS SIGN
    dash_variants = ['\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2212']
    normalized_text = description_text
    for dash_char in dash_variants:
        normalized_text = normalized_text.replace(dash_char, '-')
    
    # Use the same patterns from get_adventure_code_and_campaigns but search anywhere in text
    # Patterns for Adventurers League codes (DDAL, DDEX, DDHC, CCC, etc.)
    # All patterns are case-insensitive
    patterns = [
        # DC codes (e.g., FR-DC-STRAT-TALES-02, RV-DC-01, DC-PoA-ICE01-01)
        (r'\b(FR|DL|EB|PS|RV|SJ|WBW)-DC-([A-Z0-9-]+)-(\d{1,2})\b', lambda m: f"{m.group(1).upper()}-DC-{m.group(2).upper()}-{m.group(3)}"),
        # More general DC codes (e.g., RV-DC01)
        (r'\b(FR|DL|EB|PS|RV|SJ|WBW)-DC(\d{1,2})\b', lambda m: f"{m.group(1).upper()}-DC{m.group(2)}"),
        # DC-POA codes (e.g., DC-PoA-ICE01-01, DC-POA01, dc-poa-ice01-01) - normalize to all caps
        (r'\b(DC-[Pp][Oo][Aa])(\d{1,2}|-[A-Z0-9-]+-\d{1,2})\b', lambda m: 'DC-POA' + m.group(2).upper()),
        # Specific recognized prefixes (e.g., DDALELW00, DDALDRW01, SJA01)
        (r'\b(DDALELW\d{2}|DDALDRW\d{1,2}(?:-\d{1,2})?|SJA\d{1,2}(?:-\d{1,2})?)\b', lambda m: m.group(0).upper()),
        # DDHC hardcover tie-in codes (e.g., DDHC-TOA-10, DDHC-MORD-03, DDHC-LoX-Ch-1)
        # Pattern: DDHC- followed by 3-5 letter hardcover code, dash, then identifier (alphanumeric, may include dashes)
        (r'\b(DDHC-[A-Za-z]{3,5}-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\b', lambda m: m.group(0).upper()),
        # Standard DDAL/DDEX/DDHC (e.g., DDAL09-01, DDEX3-01, DDHC01)
        (r'\b(DDAL|DDEX|DDHC)\d{1,2}(?:-\d{1,2})?(?:-[A-Za-z0-9]+)?\b', lambda m: m.group(0).upper()),
        # DDIA codes (e.g., DDIA-MORD, DDIA-VOLO, DDIA-MORD-01, DDIA05) - hardcover tie-in adventures
        (r'\b(DDIA-[A-Za-z]+(?:-\d{1,2})?|DDIA\d{1,2})\b', lambda m: m.group(0).upper()),
        # CCCs with optional extra part (e.g., CCC-BMG-01, CCC-GSP-01-01)
        (r'\b(AL|CCC-)[A-Z]{2,3}-\d{1,2}(?:-\d{1,2})?(?:-[A-Za-z0-9]+)?\b', lambda m: m.group(0).upper()),
        # BMG codes (e.g., BMG-DRW-01, PO-BK-1-04) - may have additional dash-number sequence
        (r'\b(BMG-DRW|BMG-MOON|BMG-DL|PO-BK)-\d{1,2}(?:-\d{1,2})?\b', lambda m: m.group(0).upper()),
        # Ravenloft Module Hunt (e.g., RMH-01)
        (r'\b(RMH)-(\d{1,2})\b', lambda m: f"{m.group(1).upper()}-{m.group(2)}"),
        # Eberron Sharn Modules (e.g., EB-SM-01)
        (r'\b(EB-SM)-(\d{1,2})\b', lambda m: f"{m.group(1).upper()}-{m.group(2)}"),
    ]
    
    for pattern, code_builder in patterns:
        # Use normalized_text to handle Unicode dash variants
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if match:
            code = code_builder(match)
            # Normalize DDAL/DDEX codes to zero-pad single-digit season numbers
            code = normalize_ddal_ddex_code(code)
            campaigns = get_campaigns_from_code(code)
            return (code, campaigns)
    
    return None


def get_dc_code_and_campaign(product_title):
    """
    Extract adventure code and campaign from a product title.
    Case-insensitive matching.
    
    Args:
        product_title: Full product title string
        
    Returns:
        Tuple of (code, campaigns_list) or (product_title, None) if no code found
    """
    content = str(product_title).upper().split()
    for text in content:
        text = text.replace(',', '').replace(
            '(', '').replace(')', '').replace("'", '').replace(':', '-')
        text = text.strip()
        if text:
            # Special case: "BK-XX-XX" codes should be treated as "PO-BK" variants
            # This handles cases where the HTML doesn't include the "PO-" prefix
            # (e.g., "BK-05-02" should map to PO-BK campaign)
            if text.startswith('BK-') and re.match(r'^BK-\d+', text):
                campaign_val = DC_CAMPAIGNS.get('PO-BK')
                if campaign_val:
                    # Keep the original code format but recognize it as PO-BK campaign
                    return (text, [campaign_val] if not isinstance(campaign_val, list) else campaign_val)
            
            # Case-insensitive matching against DC_CAMPAIGNS keys
            text_upper = text.upper()
            for code_key in DC_CAMPAIGNS:
                if text_upper.startswith(code_key.upper()):
                    campaign_val = DC_CAMPAIGNS.get(code_key)
                    # Normalize code to all uppercase
                    return (text.upper(), [campaign_val] if not isinstance(campaign_val, list) else campaign_val)
            
            # Case-insensitive matching against DDAL_CAMPAIGN keys
            for code_key in DDAL_CAMPAIGN:
                if text_upper.startswith(code_key.upper()):
                    campaign_val = DDAL_CAMPAIGN.get(code_key)
                    return (text, [campaign_val] if not isinstance(campaign_val, list) else campaign_val)
    return (product_title, None)


def merge_adventure_data(existing_data, new_data, force_overwrite=False, careful_mode=False):
    """
    Merge new adventure data into existing data with configurable merge strategies.
    
    Args:
        existing_data: Dictionary of existing adventure data (may be None or empty)
        new_data: Dictionary of new adventure data to merge
        force_overwrite: If True, overwrite fields with new_data, but preserve existing fields
                         that are missing or null/empty in new_data (e.g., manually-added fields like 'seed')
        careful_mode: If True, preserve existing non-empty values; only fill in empty ones
        
    Returns:
        Merged dictionary of adventure data
    """
    merged_data = new_data.copy()  # Start with all keys from new_data

    if force_overwrite:
        # Even in force mode, preserve existing fields that are missing or empty in new_data
        # This prevents overwriting manually-added fields like 'seed' with null values
        if existing_data:
            for key, existing_value in existing_data.items():
                # Skip if this key is already in new_data with a non-empty value
                if key in new_data:
                    new_value = new_data[key]
                    is_new_value_empty = new_value is None or new_value == "" or new_value == [] or new_value == {}
                    if not is_new_value_empty:
                        continue  # Use the new non-empty value
                
                # Preserve existing value if:
                # 1. Key is missing from new_data, OR
                # 2. Key exists in new_data but is empty/null
                is_existing_value_empty = existing_value is None or existing_value == "" or existing_value == [] or existing_value == {}
                if not is_existing_value_empty:  # Only preserve non-empty existing values
                    merged_data[key] = existing_value
        return merged_data

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
                    # Always use new non-empty value (including boolean False which is a valid non-empty value)
                    merged_data[key] = new_value
                elif not is_existing_value_empty:  # If new is empty, but existing is not, keep existing
                    merged_data[key] = existing_value
    return merged_data


def extract_data_from_html(parsed_html, product_id, product_alt=None, existing_data=None, force_overwrite=False,
                           careful_mode=False):
    """
    Main entry point for extracting adventure data from HTML.
    Performs extraction, normalization, inference, and merging.
    
    Args:
        parsed_html: BeautifulSoup parsed HTML document
        product_id: Product ID string
        product_alt: Optional alternate product identifier (currently unused)
        existing_data: Optional existing adventure data to merge with
        force_overwrite: If True, completely overwrite existing data
        careful_mode: If True, preserve existing non-empty values
        
    Returns:
        Dictionary of merged adventure data
    """
    raw_data = _extract_raw_data_from_html(parsed_html, product_id)
    normalized_data = _normalize_and_convert_data(raw_data)
    new_data = _infer_missing_adventure_data(normalized_data)
    
    # Ensure is_adventure is set correctly after inference
    # Double-check: if we have a code and title doesn't contain exclusion keywords, it's an adventure
    if new_data.get("code") and (new_data.get("module_name") or new_data.get("full_title")):
        title_check = (new_data.get("module_name") or new_data.get("full_title") or "").lower()
        if not any(keyword in title_check for keyword in ['bundle', 'compendium', 'roll20', 'fantasy grounds']):
            new_data["is_adventure"] = True

    return merge_adventure_data(existing_data, new_data, force_overwrite, careful_mode)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    ## Extract data from a JSON if a JSON is specified on the command line and display
    pass
