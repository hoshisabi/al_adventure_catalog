import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from maintaindb.stats import (
        normalize_tier_stats,
        normalize_duration_stats,
        _tier_label,
    )
except ImportError:
    from stats import (
        normalize_tier_stats,
        normalize_duration_stats,
        _tier_label,
    )


def test_tier_label_valid_and_invalid():
    assert _tier_label(1) == 'Tier 1'
    assert _tier_label(4) == 'Tier 4'
    assert _tier_label(0) is None
    assert _tier_label(None) is None


def test_normalize_tier_stats_canonical_keys():
    raw = {'Tier 1': 10, 'Tier 2': 5, 'Unknown': 2}
    out = normalize_tier_stats(raw)
    assert out['Tier 1'] == 10
    assert out['Unknown'] == 2


def test_normalize_tier_stats_zero_indexed_legacy():
    raw = {'0': 830, '1': 869, '2': 344, '3': 92, '4': 10}
    out = normalize_tier_stats(raw)
    assert out['Tier 1'] == 830
    assert out['Tier 2'] == 869
    assert out['Tier 4'] == 92
    assert out['Unknown'] == 10


def test_normalize_tier_stats_one_indexed_legacy():
    raw = {'1': 835, '2': 871, '3': 345, '4': 92}
    out = normalize_tier_stats(raw)
    assert out['Tier 1'] == 835
    assert out['Tier 4'] == 92


def test_normalize_duration_stats_legacy_numeric_keys():
    raw = {'1': 23, '2': 621, '4': 1515, 'All Others': 221, 'Unknown': 61}
    out = normalize_duration_stats(raw)
    assert out['1 Hours'] == 23
    assert out['2 Hours'] == 621
    assert out['4 Hours'] == 1515
    assert out['All Others'] == 221


try:
    from maintaindb.adventure_utils import resolve_al_season, AL_SEASON_ORDER
except ImportError:
    from adventure_utils import resolve_al_season, AL_SEASON_ORDER


def test_resolve_al_season_numeric_and_named():
    assert resolve_al_season(code='DDAL09-01') == '9 - Avernus Rising'
    assert resolve_al_season(code='WBW-DC-TEST-01') == '11 - Wild Beyond the Witchlight'
    assert resolve_al_season(code='SJ-DC-FOO-01') == '12 - Spelljammer'
    assert resolve_al_season(code='PS-DC-BAR-01') == '13 - Planescape'
    assert resolve_al_season(code='DC-POA-01') == '10 - Icewind Dale'


def test_resolve_al_season_excludes_non_al_programs():
    assert resolve_al_season(season='Oracle of War') is None
    assert resolve_al_season(code='EB-EP-01') is None
    assert resolve_al_season(season='Embers of War') is None
    assert resolve_al_season(season='Ravenloft Dungeoncraft') is None


def test_al_season_order_covers_1_through_13():
    assert len(AL_SEASON_ORDER) == 13
    assert AL_SEASON_ORDER[0].startswith('1 - ')
    assert AL_SEASON_ORDER[10].startswith('11 - ')
    assert AL_SEASON_ORDER[12].startswith('13 - ')
