"""
Audit DMsGuild browse-list exports against ingested _dc/ JSON files.

Browse pages are captured with the bookmarklet in dmsguild_browse_bookmarklet.js,
which downloads small JSON files (aldc-page-NNN.json) into maintaindb/dmsguildinfo/.
This script merges those exports and reports which products are not yet in _dc/.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .adventure_utils import (
    get_base_product_id_from_component_filename,
    is_component_filename,
)
from .paths import DC_DIR, DMSGUILDINFO_DIR, MAINTAINDB_DIR

logger = logging.getLogger(__name__)

LIST_FILE_GLOB = "aldc-*.json"
EXCLUSIONS_FILE = MAINTAINDB_DIR / "browse_audit_exclusions.json"


@dataclass
class BrowseEntry:
    id: str
    title: str
    url: str
    page: Optional[int] = None


@dataclass
class AuditResult:
    files: list[Path] = field(default_factory=list)
    pages: list[Optional[int]] = field(default_factory=list)
    entries: dict[str, BrowseEntry] = field(default_factory=dict)
    duplicate_ids: list[tuple[str, Optional[int], Optional[int]]] = field(default_factory=list)
    ingested_ids: set[str] = field(default_factory=set)

    @property
    def ingested_count(self) -> int:
        return sum(1 for entry_id in self.entries if entry_id in self.ingested_ids)

    @property
    def missing_entries(self) -> list[BrowseEntry]:
        return [
            entry
            for entry_id, entry in sorted(self.entries.items(), key=lambda item: item[1].title.lower())
            if entry_id not in self.ingested_ids
        ]


def classify_list_entry(title: str) -> str:
    upper = title.upper()
    if "[BUNDLE]" in upper or " BUNDLE" in upper:
        return "bundle"
    if "LOGSHEET" in upper or "LOG SHEET" in upper or "CHARACTER LOG" in upper:
        return "logsheet"
    if "LOGO" in upper:
        return "logo"
    if "ROLL20" in upper:
        return "roll20"
    return "adventure"


def is_roll20_variant(title: str) -> bool:
    return "ROLL20" in title.upper()


def is_fantasy_grounds_variant(title: str) -> bool:
    upper = title.upper()
    return "FANTASY GROUNDS" in upper or " FOR FANTASY GROUNDS" in upper


def load_browse_audit_exclusions(
    path: Path = EXCLUSIONS_FILE,
) -> tuple[dict[str, str], dict[str, str]]:
    """Load curated exclude/notes maps from browse_audit_exclusions.json."""
    if not path.exists():
        return {}, {}
    data = json.loads(path.read_text(encoding="utf-8"))
    exclude = {str(k): str(v) for k, v in data.get("exclude", {}).items()}
    notes = {str(k): str(v) for k, v in data.get("notes", {}).items()}
    return exclude, notes


def split_missing_entries(
    missing: list[BrowseEntry],
    exclude: dict[str, str],
) -> tuple[list[BrowseEntry], list[tuple[BrowseEntry, str]]]:
    actionable: list[BrowseEntry] = []
    excluded: list[tuple[BrowseEntry, str]] = []
    for entry in missing:
        reason = exclude.get(entry.id)
        if reason:
            excluded.append((entry, reason))
        else:
            actionable.append(entry)
    return actionable, excluded


def collect_list_json_files(list_dir: Path) -> list[Path]:
    return sorted(list_dir.glob(LIST_FILE_GLOB))


def collect_ingested_product_ids(dc_dir: Path) -> set[str]:
    ingested: set[str] = set()
    for path in dc_dir.glob("*.json"):
        stem = path.stem
        filename = f"{stem}.json"
        if is_component_filename(filename):
            base_id = get_base_product_id_from_component_filename(filename)
            if base_id:
                ingested.add(base_id)
        elif re.fullmatch(r"\d+", stem):
            ingested.add(stem)
    return ingested


def load_browse_entries(files: list[Path]) -> tuple[dict[str, BrowseEntry], list[Optional[int]], list[tuple[str, Optional[int], Optional[int]]]]:
    entries: dict[str, BrowseEntry] = {}
    pages: list[Optional[int]] = []
    duplicate_ids: list[tuple[str, Optional[int], Optional[int]]] = []

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        page = data.get("page")
        pages.append(page)
        for raw in data.get("entries", []):
            entry = BrowseEntry(
                id=str(raw["id"]),
                title=str(raw.get("title") or "").strip(),
                url=str(raw.get("url") or f"https://www.dmsguild.com/product/{raw['id']}"),
                page=page,
            )
            if entry.id in entries:
                duplicate_ids.append((entry.id, entries[entry.id].page, page))
                continue
            entries[entry.id] = entry

    return entries, pages, duplicate_ids


def audit_browse_lists(list_dir: Path, dc_dir: Path) -> AuditResult:
    files = collect_list_json_files(list_dir)
    entries, pages, duplicate_ids = load_browse_entries(files)
    return AuditResult(
        files=files,
        pages=pages,
        entries=entries,
        duplicate_ids=duplicate_ids,
        ingested_ids=collect_ingested_product_ids(dc_dir),
    )


def _entries_for_category(entries: list[BrowseEntry], category: str) -> list[BrowseEntry]:
    if category == "all":
        return entries
    return [entry for entry in entries if classify_list_entry(entry.title) == category]


def _filter_shown_entries(
    missing: list[BrowseEntry],
    *,
    category: str,
    exclude_roll20: bool,
    exclude_fantasy_grounds: bool,
) -> list[BrowseEntry]:
    shown = _entries_for_category(missing, category)
    if exclude_roll20:
        shown = [entry for entry in shown if not is_roll20_variant(entry.title)]
    if exclude_fantasy_grounds:
        shown = [entry for entry in shown if not is_fantasy_grounds_variant(entry.title)]
    return shown


def format_audit_report(
    result: AuditResult,
    *,
    missing_only: bool = False,
    category: str = "all",
    exclude_roll20: bool = False,
    exclude_fantasy_grounds: bool = False,
    exclude_curated: bool = True,
    exclude_map: Optional[dict[str, str]] = None,
    notes_map: Optional[dict[str, str]] = None,
) -> str:
    exclude_map = exclude_map if exclude_map is not None else {}
    notes_map = notes_map if notes_map is not None else {}

    lines: list[str] = []
    lines.append(f"Browse list audit ({len(result.files)} files)")
    if result.pages:
        page_nums = [page for page in result.pages if page is not None]
        if page_nums:
            lines.append(f"Pages: {min(page_nums)}-{max(page_nums)}")
    lines.append(f"Unique products: {len(result.entries)}")
    lines.append(f"Ingested: {result.ingested_count} / {len(result.entries)}")
    if result.duplicate_ids:
        lines.append(f"Duplicate IDs across pages: {len(result.duplicate_ids)}")

    missing = result.missing_entries
    if exclude_curated and exclude_map:
        missing, excluded = split_missing_entries(missing, exclude_map)
    else:
        excluded = []

    by_category: dict[str, list[BrowseEntry]] = {}
    for entry in missing:
        cat = classify_list_entry(entry.title)
        by_category.setdefault(cat, []).append(entry)

    if not missing_only:
        lines.append("")
        lines.append("Missing by category:")
        for cat in ("adventure", "roll20", "bundle", "logsheet", "logo"):
            items = by_category.get(cat, [])
            if items:
                lines.append(f"  {cat}: {len(items)}")
        if excluded:
            lines.append(f"  excluded (curated): {len(excluded)}")

    shown = _filter_shown_entries(
        missing,
        category=category,
        exclude_roll20=exclude_roll20,
        exclude_fantasy_grounds=exclude_fantasy_grounds,
    )

    if shown:
        lines.append("")
        label = "Missing"
        if category != "all":
            label += f" ({category})"
        filters = []
        if exclude_roll20:
            filters.append("Roll20")
        if exclude_fantasy_grounds:
            filters.append("Fantasy Grounds")
        if exclude_curated and exclude_map:
            filters.append("curated exclusions")
        if filters:
            label += f" (excluding {', '.join(filters)})"
        lines.append(f"{label}:")
        for entry in shown:
            lines.append(f"  {entry.id:>8}  {entry.title}")

    if excluded and not missing_only:
        lines.append("")
        lines.append("Excluded (curated):")
        for entry, reason in excluded:
            lines.append(f"  {entry.id:>8}  {entry.title}")
            lines.append(f"             {reason}")

    noted = [
        (entry, notes_map[entry.id])
        for entry in result.missing_entries
        if entry.id in notes_map
    ]
    if noted and not missing_only:
        lines.append("")
        lines.append("Notes:")
        for entry, note in noted:
            lines.append(f"  {entry.id:>8}  {entry.title}")
            lines.append(f"             {note}")

    return "\n".join(lines)


def audit_result_to_json(
    result: AuditResult,
    *,
    category: str = "all",
    exclude_roll20: bool = False,
    exclude_fantasy_grounds: bool = False,
    exclude_curated: bool = True,
    exclude_map: Optional[dict[str, str]] = None,
    notes_map: Optional[dict[str, str]] = None,
) -> dict:
    exclude_map = exclude_map if exclude_map is not None else {}
    notes_map = notes_map if notes_map is not None else {}

    missing = result.missing_entries
    if exclude_curated and exclude_map:
        missing, excluded = split_missing_entries(missing, exclude_map)
    else:
        excluded = []

    shown = _filter_shown_entries(
        missing,
        category=category,
        exclude_roll20=exclude_roll20,
        exclude_fantasy_grounds=exclude_fantasy_grounds,
    )

    return {
        "files": [path.name for path in result.files],
        "pages": result.pages,
        "unique_products": len(result.entries),
        "ingested_count": result.ingested_count,
        "missing_count": len(result.missing_entries),
        "duplicate_ids": [
            {"id": entry_id, "first_page": first_page, "second_page": second_page}
            for entry_id, first_page, second_page in result.duplicate_ids
        ],
        "missing": [
            {
                "id": entry.id,
                "title": entry.title,
                "url": entry.url,
                "page": entry.page,
                "category": classify_list_entry(entry.title),
                "note": notes_map.get(entry.id),
            }
            for entry in shown
        ],
        "excluded": [
            {
                "id": entry.id,
                "title": entry.title,
                "url": entry.url,
                "page": entry.page,
                "category": classify_list_entry(entry.title),
                "reason": reason,
            }
            for entry, reason in excluded
        ],
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit DMsGuild browse-list JSON exports against maintaindb/_dc/."
    )
    parser.add_argument(
        "--list-dir",
        type=Path,
        default=DMSGUILDINFO_DIR,
        help="Directory containing aldc-page-*.json files (default: maintaindb/dmsguildinfo/)",
    )
    parser.add_argument(
        "--dc-dir",
        type=Path,
        default=DC_DIR,
        help="Directory containing ingested adventure JSON files (default: maintaindb/_dc/)",
    )
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="Omit the summary section and print only missing entries.",
    )
    parser.add_argument(
        "--category",
        choices=("all", "adventure", "roll20", "bundle", "logsheet", "logo"),
        default="all",
        help="Only show missing entries in this category (default: all).",
    )
    parser.add_argument(
        "--exclude-roll20",
        action="store_true",
        help="Hide Roll20-only variants from the missing-entry list.",
    )
    parser.add_argument(
        "--exclude-fantasy-grounds",
        action="store_true",
        help="Hide Fantasy Grounds-only variants from the missing-entry list.",
    )
    parser.add_argument(
        "--no-exclude-curated",
        action="store_true",
        help="Include products listed in browse_audit_exclusions.json.",
    )
    parser.add_argument(
        "--exclusions-file",
        type=Path,
        default=EXCLUSIONS_FILE,
        help="Curated exclusions/notes JSON (default: maintaindb/browse_audit_exclusions.json).",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        default=None,
        help="Write full audit results to this JSON file.",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)

    if not args.list_dir.exists():
        logger.error("List directory does not exist: %s", args.list_dir)
        return 1

    result = audit_browse_lists(args.list_dir, args.dc_dir)
    if not result.files:
        logger.error("No %s files found in %s", LIST_FILE_GLOB, args.list_dir)
        return 1

    exclude_map, notes_map = load_browse_audit_exclusions(args.exclusions_file)
    exclude_curated = not args.no_exclude_curated

    report = format_audit_report(
        result,
        missing_only=args.missing_only,
        category=args.category,
        exclude_roll20=args.exclude_roll20,
        exclude_fantasy_grounds=args.exclude_fantasy_grounds,
        exclude_curated=exclude_curated,
        exclude_map=exclude_map,
        notes_map=notes_map,
    )
    print(report)

    if args.json_path:
        args.json_path.write_text(
            json.dumps(
                audit_result_to_json(
                    result,
                    category=args.category,
                    exclude_roll20=args.exclude_roll20,
                    exclude_fantasy_grounds=args.exclude_fantasy_grounds,
                    exclude_curated=exclude_curated,
                    exclude_map=exclude_map,
                    notes_map=notes_map,
                ),
                indent=2,
            ),
            encoding="utf-8",
        )
        logger.info("Wrote %s", args.json_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
