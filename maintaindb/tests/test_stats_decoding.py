
import sys
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from stats import catalog_entry_to_dungeoncraft_params
    from adventure_utils import CAMPAIGN_BITMASK
except ImportError:
    from maintaindb.stats import catalog_entry_to_dungeoncraft_params
    from maintaindb.adventure_utils import CAMPAIGN_BITMASK

def test_catalog_entry_decoding():
    # Test bitmask decoding for campaigns
    entry = {
        'i': '12345',
        'p': 3  # Forgotten Realms (1) | Eberron (2)
    }
    params = catalog_entry_to_dungeoncraft_params(entry)
    assert 'campaigns' in params
    assert isinstance(params['campaigns'], list)
    assert 'Forgotten Realms' in params['campaigns']
    assert 'Eberron' in params['campaigns']
    assert len(params['campaigns']) == 2

def test_date_parsing():
    entry = {
        'd': '20260207'
    }
    params = catalog_entry_to_dungeoncraft_params(entry)
    assert isinstance(params['date_created'], datetime.date)
    assert params['date_created'].year == 2026
    assert params['date_created'].month == 2
    assert params['date_created'].day == 7

def test_missing_fields_handling():
    entry = {
        'i': '12345'
    }
    params = catalog_entry_to_dungeoncraft_params(entry)
    assert params['product_id'] == '12345'
    assert params['date_created'] is None
    assert 'campaigns' not in params

def test_non_bitmask_campaign():
    # Legacy support if campaigns were already a list in JSON (unlikely now but good for robustness)
    entry = {
        'p': ['Forgotten Realms']
    }
    params = catalog_entry_to_dungeoncraft_params(entry)
    assert params['campaigns'] == ['Forgotten Realms']
