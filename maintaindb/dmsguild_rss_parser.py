# Python
from __future__ import annotations

import argparse
import json
import re
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List, Optional, Tuple
import xml.etree.ElementTree as ET

import requests
from adventure import sanitize_filename

# Constants
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    )
}
PRODUCT_ID_RE = re.compile(r"/product/(\d+)/")

# Type aliases
ProductTuple = Tuple[Optional[str], str, List[str], str, str, str]


def _extract_product_id(product_url: str) -> Optional[str]:
    """Extract numeric product ID from a DMsGuild product URL."""
    match = PRODUCT_ID_RE.search(product_url or "")
    return match.group(1) if match else None


def _safe_findtext(parent: ET.Element, tag: str, default: str = "") -> str:
    """Safely get text content of a child tag or return default."""
    text = parent.findtext(tag)
    return text if text is not None else default


def parse_dmsguild_rss(url: str) -> List[ProductTuple]:
    """
    Fetch and parse a DMsGuild RSS feed URL or a local XML file path.

    If 'url' points to an existing local file (absolute or relative), the file is read
    from disk. Otherwise, it is treated as a remote URL and fetched with requests.

    Returns a list of tuples:
      (product_id, full_title, authors[], description_html, pub_date_str, product_url)
    Note: Authors are not provided by the RSS feed; an empty list is returned.
    """
    text: Optional[str] = None

    p = Path(url)
    if p.exists() and p.is_file():
        try:
            text = p.read_text(encoding="utf-8")
        except OSError as e:
            print(f"Error reading local file {url}: {e}")
            return []
    else:
        try:
            resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=20)
            resp.raise_for_status()
            text = resp.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return []

    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        print(f"Error parsing XML from {url}: {e}")
        return []

    products: List[ProductTuple] = []
    for item in root.findall(".//item"):
        full_title = _safe_findtext(item, "title")
        product_url = _safe_findtext(item, "link")
        description_html = _safe_findtext(item, "description")
        pub_date_str = _safe_findtext(item, "pubDate")

        product_id = _extract_product_id(product_url)
        authors: List[str] = []  # Authors are not available from RSS feed

        products.append(
            (product_id, full_title, authors, description_html, pub_date_str, product_url)
        )

    return products


def parse_pub_date(pub_date_str: str) -> Optional[str]:
    """
    Convert RSS pubDate to YYYYMMDD string.
    Returns None if parsing fails.
    """
    try:
        dt = parsedate_to_datetime(pub_date_str)
    except (TypeError, ValueError):
        return None
    if dt is None:
        return None
    # Normalize to naive date string
    return dt.date().strftime("%Y%m%d")


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-?", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite of existing JSON files.")
    parser.add_argument(
        "--url",
        type=str,
        default="https://www.dmsguild.com/rss.php?affiliate_id=171040&filters=45470_0_0_0_0_0_0_0_0",
        help="RSS feed URL to fetch, or a local path to an RSS XML file.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="_dc",
        help="The directory to save the JSON files to.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching products from {args.url}...")
    products = parse_dmsguild_rss(args.url)
    print(f"Found {len(products)} products.")

    # Restore legacy functionality: normalize data and write Adventure-shaped JSONs
    # without scraping product pages (RSS-only data).
    # Build DungeonCraft-style JSON objects using only RSS fields, aligning with HTML pipeline schema
    from adventure import get_dc_code_and_campaign, get_season, DungeonCraft

    def _parse_price_from_description(desc_html: str) -> Optional[float]:
        if not desc_html:
            return None
        # Try commented <price> tag first
        m = re.search(r"<!--\s*<price>([\d.]+)</price>\s*-->", desc_html, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                return None
        # Try inline "Price": $X.X in description thumb block
        m2 = re.search(r"Price(?:</b>)?\s*:\s*\$\s*([\d.]+)", desc_html, re.IGNORECASE)
        if m2:
            try:
                return float(m2.group(1))
            except ValueError:
                return None
        return None

    for product_id, full_title, _authors, description_html, pub_date_str, product_url in products:
        filename = sanitize_filename(full_title)
        file_path = output_dir / filename

        if file_path.exists() and not args.force:
            print(f"Skipping existing file (use --force to overwrite): {file_path.name}")
            continue

        date_created_str = parse_pub_date(pub_date_str)
        code = None
        campaigns = []
        season = None
        if full_title:
            cc = get_dc_code_and_campaign(full_title)
            if cc:
                code, campaigns = cc[0], cc[1]
                season = get_season(code)

        lower_title = (full_title or "").lower()
        is_bundle = "bundle" in lower_title or "compendium" in lower_title
        is_roll20 = "roll20" in lower_title
        is_fg = "fantasy grounds" in lower_title
        is_adventure_flag = bool(code) and not (is_bundle or is_roll20 or is_fg)

        price_value = _parse_price_from_description(description_html)

        dc_obj = DungeonCraft(
            product_id=product_id,
            title=full_title,
            authors=[],
            code=code,
            date_created=date_created_str,
            hours=None,
            tiers=None,
            apl=None,
            level_range=None,
            url=product_url,
            campaigns=campaigns,
            season=season,
            is_adventure=is_adventure_flag,
            price=price_value,
        )

        data = dc_obj.to_json()
        # Mark RSS-created entries for human review, since RSS lacks full fields
        data["needs_review"] = True

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"Wrote: {file_path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
