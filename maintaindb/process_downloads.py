import argparse
import datetime
import glob
import json
import logging
import os
import shutil
import sys

from pathlib import Path
from bs4 import BeautifulSoup

from .adventure import DungeonCraft, extract_data_from_html, merge_adventure_data
from .adventure_utils import product_id_from_dmsguild_html_filename
from .paths import DMSGUILDINFO_DIR, DC_DIR, DMSGUILDINFO_PROCESSED_DIR

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

# Use centralized path configuration
input_html_path = str(DMSGUILDINFO_DIR)
output_json_path = str(DC_DIR)
processed_html_path = str(DMSGUILDINFO_PROCESSED_DIR)


def _collect_html_files(from_processed=False, days=None):
    search_dir = processed_html_path if from_processed else input_html_path
    html_files = glob.glob(os.path.join(search_dir, 'dmsguildinfo-*.html'))
    if days is not None:
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        html_files = [
            path for path in html_files
            if datetime.datetime.fromtimestamp(os.path.getmtime(path)) >= cutoff
        ]
    return sorted(html_files)


def _process_html_file(file_path, args, move_when_done=True):
    # Get the modification time of the HTML file
    file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    file_name = os.path.basename(file_path)
    raw_stem = file_name.replace('dmsguildinfo-', '').replace('.html', '')
    product_id = product_id_from_dmsguild_html_filename(file_name)
    if product_id != raw_stem:
        logger.warning(
            "Browser duplicate filename %s; using product_id %s",
            file_name,
            product_id,
        )

    # Create a dummy URL for the DungeonCraft object, as it expects one
    dummy_url = f"https://www.dmsguild.com/product/{product_id}/?affiliate_id=171040"

    parsed_html = BeautifulSoup(html_content, features="html.parser")
    # Load existing JSON data if it exists to pass to extract_data_from_html
    existing_json_data_for_extraction = {}
    # Use product_id for filename (stable, reliable, no special characters)
    json_filename_for_extraction = f"{product_id}.json"
    output_file_path_for_extraction = os.path.join(output_json_path, json_filename_for_extraction)
    if os.path.exists(output_file_path_for_extraction):
        with open(output_file_path_for_extraction, 'r', encoding='utf-8') as f:
            existing_json_data_for_extraction = json.load(f)

    data = extract_data_from_html(parsed_html, product_id, product_alt=None,
                                  existing_data=existing_json_data_for_extraction, force_overwrite=args.force,
                                  careful_mode=args.careful)

    # Construct the DungeonCraft object
    dc_hours = str(data.get("hours")) if data.get("hours") is not None else None
    dc = DungeonCraft(product_id, data["full_title"], data["authors"], data["code"], data["date_created"],
                      dc_hours, data["tiers"], data["apl"], data["level_range"], dummy_url, data["campaigns"],
                      data.get("season"), data["is_adventure"], data["price"],
                      data.get("payWhatYouWant"), data.get("suggestedPrice"), data.get("needs_review"),
                      data.get("seed"), last_update=file_mtime, ai_content=data.get("ai_content"))

    # Determine output JSON filename based on product_id
    # Product IDs are stable, reliable, and contain no special characters
    json_filename = f"{product_id}.json"
    output_file_path = os.path.join(output_json_path, json_filename)

    # Load existing JSON data if it exists
    existing_json_data = {}
    output_exists = os.path.exists(output_file_path)
    if output_exists:
        with open(output_file_path, 'r', encoding='utf-8') as f:
            existing_json_data = json.load(f)

    # Merge new data with existing data
    merged_json_data = dc.to_json()

    # Check if any values were changed or if it's a new file
    is_new_or_changed = not output_exists
    if not is_new_or_changed:
        for key, new_value in merged_json_data.items():
            if key not in existing_json_data:
                # New field added
                is_new_or_changed = True
                break

            old_value = existing_json_data[key]
            if old_value != new_value:
                # Field value changed
                is_new_or_changed = True
                break

    # Perform the merge using the new function
    final_data = merge_adventure_data(existing_json_data, merged_json_data, args.force, args.careful)

    with open(output_file_path, 'w') as f:
        json.dump(final_data, f, indent=4, sort_keys=True)
    logger.info(f"Successfully processed {file_name} and saved to {output_file_path}")

    if product_id != raw_stem and os.path.basename(file_path) == file_name:
        canonical_html = os.path.join(os.path.dirname(file_path), f"dmsguildinfo-{product_id}.html")
        if os.path.exists(canonical_html):
            os.remove(file_path)
            logger.info(f"Removed duplicate download HTML {file_name}")

    # Move processed HTML file only if force is true or if data was actually new or changed
    if move_when_done and (args.force or is_new_or_changed):
        shutil.move(file_path, os.path.join(processed_html_path, file_name))
        logger.info(f"Moved {file_name} to {processed_html_path}")
    elif move_when_done:
        logger.info(f"No new data or overwrite forced for {file_name}, keeping HTML in source directory.")


def process_downloads():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-?", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force overwrite of existing JSON files and move HTML files.")
    parser.add_argument("--careful", action="store_true",
                        help="Do not overwrite existing non-null data in JSON files; only fill in nulls.")
    parser.add_argument("--from-processed", action="store_true",
                        help="Re-process HTML files already in dmsguildinfo/processed/ (no file moves).")
    parser.add_argument("--days", type=int, default=None,
                        help="Only process HTML files modified within the last N days.")
    args = parser.parse_args()

    os.makedirs(processed_html_path, exist_ok=True)

    html_files = _collect_html_files(from_processed=args.from_processed, days=args.days)
    if not html_files:
        logger.info("No HTML files to process.")
        return

    logger.info(f"Processing {len(html_files)} HTML files...")

    for file_path in html_files:
        try:
            _process_html_file(file_path, args, move_when_done=not args.from_processed)
        except Exception as ex:
            logger.error(f"Error processing {file_path}: {str(ex)}")


if __name__ == '__main__':
    process_downloads()
