# maintaindb

This directory contains Python scripts used for maintaining the adventure catalog data.

## Scripts:

*   `__init__.py`: Initializes the Python package.
*   `adventure.py`: Utility methods and data about individual AL Adventures
*   `aggregator.py`: Aggregates individual adventure JSON files (from `_dc/`) into a single `all_adventures.json` file used by the Jekyll site. This script must be run manually after new or updated JSON files are created in `_dc/`.
*   `dmsguild_rss_parser.py`: Fetches and parses the DMsGuild RSS feed to extract adventure metadata and create individual JSON files in `_dc/`. This script is RSS-only (no HTML scraping). You can pass either a remote RSS URL or a local XML file path (e.g., `maintaindb\dmsguildinfo\rss.xml`) via `--url`. RSS-derived entries are tagged with `needs_review: true` because the feed lacks some details (authors, hours, tier/APL, level range, and sometimes price). Note that the RSS feed typically only provides information for the most recently added adventures and will not update data for older adventures.
*   `generate_pages.py`: Generates static pages or data for the Jekyll site based on the processed adventure data.
*   `process_downloads.py`: Processes downloaded HTML files from the `dmsguildinfo/` directory, extracts adventure metadata, and creates/updates individual JSON files in `_dc/`. This script is used for processing manually downloaded or bookmarklet-generated HTML files.
*   `simple_fetch.py`: A utility script for simple web fetching operations.
*   `stats.py`: Generates various statistics about the adventure catalog data, utilizing the `DungeonCraft` class from `adventure.py`.