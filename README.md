# aladventures
Sortable and Filterable Catalog of Adventurers League Adventures

Final link will be [here](https://hoshisabi.com/al_adventure_catalog/)

> **Note for AI Assistants**: This project runs on Windows with PowerShell. See [`AI_ASSISTANT_GUIDELINES.md`](AI_ASSISTANT_GUIDELINES.md) for Windows-specific command-line guidelines.

## Set up

There are two primary methods for ingesting new adventure data:

### Method 1: Using the RSS Parser (Recommended for bulk updates)

1.  From the **project root** (this directory), run:
    ```bash
    uv run python -m maintaindb.process_rss
    ```
    *   This script fetches the latest adventure data from the DMsGuild RSS feed and generates JSON files in the `_dc` directory. This process is quick and efficient.
    *   You can also test with the bundled fixture: `uv run python -m maintaindb.process_rss --url maintaindb/dmsguildinfo/rss.xml --force`
    *   RSS-derived JSONs are marked with `needs_review: true` because the RSS feed lacks some details. See "RSS data gaps" below.

**Note**: The `maintaindb` directory is a Python package. Scripts must be run as modules from the project root. See `maintaindb/README.md` for details.

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
    *   From the **project root**, run:
        ```bash
        uv run python -m maintaindb.process_downloads
        ```
    *   This script will parse the HTML files saved in `dmsguildinfo` and generate JSON files in the `_dc` directory. Processed HTML files will be moved to `dmsguildinfo/processed`.
    *   Supports `--force` flag to overwrite existing files and `--careful` flag to preserve existing non-null data.

### Post-Ingestion Steps (Common to both methods)

1.  Review the generated JSON files in `_dc` and fix any missing or incorrect data.
2.  **Generate Fixup HTML (for missing data):** If you have adventures with missing `hours`, `tier`, or `campaign` data, run `python3 maintaindb/generate_fixup_html.py`. This will create a `fixup.html` file in the `_site/` directory. Open this file in your browser to get direct links to the DMsGuild pages for manual data retrieval.
3.  Run the aggregator to combine all adventure data: `python3 aggregator.py`
    *   This generates the minified `assets/data/catalog.json` used by the frontend.
    *   See [CATALOG_FORMAT.md](CATALOG_FORMAT.md) for details on the optimized JSON format (including bitmasks).
    *   See [CODE_RECOGNITION.md](CODE_RECOGNITION.md) for details on how adventure codes are recognized from titles.
4.  The aggregated results will be available in `_stats`.

## Running the Site Locally

The `lp.bat` script is a convenience script for running the site locally.

*   **`lp.bat` (no parameters):** Serves the site locally using a simple Python server.
*   **`lp.bat rebuild`:** Runs the aggregator and then serves the site locally.

Alternatively, you can run:
```bash
uv run python serve.py
```
And then visit `http://localhost:8000` in your browser.

## Git Workflow

To upload your changes to the repository:

1.  Check the status of your changes: `git status`
2.  Add all modified files to the staging area: `git add .`
3.  Commit your changes with a descriptive message: `git commit -m "Descriptive commit message"`
4.  Push your changes to the remote repository: `git push origin <your-branch-name>` (Replace `<your-branch-name>` with your actual branch name, e.g., `main`).

----

Note for later: [Warhorn](https://warhorn.net/events/pandodnd/manage/scenarios/report.json) has their own json file, we might be able to leverage this.  (those are only pando scenarios).  Global scenarios
are [here](https://warhorn.net/organized-play/p/dnd-adventurers-league#scenarios) but not in json format.

## RSS data gaps

The RSS feed does not include all fields our HTML parser can extract. Current gaps (left blank/null when using RSS):
- authors
- hours
- tiers
- apl (average party level)
- level_range
- Sometimes price (unless present in the RSS description as a commented <price> tag or inline “Price: $X.XX”).

All JSON files produced via the RSS parser are tagged with `needs_review: true` so you can fill in missing details later (e.g., by processing downloaded HTML with `process_downloads.py`).

## Data Handling Policy

This project parses DM’s Guild product pages to extract structured fields (title, code, tier, hours, etc.).  
To respect copyright and site policies:

- **Raw HTML snapshots** of DM’s Guild pages are **not published** in this repository.
- Those files are kept in a **private fixtures repo** (`private-fixtures/` submodule) for trusted collaborators only.
- Public tests use **synthetic fixtures** and **parsed JSON** outputs instead.
- If you have access to the private repo, place it at `private-fixtures/` and update submodules with:
  ```bash
  git submodule update --init --recursive
  ```
- If the private repo is missing, tests fall back to the synthetic fixtures.
This ensures the code remains public and reusable while respecting DM’s Guild’s content rights.  
