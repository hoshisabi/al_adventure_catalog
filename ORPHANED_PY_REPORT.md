Orphaned Python files assessment (2025-09-12)

Summary
- Purpose: Identify .py files in this repository that are not imported by other modules and are not used as documented/intentional entry-point scripts.
- Conclusion: 1 orphaned Python file identified for deletion; a separate minor issue found in CLI entry-point wiring.

Identified orphan(s)
1) maintaindb\generate_fixup_html_new.py
   - Evidence:
     - Not imported anywhere in the project (search: references = 0).
     - Not mentioned in README or guidelines as a supported script.
     - Duplicates the functionality of maintaindb\generate_fixup_html.py, which is the documented tool in README and GEMINI.md.
   - Action taken: Deleted from repository.

Notes on non-orphans considered
- maintaindb\dmsguild_rss_parser_new.py and maintaindb\process_downloads_new.py
  - Both have __main__ guards and are referenced in the project-specific guidelines as newer or alternative pipelines. Kept.
- maintaindb\cli.py
  - This file is referenced by the pyproject entry point (maintaindb = "maintaindb.cli:main").
  - It is not an orphan, but currently calls process_downloads.main(), which does not exist; the function exported is process_downloads(). Consider changing to process_downloads.process_downloads().
- Various utility/analysis scripts (find_missing_html.py, generate_fixup_html.py, generate_pages.py, simple_fetch.py, stats.py, warhorn_api.py, warhorn_corrector.py, aggregator.py) have __main__ blocks and/or are documented in maintaindb/README.md. Kept.

Methodology
- Enumerated all *.py files under maintaindb, excluding venv artifacts.
- Flagged library modules without __main__ and verified their imports across the codebase.
- Flagged script-like files with __main__ and verified mentions in README/guidelines or other operational references.
- Ran pytest for sanity (maintaindb\tests): current suite passes (expected skips included).

Recommendations
- Fix entry-point wiring in maintaindb\cli.py as noted above to avoid runtime error when invoking the project script via pyproject.
- If the team wants to fully deprecate the "_new" pipeline, update guidelines and remove dmsguild_rss_parser_new.py and process_downloads_new.py in a separate PR after confirming they are not needed.
