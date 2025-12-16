import argparse
import glob
import json
import logging
import os
import shutil
import sys

import pathlib
from bs4 import BeautifulSoup

from adventure import DungeonCraft, sanitize_filename, extract_data_from_html, merge_adventure_data

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_html_path = os.path.join(root, 'dmsguildinfo')
output_json_path = os.path.join(root, '_dc')
processed_html_path = os.path.join(input_html_path, 'processed')


def process_downloads():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-?", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force overwrite of existing JSON files and move HTML files.")
    parser.add_argument("--careful", action="store_true",
                        help="Do not overwrite existing non-null data in JSON files; only fill in nulls.")
    args = parser.parse_args()

    os.makedirs(processed_html_path, exist_ok=True)

    html_files = glob.glob(os.path.join(input_html_path, 'dmsguildinfo-*.html'))
    if not html_files:
        logger.info("No new HTML files to process.")
        return

    logger.info(f"Processing {len(html_files)} HTML files...")

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            file_name = os.path.basename(file_path)
            product_id = file_name.replace('dmsguildinfo-', '').replace('.html', '')

            # Create a dummy URL for the DungeonCraft object, as it expects one
            dummy_url = f"https://www.dmsguild.com/product/{product_id}/?affiliate_id=171040"

            parsed_html = BeautifulSoup(html_content, features="html.parser")
            # Load existing JSON data if it exists to pass to extract_data_from_html
            existing_json_data_for_extraction = {}
            json_filename_for_extraction = sanitize_filename(
                product_id) + ".json"  # Use product_id for initial filename guess
            output_file_path_for_extraction = os.path.join(output_json_path, json_filename_for_extraction)
            if os.path.exists(output_file_path_for_extraction):
                with open(output_file_path_for_extraction, 'r', encoding='utf-8') as f:
                    existing_json_data_for_extraction = json.load(f)

            data = extract_data_from_html(parsed_html, product_id, product_alt=None,
                                          existing_data=existing_json_data_for_extraction, force_overwrite=args.force,
                                          careful_mode=args.careful)

            # Construct the DungeonCraft object
            dc_hours = str(data.get("hours")) if data.get("hours") is not None else None
            dc = DungeonCraft(product_id, data["module_name"], data["authors"], data["code"], data["date_created"],
                              dc_hours, data["tiers"], data["apl"], data["level_range"], dummy_url, data["campaigns"],
                              data.get("season"), data["is_adventure"], data["price"],
                              data.get("payWhatYouWant"), data.get("suggestedPrice"))

            # Determine output JSON filename based on full_title
            # Sanitize full_title to create a valid filename
            json_filename = sanitize_filename(dc.full_title)
            output_file_path = os.path.join(output_json_path, json_filename)

            # Load existing JSON data if it exists
            existing_json_data = {}
            if os.path.exists(output_file_path):
                with open(output_file_path, 'r', encoding='utf-8') as f:
                    existing_json_data = json.load(f)

            # Merge new data with existing data
            merged_json_data = dc.to_json()

            # Check if any values would be overwritten (excluding nulls/empty values)
            did_overwrite = False
            for key, new_value in merged_json_data.items():
                if key in existing_json_data and existing_json_data[key] is not None and existing_json_data[
                    key] != "" and existing_json_data[key] != [] and existing_json_data[key] != {} and \
                        existing_json_data[key] != new_value:
                    did_overwrite = True
                    break

            # Perform the merge using the new function
            final_data = merge_adventure_data(existing_json_data, merged_json_data, args.force, args.careful)

            with open(output_file_path, 'w') as f:
                json.dump(final_data, f, indent=4, sort_keys=True)
            logger.info(f"Successfully processed {file_name} and saved to {output_file_path}")

            # Move processed HTML file only if force is true or if data was actually overwritten/new
            if args.force or did_overwrite:
                shutil.move(file_path, os.path.join(processed_html_path, file_name))
                logger.info(f"Moved {file_name} to {processed_html_path}")
            else:
                logger.info(f"No new data or overwrite forced for {file_name}, keeping HTML in source directory.")

        except Exception as ex:
            logger.error(f"Error processing {file_path}: {str(ex)}")


if __name__ == '__main__':
    process_downloads()
