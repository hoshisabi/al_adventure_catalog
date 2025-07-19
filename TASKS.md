# Project Tasks

## Next Up: Slicer Improvements

- [ ] **Implement Inclusive Hours Logic:**
    - **`maintaindb/stats.py`:**
        - Add a helper function `_parse_hours_string(hours_str)` to convert a string like "1,2-4,6" into a list of individual hours (e.g., `[1, 2, 3, 4, 6]`).
        - Update `generate_stats` to use `_parse_hours_string` when populating `stats['duration']`.
    - **`assets/js/filter.js`:**
        - Add a JavaScript helper function `parseHoursString(hoursStr)` for the same conversion.
        - Update `populateFilters` to use `parseHoursString` for the hours dropdown.
        - Update `applyFilters` to use `parseHoursString` for `hoursMatch` to enable inclusive filtering.
        - Update `displayResults` to correctly display the `hours` string.

- [ ] **Enhance Campaign Inclusivity:**
    - Ensure `stats['campaign']` in `maintaindb/stats.py` correctly iterates through `adventure.campaigns` (which is already a list).
    - Verify `filter.js` correctly handles `adventure.campaigns` as a list for filtering and display.

- [ ] **Apply Slicer Logic to Stats Page:** (Covered by the above changes to `stats.py`)

- [ ] **Update `filter.js`:** (Covered by the above changes to `filter.js`)

## Future Tasks:

- [ ] **Add Unit Tests for Data Parsing and Consistency:** Implement comprehensive unit tests for the `hours` parsing logic in `maintaindb/adventure.py` and `assets/js/filter.js`, as well as the data consistency and deduplication logic in `maintaindb/aggregator.py` and `maintaindb/process_downloads.py`. This will ensure the robustness and correctness of our data pipeline.

- [ ] **Clean up `_dc` directory:**
  - [ ] Remove duplicated JSON files in the _dc directory
  - [ ] Ensure that all JSON files in the _dc directory have product_id set
  - [ ] Ensure that all JSON files in the _dc directory have hours set, if they have is_adventure = true
  - [ ] Ensure that all JSON files in the _dc directory have tier set, if they have is_adventure = true
  - [ ] Ensure that all JSON files in the _dc directory have campaign set, if they have is_adventure = true
  - [ ] Find duplicate adventures (adventures with the same product id) and manually identify what data is correct
- [ ] **Add Checkbox for DDAL/DDEX Seasons:** Implement a checkbox to optionally include DDAL and DDEX adventures in season filtering.
- [ ] Create a tool that generates a "fixup.html" which we can launch in a local browser that will contain a list of links to DM'S guild URLs
    - This file would be able to be launched locally and permit a user to quickly click the links to download the HTML via bookmarklet
- [ ] Migrate our filename storage in the _dc directory to be product ID as the filename instead of title, this will eliminate our need to sanitize the filenames
    - [ ] When we do this, we will need to first update our code to read/write the new filename
    - [ ] We will also need to rename all of our existing files to the new name
- [ ] **Improve `stats.py` Output:** Enhance `stats.py` to generate more detailed statistics and potentially output them in a more structured format for easier consumption by the Jekyll site.
- [x] **Bookmarklet/Browser Extension:** The existing `dmsguild_bookmarklet.js` is sufficient for now. Further enhancements are a long-term consideration.
- [ ] **GitHub Actions for `dmsguild_rss_parser.py`:** Set up periodic execution of `dmsguild_rss_parser.py` using GitHub Actions.
