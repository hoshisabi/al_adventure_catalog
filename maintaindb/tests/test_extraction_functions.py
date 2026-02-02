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


def test_extract_hours_from_text_slash_separator():
    """Test hours extraction with slash separator."""
    text = "This is a 2/4 hour adventure."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "2-4"


def test_extract_hours_from_text_to_separator():
    """Test hours extraction with 'to' separator."""
    text = "This adventure takes 3 to 5 hours."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "3-5"


def test_extract_hours_from_text_hyphenated_word():
    """Test hours extraction with hyphenated format like '2-hour'."""
    text = "This is a 2-hour adventure."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "2"


def test_extract_hours_from_text_no_space():
    """Test hours extraction with no space before 'hour'."""
    text = "This is a 4hour adventure."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "4"


def test_extract_hours_from_text_word_numbers():
    """Test hours extraction with word numbers in range."""
    text = "This adventure takes three to six hours."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "3-6"


def test_extract_hours_from_text_mixed_word_numeric():
    """Test hours extraction with mixed word and numeric."""
    text = "This is a two to 4 hour adventure."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "2-4"


def test_extract_hours_from_text_multiple_mentions():
    """Test hours extraction when multiple hour mentions exist (should get first)."""
    text = "This is a 2-hour adventure that can be extended to 4 hours."
    hours = adventure._extract_hours_from_text(text)
    # Should extract the first mention
    assert hours == "2"


def test_extract_hours_from_text_hr_abbreviation():
    """Test hours extraction with 'hr' abbreviation."""
    text = "This adventure takes 3 hr to complete."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "3"


def test_extract_hours_from_text_hours_plural():
    """Test hours extraction with plural 'hours'."""
    text = "This adventure takes 4 hours."
    hours = adventure._extract_hours_from_text(text)
    assert hours == "4"


def test_extract_hours_from_text_ordinal_hours():
    """Test hours extraction with ordinal numbers (like 'first hour')."""
    # Note: This might not match, but tests edge case
    text = "In the first hour, players explore."
    hours = adventure._extract_hours_from_text(text)
    # This might match 'first' as '1' or might not match at all
    # Just ensuring it doesn't crash
    assert hours is None or hours == "1"


def test_extract_game_stats_from_text_apl():
    """Test APL extraction from text."""
    text = "Average Party Level (APL) 8"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "8"


def test_extract_game_stats_from_text_apl_colon():
    """Test APL extraction with colon separator."""
    text = "Optimized for APL: 3 characters"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "3"


def test_extract_game_stats_from_text_apl_dash():
    """Test APL extraction with dash separator."""
    text = "Designed for APL - 5 play"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "5"


def test_extract_game_stats_from_text_apl_simple():
    """Test APL extraction with simple space separator."""
    text = "This adventure is for APL 7"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "7"


def test_extract_game_stats_from_text_apl_average_party_level():
    """Test APL extraction using full 'Average Party Level' phrase."""
    text = "Average Party Level 10 adventure"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "10"


def test_extract_game_stats_from_text_apl_average_party_level_colon():
    """Test Average Party Level with colon separator."""
    text = "Average Party Level: 6 characters"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "6"


def test_extract_game_stats_from_text_apl_in_context():
    """Test APL extraction in realistic context text."""
    text = "A Four-Hour Adventure for Tier 4 Characters. Optimized for APL: 18."
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] == "18"
    assert stats["tiers_raw"] == "4"


def test_extract_game_stats_from_text_apl_not_found():
    """Test APL extraction when no APL is present."""
    text = "This is an adventure with no APL mentioned."
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["apl_raw"] is None


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


def test_extract_game_stats_from_text_level_range_singular():
    """Test level range extraction with singular 'Level'."""
    text = "Level 5-10 characters"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["level_range_raw"] == "5-10"


def test_extract_game_stats_from_text_level_range_lowercase():
    """Test level range extraction with lowercase 'level'."""
    text = "For level 11-16 characters"
    stats = adventure._extract_game_stats_from_text(text)
    assert stats["level_range_raw"] == "11-16"


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


# ============================================================================
# INFERENCE TESTS: APL/Tier/Level Range Defaults
# ============================================================================

def test_infer_tier_from_apl_tier1():
    """Test deriving Tier 1 from APL in range 1-4."""
    data = {"tiers": None, "apl": 3, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 1


def test_infer_tier_from_apl_tier2():
    """Test deriving Tier 2 from APL in range 5-10."""
    data = {"tiers": None, "apl": 7, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 2


def test_infer_tier_from_apl_tier3():
    """Test deriving Tier 3 from APL in range 11-16."""
    data = {"tiers": None, "apl": 13, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 3


def test_infer_tier_from_apl_tier4():
    """Test deriving Tier 4 from APL in range 17-20."""
    data = {"tiers": None, "apl": 18, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 4


def test_infer_tier_from_apl_boundary_values():
    """Test deriving tier from APL at boundary values."""
    test_cases = [
        (1, 1), (4, 1),  # Tier 1 boundaries
        (5, 2), (10, 2),  # Tier 2 boundaries
        (11, 3), (16, 3),  # Tier 3 boundaries
        (17, 4), (20, 4),  # Tier 4 boundaries
    ]
    for apl, expected_tier in test_cases:
        data = {"tiers": None, "apl": apl, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
        result = adventure._infer_missing_adventure_data(data)
        assert result["tiers"] == expected_tier, f"APL {apl} should map to Tier {expected_tier}"


def test_infer_tier_from_level_range_tier1():
    """Test deriving Tier 1 from level range 1-4."""
    data = {"tiers": None, "apl": None, "level_range": "1-4", "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 1


def test_infer_tier_from_level_range_tier2():
    """Test deriving Tier 2 from level range 5-10."""
    data = {"tiers": None, "apl": None, "level_range": "5-10", "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 2


def test_infer_tier_from_level_range_tier3():
    """Test deriving Tier 3 from level range 11-16."""
    data = {"tiers": None, "apl": None, "level_range": "11-16", "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 3


def test_infer_tier_from_level_range_tier4():
    """Test deriving Tier 4 from level range 17-20."""
    data = {"tiers": None, "apl": None, "level_range": "17-20", "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 4


def test_infer_tier_from_level_range_prefers_apl():
    """Test that APL takes precedence over level range for tier inference."""
    # If both APL and level_range are present, APL should be used
    data = {"tiers": None, "apl": 8, "level_range": "1-4", "full_title": "Test Adventure", "code": "TEST-01"}  # APL suggests Tier 2, level_range suggests Tier 1
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 2  # Should use APL


def test_infer_level_range_from_tier_tier1():
    """Test deriving level range 1-4 from Tier 1."""
    data = {"tiers": 1, "apl": None, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "1-4"


def test_infer_level_range_from_tier_tier2():
    """Test deriving level range 5-10 from Tier 2."""
    data = {"tiers": 2, "apl": None, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "5-10"


def test_infer_level_range_from_tier_tier3():
    """Test deriving level range 11-16 from Tier 3."""
    data = {"tiers": 3, "apl": None, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "11-16"


def test_infer_level_range_from_tier_tier4():
    """Test deriving level range 17-20 from Tier 4."""
    data = {"tiers": 4, "apl": None, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "17-20"


def test_infer_level_range_from_tier_overrides_invalid():
    """Test that invalid level_range is overridden by tier-derived value."""
    data = {"tiers": 2, "apl": None, "level_range": "invalid", "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "5-10"


def test_infer_level_range_from_tier_overrides_empty():
    """Test that empty level_range is overridden by tier-derived value."""
    data = {"tiers": 3, "apl": None, "level_range": "", "full_title": "Test Adventure", "code": "TEST-01"}
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "11-16"


def test_infer_level_range_from_tier_preserves_valid():
    """Test that valid existing level_range is preserved."""
    data = {"tiers": 2, "apl": None, "level_range": "5-8", "full_title": "Test Adventure", "code": "TEST-01"}  # Valid but different from default
    result = adventure._infer_missing_adventure_data(data)
    assert result["level_range"] == "5-8"  # Should preserve existing valid range


def test_infer_no_override_existing_tier():
    """Test that existing tier is not overridden."""
    data = {"tiers": 3, "apl": 5, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}  # APL suggests Tier 2, but tier is already set
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 3  # Should preserve existing tier


def test_infer_cascade_apl_to_tier_to_level_range():
    """Test inference cascade: APL -> Tier -> Level Range."""
    data = {"tiers": None, "apl": 12, "level_range": None, "full_title": "Test Adventure", "code": "TEST-01"}  # APL 12 -> Tier 3 -> Level 11-16
    result = adventure._infer_missing_adventure_data(data)
    assert result["tiers"] == 3
    assert result["level_range"] == "11-16"


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

