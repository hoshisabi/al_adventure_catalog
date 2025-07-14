import os
import glob
import json
import shutil
import subprocess
import pathlib
import logging
import sys

from bs4 import BeautifulSoup
from adventure import DungeonCraft, sanitize_filename, _parse_html_to_dc_data

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_html_path = os.path.join(root, 'dmsguildinfo')
output_json_path = os.path.join(root, '_dc')
processed_html_path = os.path.join(input_html_path, 'processed')

def process_downloads():
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
            data = _parse_html_to_dc_data(parsed_html, product_id, product_alt=None)

            # Construct the DungeonCraft object
            dc = DungeonCraft(product_id, data["module_name"], data["authors"],
                              data["code"], data["date_created"], data["hours"], data["tiers"], data["apl"], data["level_range"], dummy_url, data["campaign"], data["is_adventure"], data["price"])

            # Determine output JSON filename based on full_title
            # Sanitize full_title to create a valid filename
            json_filename = sanitize_filename(dc.full_title) + ".json"
            output_file_path = os.path.join(output_json_path, json_filename)

            with open(output_file_path, 'w') as f:
                json.dump(dc.to_json(), f, indent=4, sort_keys=True)
            logger.info(f"Successfully processed {file_name} and saved to {output_file_path}")

            # Move processed HTML file
            shutil.move(file_path, os.path.join(processed_html_path, file_name))
            logger.info(f"Moved {file_name} to {processed_html_path}")

        except Exception as ex:
            logger.error(f"Error processing {file_path}: {str(ex)}")

    logger.info("Running aggregator.py...")
    subprocess.run([sys.executable, os.path.join(root, 'aggregator.py')], check=True)
    logger.info("Processing complete.")

if __name__ == '__main__':
    process_downloads()
