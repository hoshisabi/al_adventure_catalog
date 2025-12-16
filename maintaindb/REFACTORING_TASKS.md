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

### Code Organization

- [ ] **Extract normalization logic into separate methods**
  - The `get_dc_code_and_campaign()` function is getting complex with special cases
  - Create dedicated methods for handling different code pattern variants
  - This will make it easier to add new special cases without cluttering the main function
  - Location: `adventure.py` - `get_dc_code_and_campaign()` function

## Medium Priority

### Code Quality

- [ ] **Consolidate duplicate constants**
  - `DC_CAMPAIGNS`, `DDAL_CAMPAIGN`, `SEASONS` exist in both `adventure.py` and `adventure_utils.py`
  - Consider importing from `adventure_utils.py` to reduce duplication
  - Keep exports in `adventure.py` for backward compatibility

- [ ] **Improve error handling in HTML extraction**
  - Add more specific error messages when extraction fails
  - Log warnings for missing data fields
  - Location: `adventure.py` - `_extract_raw_data_from_html()` and related functions

- [ ] **Add type hints throughout**
  - Many functions lack complete type hints
  - Improve IDE support and catch errors earlier
  - Location: All files in `maintaindb/`

## Low Priority / Future Considerations

### Architecture

- [ ] **Consider consolidating code architecture**
  - Currently have both `process_downloads.py` and `process_downloads_new.py`
  - `adventure.py` (current) vs `adventure_model.py` + `adventure_extractors.py` + `adventure_normalizers.py` (alternative architecture)
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

## Notes

- The codebase needs to remain backward compatible with existing scripts
- Any refactoring should maintain the same public API
- Test after each major change to ensure no regressions
- **Important**: The extraction code handles both old and new DMsGuild website UI formats:
  - Old format: Legacy HTML with specific class names (e.g., `grid_12 product-title`)
  - New format: Angular-based site with JSON-LD structured data and different HTML structure
  - Both formats are supported because we have a mix of downloaded HTML files, and new downloads will use the new format

