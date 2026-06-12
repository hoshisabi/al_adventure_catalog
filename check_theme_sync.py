"""Verify the SHARED THEME TOKENS block is identical in both repos.

The parchment/night-sky theme tokens are duplicated between:
  - hoshisabi.github.io/assets/css/style.scss
  - al_adventure_catalog/assets/css/catalog.css

Each copy sits between the markers below. This script compares the two
blocks (ignoring line-ending differences) and prints a diff if they have
drifted apart.

Usage (from either repo, assuming sibling checkouts):
    python check_theme_sync.py
    python check_theme_sync.py --site path/to/style.scss --catalog path/to/catalog.css
"""

import argparse
import difflib
import sys
from pathlib import Path

START_MARKER = "/* ═══ SHARED THEME TOKENS"
END_MARKER = "/* ═══ END SHARED THEME TOKENS"


def extract_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start == -1 or end == -1:
        sys.exit(f"ERROR: shared-token markers not found in {path}")
    return text[start:end]


def main() -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        default=here.parent / "hoshisabi.github.io" / "assets" / "css" / "style.scss",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=here / "assets" / "css" / "catalog.css",
    )
    args = parser.parse_args()

    site_block = extract_block(args.site)
    catalog_block = extract_block(args.catalog)

    if site_block == catalog_block:
        print("OK: shared theme tokens are in sync.")
        return 0

    diff = difflib.unified_diff(
        site_block.splitlines(keepends=True),
        catalog_block.splitlines(keepends=True),
        fromfile=str(args.site),
        tofile=str(args.catalog),
    )
    sys.stdout.writelines(diff)
    print("\nFAIL: shared theme tokens have drifted — copy the block from "
          "whichever file you just edited into the other.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
