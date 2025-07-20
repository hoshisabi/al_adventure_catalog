# process_downloads_new.py
import os
import glob
import json
import shutil
import pathlib
import logging
import sys
import argparse
import re # Make sure re is imported

from bs4 import BeautifulSoup

# NEW IMPORTS
from adventure_model import Adventure
from adventure_extractors import AdventureHTMLExtractor
from adventure_normalizers import AdventureDataNormalizer
from adventure_utils import sanitize_filename # For consistent filename generation

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_html_path = os.path.join(root, 'dmsguildinfo')
output_json_path = os.path.join(root, '_dc')
processed_html_path = os.path.join(input_html_path, 'processed')

# --- MERGE FUNCTION (adapted for Adventure object) ---
# This function will handle merging new data into existing data,
# defaulting to careful behavior unless force_overwrite is True.
def merge_adventure_data(existing_data: Dict[str, Any], new_data: Dict[str, Any], force_overwrite: bool = False) -> Dict[str, Any]:
    """
    Merges new data (dictionary representation of Adventure) into existing data.
    By default, it performs a 'careful' merge, only filling in None/empty values
    or appending to lists without duplicates.
    If force_overwrite is True, new_data completely replaces existing_data.
    Handles 'needs_review' flag specifically.
    """
    if force_overwrite:
        return new_data

    # If no existing data, just return the new data
    if not existing_data:
        return new_data

    merged_data = existing_data.copy()

    # Special handling for 'needs_review' flag
    existing_needs_review = existing_data.get('needs_review', False)
    new_needs_review = new_data.get('needs_review', False)

    if existing_needs_review is False and new_needs_review is True:
        # Human reviewed it and marked it clear, so don't revert to needing review automatically.
        # This assumes human decision overrides automated flagging.
        merged_data['needs_review'] = False
    elif existing_needs_review is True and new_needs_review is False:
        # It currently needs review, but the new data (automation) cleared it. Accept the clear.
        merged_data['needs_review'] = False
    else:
        # Otherwise, take new_needs_review (both True, both False, or one missing from old/new)
        merged_data['needs_review'] = new_needs_review


    # Iterate through new_data to merge
    for key, new_value in new_data.items():
        if key == 'needs_review': # Already handled above
            continue

        existing_value = merged_data.get(key) # Get from merged_data, as it might have been updated from existing

        # Determine if existing value is considered "empty" (None, empty string, empty list, empty dict)
        is_existing_empty = (
            existing_value is None or
            (isinstance(existing_value, str) and existing_value == "") or
            (isinstance(existing_value, list) and not existing_value) or
            (isinstance(existing_value, dict) and not existing_value)
        )
        # Determine if new value is considered "meaningful" (not None, not empty)
        is_new_meaningful = (
            new_value is not None and
            not (isinstance(new_value, str) and new_value == "") and
            not (isinstance(new_value, list) and not new_value) and
            not (isinstance(new_value, dict) and not new_value)
        )

        if is_existing_empty and is_new_meaningful:
            # If existing is empty, but new has meaningful data, use new data
            merged_data[key] = new_value
        elif isinstance(existing_value, list) and isinstance(new_value, list):
            # For lists, append new items if not already present.
            # Convert to set for unique items, then back to sorted list for consistency.
            # Convert to str for comparison in set, if elements might be mixed types (e.g., int/str numbers)
            combined_list_set = set(str(item) for item in existing_value)
            combined_list_set.update(str(item) for item in new_value)
            
            # Reconstruct list from set, attempting to preserve original type or common type (str)
            reconstructed_list = sorted(list(combined_list_set))

            merged_data[key] = reconstructed_list
        elif isinstance(existing_value, dict) and isinstance(new_value, dict):
            # For dictionaries, recursively merge them
            merged_data[key] = merge_adventure_data(existing_value, new_value) # No force for sub-dicts
        # Else: If existing_value is not empty/null and not a list/dict, and new_value is different,
        # we keep the existing value (careful behavior). This happens implicitly because we start with existing_data.copy().
        # If new_value is empty, but existing_value is not, existing_value is kept.
    return merged_data


def process_downloads():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-?", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite of existing JSON files (ignores careful merge rules).")
    args = parser.parse_args()

    os.makedirs(processed_html_path, exist_ok=True)

    html_files = glob.glob(os.path.join(input_html_path, 'dmsguildinfo-*.html'))
    if not html_files:
        logger.info("No new HTML files to process.")
        return

    logger.info(f"Processing {len(html_files)} HTML files...")

    html_extractor = AdventureHTMLExtractor()
    data_normalizer = AdventureDataNormalizer()
    # Inferer will be integrated here later

    for file_path in html_files:
        file_name = os.path.basename(file_path)
        product_id_match = re.search(r'dmsguildinfo-(\d+)\.html', file_name)
        if not product_id_match:
            logger.warning(f"Could not extract product ID from filename: {file_name}. Skipping.")
            continue

        product_id = product_id_match.group(1)
        # Use product_id for the initial output file name, before sanitizing by title
        initial_output_file_name = f"{product_id}.json"
        initial_output_file_path = os.path.join(output_json_path, initial_output_file_name)


        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')

            # --- Refactored Pipeline ---
            raw_data = html_extractor.extract(soup)
            raw_data["product_id"] = product_id # Add product_id to raw_data
            raw_data["url_raw"] = f"https://www.dmsguild.com/product/{product_id}/" # Add URL to raw_data

            normalized_data = data_normalizer.normalize(raw_data)

            # --- Determine 'needs_review' flag for the new data ---
            # This logic will eventually move to the AdventureDataInferer,
            # which will make more sophisticated decisions.
            new_needs_review_flag = False
            # Flag for review if essential fields are missing/empty after normalization
            if not normalized_data.get("title") or \
               not normalized_data.get("authors") or \
               not normalized_data.get("hours") or \
               not normalized_data.get("tiers") or \
               not normalized_data.get("level_ranges") or \
               not normalized_data.get("price"):
                new_needs_review_flag = True

            # Create a dictionary representing the new Adventure data
            # This simulates the output of an Inferer stage (if it existed)
            new_adventure_data_dict = {
                k: v for k, v in normalized_data.items() if k in Adventure.__dataclass_fields__
            }
            new_adventure_data_dict['needs_review'] = new_needs_review_flag

            # Convert to Adventure object to leverage its to_json for clean output structure
            # This ensures only defined fields are present and types are handled (e.g., Decimal to str)
            new_adventure_obj = Adventure(**new_adventure_data_dict)
            new_data_to_merge_json = new_adventure_obj.to_json()

            # Determine the final output filename based on the (normalized) full_title
            # This may change the filename from the product_id one
            final_json_filename = sanitize_filename(new_adventure_obj.full_title or new_adventure_obj.title or product_id)
            final_output_file_path = os.path.join(output_json_path, final_json_filename)

            existing_json_data = {}
            # Try to load existing data from *either* product_id.json or sanitized_title.json
            if os.path.exists(initial_output_file_path):
                with open(initial_output_file_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_json_data = json.load(f)
                    except json.JSONDecodeError:
                        logger.error(f"Error decoding JSON from {initial_output_file_path}. Treating as empty.", exc_info=True)
                        existing_json_data = {}
            
            # If a file exists at the new (title-based) path and it's different from the product_id path,
            # merge from that one too, giving preference to the existing human-edited one.
            if os.path.exists(final_output_file_path) and final_output_file_path != initial_output_file_path:
                with open(final_output_file_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_json_data_at_final_path = json.load(f)
                        # Merge existing_json_data (from product_id file) with the one from final_output_file_path
                        # This ensures human edits from the correct title-based file are respected.
                        # The 'merge_adventure_data' is careful by default, so it will fill in gaps.
                        existing_json_data = merge_adventure_data(existing_json_data, existing_json_data_at_final_path)

                        # If the initial product_id.json existed, but the file is now named differently,
                        # remove the old product_id.json file if its content is identical to the final data
                        # or if it's empty/obsolete.
                        if os.path.exists(initial_output_file_path) and initial_output_file_path != final_output_file_path:
                            with open(initial_output_file_path, 'r', encoding='utf-8') as old_f:
                                old_content = json.load(old_f)
                            # If the old content is identical to the final, or the new file is simply replacing it
                            if old_content == existing_json_data_at_final_path or not old_content:
                                os.remove(initial_output_file_path)
                                logger.info(f"Removed old product_id based JSON file: {initial_output_file_path}")

                    except json.JSONDecodeError:
                        logger.error(f"Error decoding JSON from {final_output_file_path}. Treating as empty.", exc_info=True)
                        # existing_json_data remains what was loaded from initial_output_file_path or empty

            # Merge new data with existing data, respecting human edits
            final_data = merge_adventure_data(existing_json_data, new_data_to_merge_json, force_overwrite=args.force)

            # Convert the final_data dict back to an Adventure object for type safety and to_json consistency
            final_adventure_obj = Adventure.from_json(final_data)
            final_json_data_to_save = final_adventure_obj.to_json()


            # --- Always move HTML file ---
            shutil.move(file_path, os.path.join(processed_html_path, file_name))
            logger.info(f"Moved {file_name} to {processed_html_path}")

            # Check if JSON content actually changed before writing
            # Use default=str for Decimal and date objects during serialization for comparison
            existing_serialized = json.dumps(existing_json_data, sort_keys=True, default=str)
            final_serialized = json.dumps(final_json_data_to_save, sort_keys=True, default=str)

            if final_serialized != existing_serialized or args.force:
                with open(final_output_file_path, 'w', encoding='utf-8') as f:
                    json.dump(final_json_data_to_save, f, indent=4, sort_keys=True)
                logger.info(f"Successfully processed {file_name} and updated/saved to {final_output_file_path}")
            else:
                logger.info(f"No changes to JSON content for {file_name}, skipped writing to {final_output_file_path}.")


        except Exception as ex:
            logger.error(f"Error processing {file_path}: {str(ex)}", exc_info=True)

if __name__ == "__main__":
    process_downloads()