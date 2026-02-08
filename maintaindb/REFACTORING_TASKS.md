# Refactoring Tasks

This file tracks future refactoring and improvement tasks for the maintaindb codebase.

## Completed ✅

- [x] Add display of date added
- [x] Add display of author, allow for searching by author
- [x] Add seasons for the non-FR campaigns (Eberron, Ravenloft)
- [x] Consolidate duplicate constants (CAMPAIGN_BITMASK, FLAG_BITMASK, SEASONS moved to adventure_utils.py)
- [x] Fix stats page and graphs (stats.py bugs)
  - [x] Line 39: Date parsing will crash if `date_created` is `None` - added null handling
  - [x] Line 38: `d.pop('full_title')` will fail - refactored to use `catalog_entry_to_dungeoncraft_params`
  - [x] Hours parsing: `_parse_hours_string()` will crash - added error handling and tests
- [x] Sort by Date does not appear to be working as expected.
- [x] Remove unused/incomplete `@dataclass DungeonCraft` definition
- [x] Add missing `generate_warhorn_slug` function
- [x] Organize `adventure.py` into logical sections with clear headers
- [x] Add docstrings to functions
- [x] Fix BK-05-02 campaign recognition (handle "BK-XX-XX" as PO-BK variants)
- [x] Break down `_extract_raw_data_from_html()` into smaller functions
  - Extracted into helper functions:
    - `_extract_title_from_html()`
    - `_extract_authors_from_html()`
    - `_extract_date_from_html()`
    - `_extract_hours_from_text()`
    - `_extract_game_stats_from_text()`
    - `_extract_price_from_html()`
    - `_extract_jsonld_price()`
    - `_extract_pwyw_info_from_html()`
  - Main function reduced from 257 lines to ~30 lines
- [x] Add basic unit tests for refactored extraction functions
  - Created `test_extraction_functions.py` with tests for all helper functions
  - Tests cover title, authors, hours, game stats, price, and PWYW extraction
  - Demonstrates the refactored code works correctly

## High Priority


### Code Organization

- [ ] **Extract normalization logic into separate methods**
  - The `get_dc_code_and_campaign()` function is getting complex with special cases
  - Create dedicated methods for handling different code pattern variants
  - This will make it easier to add new special cases without cluttering the main function
  - Location: `adventure.py` - `get_dc_code_and_campaign()` function

### Bug Fixes

- [x] **Fix stats page and graphs (Backend fixed, Frontend/HTML pending)**
  - [x] Stats numbers are incorrect (Verified: Unknown campaigns reduced from ~1700 to 38)
  - [ ] Graphs in stats.html don't render properly or show incorrect data
  - [x] Issues identified in `stats.py` resolved:
    - [x] Line 39: Date parsing will crash if `date_created` is `None` - added null handling
    - [x] Line 38: `d.pop('full_title')` will fail - refactored to use `catalog_entry_to_dungeoncraft_params`
    - [x] Missing filter: Catalog input is now pre-filtered for `is_adventure == True` in aggregator
    - [x] Hours parsing: `_parse_hours_string()` will crash - added error handling and tests
    - [x] Campaign counting: Fixed bitmask decoding to correctly count campaigns
    - [x] Empty campaigns: Verified and handled during bitmask decoding
  - Issues remaining in `stats.html`:
    - Uses Chart.js v2 API (`getContext('2d')`) which may be outdated
    - No error handling if stats.json fails to load
    - Chart configuration may need updates for better display (sorting, colors, labels)
  - Location: `maintaindb/stats.py` and `stats.html`
  - Need to verify data accuracy, add error handling, and ensure graphs render correctly

## Medium Priority
- [ ] For adventures with missing information, we can make our audit tools provide a link to the Warhorn site,
      which can have a URL like this: https://warhorn.net/organized-play/p/dnd-adventurers-league?q=(keyword)
      where keyword could be the code or the title

### New Tools

- [ ] **Create auditor tool for data quality checks**
  - Tool to help identify adventures that may need human review/editing
  - Use jq-like queries (or Python equivalents) to find common data quality issues:
    - Missing or null fields (date_created, campaigns, season, etc.)
    - Invalid or suspicious values (e.g., hours < 1, tier 0, etc.)
    - Inconsistent data (e.g., tier doesn't match level_range)
    - PWYW adventures that might need verification
    - Adventures with multiple campaigns that might need review
  - **CRITICAL**: Flag adventures with `needs_review: true` (created by RSS parser)
    - RSS parser creates partial data and requires human intervention
    - These should be prominently displayed/highlighted in auditor output
  - Display HTML file availability:
    - Check if `dmsguildinfo-{product_id}.html` exists in `dmsguildinfo/` folder
    - Show status (exists, missing, or in processed folder)
  - Provide download assistance:
    - Display URL for adventures missing HTML files
    - Option to open URL in browser for manual download
    - This helps maintain the catalog without full scraping (which would burden DMsGuild servers)
  - Output format:
    - Interactive CLI with color-coded status
    - Option to export results to CSV/JSON for batch processing
    - Filter by issue type (missing HTML, missing data, data inconsistencies, needs_review)
  - Location: New file `maintaindb/auditor.py`
  - Should integrate with existing data structure and use `all_adventures.json` as input

- [ ] **Create HTML restore tool for processed DMsGuild pages**
  - Purpose: Rehydrate HTML from `dmsguildinfo/processed/` back into `dmsguildinfo/` so existing parsers can run without re-downloading.
  - Paths: Use `DMSGUILDINFO_DIR` and `DMSGUILDINFO_PROCESSED_DIR` from `maintaindb/paths.py`.
  - Inputs/CLI:
    - `--product-id <id>` (repeatable)
    - `--from-file <ids.txt>` (newline-separated list)
    - `--all-missing` (copy any processed HTML not present in `dmsguildinfo/`)
    - `--dry-run`, `--overwrite`, `--checksum` (skip if same hash), `--report <csv|json>`
  - Behavior: For each product_id, find `dmsguildinfo-{product_id}.html` under `processed/` and copy to `dmsguildinfo/`.
  - Output: Console log + optional summary report of copied/skipped/missing files.
  - Location: New file `maintaindb/restore_html.py`; optional wiring via `maintaindb/cli.py`.
  - Tests: `tests/test_restore_html.py` covering dry-run, overwrite, checksum, and missing-file cases.
  - estimated effort: 2–4 hours (incl. tests and docs).
  - Risks/Issues:
    - Filename mismatches or legacy naming schemes; consider tolerant lookup/glob.
    - Stale HTML vs latest site; make behavior explicit in docs.
    - Existing file conflicts; default to no-overwrite unless `--overwrite`.
    - Case sensitivity and Windows path edge cases; use pathlib and safe copy.
    - Ensure no network calls; purely local file operations.
- [ ] **Add RSS processing to GitHub Actions**
  - Automate running `process_rss.py` on a schedule (e.g., daily or weekly)
  - This will make RSS-based data collection more prompt/regular
  - Should commit new/updated JSON files created from RSS feed
  - Consider rate limiting to avoid overloading DMsGuild servers
  - Location: `.github/workflows/` directory

### Data Quality & Workflow

- [ ] **Document and standardize `needs_review` flag usage**
  - The `needs_review` flag is used throughout the codebase to mark adventures that require human intervention
  - **Current usage:**
    - RSS parser (`process_rss.py`): Always sets `needs_review: true` because RSS feeds lack complete data
    - HTML processing (`adventure.py`): Sets `needs_review: true` when module_name cannot be extracted (line 1053)
    - Normalizer (`adventure_normalizers.py`): Sets `needs_review: true` if critical fields (code, level_range, tiers, hours) are missing (lines 174-178)
  - **Documentation needed:**
    - Create a clear specification of when `needs_review` should be set
    - Document the workflow for clearing the flag after human review
    - Ensure all processing scripts handle the flag consistently
    - Consider adding `needs_review` to the data model schema/documentation
  - **Related tools:**
    - `generate_fixup_html.py` already uses `needs_review` to highlight adventures needing attention
    - Future auditor tool should prominently display adventures with `needs_review: true`

### Code Quality

- [x] **Consolidate duplicate constants** (Completed)
  - Moved `CAMPAIGN_BITMASK`, `FLAG_BITMASK`, `SEASONS`, and `DC_CAMPAIGNS` to `adventure_utils.py`
  - Refactored `adventure.py`, `aggregator.py`, and `stats.py` to import from common location

- [ ] **Improve error handling in HTML extraction**
  - Add more specific error messages when extraction fails
  - Log warnings for missing data fields
  - Location: `adventure.py` - `_extract_raw_data_from_html()` and related functions

- [ ] **Replace print statements with proper logging in RSS parser**
  - Convert `print()` statements to use Python's `logging` module
  - Add appropriate log levels (INFO, WARNING, ERROR)
  - Improve error messages and make them more informative
  - Location: `maintaindb/process_rss.py`

- [ ] **Add type hints throughout**
  - Many functions lack complete type hints
  - Improve IDE support and catch errors earlier
  - Location: All files in `maintaindb/`

## Low Priority / Future Considerations

### Data Management & File Naming

- [x] **Use product_id for JSON filenames instead of title**
  - **Rationale**: Product IDs are stable, reliable, and contain only alphanumeric characters (no special characters that need sanitization)
  - **Benefits**: 
    - Eliminates issues with special characters, Unicode, and metadata in titles
    - More reliable file lookups and deduplication
    - Simpler, more maintainable code (no need for sanitize_filename)
    - Product IDs are unique and don't change, making filenames predictable
  - **Implementation**: Changed `process_downloads.py` and `process_rss.py` to use `f"{product_id}.json"` instead of `sanitize_filename(full_title)`
  - **Location**: `maintaindb/process_downloads.py` (line 78), `maintaindb/process_rss.py` (line 166)

### Architecture

- [ ] **Consider consolidating code architecture**
  - Currently have both `process_downloads.py` and `process_downloads_new.py`
  - `adventure.py` (current) vs `adventure_extractors.py` + `adventure_normalizers.py` (alternative architecture)
  - Decide on migration path or consolidation strategy
  - Note: `generate_pages.py` appears redundant and is currently broken due to `catalog.json` bitmask optimizations. Dynamic filtering is now handled by `filter.js`.
  - Note: The extraction code already handles both old and new DMsGuild website UI formats (legacy HTML vs new Angular-based HTML), which is necessary since we have a mix of downloaded HTML files. This is separate from the code architecture question.

- [ ] **Expand unit test coverage**
  - Add more comprehensive tests for extraction functions with real HTML fixtures
  - [x] Add unit tests for normalization logic (bitmask decoding, catalog entry reconstruction)
  - Add integration tests for the full extraction pipeline
  - [x] Test edge cases and error handling (date parsing, malformed hours in stats)
  - Location: `tests/` directory

- [x] **Document code pattern recognition rules**
  - Create a reference document explaining how different code formats are recognized
  - Include examples of special cases (like BK-05-02 → PO-BK)
  - See [CODE_RECOGNITION.md](../CODE_RECOGNITION.md)

### Advanced Data Extraction

- [x] **Warhorn-based validation and auditing**
  - Integrate Warhorn API data into `generate_fixup_html.py`
  - Cross-reference local JSON data with Warhorn's scenario data (hours, level range, tiers)
  - Flag discrepancies between local data and Warhorn data in the audit report
  - **Note**: Warhorn auditing is disabled by default (use `--warhorn` flag) to avoid rate limiting.
  - [x] **Investigate and implement GraphQL batching for Warhorn API**
    - Implemented query-level batching using GraphQL aliases to reduce API load.
    - Updated `generate_fixup_html.py` to use batched requests (batch size: 20).

## Notes

- The codebase needs to remain backward compatible with existing scripts
- Any refactoring should maintain the same public API
- Test after each major change to ensure no regressions
- **Important**: The extraction code handles both old and new DMsGuild website UI formats:
  - Old format: Legacy HTML with specific class names (e.g., `grid_12 product-title`)
  - New format: Angular-based site with JSON-LD structured data and different HTML structure
  - Both formats are supported because we have a mix of downloaded HTML files, and new downloads will use the new format

