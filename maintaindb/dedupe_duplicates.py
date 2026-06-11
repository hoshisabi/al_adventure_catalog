"""
Remove browser duplicate download files from _dc/ and dmsguildinfo/.

Windows and some browsers save re-downloads as "name (1).ext". These create
spurious JSON entries when processed. This script deletes duplicate JSON/HTML
when a canonical file exists and content matches.
"""
import argparse
import json
import logging
import sys
from pathlib import Path

try:
    from .adventure_utils import (
        adventure_json_equivalent,
        is_browser_duplicate_filename,
        strip_browser_duplicate_suffix,
    )
    from .paths import DC_DIR, DMSGUILDINFO_DIR, DMSGUILDINFO_PROCESSED_DIR
except ImportError:
    from adventure_utils import (
        adventure_json_equivalent,
        is_browser_duplicate_filename,
        strip_browser_duplicate_suffix,
    )
    from paths import DC_DIR, DMSGUILDINFO_DIR, DMSGUILDINFO_PROCESSED_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")


def dedupe_json_files(dc_dir: Path, dry_run: bool = False) -> int:
    removed = 0
    for path in sorted(dc_dir.glob("*.json")):
        if not is_browser_duplicate_filename(path.name):
            continue

        canonical_stem = strip_browser_duplicate_suffix(path.stem)
        canonical_path = dc_dir / f"{canonical_stem}.json"
        if not canonical_path.exists():
            logger.warning(
                "Skip %s: no canonical %s.json",
                path.name,
                canonical_stem,
            )
            continue

        try:
            duplicate = json.loads(path.read_text(encoding="utf-8"))
            canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            logger.warning("Skip %s: invalid JSON (%s)", path.name, exc)
            continue

        if not adventure_json_equivalent(duplicate, canonical):
            logger.warning(
                "Skip %s: content differs from %s",
                path.name,
                canonical_path.name,
            )
            continue

        if dry_run:
            logger.info("[dry-run] Would remove duplicate JSON %s", path.name)
        else:
            path.unlink()
            logger.info("Removed duplicate JSON %s", path.name)
        removed += 1

    return removed


def dedupe_html_files(*html_dirs: Path, dry_run: bool = False) -> int:
    removed = 0
    for html_dir in html_dirs:
        if not html_dir.is_dir():
            continue
        for path in sorted(html_dir.glob("dmsguildinfo-*.html")):
            if not is_browser_duplicate_filename(path.name):
                continue

            raw_stem = path.name.replace("dmsguildinfo-", "").replace(".html", "")
            canonical_stem = strip_browser_duplicate_suffix(raw_stem)
            canonical_path = html_dir / f"dmsguildinfo-{canonical_stem}.html"
            if not canonical_path.exists():
                logger.warning(
                    "Skip %s: no canonical %s",
                    path.name,
                    canonical_path.name,
                )
                continue

            if dry_run:
                logger.info("[dry-run] Would remove duplicate HTML %s", path)
            else:
                path.unlink()
                logger.info("Removed duplicate HTML %s", path)
            removed += 1

    return removed


def dedupe_duplicates(dry_run: bool = False) -> int:
    json_removed = dedupe_json_files(DC_DIR, dry_run=dry_run)
    html_removed = dedupe_html_files(
        DMSGUILDINFO_DIR,
        DMSGUILDINFO_PROCESSED_DIR,
        dry_run=dry_run,
    )
    total = json_removed + html_removed
    logger.info(
        "Done: %d duplicate JSON, %d duplicate HTML (%d total)%s",
        json_removed,
        html_removed,
        total,
        " [dry-run]" if dry_run else "",
    )
    return total


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove browser duplicate download JSON/HTML files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report actions without deleting files.",
    )
    args = parser.parse_args()
    dedupe_duplicates(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
