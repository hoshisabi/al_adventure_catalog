
import sys
import unittest
from pathlib import Path

# Ensure PROJECT_ROOT is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from maintaindb.adventure import merge_adventure_data
except ImportError:
    from adventure import merge_adventure_data

class TestMergeLogic(unittest.TestCase):

    def test_merge_basic_new_fields(self):
        """Test that new non-empty fields populate empty existing fields."""
        existing = {
            "title": "Old Title",
            "hours": None,
            "seed": None
        }
        new_data = {
            "title": "New Title",
            "hours": "4",
            "seed": None
        }
        # Default behavior: updates existing if new is not empty
        result = merge_adventure_data(existing, new_data)
        self.assertEqual(result["title"], "New Title")
        self.assertEqual(result["hours"], "4")
        self.assertIsNone(result["seed"])

    def test_merge_preserve_existing_when_new_is_empty(self):
        """Test that existing valid data is kept if new data is empty/null."""
        existing = {
            "title": "Existing Title",
            "hours": "4",
            "seed": "Manual Seed"
        }
        new_data = {
            "title": None,
            "hours": "",
            "seed": None
        }
        result = merge_adventure_data(existing, new_data)
        self.assertEqual(result["title"], "Existing Title")
        self.assertEqual(result["hours"], "4")
        self.assertEqual(result["seed"], "Manual Seed")

    def test_careful_mode_preserves_existing(self):
        """Test that careful_mode=True prevents overwriting existing non-empty data."""
        existing = {
            "title": "Important Manual Title",
            "hours": "4",
        }
        new_data = {
            "title": "Scraped Title",
            "hours": "5",
        }
        result = merge_adventure_data(existing, new_data, careful_mode=True)
        self.assertEqual(result["title"], "Important Manual Title") # Should keep existing
        self.assertEqual(result["hours"], "4") # Should keep existing

    def test_careful_mode_fills_gaps(self):
        """Test that careful_mode=True still fills in missing data."""
        existing = {
            "title": "Manual Title",
            "hours": None, # Missing
        }
        new_data = {
            "title": "Scraped Title",
            "hours": "4",
        }
        result = merge_adventure_data(existing, new_data, careful_mode=True)
        self.assertEqual(result["title"], "Manual Title") # Preserved
        self.assertEqual(result["hours"], "4") # Filled in

    def test_force_overwrite_updates_values(self):
        """Test that force_overwrite=True updates values even if existing is non-empty."""
        existing = {
            "title": "Old Title",
            "hours": "2",
        }
        new_data = {
            "title": "New Title",
            "hours": "4",
        }
        result = merge_adventure_data(existing, new_data, force_overwrite=True)
        self.assertEqual(result["title"], "New Title")
        self.assertEqual(result["hours"], "4")

    def test_force_overwrite_preserves_manual_fields_if_new_is_empty(self):
        """
        Test that force_overwrite=True DOES NOT wipe out existing data if the new data is empty.
        This is critical for fields like 'seed' that might not be in the scrape.
        """
        existing = {
            "title": "Old Title",
            "seed": "Manual Seed", # Exists locally
        }
        new_data = {
            "title": "New Title",
            "seed": None, # Missing in scrape
        }
        result = merge_adventure_data(existing, new_data, force_overwrite=True)
        self.assertEqual(result["title"], "New Title") # Updated
        self.assertEqual(result["seed"], "Manual Seed") # Preserved!

    def test_handle_none_string_title(self):
        """Test that 'None' string titles are treated as empty."""
        existing = {
            "full_title": "Real Title",
        }
        new_data = {
            "full_title": "None", # Literal string "None" often returned by extractors
        }
        # Should preserve existing
        result = merge_adventure_data(existing, new_data)
        self.assertEqual(result["full_title"], "Real Title")

    def test_last_update_logic(self):
        """Test that last_update takes the maximum date."""
        existing = { "last_update": "20250101" }
        new_data = { "last_update": "20260101" }
        
        result = merge_adventure_data(existing, new_data)
        self.assertEqual(result["last_update"], "20260101")

        # Reverse case
        existing = { "last_update": "20260101" }
        new_data = { "last_update": "20250101" } # e.g. re-scraping an old page?
        
        result = merge_adventure_data(existing, new_data)
        self.assertEqual(result["last_update"], "20260101") # Should keep max

if __name__ == '__main__':
    unittest.main()
