
import sys
from pathlib import Path
import pytest

# Import adventure from project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Try both layout options: project root module or package under maintaindb
try:
    import adventure  # type: ignore
except ModuleNotFoundError:
    from maintaindb import adventure  # type: ignore

PRODUCT_ID = "536025"

def _extract_to_json(bs_doc):
    obj = adventure.extract_data_from_html(
        bs_doc,
        product_id=PRODUCT_ID,
        existing_data=None,
        force_overwrite=True,
        careful_mode=False
    )
    return obj.to_json()

def test_title_and_price_parity(bs_html_old, bs_html_new):
    j_old = _extract_to_json(bs_html_old)
    j_new = _extract_to_json(bs_html_new)

    assert j_old["title"]
    assert j_new["title"]
    assert j_old["title"] == j_new["title"]

    assert j_old["full_title"]
    assert j_new["full_title"]

    assert j_old["price"] is not None
    assert j_new["price"] is not None
    assert float(j_old["price"]) == pytest.approx(float(j_new["price"]), rel=0, abs=1e-6)

def test_date_created_allows_none(bs_html_new):
    j_new = _extract_to_json(bs_html_new)
    assert "date_created" in j_new
    dc = j_new["date_created"]
    if dc is not None:
        assert isinstance(dc, str) and len(dc) == 8 and dc.isdigit()

def test_core_fields_present(bs_html_old, bs_html_new):
    j_old = _extract_to_json(bs_html_old)
    j_new = _extract_to_json(bs_html_new)

    for key in ["product_id", "title", "authors"]:
        assert key in j_old and key in j_new

    for j in (j_old, j_new):
        assert ("hours" not in j) or (j.get("hours") is None or isinstance(j.get("hours"), str))
        for k in ["tiers", "apl", "level_range"]:
            assert (j.get(k) is None) or isinstance(j.get(k), str)
