import re
import unicodedata
from word2number import w2n

def str_to_int(s):
    """Converts a string (either a digit or a word) to an integer."""
    if not s or not isinstance(s, str):
        return None
    s = s.strip().lower()
    try:
        # First, try to convert as a regular integer
        return int(s)
    except (ValueError, TypeError):
        try:
            # If that fails, try as a number word
            return w2n.word_to_num(s)
        except ValueError:
            return None

def get_patt_first_matching_group(patt, text):
    """Finds the first match for a regex pattern and returns the first captured group."""
    match = re.search(patt, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def sanitize_filename(filename):
    """Sanitizes a string to be a valid filename, ending in .json."""
    # Normalize unicode characters to their closest ASCII representation
    normalized_name = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    
    # Check for existing extension and separate it from the base name
    base_name = normalized_name
    extension = ".json" # We always want a .json extension
    if normalized_name.lower().endswith('.json'):
        base_name = normalized_name[:-5]
    else:
        # If another extension exists, remove it
        parts = normalized_name.rsplit('.', 1)
        if len(parts) > 1:
            base_name = parts[0]

    # Replace any remaining periods in the base name with dashes
    base_name = base_name.replace('.', '-')
    
    # Remove any character that is not a letter, number, underscore, or dash
    base_name = re.sub(r'[^\w\s-]', '', base_name).strip()
    # Replace sequences of whitespace with a single dash
    base_name = re.sub(r'\s+', '-', base_name)
    
    return f"{base_name}{extension}"


def _extract_hours(text):
    """Extracts adventure duration (hours) from text content."""
    # Normalize text to simplify regex: use spaces, handle "-hour" and "-to-"
    processed_text = text.lower().replace('-hour', ' hour').replace('-to-', ' to ')

    # Pattern 1: Look for a range, e.g., "2-4 hour" or "two to four hour"
    patt_range = re.compile(r"\b([a-z0-9]+)\b\s*(?:-|to)\s*\b([a-z0-9]+)\b(?=\s+hour)")
    match = patt_range.search(processed_text)
    if match:
        start_str, end_str = match.groups()
        start_num = str_to_int(start_str)
        end_num = str_to_int(end_str)
        if start_num is not None and end_num is not None:
            return f"{start_num}-{end_num}"  # Ensure range is returned as a string

    # If range pattern matched, but parsing failed, OR no range pattern match
    # Pattern 2: Look for a single value, e.g., "2 hour" or "four hour"
    patt_single = re.compile(r"\b([a-z0-9]+)(?=\s+hour)")
    match = patt_single.search(processed_text)
    if match:
        hour_str = match.group(1)
        hour_num = str_to_int(hour_str)
        if hour_num is not None:
            return hour_num

    return None   # Return None if no hour information is found


def extract_data_from_html(parsed_html, product_id, existing_data):
    """Extracts adventure data from parsed HTML content."""
    data = existing_data.copy()
    data['product_id'] = product_id
    prod_content_div = parsed_html.find('div', class_='prod-content')
    if prod_content_div:
        text = prod_content_div.get_text(separator=' ', strip=True)
        hours = _extract_hours(text)
        if hours is not None:
            data['hours'] = hours
    return data