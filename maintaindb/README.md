# maintaindb

This directory contains Python scripts used for maintaining the adventure catalog data.

> **Note for AI Assistants**: This project runs on Windows with PowerShell. See [`AI_ASSISTANT_GUIDELINES.md`](../AI_ASSISTANT_GUIDELINES.md) for Windows-specific command-line guidelines.

## How to Run Scripts

**IMPORTANT**: This is a Python package. Scripts use relative imports (`.adventure`, `.adventure_utils`) which only work when Python recognizes the package structure.

### Recommended: Run as Module with `uv run`
From the **project root**, use `uv run` with the module syntax:
```bash
uv run python -m maintaindb.stats
uv run python -m maintaindb.process_downloads
uv run python -m maintaindb.aggregator
uv run python -m maintaindb.process_rss --url <url>
```

### Alternative: Use Entry Points (requires package installation)
Entry points are configured in `pyproject.toml`. After installing/syncing the package, you can use:
```bash
uv sync  # Install package in editable mode
uv run maintaindb-stats              # Generate statistics
uv run maintaindb-process            # Process downloaded HTML files  
uv run maintaindb-aggregate          # Aggregate JSON files
uv run maintaindb-rss --url <url>    # Parse RSS feed
```

### Why This Structure?

**Your project organization is correct and follows Python standards:**
- ✅ `maintaindb/` is a proper Python package (has `__init__.py`)
- ✅ Relative imports (`.adventure`, `.adventure_utils`) are **standard practice** for package-internal imports
- ✅ This structure allows clean separation between library code and scripts

**What doesn't work:**
- ❌ Running scripts directly: `python maintaindb/stats.py` (Python doesn't recognize package structure)
- ❌ `cd maintaindb && python stats.py` (same issue)

**What works:**
- ✅ `uv run python -m maintaindb.stats` (Python recognizes `maintaindb` as a package)
- ✅ Entry points after package sync (cleanest, but requires installation step)

## Main Scripts (Entry Points):

*   `process_downloads.py`: Processes downloaded HTML files from the `dmsguildinfo/` directory, extracts adventure metadata, and creates/updates individual JSON files in `_dc/`. This script is used for processing manually downloaded or bookmarklet-generated HTML files. Supports `--force` flag to overwrite existing files and `--careful` flag to preserve existing non-null data.
*   `process_rss.py`: Fetches and parses the DMsGuild RSS feed to extract adventure metadata and create individual JSON files in `_dc/`. This script is RSS-only (no HTML scraping). You can pass either a remote RSS URL or a local XML file path (e.g., `maintaindb/dmsguildinfo/rss.xml`) via `--url`. RSS-derived entries are tagged with `needs_review: true` because the feed lacks some details (authors, hours, tier/APL, level range, and sometimes price). Note that the RSS feed typically only provides information for the most recently added adventures and will not update data for older adventures.
*   `aggregator.py`: Aggregates individual adventure JSON files (from `_dc/`) into a single `all_adventures.json` file used by the Jekyll site. This script must be run manually after new or updated JSON files are created in `_dc/`.
*   `stats.py`: Generates various statistics about the adventure catalog data, utilizing the `DungeonCraft` class from `adventure.py`.
*   `generate_pages.py`: Generates static pages or data for the Jekyll site based on the processed adventure data.
*   `generate_fixup_html.py`: Generates a `fixup.html` file listing adventures with missing data (hours, tier, campaign) along with direct links to their DMsGuild pages for manual data retrieval. See main README.md for usage details.
*   `find_missing_html.py`: Scans the `_dc/` directory for JSON files and checks if corresponding HTML files exist in `dmsguildinfo/` or `dmsguildinfo/processed/`. Generates a `missing_html.html` file listing adventures that have JSON but no HTML file.
*   `warhorn_corrector.py`: Uses the Warhorn API to correct/additional data for adventures. Can process individual files, glob patterns, or all files in `_dc/` (with `--all` flag). Requires `WARHORN_APPLICATION_TOKEN` environment variable.
*   `simple_fetch.py`: A utility script for simple web fetching operations.

## Library Modules:

*   `adventure.py`: **Main library module** currently in use. Provides utility methods and data structures for individual AL Adventures. Contains the `DungeonCraft` class and functions for HTML extraction, normalization, and data merging. This is the active implementation used by `process_downloads.py` and other scripts.
*   `adventure_utils.py`: Shared utility functions used across modules (date parsing, code/campaign extraction, season mapping, etc.). Used by both the current and refactored architectures.
*   `warhorn_api.py`: Library module providing functions to interact with the Warhorn GraphQL API. Used by `warhorn_corrector.py`.

### Refactored Architecture Modules (Currently Unused):

The following modules are part of an alternative/refactored architecture but are **not currently used** by any active scripts. They are kept for future refactoring work (see `REFACTORING_TASKS.md` and `REFACTOR.md` for details):

*   `adventure_extractors.py`: HTML extraction classes (`AdventureHTMLExtractor`) for the refactored architecture.
*   `adventure_normalizers.py`: Data normalization classes (`AdventureDataNormalizer`) for the refactored architecture.

## Package Files:

*   `__init__.py`: Initializes the Python package.
*   `cli.py`: CLI entry point for the maintaindb package (configured in `pyproject.toml`). Currently delegates to `process_downloads`.