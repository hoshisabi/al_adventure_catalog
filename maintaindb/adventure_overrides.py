"""
Curated per-product field overrides for _dc JSON files.

Some values can't be derived correctly from DMsGuild data: translations carry
a code and get inferred as adventures, and hours get picked up from numbers in
the fiction. adventure_overrides.json maps product_id to the fields to force:

    {"587544": {"reason": "...", "fields": {"is_adventure": false}}}

Overrides are applied as the last step before a _dc file is written, so the
parsers can't undo them. Run this module to apply them to existing files:

    uv run python -m maintaindb.adventure_overrides
"""
import json
import logging
from pathlib import Path

from .paths import ADVENTURE_OVERRIDES_JSON, DC_DIR

logger = logging.getLogger(__name__)


def load_adventure_overrides(path: Path = ADVENTURE_OVERRIDES_JSON) -> dict[str, dict]:
    """Return {product_id: {field: value}} from the overrides file."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return {str(pid): entry.get("fields", {}) for pid, entry in data.items()}


def apply_adventure_overrides(product_id, data: dict, overrides: dict[str, dict] | None = None) -> bool:
    """Set overridden fields on data in place. Returns True if anything changed."""
    if overrides is None:
        overrides = load_adventure_overrides()
    fields = overrides.get(str(product_id))
    if not fields:
        return False
    changed = False
    for key, value in fields.items():
        if data.get(key) != value:
            logger.info("Override %s: %s %r -> %r", product_id, key, data.get(key), value)
            data[key] = value
            changed = True
    return changed


def apply_overrides_to_dc_files(dc_dir: Path = DC_DIR, overrides: dict[str, dict] | None = None) -> list[str]:
    """Apply overrides to existing _dc files. Returns the product_ids that changed."""
    if overrides is None:
        overrides = load_adventure_overrides()
    changed = []
    for product_id in overrides:
        path = dc_dir / f"{product_id}.json"
        if not path.exists():
            logger.warning("Override for %s has no matching file %s", product_id, path.name)
            continue
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        if apply_adventure_overrides(product_id, data, overrides):
            with path.open("w") as f:
                json.dump(data, f, indent=4, sort_keys=True)
            changed.append(product_id)
    return changed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    updated = apply_overrides_to_dc_files()
    print(f"Updated {len(updated)} file(s): {', '.join(updated) if updated else 'none'}")
