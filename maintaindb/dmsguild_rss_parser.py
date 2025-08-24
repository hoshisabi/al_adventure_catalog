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
PRODUCT_ID_RE = re.compile(r"/product/(\d+)//")

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
    Fetch and parse a DMsGuild RSS feed URL.

    Returns a list of tuples:
      (product_id, full_title, authors[], description_html, pub_date_str, product_url)
    Note: Authors are not provided by the RSS feed; an empty list is returned.
    """
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    try:
        root = ET.fromstring(resp.text)
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
        help="The full RSS feed URL to parse.",
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
    try:
        from adventure_model import Adventure
        from adventure_normalizers import AdventureDataNormalizer
    except ImportError as e:
        print(f"Required modules missing for normalization: {e}")
        # Fallback to the minimal RSS write if normalization modules are unavailable
        for product_id, full_title, _authors, description_html, pub_date_str, product_url in products:
            filename = sanitize_filename(full_title)  # returns a safe .json filename
            file_path = output_dir / filename

            if file_path.exists() and not args.force:
                print(f"Skipping existing file (use --force to overwrite): {file_path.name}")
                continue

            date_created_str = parse_pub_date(pub_date_str)

            data = {
                "id": product_id,
                "title": full_title,
                "url": product_url,
                "pub_date": pub_date_str,
                "date_created": date_created_str,
                "description_html": description_html,
            }

            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Wrote: {file_path.name}")
        return 0

    normalizer = AdventureDataNormalizer()

    for product_id, full_title, _authors, description_html, pub_date_str, product_url in products:
        # Construct "extracted_data" using only RSS fields.
        extracted_data = {
            "product_id": product_id,
            "full_title_raw": full_title,
            "url_raw": product_url,
            "date_created_raw": pub_date_str,  # Normalizer will parse pubDate
            "authors_raw": [],                 # Not in RSS
            "price_raw": None,                 # Not in RSS
            "page_count_raw": None,            # Not in RSS
            "apl_raw": None,                   # Not in RSS
            "tiers_raw": None,                 # Not in RSS
            "level_range_raw": None,           # Not in RSS
            "hours_raw": [],                   # Not in RSS
            "description_html_raw": description_html,  # Keep RSS snippet
        }

        normalized = normalizer.normalize(extracted_data)

        # Heuristic: mark as adventure if a code is parsed; RSS data is incomplete otherwise.
        is_adventure_flag = True if normalized.get("code") else False

        # Build Adventure object payload
        adventure_payload = {k: v for k, v in normalized.items() if hasattr(type("A", (), {}), k)}
        # Since hasattr trick above isn't reliable for dataclasses, pick known fields via Adventure
        try:
            model_fields = set(getattr(Adventure, "__dataclass_fields__", {}).keys())
            adventure_payload = {k: v for k, v in normalized.items() if k in model_fields}
        except Exception:
            pass

        adventure_payload["is_adventure"] = is_adventure_flag
        adventure_payload["needs_review"] = True  # RSS-only entries should be reviewed

        adventure = Adventure(**adventure_payload)
        data_to_save = adventure.to_json()

        # Prefer full_title/title/product_id for filename
        filename_base = adventure.full_title or adventure.title or (product_id or "unknown")
        file_path = output_dir / sanitize_filename(filename_base)

        should_write = True
        if file_path.exists() and not args.force:
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    existing = json.load(f)
                # Only skip if identical
                if json.dumps(existing, sort_keys=True, default=str) == json.dumps(data_to_save, sort_keys=True, default=str):
                    print(f"(CACHED) Left alone {file_path.name}")
                    should_write = False
                else:
                    print(f"(CHANGED) Will overwrite {file_path.name} (use --force to suppress check).")
            except json.JSONDecodeError:
                print(f"Existing JSON invalid, will overwrite: {file_path.name}")

        if should_write:
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4, sort_keys=True)
            print(f"Saved {file_path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
