
import sys
import os
import pytest
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure PROJECT_ROOT is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import adventure
    import adventure_utils
except ModuleNotFoundError:
    from maintaindb import adventure
    from maintaindb import adventure_utils

@pytest.fixture
def bs_555262():
    # Attempt to find the fixture file
    paths = [
        Path("dmsguildinfo/dmsguildinfo-555262.html"),
        Path("maintaindb/dmsguildinfo/dmsguildinfo-555262.html"),
        Path(__file__).resolve().parents[1] / "dmsguildinfo" / "dmsguildinfo-555262.html"
    ]
    p = None
    for cand in paths:
        if cand.exists():
            p = cand
            break
    
    if not p:
        pytest.skip("HTML fixture dmsguildinfo-555262.html not found.")
    
    return BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "html.parser")

def test_extract_jsonld_sku_logic():
    # Test SKU extraction from JSON-LD
    html = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "Test Adventure",
      "sku": "FR-DC-TEST-01"
    }
    </script>
    """
    soup = BeautifulSoup(html, "html.parser")
    sku = adventure._extract_jsonld_sku(soup)
    assert sku == "FR-DC-TEST-01"

    # Test MPN extraction
    html_mpn = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Product",
      "mpn": "SJ-DC-TEST-02"
    }
    </script>
    """
    soup_mpn = BeautifulSoup(html_mpn, "html.parser")
    sku = adventure._extract_jsonld_sku(soup_mpn)
    assert sku == "SJ-DC-TEST-02"

def test_extract_code_from_description_3digit():
    # Test that 3-digit suffixes are now supported
    text = "Suitable for Adventure League style gameplay using the code FR-DC-SCROOGE-002."
    result = adventure._extract_code_from_description(text)
    assert result is not None
    code, campaigns = result
    assert code == "FR-DC-SCROOGE-002"
    assert "Forgotten Realms" in campaigns

    # Test with 1 and 2 digits as well
    text2 = "Using code RV-DC-TEST-1"
    result2 = adventure._extract_code_from_description(text2)
    assert result2[0] == "RV-DC-TEST-1"

    text3 = "Using code WBW-DC-TEST-12"
    result3 = adventure._extract_code_from_description(text3)
    assert result3[0] == "WBW-DC-TEST-12"

@pytest.mark.parametrize("text, expected", [
    ("Adventure Code: PO-MURGHÔM-AL-01-00\n\nDescription", "PO-MURGHÔM-AL-01-00"),
    ("Adventure Code: PO-MURGHÔM-EP-01-01", "PO-MURGHÔM-EP-01-01"),
    ("adventure code po-murghôm-al-01-01", "PO-MURGHÔM-AL-01-01"),
    ("Part of the PO-BK-1-04 series", "PO-BK-1-04"),
    ("Code: PO-BK2-03", "PO-BK2-03"),
])
def test_extract_premier_organization_code_from_description(text, expected):
    result = adventure._extract_code_from_description(text)
    assert result is not None
    code, campaigns = result
    assert code == expected
    assert campaigns == ["Forgotten Realms"]

def test_premier_organization_code_in_title():
    code, campaigns = adventure_utils.get_adventure_code_and_campaigns("PO-MURGHÔM-AL-01-01 Trouble at Kobold Crown")
    assert code == "PO-MURGHÔM-AL-01-01"
    assert campaigns == ["Forgotten Realms"]

def test_en_dash_ranges_in_description():
    html = """
    <title>The Grand Bazaar of Skalnaedyr - Dungeon Masters Guild</title>
    <div class="prod-content">
    Format: D&amp;D Adventurers League Adventure (Tier 1)
    Optimized For: APL 3 (Levels 1–4)
    Length: 4–6 Hours
    Adventure Code: PO-MURGHÔM-AL-01-00
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    data = adventure.extract_data_from_html(soup, product_id="999998")
    assert data["code"] == "PO-MURGHÔM-AL-01-00"
    assert data["hours"] == "4-6"
    assert data["level_range"] == "1-4"
    assert data["is_adventure"] is True

def test_full_extraction_555262(bs_555262):
    # This tests the integration of JSON-LD SKU and description fallback
    data = adventure.extract_data_from_html(bs_555262, product_id="555262")
    
    # The code should be detected either from SKU or description
    assert data["code"] == "FR-DC-SCROOGE-002"
    assert data["is_adventure"] is True
    assert "Forgotten Realms" in data["campaigns"]

def test_code_normalization_in_extraction():
    # Test that SKU-based code is normalized (uppercased)
    html = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "Product",
      "sku": "fr-dc-lowercase-01"
    }
    </script>
    <div class="prod-content">This is a test.</div>
    """
    soup = BeautifulSoup(html, "html.parser")
    # We need a product_id for extraction
    data = adventure.extract_data_from_html(soup, product_id="999999")
    assert data["code"] == "FR-DC-LOWERCASE-01"
