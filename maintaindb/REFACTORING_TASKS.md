# Refactoring Tasks

This file tracks future refactoring and improvement tasks for the maintaindb codebase.

## Completed ✅

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
- [ ] Sort by Date does not appear to be working as expected.
- [ ] Add display of date added
- [ ] Add display of author, allow for searching by author
- [ ] Add seasons for the non-FR campaigns


### Code Organization

- [ ] **Extract normalization logic into separate methods**
  - The `get_dc_code_and_campaign()` function is getting complex with special cases
  - Create dedicated methods for handling different code pattern variants
  - This will make it easier to add new special cases without cluttering the main function
  - Location: `adventure.py` - `get_dc_code_and_campaign()` function

### Bug Fixes

- [ ] **Fix stats page and graphs**
  - Stats numbers are incorrect (e.g., 1698 "Unknown" campaigns seems wrong)
  - Graphs don't render properly or show incorrect data
  - Issues identified in `stats.py`:
    - **Line 39**: Date parsing will crash if `date_created` is `None` - needs null handling
    - **Line 38**: `d.pop('full_title')` will fail if key doesn't exist - should use `.get()` with fallback
    - **Missing filter**: Code doesn't filter out non-adventures (bundles, Roll20, Fantasy Grounds) - should only count where `is_adventure == True`
    - **Hours parsing**: `_parse_hours_string()` will crash on malformed input (non-numeric, invalid ranges) - needs error handling
    - **Campaign counting**: Counts each adventure multiple times if it has multiple campaigns - may be intentional but inflates totals
    - **Empty campaigns**: Treats empty list `[]` as "Unknown" - may be correct but worth verifying
  - Issues identified in `stats.html`:
    - Uses Chart.js v2 API (`getContext('2d')`) which may be outdated
    - No error handling if stats.json fails to load
    - Chart configuration may need updates for better display (sorting, colors, labels)
  - Location: `maintaindb/stats.py` and `stats.html`
  - Need to verify data accuracy, add error handling, and ensure graphs render correctly

## Medium Priority

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

- [ ] **Consolidate duplicate constants**
  - `DC_CAMPAIGNS`, `DDAL_CAMPAIGN`, `SEASONS` exist in both `adventure.py` and `adventure_utils.py`
  - Consider importing from `adventure_utils.py` to reduce duplication
  - Keep exports in `adventure.py` for backward compatibility

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
  - **Migration**: Created `migrate_filenames_to_product_id.py` script to rename existing JSON files from title-based to product_id-based filenames
    - Run with `--dry-run` first to see what will be changed
    - Use `--force` to overwrite existing files if there are conflicts
    - Handles edge cases: missing product_id, already-migrated files, duplicate product_ids
  - **Location**: `maintaindb/process_downloads.py` (line 78), `maintaindb/process_rss.py` (line 166), `maintaindb/migrate_filenames_to_product_id.py`

### Architecture

- [ ] **Consider consolidating code architecture**
  - Currently have both `process_downloads.py` and `process_downloads_new.py`
  - `adventure.py` (current) vs `adventure_extractors.py` + `adventure_normalizers.py` (alternative architecture)
  - Decide on migration path or consolidation strategy
  - Note: The extraction code already handles both old and new DMsGuild website UI formats (legacy HTML vs new Angular-based HTML), which is necessary since we have a mix of downloaded HTML files. This is separate from the code architecture question.

- [ ] **Expand unit test coverage**
  - Add more comprehensive tests for extraction functions with real HTML fixtures
  - Add unit tests for normalization logic (code pattern variants, campaign/season detection)
  - Add integration tests for the full extraction pipeline
  - Test edge cases and error handling
  - Location: `tests/` directory

- [ ] **Document code pattern recognition rules**
  - Create a reference document explaining how different code formats are recognized
  - Include examples of special cases (like BK-05-02 → PO-BK)

### Advanced Data Extraction

- [ ] **OCR/Image analysis for thumbnail extraction**
  - Evaluate thumbnail images to extract data not available on download page
  - Use OCR or image analysis to read text from product thumbnails
  - Could extract: level range, hours, tier information that might be visible in thumbnails
  - **Note**: PDF preview interaction may be forbidden by DMsGuild terms of service
  - This is exploratory - verify legal/ethical constraints before implementation
  - Consider using libraries like Tesseract (OCR) or image processing libraries
  - Location: New file `maintaindb/image_extractor.py` (if pursued)

## Notes

- The codebase needs to remain backward compatible with existing scripts
- Any refactoring should maintain the same public API
- Test after each major change to ensure no regressions
- **Important**: The extraction code handles both old and new DMsGuild website UI formats:
  - Old format: Legacy HTML with specific class names (e.g., `grid_12 product-title`)
  - New format: Angular-based site with JSON-LD structured data and different HTML structure
  - Both formats are supported because we have a mix of downloaded HTML files, and new downloads will use the new format

