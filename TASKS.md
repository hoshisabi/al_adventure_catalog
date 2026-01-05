# Adventure Catalog Master Task List

## 1. High-Performance Data Architecture (New Optimization)
- [x] **Python: Generate Summary Index (`summary_index.json`)**
    - Only include fields needed for UI display/slicers (ID, Title, Code, Tier, Level, Campaign).
- [ ] **Python: Generate Search Index (`search_index.json`)**
    - Create a map of `{ id: "normalized_search_string" }`.
    - Normalize: Lowercase, remove punctuation, concatenate Title + Code + Authors.
- [ ] **JS: Async Detail Fetching**
    - Update `index.html` to load the small indices on page load.
    - Fetch `_data/{product_id}.json` only when a user selects an adventure.
    - Implement a simple JS cache for fetched details.

## 2. Python Aggregator & Data Quality
- [ ] **Validation Enhancements** (in `aggregator.py`)
    - Flag malformed `hours` or `apl` fields.
    - Add a "Sanity Check" build step: Ensure every index entry has a matching individual JSON file.
- [ ] **Deduplication Strategy**
    - Refine logic to handle duplicate codes or titles during aggregation.
- [ ] **Stats Generation**
    - Update aggregator to output `stats.json` for the stats dashboard.

## 3. Web UI Improvements
- [ ] **Search Experience**
    - Add the text search box using the new `search_index.json`.
- [ ] **Detail View**
    - Create a UI component (modal or side-panel) to display the "fetched" individual adventure data.
- [ ] **Result Counts**
    - Ensure result counts update dynamically based on filters + search.

## 4. Repository & Maintenance (Plan 2 Implementation)
- [ ] **Fixture Management**
    - Move raw HTML snapshots to a private fixtures submodule.
    - Update `.gitignore` to protect DMG HTML.
- [ ] **History Scrubbing**
    - Use `git filter-repo` to remove any accidentally published HTML from the history.

## Data Quality & Validation

* [ ] Extend `aggregator.py` to perform stronger validation, not just parsing:

    * Flag empty or malformed `hours` (e.g., `""`, `"2,2"`, or mixed range/list formats).
    * Normalize `product_id` to string type.
    * Normalize `apl` to numeric or array of numbers.
    * Handle missing or null `season` (mark as placeholder or future tag).
    * Detect duplicated or conflicting entries.
* [ ] Improve resilience against inconsistent human-entered data (graceful fallbacks, warnings rather than crashes).
* [ ] Add validation reports/logs so problems are visible without breaking the build.

## Stats Page

* [ ] Ensure `stats.json` is published to `assets/data/` so `stats.html` loads correct values.
* [ ] Update `aggregator.py` to compute grouped counts:

    * by `campaign`
    * by `tier`
    * by `hours`
    * by `season`
* [ ] Confirm chart data aligns with validated catalog entries.

## Index Page Improvements

* [ ] Add a text search box for adventures (filter by title, code, campaign, season, tags).
* [ ] Replace client-side slicing with pre-generated JSON files (`by_campaign.json`, `by_tier.json`, `by_hours.json`).
* [ ] Update result count display to reflect filters + search.

## Build & Deployment

* [ ] Update aggregator to write all outputs (`catalog.json`, `stats.json`, grouped JSON) into `assets/data/`.
* [ ] Remove reliance on `_stats/` (or configure `_config.yml` to include it).
* [ ] Standardize Python version to `3.12` for GitHub Actions unless 3.13-specific features are required.

---

## Data Handling & Repo Restructure (Plan 2)

> Goal: keep **code public** while storing **real HTML snapshots** in a **private fixtures repo**.

### Immediate Safety

* [ ] **Make current repo private** temporarily if any HTML snapshots are public.
* [ ] Add a protective `.gitignore` in the public repo:

  ```gitignore
  dmsguildinfo/
  **/dmsguildinfo-*.html
  _dc/
  private-fixtures/
  ```
* [ ] Add an optional pre-commit hook to prevent accidental adds:

  ```bash
  # .git/hooks/pre-commit
  if git diff --cached --name-only | grep -E '(^|/)(dmsguildinfo-.*\.html|dmsguildinfo/)' >/dev/null; then
    echo "❌ Refusing to commit DMG HTML into the public repo."; exit 1; fi
  ```

### Split Public Code vs Private Fixtures

* [ ] Create **private** repo `al_catalog-fixtures-private` and move real HTML snapshots there (`dmsguildinfo/`, optional `_dc/`).
* [ ] In the public repo, mount it as a **git submodule**:

  ```bash
  git submodule add git@github.com:<you>/al_catalog-fixtures-private.git private-fixtures
  git commit -m "Add private fixtures submodule"
  ```
* [ ] Document collaborator setup:

  ```bash
  git clone --recurse-submodules git@github.com:<you>/al_adventure_catalog.git
  # or
  git submodule update --init --recursive
  ```
* [ ] Update tests to **fall back** to synthetic fixtures if `private-fixtures/` is missing (CI-friendly).

### Purge Previously-Published HTML from History

* [ ] Remove tracked HTML files from the current tip:

  ```bash
  git rm -r --cached dmsguildinfo || true
  git commit -m "Remove DMG HTML snapshots from tree"
  ```
* [ ] Rewrite history to purge past commits containing HTML (choose one):

    * **git filter-repo** (recommended):

      ```bash
      pipx install git-filter-repo  # or brew install git-filter-repo
      git filter-repo --invert-paths --paths dmsguildinfo --force
      git push --force origin main
      ```
    * **BFG Repo-Cleaner** (alternative):

      ```bash
      java -jar bfg.jar --delete-folders dmsguildinfo --no-blob-protection
      git reflog expire --expire=now --all && git gc --prune=now --aggressive
      git push --force origin main
      ```
* [ ] Invalidate downstream clones: open an issue/notice advising collaborators to re-clone.
* [ ] (Optional) Temporarily disable GitHub Pages until rewrite is complete, then re-enable.

### Licensing & Policy

* [ ] Add a permissive license for code (e.g., **MIT**), or "public domain"-style (**Unlicense** or **CC0**) if preferred.
* [ ] Add a short **Data Handling Policy** in README explaining that raw third-party HTML is not published; real snapshots live in `private-fixtures`.

---

## Future Enhancements

* [ ] Convert `season` to a tag-based system.
* [ ] Add richer stats (e.g., adventures per year, adventures per publisher).
* [ ] Consider basic test coverage for `aggregator.py` functions.
* [ ] Explore alternate visualizations (e.g., search facets, tag clouds).
* [ ] Consider adding optional CV-style auto-generated thumbnails (stretch goal).

---

## Aggregator.py – Parsing & Validation Roadmap

> Goal: make the generator tolerant to messy, human-entered data and emit normalized, validated outputs.

### 1) Canonical Schema (target fields)

* `code: string` (uppercased, trimmed)
* `title: string`
* `campaign: string` (normalized via synonyms map)
* `tier: integer` in {1,2,3,4}
* `hours: string` (original), plus derived:

    * `hours_min: number`, `hours_max: number`, `hours_avg: number`
    * `hours_list: number[]` (expanded from lists/ranges)
* `season: string | null` (also mirrored in `tags: string[]`)
* `apl: number | number[]` (normalized list), plus `apl_min`, `apl_max`
* `product_id: string` (stringified)
* `tags: string[]` (lowercase kebab-case)

### 2) Normalization Rules

* **code**: remove whitespace then uppercase; map known prefixes; trim suffix junk.
* **campaign**: title-case + synonyms map `{ "DDAL": "Adventurers League", "AL": "Adventurers League", "FR": "Forgotten Realms" }` (extendable in YAML).
* **tier**: accept `"1"`, `"T1"`, `"Tier 1"` → `1` (regex friendly).
* **hours**: accept patterns → derive numbers:

    * single: `"2"`, `"2.5"`
    * range: `"2-4"` → expand to `[2,3,4]`; set min/max/avg
    * list: `"1,2-4,6"` → expand to `[1,2,3,4,6]`
    * variants: strip `hrs|hours|~|approx|about`
    * unknown tokens: keep original, set derived fields `null`, register **warning**
* **apl**: parse `"13,18"`, `"7-9"`, `"APL 5"` → list of ints; compute `apl_min`, `apl_max`.
* **season**: accept `"S9"`, `"Season 9"`, `"9"`; store canonical `S9` and add tag `season-9`.
* **product\_id**: cast to string, strip non-printing; keep leading zeros if present.
* **tags**: lowercase kebab-case; split on `[,/;]` and whitespace; de-dup.

### 3) Validation (errors vs warnings)

* **Errors** (fail item): missing `title` or `code`; invalid `tier` (not 1–4) if `is_adventure=true`.
* **Warnings** (emit but keep item): unparseable `hours`/`apl`; unknown `campaign`; duplicate `code`.
* Emit `assets/data/validation_report.json` with counts and samples per rule.

### 4) Deduplication Strategy

* Primary key: `code` when present; fallback: `(normalized_title, campaign)`.
* On conflict, prefer: newer `updated_at` > richer fields > longer description.
* Log merge decisions in the validation report (top N examples).

### 5) Output Paths

* Normalized catalog → `assets/data/catalog.json`.
* Grouped slices → `assets/data/by_campaign.json`, `by_tier.json`, `by_hours.json`.
* Stats for charts → `assets/data/stats.json`.

### 6) Tests & Fixtures

* `/tests/fixtures/*.json` for messy examples (hours ranges, lists, typos, tiers, seasons, apl formats).
* Golden tests: run aggregator, compare to snapshots.
* (Optional) Property-based tests for hours/tier parsers.

### 7) Logging & CI

* Structured logs: `INFO` normalize, `WARN` recoverable, `ERROR` drops.
* GitHub Actions: run aggregator; publish `assets/data/*`; attach `validation_report.json` artifact.
* Fail build if **error** count > 0; allow **warnings** with a summary.

### 8) Performance & Stability

* Streaming I/O for large JSON; avoid full-buffer when possible.
* Deterministic ordering (sort keys/arrays) for minimal diffs.
* Add `--dry-run` and `--only-validate` flags for safe CI runs.

---

## Repository & Licensing Tasks

* [ ] Transition to **Plan 2**: keep parsing code public, but move raw HTML snapshots into a **separate private repo** (`private-fixtures`) mounted as a submodule.
* [ ] Add `.gitignore` rules to prevent committing `dmsguildinfo-*.html` or `_dc/` outputs to the public repo.
* [ ] (Optional) Add a pre-commit hook that refuses to commit any DM’s Guild HTML into the public repo.
* [ ] Write a short “Data handling policy” section in the README:

    * Explain that raw DM’s Guild HTML is excluded for copyright reasons.
    * Mention that collaborators with access can pull the `private-fixtures` submodule.
    * Document fallback to synthetic fixtures for public CI/tests.
* [ ] Scrub history: remove any accidentally published HTML from the current public repo (filter-branch or BFG).
* [ ] Decide on license: open-source but permissive (MIT/Apache) or “public domain” style (CC0/Unlicense) depending on preference. Emphasize that code is special-purpose.
