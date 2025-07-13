# maintaindb

This directory contains Python scripts used for maintaining the adventure catalog data.

## Scripts:

*   `__init__.py`: Initializes the Python package.
*   `aggregator.py`: Aggregates individual adventure JSON files (from `_dc/`) into a single `all_adventures.json` file used by the Jekyll site.
*   `collate_csv_poa.py`: Processes CSV data specifically related to "Princes of the Apocalypse" adventures. This script may require further review for its current utility.
*   `collate_csv.py`: A general script for collating CSV data. This script may require further review for its current utility.
*   `dmsguild_rss_parser.py`: Fetches and parses the DMsGuild RSS feed to extract adventure metadata and create individual JSON files in `_dc/`.
*   `dmsguild_webpage.py`: Contains functions for parsing HTML content from DMsGuild product pages. It is used by `process_downloads.py`.
*   `generate_pages.py`: Generates static pages or data for the Jekyll site based on the processed adventure data.
*   `process_downloads.py`: Processes downloaded DMsGuild HTML files (from `dmsguildinfo/`) to extract adventure data and save it as JSON files in `_dc/`.
*   `simple_fetch.py`: A utility script for simple web fetching operations.
*   `stats.py`: Generates various statistics about the adventure catalog data.