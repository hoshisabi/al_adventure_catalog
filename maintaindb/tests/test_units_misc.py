
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Try both layout options: project root module or package under maintaindb
try:
    import adventure  # type: ignore
except ModuleNotFoundError:
    from maintaindb import adventure  # type: ignore

def test_sanitize_filename():
    s = "Una: chiave / Maledetta?*"
    out = adventure.sanitize_filename(s)
    assert ":" not in out and "/" not in out and "?" not in out and "*" not in out
    assert out

def test_str_to_int_words_and_digits():
    assert adventure.str_to_int("three") == 3
    assert adventure.str_to_int("10") == 10
    assert adventure.str_to_int("twenty-one") == 21

def test_get_dc_code_and_campaign():
    title = "CCC-WWC-01-01 The Joy of Extradimensional Spaces (Tier 1)"
    code, campaigns = adventure.get_dc_code_and_campaign(title)
    assert code and isinstance(code, str)
    assert isinstance(campaigns, list)
