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
        # Test DC codes with 3-digit numbers (the bug fix)
        ("PS-DC-TT-202 May the Cause be with You", "PS-DC-TT-202"),
        ("FR-DC-TT-201 Return to Mountain's Toe Gold Mine", "FR-DC-TT-201"),
        ("FR-DC-TT-301 Seelie, Rabbit, Tricks are for Fools", "FR-DC-TT-301"),
        ("FR-DC-TT-101 Water has no Shape", "FR-DC-TT-101"),
        ("SJ-DC-HBI-001", "SJ-DC-HBI-001"),
        ("RV-DC-HBI-003", "RV-DC-HBI-003"),
        # Test DC codes ending with letters (the bug fix)
        ("FR-DC-ELEMENT-DEATH Everything Changed", "FR-DC-ELEMENT-DEATH"),
        ("Iron Cook (PS-DC-IC)", "PS-DC-IC"),
        ("PS-DC-IC", "PS-DC-IC"),
        # Test DC codes with 2-digit numbers (e.g., PS-DC-PKL-08)
        ("PS-DC-PKL-08 Darker Shade of Pale", "PS-DC-PKL-08"),
        # Test DC codes with multiple dash-number sequences (e.g., FR-DC-DIGM-01-01)
        ("FR-DC-DIGM-01-01 Sweet Tooth", "FR-DC-DIGM-01-01"),
        # Test DC codes ending with alphanumeric (e.g., FR-DC-UCON24)
        ("FR-DC-UCON24 The Icarus Connection", "FR-DC-UCON24"),
        # Test DC codes with dash-number (e.g., PS-DC-NBDD-01, FR-DC-REIN-VR-01)
        ("PS-DC-NBDD-01 The Greatest Gameshow", "PS-DC-NBDD-01"),
        ("FR-DC-REIN-VR-01 The Pale Steed", "FR-DC-REIN-VR-01"),
        # Test CCC codes with series code ending in numbers (e.g., CCC-UCON03)
        ("CCC-UCON03 The Straw Bears", "CCC-UCON03"),
    ]
    
    for title, expected_code in test_cases:
        code, campaigns = get_adventure_code_and_campaigns(title)
        assert code == expected_code, f"Expected {expected_code}, got {code} for title: {title}"


def test_all_bug_fixes_covered():
    """Test that all the reported bug fixes are working correctly."""
    # Bug fix 1: CCC codes with longer series names (e.g., KUMORI)
    code, _ = get_adventure_code_and_campaigns("CCC-KUMORI-01-02 Wretches")
    assert code == "CCC-KUMORI-01-02", f"Failed: got {code}, expected CCC-KUMORI-01-02"
    
    # Bug fix 2: CCC codes without dash after CCC (e.g., CCCTHENT01-03)
    code, _ = get_adventure_code_and_campaigns("CCCTHENT01-03 The Dreaming Relic")
    assert code == "CCC-THENT01-03", f"Failed: got {code}, expected CCC-THENT01-03"
    
    # Bug fix 3: CCC codes with alphanumeric suffixes (e.g., CCC-PRETZ-PLA02)
    code, _ = get_adventure_code_and_campaigns("CCC-PRETZ-PLA02 A Mine of Their Own")
    assert code == "CCC-PRETZ-PLA02", f"Failed: got {code}, expected CCC-PRETZ-PLA02"
    
    # Bug fix 4: CCC codes with 3-digit numbers (e.g., CCC-BWM-005)
    code, _ = get_adventure_code_and_campaigns("CCC-BWM-005 Chasing Madness")
    assert code == "CCC-BWM-005", f"Failed: got {code}, expected CCC-BWM-005"
    
    # Bug fix 5: DC codes with 3-digit numbers (e.g., PS-DC-TT-202)
    code, _ = get_adventure_code_and_campaigns("PS-DC-TT-202 May the Cause be with You")
    assert code == "PS-DC-TT-202", f"Failed: got {code}, expected PS-DC-TT-202"
    
    # Bug fix 6: DC codes ending with letters after a dash (e.g., FR-DC-ELEMENT-DEATH)
    code, _ = get_adventure_code_and_campaigns("FR-DC-ELEMENT-DEATH Everything Changed")
    assert code == "FR-DC-ELEMENT-DEATH", f"Failed: got {code}, expected FR-DC-ELEMENT-DEATH"
    
    # Bug fix 7: DC codes ending with just letters (e.g., PS-DC-IC)
    code, _ = get_adventure_code_and_campaigns("Iron Cook (PS-DC-IC)")
    assert code == "PS-DC-IC", f"Failed: got {code}, expected PS-DC-IC"
    
    # Bug fix 8: DC codes with 2-digit numbers (e.g., PS-DC-PKL-08)
    code, _ = get_adventure_code_and_campaigns("PS-DC-PKL-08 Darker Shade of Pale")
    assert code == "PS-DC-PKL-08", f"Failed: got {code}, expected PS-DC-PKL-08"
    
    # Bug fix 9: DC codes with multiple dash-number sequences (e.g., FR-DC-DIGM-01-01)
    code, _ = get_adventure_code_and_campaigns("FR-DC-DIGM-01-01 Sweet Tooth")
    assert code == "FR-DC-DIGM-01-01", f"Failed: got {code}, expected FR-DC-DIGM-01-01"
    
    # Bug fix 10: DC codes ending with alphanumeric (e.g., FR-DC-UCON24)
    code, _ = get_adventure_code_and_campaigns("FR-DC-UCON24 The Icarus Connection")
    assert code == "FR-DC-UCON24", f"Failed: got {code}, expected FR-DC-UCON24"
    
    # Bug fix 11: DC codes with dash-number sequences (e.g., PS-DC-NBDD-01, FR-DC-REIN-VR-01)
    code, _ = get_adventure_code_and_campaigns("PS-DC-NBDD-01 The Greatest Gameshow")
    assert code == "PS-DC-NBDD-01", f"Failed: got {code}, expected PS-DC-NBDD-01"
    
    code, _ = get_adventure_code_and_campaigns("FR-DC-REIN-VR-01 The Pale Steed")
    assert code == "FR-DC-REIN-VR-01", f"Failed: got {code}, expected FR-DC-REIN-VR-01"
    
    # Bug fix 12: CCC codes with series code ending in numbers directly (e.g., CCC-UCON03)
    code, _ = get_adventure_code_and_campaigns("CCC-UCON03 The Straw Bears")
    assert code == "CCC-UCON03", f"Failed: got {code}, expected CCC-UCON03"


if __name__ == '__main__':
    # Run tests
    test_ccc_codes_with_short_series_names()
    test_ccc_codes_with_long_series_names()
    test_ccc_codes_with_numbers_in_series()
    test_ccc_kumori_specific()
    test_ccc_codes_case_insensitive()
    test_non_ccc_codes_still_work()
    test_all_bug_fixes_covered()
    print("All tests passed!")

