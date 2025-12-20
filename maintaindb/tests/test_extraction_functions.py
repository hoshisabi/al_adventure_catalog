"""
Unit tests for the refactored HTML extraction helper functions.

These tests demonstrate the newly refactored extraction code and ensure
each helper function works correctly in isolation.
"""

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

from bs4 import BeautifulSoup


def test_extract_title_from_html_legacy_format():
    """Test title extraction from legacy HTML format."""
    html = """
    <div class="grid_12 product-title">
        <span itemprop="name">DDAL09-01 Escape from Elturgard</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    title = adventure._extract_title_from_html(soup)
    assert title == "DDAL09-01 Escape from Elturgard"


def test_extract_title_from_html_og_title():
    """Test title extraction from og:title meta tag."""
    html = """
    <meta property="og:title" content="BK-05-02 The Anchorite - Dungeon Masters Guild | Dungeon Masters Guild">
    """
    soup = BeautifulSoup(html, "html.parser")
    title = adventure._extract_title_from_html(soup)
    assert title == "BK-05-02 The Anchorite"


def test_extract_title_from_html_title_tag():
    """Test title extraction from <title> tag as fallback."""
    html = """
    <title>PO-BK-3-12 Rule or Ruin - Dungeon Masters Guild</title>
    """
    soup = BeautifulSoup(html, "html.parser")
    title = adventure._extract_title_from_html(soup)
    assert title == "PO-BK-3-12 Rule or Ruin"


def test_extract_title_from_html_not_found():
    """Test title extraction when no title is found."""
    html = "<div>Some content</div>"
    soup = BeautifulSoup(html, "html.parser")
    title = adventure._extract_title_from_html(soup)
    assert title is None


def test_extract_authors_from_html_legacy_format():
    """Test author extraction from legacy HTML format."""
    html = """
    <div class="grid_12 product-from">
        <a>Author One</a>
        <a>Author Two</a>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    authors = adventure._extract_authors_from_html(soup)
    assert authors == ["Author One", "Author Two"]


def test_extract_authors_from_html_jsonld():
    """Test author extraction from JSON-LD structured data."""
    html = """
    <script type="application/ld+json">
    {
        "author": {
            "name": "John Doe"
        }
    }
    </script>
    """
    soup = BeautifulSoup(html, "html.parser")
    authors = adventure._extract_authors_from_html(soup)
    assert "John Doe" in authors


def test_extract_authors_from_html_angular_format():
    """Test author extraction from new Angular format (table with obs-publisher-or-creators)."""
    html = """
    <table class="table-list full w-lines">
        <tbody>
            <tr>
                <td><p data-codeid="authors" class="u-text-bold"> Author(s) </p></td>
                <td>
                    <obs-publisher-or-creators listonly="authors">
                        <a href="/en/browse?author=%22Richard%20Bellotti%22"> Richard Bellotti</a>
                    </obs-publisher-or-creators>
                </td>
            </tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    authors = adventure._extract_authors_from_html(soup)
    assert "Richard Bellotti" in authors
    assert authors == ["Richard Bellotti"]


def test_extract_authors_from_html_angular_format_multiple():
    """Test author extraction from new Angular format with multiple authors."""
    html = """
    <table class="table-list full w-lines">
        <tbody>
            <tr>
                <td><p data-codeid="authors" class="u-text-bold"> Author(s) </p></td>
                <td>
                    <obs-publisher-or-creators listonly="authors">
                        <a href="/en/browse?author=%22Author%20One%22"> Author One</a>
                        <a href="/en/browse?author=%22Author%20Two%22"> Author Two</a>
                    </obs-publisher-or-creators>
                </td>
            </tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    authors = adventure._extract_authors_from_html(soup)
    assert "Author One" in authors
    assert "Author Two" in authors
    assert len(authors) == 2


def test_extract_authors_from_html_empty():
    """Test author extraction when no authors are found."""
    html = "<div>Some content</div>"
    soup = BeautifulSoup(html, "html.parser")
    authors = adventure._extract_authors_from_html(soup)
    assert authors == []


def test_extract_hours_from_text_single_hour():
    """Test hours extraction for single hour value."""
    text = "This is a 4-hour adventure for Tier 2 characters."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "4"


def test_extract_hours_from_text_range():
    """Test hours extraction for hour range."""
    text = "This adventure takes 2-4 hours to complete."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "2-4"


def test_extract_hours_from_text_word_form():
    """Test hours extraction with word forms."""
    text = "This is a two-hour adventure."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "2"


def test_extract_hours_from_text_word_range():
    """Test hours extraction with word range."""
    text = "This adventure takes two to four hours."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "2-4"


def test_extract_hours_from_text_not_found():
    """Test hours extraction when no hours are found."""
    text = "This is an adventure with no time specified."
    hours = adventure._extract_hours_from_text(text)
    assert hours is None


def test_extract_game_stats_from_text_apl():
    """Test APL extraction from text."""
    text = "Average Party Level (APL) 8"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "8"


def test_extract_game_stats_from_text_tier():
    """Test tier extraction from text."""
    text = "Tier 2 adventure for levels 5-10"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["tiers_raw"] == "2"


def test_extract_game_stats_from_text_level_range():
    """Test level range extraction from text."""
    text = "Levels 1-4 adventure"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["level_range_raw"] == "1-4"


def test_extract_game_stats_from_text_ordinal_levels():
    """Test level range extraction with ordinal numbers."""
    text = "1st-4th level characters"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["level_range_raw"] == "1-4"


def test_extract_game_stats_from_text_all_stats():
    """Test extraction of all game stats at once."""
    text = "Tier 2 adventure for APL 8, Levels 5-10"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["tiers_raw"] == "2"
    assert stats["apl_raw"] == "8"
    assert stats["level_range_raw"] == "5-10"


def test_extract_price_from_html_meta_itemprop():
    """Test price extraction from meta itemprop."""
    html = """
    <meta itemprop="price" content="4.99">
    """
    soup = BeautifulSoup(html, "html.parser")
    price = adventure._extract_price_from_html(soup)
    assert price == 4.99


def test_extract_price_from_html_div_price():
    """Test price extraction from div.price."""
    html = """
    <div class="price">$4.99</div>
    """
    soup = BeautifulSoup(html, "html.parser")
    price = adventure._extract_price_from_html(soup)
    assert price == 4.99


def test_extract_price_from_html_price_old():
    """Test price extraction from div.price-old."""
    html = """
    <div class="price-old">$9.99</div>
    """
    soup = BeautifulSoup(html, "html.parser")
    price = adventure._extract_price_from_html(soup)
    assert price == 9.99


def test_extract_price_from_html_not_found():
    """Test price extraction when no price is found."""
    html = "<div>Some content</div>"
    soup = BeautifulSoup(html, "html.parser")
    price = adventure._extract_price_from_html(soup)
    assert price is None


def test_extract_jsonld_price():
    """Test price extraction from JSON-LD structured data."""
    html = """
    <script type="application/ld+json">
    {
        "offers": {
            "price": "4.99"
        }
    }
    </script>
    """
    soup = BeautifulSoup(html, "html.parser")
    price = adventure._extract_jsonld_price(soup)
    assert price == 4.99


def test_extract_pwyw_info_from_html_flag():
    """Test PWYW flag detection."""
    html = """
    <input name="pwyw_price" value="1.00">
    """
    soup = BeautifulSoup(html, "html.parser")
    pwyw_info = adventure._extract_pwyw_info_from_html(soup)
    assert pwyw_info["pwyw_flag_raw"] is True


def test_extract_pwyw_info_from_html_suggested_price():
    """Test PWYW suggested price extraction."""
    html = """
    <div pwyw_average="1.00"></div>
    """
    soup = BeautifulSoup(html, "html.parser")
    pwyw_info = adventure._extract_pwyw_info_from_html(soup)
    assert pwyw_info["suggested_price_raw"] == 1.00


def test_extract_pwyw_info_from_html_text():
    """Test PWYW suggested price from visible text."""
    html = """
    <div>Suggested Price $1.00</div>
    """
    soup = BeautifulSoup(html, "html.parser")
    pwyw_info = adventure._extract_pwyw_info_from_html(soup)
    assert pwyw_info["suggested_price_raw"] == 1.00


def test_extract_pwyw_info_from_html_not_found():
    """Test PWYW extraction when no PWYW info is found."""
    html = "<div>Regular product</div>"
    soup = BeautifulSoup(html, "html.parser")
    pwyw_info = adventure._extract_pwyw_info_from_html(soup)
    assert pwyw_info["pwyw_flag_raw"] is False
    assert pwyw_info["suggested_price_raw"] is None

