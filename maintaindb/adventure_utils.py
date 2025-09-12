# adventure_utils.py
import re
import unicodedata
import os
import datetime
from word2number import w2n
from typing import List, Optional, Tuple, Any

# --- Campaign Dictionaries ---
# Season labels (named programs + numeric seasons 1-10)
SEASONS = {
    'WBW-DC': "The Wild Beyond the Witchlight",
    'SJ-DC': "Spelljammer",
    'PS-DC': "Planescape",
    'DC-POA': "Icewind Dale",
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
DC_CAMPAIGNS = {
    'DL-DC': 'Dragonlance',
    'EB-DC': 'Eberron',
    'EB-SM': 'Eberron', # Eberron Sharn Modules
    'FR-DC': 'Forgotten Realms',
    'PS-DC': 'Forgotten Realms', # Changed from Planescape
    'SJ-DC': 'Forgotten Realms', # Changed from Spelljammer
    'WBW-DC': 'Forgotten Realms', # Changed from The Wild Beyond the Witchlight
    'DC-POA': 'Forgotten Realms', # Changed from Icewind Dale: Rime of the Frostmaiden
    'PO-BK': 'Forgotten Realms',
    'BMG-DRW': 'Forgotten Realms',
    'BMG-DL': 'Dragonlance',
    'BMG-MOON': 'Forgotten Realms',
    'CCC-': 'Forgotten Realms',
    'RV-DC': 'Ravenloft',
}

DDAL_CAMPAIGN = {
    'RMH':    ['Ravenloft'], # Ravenloft Mist Hunters
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
    'DDAL8':  ['Forgotten Realms'], # Covers Baldur's Gate AL content (Season 8)
    'DDAL08': ['Forgotten Realms'], # Covers Baldur's Gate AL content (Season 8)
    'DDAL9':  ['Forgotten Realms'],
    'DDAL09': ['Forgotten Realms'],
    'DDAL10': ['Forgotten Realms'],
    'DDAL11': ['Forgotten Realms'],
    'DDALEL': ['Eberron'], # Confirmed: Era of the Last War
    'DDALDRW': ['Forgotten Realms'], # Corrected: Dreams of the Red Wizards is Forgotten Realms
    'SJA':    ['Spelljammer'], # Confirmed: Spelljammer Adventures (4 modules)
}


# --- Utility Functions ---
def sanitize_filename(filename: str) -> str:
    """Sanitizes a string to be a valid filename."""
    # Replace invalid characters with an underscore
    s = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces or dots
    s = s.strip()
    s = s.strip('.')
    # Truncate to a reasonable length if needed (e.g., 200 characters)
    return s[:200]

def get_patt_first_matching_group(pattern: str, text: Optional[str]) -> Optional[str]:
    """
    Returns the first matching group for a regex pattern in text.
    If no group, returns the full match.
    """
    if not text:
        return None
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        if match.groups():
            return match.group(1).strip()
        else:
            return match.group(0).strip()
    return None

def parse_number_string_to_int(s: Any) -> Optional[int]:
    """
    Parses a string that might contain numbers or number words into an integer.
    Handles 'half', 'one', 'two', etc., and numeric strings.
    """
    if s is None:
        return None
    if isinstance(s, (int, float)): # Already a number
        return int(s)
    if not isinstance(s, str): # Not a string, not a number, can't parse
        return None

    s = s.strip().lower()

    # Handle fractions (e.g., "1/2") or "half"
    if '1/2' in s or 'half' in s:
        return 1 # Or 0 depending on how you want to handle half levels/hours

    # Try converting number words (one, two, etc.)
    try:
        return w2n.word_to_num(s)
    except ValueError:
        pass # Not a number word, continue to next check

    # Extract first sequence of digits
    match = re.search(r'\d+', s)
    if match:
        try:
            return int(match.group(0))
        except ValueError:
            pass # Should not happen if regex matched digits

    return None

def parse_date_string(date_str: Optional[str]) -> Optional[datetime.date]:
    """Parses a date string into a datetime.date object (e.g., 'July 17, 2025')."""
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str, '%B %d, %Y').date()
    except ValueError:
        try:
            return datetime.datetime.strptime(date_str, '%b %d, %Y').date()
        except ValueError:
            return None

def parse_rss_date_string(date_str: Optional[str]) -> Optional[datetime.date]:
    """Parses an RSS date string (e.g., 'Wed, 21 Jun 2023 12:00:00 GMT' or 'Thu, 17 Jul 2025 04:12:40 CDT') into a datetime.date object."""
    if not date_str:
        return None
    try:
        # Attempt to strip the timezone abbreviation if present, as %Z can be finicky.
        # This regex looks for ' day_of_week, day month year hh:mm:ss ' followed by anything,
        # and captures just the date and time part.
        date_time_part_match = re.match(r'^(.*? \d{2}:\d{2}:\d{2})', date_str)
        if date_time_part_match:
            date_time_str = date_time_part_match.group(1)
            dt_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S')
            return dt_obj.date()
        else:
            return None # Could not extract the date-time part
    except ValueError:
        return None # Parsing failed due to format mismatch


def get_campaigns_from_code(code: str) -> List[str]:
    campaigns = []
    if not code:
        return []

    # Check against DDAL_CAMPAIGN first
    for prefix, campaign_list in DDAL_CAMPAIGN.items():
        # Handle prefixes like DDAL4/DDAL04, DDEX1/DDEX01
        if prefix.endswith('0') and code.startswith(prefix[:-1]) and code[len(prefix[:-1])].isdigit():
             campaigns.extend(campaign_list)
             break
        # Handle exact code matches (e.g., DDALEL, DDALBG) or direct prefixes (DDAL9)
        elif code.startswith(prefix):
            campaigns.extend(campaign_list)
            break # Assuming one primary DDAL campaign per code prefix

    # If no DDAL campaign found, check against DC_CAMPAIGNS
    if not campaigns:
        for prefix, campaign_name in DC_CAMPAIGNS.items():
            if code.startswith(prefix):
                campaigns.append(campaign_name)
                break # Assuming one primary DC campaign per code prefix
    
    # Remove duplicates and return
    return sorted(list(set(campaigns)))


def get_season(code: Optional[str]):
    """
    Return a descriptive season label for a given code.
    - For codes starting with WBW-DC, SJ-DC, PS-DC, DC-POA return the program name.
    - For DDEXn/DDALn (optionally zero-padded), map known numeric seasons (1-10) to human-friendly names;
      if an unknown number is encountered, return the number to avoid data loss.
    """
    if not code:
        return None
    code_u = str(code).upper()
    # Named programs
    for prefix, season in SEASONS.items():
        if isinstance(prefix, str) and code_u.startswith(prefix):
            return season
    # Numeric AL seasons
    m = re.match(r"^(DDEX|DDAL)0?(\d+)", code_u)
    if m:
        try:
            season_num = int(m.group(2))
            # Prefer descriptive label when known
            return SEASONS.get(season_num, season_num)
        except Exception:
            pass
    return None


def get_adventure_code_and_campaigns(full_title: Optional[str]) -> Tuple[Optional[str], List[str]]:
    code = None
    campaigns = []
    
    if not full_title:
        return None, []

    # Patterns for Adventurers League codes (DDAL, DDEX, DDHC, CCC, etc.)
    # Ordered roughly by specificity or commonality
    patterns = [
        # DC codes (e.g., FR-DC-STRAT-TALES-02, RV-DC-01) - flexible for series name
        r"^(FR|DL|EB|PS|RV|SJ|WBW)-DC-([A-Z0-9-]+)-(\d{1,2})", 
        # More general DC codes (e.g., RV-DC01)
        r"^(FR|DL|EB|PS|RV|SJ|WBW)-DC(\d{1,2})", 
        # Specific recognized prefixes (e.g., DDALELW00, DDALDRW01, SJA01)
        r"^(DDALELW\d{2}|DDALDRW\d{1,2}(?:-\d{1,2})?|SJA\d{1,2}(?:-\d{1,2})?)",
        # Standard DDAL/DDEX/DDHC (e.g., DDAL09-01, DDEX3-01)
        r"^(DDAL|DDEX|DDHC)\d{1,2}(?:-\d{1,2})?(?:-[A-Za-z0-9]+)?", 
        # CCCs with optional extra part (e.g., CCC-BMG-01, CCC-GSP-01-01)
        r"^(AL|CCC-)[A-Z]{2,3}-\d{1,2}(?:-\d{1,2})?(?:-[A-Za-z0-9]+)?", 
        # BMG codes (e.g., BMG-DRW-01)
        r"^(BMG-DRW|BMG-MOON|BMG-DL|PO-BK)-\d{1,2}", 
        # Specific DC codes (e.g., DC-POA01)
        r"^(DC-POA)\d{1,2}", 
        # Ravenloft Module Hunt (e.g., RMH-01)
        r"^(RMH)-(\d{1,2})", 
        # Eberron Sharn Modules (e.g., EB-SM-01)
        r"^(EB-SM)-(\d{1,2})", 
    ]

    for patt in patterns:
        # Match from the beginning of the string
        match = re.match(patt, full_title, re.IGNORECASE)
        if match:
            # Reconstruct code based on pattern type and matched groups
            matched_text = match.group(0).upper().strip()

            if "-DC-" in matched_text: # e.g., FR-DC-STRAT-TALES-02
                if len(match.groups()) >= 3:
                    code = f"{match.group(1).upper()}-DC-{match.group(2).upper()}-{match.group(3)}"
                else: # Fallback for simpler DC codes like RV-DC01
                    code = matched_text.split(' ')[0]
            elif matched_text.startswith(('DDALELW', 'DDALDRW', 'SJA', 'RMH', 'EB-SM', 'DC-POA', 'BMG')):
                # These are already captured well as full prefixes
                code = matched_text.split(' ')[0]
            else: # For other standard AL codes (DDAL, DDEX, DDHC, CCC etc.)
                code = matched_text.split(' ')[0]
            break

    if code:
        campaigns = get_campaigns_from_code(code)

    return code, campaigns