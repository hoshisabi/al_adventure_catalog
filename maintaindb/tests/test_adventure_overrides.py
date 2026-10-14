import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maintaindb.adventure_overrides import (  # noqa: E402
    apply_adventure_overrides,
    apply_overrides_to_dc_files,
    load_adventure_overrides,
)
from maintaindb.paths import ADVENTURE_OVERRIDES_JSON  # noqa: E402


def test_load_adventure_overrides(tmp_path):
    path = tmp_path / "overrides.json"
    path.write_text(json.dumps({
        "123": {"reason": "translation", "fields": {"is_adventure": False}},
        456: {"reason": "hours in fiction", "fields": {"hours": "2"}},
    }))
    assert load_adventure_overrides(path) == {
        "123": {"is_adventure": False},
        "456": {"hours": "2"},
    }


def test_load_adventure_overrides_missing_file(tmp_path):
    assert load_adventure_overrides(tmp_path / "nope.json") == {}


def test_apply_adventure_overrides():
    overrides = {"123": {"is_adventure": False, "hours": "2"}}
    data = {"is_adventure": True, "hours": "8", "code": "FR-DC-X"}
    assert apply_adventure_overrides("123", data, overrides) is True
    assert data == {"is_adventure": False, "hours": "2", "code": "FR-DC-X"}
    # Already matching: no change reported
    assert apply_adventure_overrides(123, data, overrides) is False


def test_apply_adventure_overrides_other_product_untouched():
    data = {"is_adventure": True}
    assert apply_adventure_overrides("999", data, {"123": {"is_adventure": False}}) is False
    assert data == {"is_adventure": True}


def test_apply_overrides_to_dc_files(tmp_path):
    (tmp_path / "123.json").write_text(json.dumps({"is_adventure": True, "title": "T"}))
    (tmp_path / "456.json").write_text(json.dumps({"is_adventure": False}))
    overrides = {"123": {"is_adventure": False}, "456": {"is_adventure": False}, "789": {"hours": "4"}}
    assert apply_overrides_to_dc_files(tmp_path, overrides) == ["123"]
    assert json.loads((tmp_path / "123.json").read_text()) == {"is_adventure": False, "title": "T"}


def test_checked_in_overrides_file_is_well_formed():
    raw = json.loads(ADVENTURE_OVERRIDES_JSON.read_text(encoding="utf-8"))
    for product_id, entry in raw.items():
        assert product_id.isdigit() or "-" in product_id, product_id
        assert entry.get("reason"), f"{product_id} has no reason"
        assert isinstance(entry.get("fields"), dict) and entry["fields"], f"{product_id} has no fields"
