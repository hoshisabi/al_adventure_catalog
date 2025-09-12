import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Make project importable from either repo root or maintaindb package context
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import adventure  # type: ignore
except ModuleNotFoundError:
    from maintaindb import adventure  # type: ignore


def _load_fixture_html(product_id: str) -> BeautifulSoup:
    # Use in-repo processed fixture path
    html_path = PROJECT_ROOT / 'maintaindb' / 'dmsguildinfo' / 'processed' / f'dmsguildinfo-{product_id}.html'
    if not html_path.exists():
        # If the fixture is missing, skip the test gracefully
        import pytest
        pytest.skip(f"Fixture not found: {html_path}")
    html = html_path.read_text(encoding='utf-8', errors='ignore')
    return BeautifulSoup(html, 'html.parser')


def test_pwyw_and_suggested_price_parsed_for_432577():
    soup = _load_fixture_html('432577')
    data = adventure.extract_data_from_html(soup, '432577', existing_data={})

    # Should detect Pay What You Want
    assert 'payWhatYouWant' in data, 'payWhatYouWant not present in parsed data'
    assert data['payWhatYouWant'] is True, 'Expected PWYW to be True for product 432577'

    # Suggested price should be parsed as 1.00
    assert 'suggestedPrice' in data, 'suggestedPrice not present in parsed data'
    assert data['suggestedPrice'] is not None, 'suggestedPrice should not be None for PWYW product'
    # Allow minor float representation differences
    assert abs(float(data['suggestedPrice']) - 1.00) < 1e-6
