import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maintaindb.adventure_normalizers import AdventureDataNormalizer

def test_normalize_title_strips_code():
    normalizer = AdventureDataNormalizer()
    
    test_cases = [
        # Base case no brackets
        ({"code": "FR-DC-F&ADDM-LES2", "full_title_raw": "FR-DC-F&ADDM-LES2 The Draught of Qebehsenuef"}, "The Draught of Qebehsenuef"),
        ({"code": "FR-DC-F&ADDM-LES2", "full_title_raw": "The Draught of Qebehsenuef FR-DC-F&ADDM-LES2"}, "The Draught of Qebehsenuef"),
        
        # With various brackets
        ({"code": "FR-DC-F&ADDM-GW1", "full_title_raw": "[FR-DC-F&ADDM-GW1] The Genie's Wishes, Chap. 1 Cold Open"}, "The Genie's Wishes, Chap. 1 Cold Open"),
        ({"code": "FR-DC-F&ADDM-GW1", "full_title_raw": "The Genie's Wishes, Chap. 1 Cold Open (FR-DC-F&ADDM-GW1)"}, "The Genie's Wishes, Chap. 1 Cold Open"),
        ({"code": "FR-DC-F&ADDM-LES2", "full_title_raw": "<FR-DC-F&ADDM-LES2> The Draught of Qebehsenuef"}, "The Draught of Qebehsenuef"),
        
        # With trailing/leading punctuation
        ({"code": "TEST-01", "full_title_raw": "TEST-01, Moonshire"}, "Moonshire"),
        ({"code": "TEST-01", "full_title_raw": "Moonshire - TEST-01"}, "Moonshire"),
        ({"code": "TEST-01", "full_title_raw": "Moonshire : TEST-01"}, "Moonshire"),
        
        # With optional trailing letter
        ({"code": "SJ-DC-PANDORA-JWEI-03A", "full_title_raw": "SJ-DC-PANDORA-JWEI-03A A, Title Here"}, "A, Title Here"),
        
        # Shouldn't strip if it is the only thing
        ({"code": "TEST-01", "full_title_raw": "TEST-01"}, "TEST-01"),
        ({"code": "TEST-01", "full_title_raw": "[TEST-01]"}, "[TEST-01]")
    ]
    
    for data, expected in test_cases:
        res = normalizer.normalize(data)
        assert res["title"] == expected, f"Failed: expected '{expected}', got '{res['title']}' for '{data['full_title_raw']}'"

if __name__ == '__main__':
    test_normalize_title_strips_code()
    print("All title normalization tests passed!")
