# aladventures
Sortable and Filterable Catalog of Adventurers League Adventures

Final link will be [here](https://hoshisabi.com/al_adventure_catalog/)

## Set up

There are two primary methods for ingesting new adventure data:

### Method 1: Using the RSS Parser (Recommended for bulk updates)

1.  Navigate to the `maintaindb` directory: `cd maintaindb`
2.  Run the RSS parser: `python3 dmsguild_rss_parser.py`
    *   This script fetches the latest adventure data from the DMsGuild RSS feed and generates JSON files in the `_dc` directory. This process is quick and efficient.

### Method 2: Using the DMsGuild Bookmarklet (For individual adventure updates or when RSS is insufficient)

1.  **Install the Bookmarklet**:
    *   Create a new bookmark in your web browser.
    *   Edit the bookmark and set its URL to the content of `dmsguild_bookmarklet.js` (located in the project root).
    *   Name the bookmark something descriptive, e.g., "DMsGuild Scraper".
2.  **Ingest an Adventure**:
    *   Navigate to the DMsGuild product page of the adventure you wish to ingest.
    *   Click on the "DMsGuild Scraper" bookmarklet.
    *   The bookmarklet will prompt you to save an HTML file. Save this file into the `maintaindb/dmsguildinfo` directory (e.g., `maintaindb/dmsguildinfo/`).
3.  **Process Downloaded Files**:
    *   Navigate to the `maintaindb` directory: `cd maintaindb`
    *   Run the processing script: `python3 process_downloads.py`
    *   This script will parse the HTML files saved in `dmsguildinfo` and generate JSON files in the `_dc` directory. Processed HTML files will be moved to `dmsguildinfo/processed`.

### Post-Ingestion Steps (Common to both methods)

1.  Review the generated JSON files in `_dc` and fix any missing or incorrect data.
2.  Run the aggregator to combine all adventure data: `python3 aggregator.py`
3.  The aggregated results will be available in `_stats`.

## Git Workflow

To upload your changes to the repository:

1.  Check the status of your changes: `git status`
2.  Add all modified files to the staging area: `git add .`
3.  Commit your changes with a descriptive message: `git commit -m "Descriptive commit message"`
4.  Push your changes to the remote repository: `git push origin <your-branch-name>` (Replace `<your-branch-name>` with your actual branch name, e.g., `main` or `master`).
