# Contributing

This guide is for people maintaining the catalog data or running the project locally.

## Adding or updating adventure data

There are two ways to ingest adventure data into `maintaindb/_dc/`.

### Method 1: RSS parser (recommended for bulk updates)

From the project root:

```bash
uv run python -m maintaindb.process_rss
```

This fetches the latest adventures from the DMsGuild RSS feed and writes JSON files to
`_dc/`. RSS-derived entries are tagged `needs_review: true` because the feed is missing
some fields — see [RSS data gaps](#rss-data-gaps) below.

You can test against the bundled fixture instead of the live feed with:

```bash
uv run python -m maintaindb.process_rss --url maintaindb/dmsguildinfo/rss.xml --force
```

### Method 2: DMsGuild bookmarklet (for individual adventures)

1. Create a browser bookmark whose URL is the contents of `dmsguild_bookmarklet.js`.
2. Visit the DMsGuild product page for the adventure and click the bookmarklet — it
   will prompt you to save an HTML file.
3. Save that file into `maintaindb/dmsguildinfo/`.
4. Run:

   ```bash
   uv run python -m maintaindb.process_downloads
   ```

   This parses the saved HTML, writes/updates JSON in `_dc/`, and moves processed files
   to `dmsguildinfo/processed/`. Supports `--force` (overwrite existing files) and
   `--careful` (preserve existing non-null data).

### Post-ingestion steps

1. Review the generated JSON in `maintaindb/_dc/` and fix any missing or incorrect
   fields.
2. If adventures are missing `hours`, `tier`, or `campaign`, run
   `uv run python -m maintaindb.generate_fixup_html` to produce `fixup.html` with
   direct links back to DMsGuild for manual lookup.
3. Run the aggregator to rebuild the published catalog:

   ```bash
   uv run python -m maintaindb.aggregator
   ```

   This produces `assets/data/catalog.json` (see [CATALOG_FORMAT.md](CATALOG_FORMAT.md)
   for the format and [CODE_RECOGNITION.md](CODE_RECOGNITION.md) for how adventure
   codes are recognized).

### Automated RSS sync

A scheduled GitHub Action (`.github/workflows/rss-sync.yml`) runs `process_rss` every 8
hours, rebuilds `catalog.json`/`stats.json`, and commits any new adventures it finds.
This gets a "shell" entry onto the site quickly after release; the entries still need
the manual review described above.

### RSS data gaps

The RSS feed doesn't include everything the HTML parser can extract. These fields are
left blank/null when using the RSS method:

- authors
- hours
- tier
- apl (average party level)
- level_range
- price (unless present in the description as a `<price>` tag or "Price: $X.XX")

Entries from the RSS parser are tagged `needs_review: true` so they can be filled in
later, e.g. by processing downloaded HTML with `process_downloads.py`.

## Running the site locally

```powershell
lp.bat            # serve the site locally
lp.bat rebuild    # rebuild catalog.json, then serve
```

Or directly:

```bash
uv run python serve.py
```

Then visit http://localhost:8000.

## Submitting changes

1. `git status` — check what's changed
2. `git add <files>` — stage your changes
3. `git commit -m "Descriptive message"`
4. `git push origin <your-branch>`

## Data handling policy

This project parses DM's Guild product pages for structured metadata (title, code,
tier, hours, etc.). To respect DM's Guild's content rights:

- Raw HTML snapshots are **not published** in this repository.
- They're kept in a private fixtures repo (`private-fixtures/` submodule) for trusted
  collaborators.
- Public tests use synthetic fixtures and parsed JSON instead of real HTML.

If you have access to the private fixtures repo:

```bash
git submodule update --init --recursive
```

If it's missing, tests fall back to the synthetic fixtures.

## Editorial conventions for `_dc/` JSON fields

### `full_title` — author's title, untouched

`full_title` is the product name as the author published it. We do not edit it. Even if it
contains redundant format descriptors ("A 4 hour Tier 1 Salvage Mission"), a verbose code
prefix, or an unconventional style, we leave it as-is. It is the source-of-truth string
for re-ingestion and should reflect what's on DMsGuild.

### `title` — our curated display title

`title` is what appears in the catalog UI. We trim format descriptors that add no content
value, such as:

- `": A 4 hour Tier 1 Salvage Mission"` / `": A Salvage Mission"` → drop the subtitle
- `"| An Eberron Salvage Mission for Oracle of War"` → drop the descriptor after `|`
- `": Eberron Salvage Mission Anthology"` / `": Eberron Salvage Mission Trilogy"` → drop

Keep subtitles that are part of the actual adventure name (e.g. a story arc title).

### `code` — our canonical code, may differ from the author's

We assign codes that follow our preferred conventions even when an author embedded a
different format in their product title. For example:

- An adventure published as `EB-SALVAGE-RSM-T4.4 Daughter of Khyber` gets our code
  `EB-SM-RSM-T4.4` to align with the `EB-SM-*` series.
- Eberron salvage missions without any author-assigned code get a `EB-SM-<KEYWORD>` code
  derived from the adventure name.

The `full_title` retains the author's original prefix; only `code` and `title` reflect
our conventions.

## Ideas / future data sources

[Warhorn](https://warhorn.net/events/pandodnd/manage/scenarios/report.json) has its own
JSON export we might be able to leverage (currently Pando scenarios only). Global AL
scenarios are listed
[here](https://warhorn.net/organized-play/p/dnd-adventurers-league#scenarios) but not in
JSON format.
