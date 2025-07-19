# Project Tasks

## Next Up: Slicer Improvements

- [ ] **Duration Range Filtering:** Modify the system to interpret adventure durations (e.g., "2-4 hours") as inclusive. An adventure with a 2-4 hour range should appear when filtering for 2, 3, or 4 hours.
    - This will likely require changes to how `hours` is stored in the JSON (e.g., as a list of integers or a min/max range) and how it's processed in Python scripts and `filter.js`.
- [ ] **Campaign Inclusivity:** Ensure that adventures belonging to multiple campaigns (e.g., "Forgotten Realms", "Ravenloft") are correctly displayed when filtering for any of their associated campaigns.
    - This will require `campaign` to be stored as a list in the JSON and handled as such in Python scripts and `filter.js`.
- [ ] **Apply Slicer Logic to Stats Page:** Update `stats.py` to reflect the new inclusive logic for duration and campaign when generating statistics.
- [ ] **Update `filter.js`:** Modify the JavaScript filtering logic to correctly handle the new data structures for duration and campaign.

## Future Tasks:

- [ ] **Add Checkbox for DDAL/DDEX Seasons:** Implement a checkbox to optionally include DDAL and DDEX adventures in season filtering.
- [ ] **Improve `stats.py` Output:** Enhance `stats.py` to generate more detailed statistics and potentially output them in a more structured format for easier consumption by the Jekyll site.
- [ ] **Bookmarklet/Browser Extension:** Explore creating a bookmarklet or browser extension to scrape DMsGuild page data (or full HTML) and save it to `maintaindb/_dc/`.
- [ ] **GitHub Actions for `dmsguild_rss_parser.py`:** Set up periodic execution of `dmsguild_rss_parser.py` using GitHub Actions.