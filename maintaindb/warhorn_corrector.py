import json
import os
import re
import logging
import sys
import time
import requests
import argparse
import glob
from warhorn_api import run_query
from adventure import str_to_int, get_season, generate_warhorn_slug # Import necessary functions from adventure.py

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

def correct_adventure_data_from_warhorn(json_file_path):
    logger.info(f"Processing {json_file_path} for Warhorn corrections...")
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            adventure_data = json.load(f)

        # Check if essential fields are already present
        if adventure_data.get("hours") is not None and \
           adventure_data.get("apl") is not None and \
           adventure_data.get("tiers") is not None and \
           adventure_data.get("level_range") is not None:
            logger.info(f"All relevant fields already populated in {json_file_path}. Skipping Warhorn lookup.")
            return

        search_title = adventure_data.get("full_title") or adventure_data.get("title")
        if not search_title:
            logger.warning(f"Could not find a title to search for in {json_file_path}. Skipping Warhorn lookup.")
            return

        expected_slug = generate_warhorn_slug(search_title)

        warhorn_query = """
            query ($searchQuery: String!) {
                globalScenarios(query: $searchQuery) {
                    nodes {
                        name
                        blurb
                        author
                        minLevel
                        maxLevel
                        campaign {
                            name
                        }
                        gameSystem {
                            name
                        }
                        tags {
                            name
                        }
                        slug
                    }
                }
            }
        """
        
        warhorn_result = run_query(warhorn_query, {"searchQuery": search_title})
        time.sleep(1) # Add a 1-second delay to avoid rate limiting
        
        warhorn_scenario = None
        if warhorn_result and warhorn_result.get("data") and warhorn_result["data"].get("globalScenarios") and warhorn_result["data"]["globalScenarios"].get("nodes"):
            # Prioritize exact slug match
            for node in warhorn_result["data"]["globalScenarios"]["nodes"]:
                if node.get("slug") == expected_slug:
                    warhorn_scenario = node
                    break
            # Fallback to first result if no exact slug match
            if not warhorn_scenario:
                warhorn_scenario = warhorn_result["data"]["globalScenarios"]["nodes"][0]

        if warhorn_scenario:
            # Extract data from Warhorn scenario data
            warhorn_hours = None
            if warhorn_scenario.get("blurb"):
                hours_match = re.search(r'(\d+)(?:-(\d+))?\s*[-h]*(?:hour|hours|hr)', warhorn_scenario["blurb"], re.IGNORECASE)
                if hours_match:
                    if hours_match.group(2):
                        warhorn_hours = f"{hours_match.group(1)}-{hours_match.group(2)}"
                    else:
                        warhorn_hours = hours_match.group(1)

            warhorn_apl = str_to_int(warhorn_scenario.get("minLevel")) # Warhorn has min/max level, not APL directly
            warhorn_level_range = None
            if warhorn_scenario.get("minLevel") is not None and warhorn_scenario.get("maxLevel") is not None:
                warhorn_level_range = f"{warhorn_scenario["minLevel"]}-{warhorn_scenario["maxLevel"]}"
            
            warhorn_tiers = None
            if warhorn_apl is not None:
                if 1 <= warhorn_apl <= 4: warhorn_tiers = 1
                elif 5 <= warhorn_apl <= 10: warhorn_tiers = 2
                elif 11 <= warhorn_apl <= 16: warhorn_tiers = 3
                elif 17 <= warhorn_apl <= 20: warhorn_tiers = 4

            warhorn_season = None
            if warhorn_scenario.get("campaign") and warhorn_scenario["campaign"].get("name"):
                # Attempt to map Warhorn campaign name to our season logic
                # This might need more sophisticated mapping based on actual Warhorn campaign names
                warhorn_season = get_season(warhorn_scenario["campaign"]["name"])

            # Update original JSON data only if fields are null
            if adventure_data.get("hours") is None and warhorn_hours is not None:
                adventure_data["hours"] = warhorn_hours
            if adventure_data.get("apl") is None and warhorn_apl is not None:
                adventure_data["apl"] = warhorn_apl
            if adventure_data.get("tiers") is None and warhorn_tiers is not None:
                adventure_data["tiers"] = warhorn_tiers
            if adventure_data.get("level_range") is None and warhorn_level_range is not None:
                adventure_data["level_range"] = warhorn_level_range
            if adventure_data.get("season") is None and warhorn_season is not None:
                adventure_data["season"] = warhorn_season

            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(adventure_data, f, indent=4, sort_keys=True)
            logger.info(f"Successfully updated {json_file_path} with Warhorn data.")
        else:
            logger.info(f"No matching scenario found on Warhorn for '{search_title}'.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Warhorn API request for {json_file_path}: {e}")
    except Exception as e:
        logger.error(f"Error processing {json_file_path}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Correct adventure data from Warhorn API.")
    parser.add_argument("--all", action="store_true", help="Process all JSON files in the _dc directory.")
    parser.add_argument("files", nargs='*', help="Specific JSON files or glob patterns to process (e.g., 'maintaindb/_dc/CCC-*.json').")
    args = parser.parse_args()

    if args.all:
        dc_path = os.path.join(os.path.dirname(__file__), '_dc')
        json_files = [os.path.join(dc_path, f) for f in os.listdir(dc_path) if f.endswith('.json')]
    elif args.files:
        json_files = []
        for pattern in args.files:
            # Handle glob patterns and direct file paths
            if '*' in pattern or '?' in pattern:
                # Use glob.glob for patterns, ensuring absolute paths
                expanded_files = glob.glob(os.path.join(os.path.dirname(__file__), pattern))
                json_files.extend(expanded_files)
            else:
                # Assume it's a direct file path, make it absolute
                json_files.append(os.path.join(os.path.dirname(__file__), pattern))
    else:
        parser.print_help()
        sys.exit(1)

    for json_file in json_files:
        correct_adventure_data_from_warhorn(json_file)
