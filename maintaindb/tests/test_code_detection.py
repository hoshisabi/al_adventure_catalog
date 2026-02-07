
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
except ModuleNotFoundError:
    from maintaindb import adventure

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
