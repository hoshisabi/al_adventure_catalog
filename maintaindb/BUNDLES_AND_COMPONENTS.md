# Bundles and Component Files

Some catalog entries are **bundles** (one store product that contains multiple adventures or tier variants). We represent them as a **parent** JSON file plus one or more **component** JSON files so DMs can find individual adventures (e.g. "tier 1, 2-hour adventure") while the store only sells the bundle.

## Convention

- **Parent**: `X.json` where `X` is the store product ID (digits only). Example: `545950.json`, `200609.json`.
- **Component**: `X-Y.json` where `X` is the same base product ID and `Y` is a digit suffix (e.g. `01`, `2`, `4`). Examples: `545950-01.json`, `545950-03.json`, `200609-2.json`, `200609-4.json`.

Component filenames are detected by the pattern **digits-hyphen-digits** (stem only). Both zero-padded (`545950-01`) and non-padded (`200609-4`) are valid.

## Two use cases

1. **Bundle = one PDF, multiple adventures**  
   The store product is a single PDF; individual adventures are not sold separately. We create virtual entries so each adventure is searchable (tier, duration, code, title). Example: `545950.json` (bundle) and `545950-01.json`, `545950-02.json`, `545950-03.json` (the three adventures in that PDF).

2. **Same adventure, multiple tiers**  
   One store product can be run at different tiers; we use component files so each tier appears as its own catalog entry. Example: `200609.json` (main) and `200609-2.json`, `200609-3.json`, `200609-4.json` (tier 2, 3, 4 variants).

## Rules for component JSON files

- **`product_id`** must match the filename (e.g. `545950-01` for `545950-01.json`). This is the unique catalog identity for the component.
- **`url`** must point at the store product (the base product ID). For example, all of `545950-01.json`, `545950-02.json`, `545950-03.json` use the same URL: the product page for `545950`.
- All other fields (code, title, hours, tiers, level_range, etc.) describe that specific adventure or tier variant.

## Automation

- **normalize_data.py**: Uses the filename as the source of truth for `product_id`, so component files keep their correct `product_id` (e.g. `545950-01`).
- **process_downloads.py** / **process_rss.py**: Only create or update files for store product IDs (e.g. `545950.json`). They never create or overwrite component files like `545950-01.json`.
- **aggregator.py**: Includes every JSON in `_dc/` in the catalog; each component is a separate entry keyed by its `product_id`.

**Important**: Automation must **never** set a component file’s `product_id` from the URL (which contains only the base product ID). The helpers in `adventure_utils.py`—`is_component_filename()` and `get_base_product_id_from_component_filename()`—exist so any future script that infers product ID from URL or filename can treat component files as authoritative and leave their `product_id` unchanged.

## Adding new components

1. Create `X-Y.json` in `_dc/` with `product_id` equal to `X-Y` and `url` pointing to the store product `X`.
2. Fill in the rest of the metadata for that adventure or tier variant.
3. Run `normalize_data.py` and `aggregator.py` as usual; the new component will appear in the catalog.
