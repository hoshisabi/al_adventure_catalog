"""
Unit tests for adventure_utils module, specifically testing get_adventure_code_and_campaigns
for CCC codes with various series name lengths.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Try both layout options: project root module or package under maintaindb
try:
    from adventure_utils import get_adventure_code_and_campaigns  # type: ignore
except ModuleNotFoundError:
    from maintaindb.adventure_utils import get_adventure_code_and_campaigns  # type: ignore


def test_ccc_codes_with_short_series_names():
    """Test CCC codes with 2-3 letter series names (original pattern)."""
    test_cases = [
        ("CCC-BMG-01", "CCC-BMG-01"),
        ("CCC-GSP-01-01", "CCC-GSP-01-01"),
        ("CCC-WWC-01-01 The Joy of Extradimensional Spaces", "CCC-WWC-01-01"),
    ]
    
    for title, expected_code in test_cases:
        code, campaigns = get_adventure_code_and_campaigns(title)
        assert code == expected_code, f"Expected {expected_code}, got {code} for title: {title}"
        assert isinstance(campaigns, list)


def test_ccc_codes_with_long_series_names():
    """Test CCC codes with longer series names (4+ letters) - the bug fix."""
    test_cases = [
        ("CCC-KUMORI-01-02 Wretches", "CCC-KUMORI-01-02"),
        ("CCC-KUMORI-01-01 Wreckers", "CCC-KUMORI-01-01"),
        ("CCC-SFBAY-04-02 Under Earth & Stone", "CCC-SFBAY-04-02"),
        ("CCC-SFBAY-02-01", "CCC-SFBAY-02-01"),
        ("CCC-PDXAGE-02-01 The Dark Hunt", "CCC-PDXAGE-02-01"),
        ("CCC-PDXAGE-01-01 The White Well", "CCC-PDXAGE-01-01"),
        ("CCC-PRIORY-01 Maritime Mayhem", "CCC-PRIORY-01"),
        ("CCC-PRIORY-02 Prison Pitfalls", "CCC-PRIORY-02"),
        ("CCC-STORM-01 The Barrows of Solina", "CCC-STORM-01"),
        ("CCC-LINKS-01 Champion of the People", "CCC-LINKS-01"),
        ("CCC-LINKS-02 The Secrets We Keep", "CCC-LINKS-02"),
        # Test codes with alphanumeric suffixes (e.g., -PLA02, -005)
        ("CCC-PRETZ-PLA02 A Mine of Their Own", "CCC-PRETZ-PLA02"),
        ("CCC-PRETZ-PLA01 The Mystery at Coppertop Manor", "CCC-PRETZ-PLA01"),
        ("CCC-PRETZ-PLA03 The Necroforge", "CCC-PRETZ-PLA03"),
        ("CCC-BWM-005 Chasing Madness", "CCC-BWM-005"),
        ("CCC-BWM-001 Howling on the Moonsea", "CCC-BWM-001"),
        ("CCC-BWM-06 Introduction to Adventuring", "CCC-BWM-06"),
        ("CCC-BWM-04-02 Thralls of Zuggtmoy", "CCC-BWM-04-02"),
        ("CCC-BWM-007-01 The Beast Beneath", "CCC-BWM-007-01"),
    ]
    
    for title, expected_code in test_cases:
        code, campaigns = get_adventure_code_and_campaigns(title)
        assert code == expected_code, f"Expected {expected_code}, got {code} for title: {title}"
        assert isinstance(campaigns, list)


def test_ccc_codes_with_numbers_in_series():
    """Test CCC codes where series name includes numbers (e.g., ODFC01, THENT01)."""
    test_cases = [
        ("CCC-ODFC01-01 Hammer and Anvil", "CCC-ODFC01-01"),
        ("CCC-ODFC01-02 Black Blades, Black Wings", "CCC-ODFC01-02"),
        ("CCC-ODFC01-03 Elders' Eyes Upon You", "CCC-ODFC01-03"),
        ("CCC-THENT01-01 Beneath the Surface", "CCC-THENT01-01"),
        ("CCC-THENT01-02 Those That Dwell Beneath", "CCC-THENT01-02"),
        ("CCC-THENT01-03 The Dreaming Relic", "CCC-THENT01-03"),
        # Test cases without dash after CCC (the bug fix)
        ("CCCTHENT01-01 Beneath the Surface", "CCC-THENT01-01"),
        ("CCCTHENT01-02 Those That Dwell Beneath", "CCC-THENT01-02"),
        ("CCCTHENT01-03 The Dreaming Relic", "CCC-THENT01-03"),
        ("CCC-SRCC01-01 Trouble in the Old City", "CCC-SRCC01-01"),
        ("CCC-SRCC01-02 Down the River of Snakes", "CCC-SRCC01-02"),
        ("CCC-SRCC01-03 Altar of the Smoldering Eye", "CCC-SRCC01-03"),
        ("CCC-SCAR01-01 Corrupted Artery", "CCC-SCAR01-01"),
        ("CCC-SCAR01-02 Glister By Light", "CCC-SCAR01-02"),
        ("CCC-MACE01-01 The Blight of Geoffrey", "CCC-MACE01-01"),
        ("CCC-MACE01-02 A Panthers Peril", "CCC-MACE01-02"),
        ("CCC-MACE01-03 Haunted Memories", "CCC-MACE01-03"),
        ("CCC-HATMS01-01", "CCC-HATMS01-01"),
        ("CCC-HATMS01-02", "CCC-HATMS01-02"),
        ("CCC-HATMS01-03", "CCC-HATMS01-03"),
        ("CCC-TAROT01-03 A Martyred Heart", "CCC-TAROT01-03"),
        ("CCC-TAROT01-02 By the Light of the Moon", "CCC-TAROT01-02"),
        ("CCC-MIND01-01 Lost in Thought", "CCC-MIND01-01"),
        ("CCC-MIND01-02 Mind Trip", "CCC-MIND01-02"),
        ("CCC-MIND01-03 Dream Walkers", "CCC-MIND01-03"),
        ("CCC-YLRA01-01 Her Dying Wish", "CCC-YLRA01-01"),
        ("CCC-YLRA01-02 Uneasy Lies the Head", "CCC-YLRA01-02"),
        ("CCC-YLRA01-03 Bound By Duty", "CCC-YLRA01-03"),
    ]
    
    for title, expected_code in test_cases:
        code, campaigns = get_adventure_code_and_campaigns(title)
        assert code == expected_code, f"Expected {expected_code}, got {code} for title: {title}"
        assert isinstance(campaigns, list)


def test_ccc_kumori_specific():
    """Specific test for the reported bug: CCC-KUMORI-01-02."""
    title = "CCC-KUMORI-01-02 Wretches"
    code, campaigns = get_adventure_code_and_campaigns(title)
    assert code == "CCC-KUMORI-01-02", f"Expected CCC-KUMORI-01-02, got {code}"
    assert isinstance(campaigns, list)
    # This code should be recognized as an adventure (code is not None)
    assert code is not None


def test_ccc_codes_case_insensitive():
    """Test that CCC codes are matched case-insensitively."""
    test_cases = [
        ("ccc-kumori-01-02 Wretches", "CCC-KUMORI-01-02"),
        ("Ccc-Sfbay-04-02", "CCC-SFBAY-04-02"),
        ("ccc-odfc01-01", "CCC-ODFC01-01"),
    ]
    
    for title, expected_code in test_cases:
        code, campaigns = get_adventure_code_and_campaigns(title)
        assert code == expected_code, f"Expected {expected_code}, got {code} for title: {title}"


def test_non_ccc_codes_still_work():
    """Test that other adventure code patterns still work correctly."""
    test_cases = [
        ("DDAL09-01 Escape from Elturgard", "DDAL09-01"),
        ("DDEX3-01", "DDEX03-01"),  # Should normalize to zero-padded
        ("DDAL5-01", "DDAL05-01"),  # Should normalize to zero-padded
        ("WBW-DC-STRAT-TALES-01", "WBW-DC-STRAT-TALES-01"),
        ("SJ-DC-01", "SJ-DC-01"),
    ]
    
    for title, expected_code in test_cases:
        code, campaigns = get_adventure_code_and_campaigns(title)
        assert code == expected_code, f"Expected {expected_code}, got {code} for title: {title}"


if __name__ == '__main__':
    # Run tests
    test_ccc_codes_with_short_series_names()
    test_ccc_codes_with_long_series_names()
    test_ccc_codes_with_numbers_in_series()
    test_ccc_kumori_specific()
    test_ccc_codes_case_insensitive()
    test_non_ccc_codes_still_work()
    print("All tests passed!")

