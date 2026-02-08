
import sys
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from aggregator import create_catalog_entry
except ImportError:
    from maintaindb.aggregator import create_catalog_entry

def test_bitmask_flags():
    # cc=1, dc=2, sm=4
    # All flags
    adv = {
        'community_content': True,
        'dungeoncraft': True,
        'salvage_mission': True
    }
    entry = create_catalog_entry(adv)
    assert entry['f'] == 7

    # Just CC
    adv = {'community_content': True}
    entry = create_catalog_entry(adv)
    assert entry['f'] == 1

    # DC and SM
    adv = {'dungeoncraft': True, 'salvage_mission': True}
    entry = create_catalog_entry(adv)
    assert entry['f'] == 6

    # No flags -> 'f' should be missing
    adv = {}
    entry = create_catalog_entry(adv)
    assert 'f' not in entry

def test_campaign_bitmask():
    # FR=1, Eberron=2, Ravenloft=4, Dragonlance=8
    
    # Multiple campaigns
    adv = {'campaigns': ['Forgotten Realms', 'Eberron']}
    entry = create_catalog_entry(adv)
    assert entry['p'] == 3

    # All campaigns
    adv = {'campaigns': ['Forgotten Realms', 'Eberron', 'Ravenloft', 'Dragonlance']}
    entry = create_catalog_entry(adv)
    assert entry['p'] == 15

    # Single campaign (string)
    adv = {'campaigns': 'Ravenloft'}
    entry = create_catalog_entry(adv)
    assert entry['p'] == 4

    # No known campaigns
    adv = {'campaigns': ['Unknown']}
    entry = create_catalog_entry(adv)
    assert 'p' not in entry

def test_url_optimization():
    # Standard URL
    adv = {
        'product_id': '123456',
        'url': 'https://www.dmsguild.com/product/123456/?affiliate_id=171040'
    }
    entry = create_catalog_entry(adv)
    assert 'u' not in entry

    # Suffix URL
    adv = {
        'product_id': '123456-2',
        'url': 'https://www.dmsguild.com/product/123456/?affiliate_id=171040'
    }
    entry = create_catalog_entry(adv)
    assert 'u' not in entry

    # Non-standard URL
    adv = {
        'product_id': '123456',
        'url': 'https://www.dmsguild.com/product/123456/Some-Title?affiliate_id=171040'
    }
    entry = create_catalog_entry(adv)
    assert entry['u'] == adv['url']

    # URL without affiliate ID
    adv = {
        'product_id': '123456',
        'url': 'https://www.dmsguild.com/product/123456/'
    }
    entry = create_catalog_entry(adv)
    assert entry['u'] == adv['url']

def test_optional_fields():
    # Seed
    adv = {'seed': 'Some seed'}
    entry = create_catalog_entry(adv)
    assert entry['e'] == 'Some seed'

    # Missing seed
    adv = {}
    entry = create_catalog_entry(adv)
    assert 'e' not in entry

    # Last update
    adv = {'last_update': '20260207'}
    entry = create_catalog_entry(adv)
    assert entry['lu'] == '20260207'
