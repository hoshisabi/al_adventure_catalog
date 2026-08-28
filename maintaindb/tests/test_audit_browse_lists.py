import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maintaindb.audit_browse_lists import (  # noqa: E402
    audit_browse_lists,
    classify_list_entry,
    collect_ingested_product_ids,
    format_audit_report,
    is_fantasy_grounds_variant,
    is_roll20_variant,
    load_browse_audit_exclusions,
    load_browse_entries,
    split_missing_entries,
)


def test_classify_list_entry():
    assert classify_list_entry("Foo [BUNDLE]") == "bundle"
    assert classify_list_entry("Adventurers League Character Log (AL 2026)") == "logsheet"
    assert classify_list_entry("Adventurers League Community Logo") == "logo"
    assert classify_list_entry("Something | Roll20") == "roll20"
    assert classify_list_entry("DDAL09-01") == "adventure"


def test_is_roll20_variant():
    assert is_roll20_variant("CCC-ARCON01-03 Pharmacist Wanted (Roll20)")
    assert not is_roll20_variant("CCC-ARCON01-03 Pharmacist Wanted")


def test_is_fantasy_grounds_variant():
    assert is_fantasy_grounds_variant("Bear in Mind (Fantasy Grounds)")
    assert is_fantasy_grounds_variant("A Blight in Mordynia for Fantasy Grounds")
    assert not is_fantasy_grounds_variant("Bear in Mind")


def test_load_browse_audit_exclusions(tmp_path):
    exclusions = {
        "exclude": {"999": "Not AL legal"},
        "notes": {"888": "Code only on cover image"},
    }
    path = tmp_path / "browse_audit_exclusions.json"
    path.write_text(json.dumps(exclusions), encoding="utf-8")

    exclude_map, notes_map = load_browse_audit_exclusions(path)
    assert exclude_map == {"999": "Not AL legal"}
    assert notes_map == {"888": "Code only on cover image"}


def test_split_missing_entries():
    from maintaindb.audit_browse_lists import BrowseEntry

    missing = [
        BrowseEntry(id="100", title="Keep", url="https://example.com/100"),
        BrowseEntry(id="999", title="Drop", url="https://example.com/999"),
    ]
    actionable, excluded = split_missing_entries(missing, {"999": "reason"})
    assert [entry.id for entry in actionable] == ["100"]
    assert excluded == [(missing[1], "reason")]


def test_load_browse_entries_dedupes(tmp_path):
    page1 = {
        "page": 1,
        "entries": [{"id": "100", "title": "Alpha", "url": "https://www.dmsguild.com/product/100"}],
    }
    page2 = {
        "page": 2,
        "entries": [
            {"id": "100", "title": "Alpha duplicate", "url": "https://www.dmsguild.com/product/100"},
            {"id": "200", "title": "Beta", "url": "https://www.dmsguild.com/product/200"},
        ],
    }
    (tmp_path / "aldc-page-001.json").write_text(json.dumps(page1), encoding="utf-8")
    (tmp_path / "aldc-page-002.json").write_text(json.dumps(page2), encoding="utf-8")

    entries, pages, duplicate_ids = load_browse_entries(sorted(tmp_path.glob("aldc-*.json")))
    assert pages == [1, 2]
    assert set(entries) == {"100", "200"}
    assert duplicate_ids == [("100", 1, 2)]


def test_collect_ingested_product_ids(tmp_path):
    (tmp_path / "100.json").write_text("{}", encoding="utf-8")
    (tmp_path / "200-01.json").write_text("{}", encoding="utf-8")
    (tmp_path / "dndbeyond-sja-01.json").write_text("{}", encoding="utf-8")

    ingested = collect_ingested_product_ids(tmp_path)
    assert ingested == {"100", "200"}


def test_audit_browse_lists_integration(tmp_path):
    list_dir = tmp_path / "lists"
    dc_dir = tmp_path / "_dc"
    list_dir.mkdir()
    dc_dir.mkdir()

    list_payload = {
        "page": 3,
        "entries": [
            {"id": "111", "title": "Present Adventure", "url": "https://www.dmsguild.com/product/111"},
            {"id": "222", "title": "Missing Adventure", "url": "https://www.dmsguild.com/product/222"},
            {"id": "333", "title": "Missing Bundle [BUNDLE]", "url": "https://www.dmsguild.com/product/333"},
        ],
    }
    (list_dir / "aldc-page-003.json").write_text(json.dumps(list_payload), encoding="utf-8")
    (dc_dir / "111.json").write_text("{}", encoding="utf-8")

    result = audit_browse_lists(list_dir, dc_dir)
    report = format_audit_report(result, exclude_roll20=True)

    assert result.ingested_count == 1
    assert len(result.missing_entries) == 2
    assert "Missing Adventure" in report
    assert "Present Adventure" not in report


def test_format_audit_report_excludes_curated(tmp_path):
    list_dir = tmp_path / "lists"
    dc_dir = tmp_path / "_dc"
    list_dir.mkdir()
    dc_dir.mkdir()

    list_payload = {
        "page": 1,
        "entries": [
            {"id": "222", "title": "Missing Adventure", "url": "https://www.dmsguild.com/product/222"},
            {"id": "999", "title": "Bad Product", "url": "https://www.dmsguild.com/product/999"},
        ],
    }
    (list_dir / "aldc-page-001.json").write_text(json.dumps(list_payload), encoding="utf-8")

    result = audit_browse_lists(list_dir, dc_dir)
    report = format_audit_report(
        result,
        exclude_map={"999": "Not AL legal"},
        notes_map={"222": "Needs manual code"},
    )

    assert "Missing Adventure" in report
    assert "Bad Product" not in report.split("Excluded (curated):")[0]
    assert "Excluded (curated):" in report
    assert "Not AL legal" in report
    assert "Needs manual code" in report
