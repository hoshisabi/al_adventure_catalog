# Purpose of this directory

This directory stores DM's Guild source material used by the maintaindb scripts.

We are not checking those files into the repository so that we avoid any sort of
copyright issues. We only keep the extracted metadata in `maintaindb/_dc/`, not
the descriptive text from DM's Guild pages.

Let's be good citizens. :)

## Product page HTML (`dmsguildinfo-*.html`)

Saved from the product-page bookmarklet (`dmsguild_bookmarklet.js` in the project
root). Processed by:

```powershell
uv run python -m maintaindb.process_downloads
```

Processed HTML files are moved to `processed/`.

## Browse list exports (`aldc-page-*.json`)

Saved from the browse-page bookmarklet (`dmsguild_browse_bookmarklet.js` in the
project root). These are small JSON snapshots of a browse/results page and are
**not** processed by `process_downloads.py`.

Audit them against ingested catalog data with:

```powershell
uv run python -m maintaindb.audit_browse_lists
```

Useful flags:

- `--exclude-roll20` — hide Roll20-only variants from the missing list
- `--category adventure` — only show missing adventures
- `--json path/to/report.json` — write machine-readable output