
import sys
import unittest
import json
import logging
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Ensure PROJECT_ROOT is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Mock paths before importing to avoid I/O side effects during import
with patch('maintaindb.paths.DC_DIR', Path('/fake/dc')), \
     patch('maintaindb.paths.STATS_DIR', Path('/fake/output')):
    from maintaindb import aggregator

class TestAggregatorLogic(unittest.TestCase):
    
    def setUp(self):
        # Reset the global map before each test
        aggregator.all_adventures_map = {}
        # Suppress logging during tests
        logging.getLogger().setLevel(logging.CRITICAL)

    def test_add_to_map_logic(self):
        """Test the logic for adding items to the internal map, including deduplication."""
        # Setup mock maps
        aggregated_by_dc_code = {}
        
        # Use getattr to avoid name mangling of double-underscore function inside a class
        add_to_map = getattr(aggregator, "__add_to_map")
        
        # Test 1: Add a standard adventure
        adv1 = {
            "product_id": "111",
            "full_title": "Test Adv 1",
            "code": "DDAL09-01",
            "date_created": "20200101"
        }
        add_to_map(adv1, aggregated_by_dc_code)
        self.assertIn("111", aggregator.all_adventures_map)
        self.assertEqual(aggregator.all_adventures_map["111"]["code"], "DDAL09-01")

        # Test 2: Add same ID with different data (should update map)
        adv1_update = {
            "product_id": "111",
            "full_title": "Test Adv 1 Updated",
            "code": "DDAL09-01",
            "date_created": "20200102"
        }
        add_to_map(adv1_update, aggregated_by_dc_code)
        self.assertEqual(aggregator.all_adventures_map["111"]["full_title"], "Test Adv 1 Updated")

        # Test 3: Normalize DDEX code
        adv2 = {
            "product_id": "222",
            "full_title": "Legacy Adv",
            "code": "DDEX3-02" # Should become DDEX03-02
        }
        add_to_map(adv2, aggregated_by_dc_code)
        self.assertEqual(aggregator.all_adventures_map["222"]["code"], "DDEX03-02")


    @patch('maintaindb.aggregator.glob.glob')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump') # Mock writing the output file
    def test_aggregate_normalization(self, mock_json_dump, mock_json_load, mock_file_open, mock_glob):
        """Test the normalization logic inside aggregate()."""
        
        # Mock finding one file
        mock_glob.return_value = ['/fake/dc/1.json']
        
        # Mock the JSON content of that file
        # Test case: string campaign, string tier, null hours
        mock_json_content = {
            "product_id": "999",
            "full_title": "Normalization Test",
            "is_adventure": True,
            "campaign": "Forgotten Realms", # Legacy singular key
            "tiers": "1-4", # String range
            "hours": None,
            "code": "DDAL09-01"
        }
        mock_json_load.return_value = mock_json_content
        
        # Run aggregation
        aggregator.aggregate()
        
        # Verify normalization results in all_adventures_map
        adv = aggregator.all_adventures_map.get("999")
        self.assertIsNotNone(adv)
        
        # Campaign should be a list
        self.assertEqual(adv['campaigns'], ["Forgotten Realms"])
        
        # Tiers should be an int (start of range)
        self.assertEqual(adv['tiers'], 1)
        
        # Hours should be an empty string, not None
        self.assertEqual(adv['hours'], "")

    @patch('maintaindb.aggregator.glob.glob')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_aggregate_filter_non_adventure(self, mock_json_dump, mock_json_load, mock_file_open, mock_glob):
        """Test that non-adventure items are skipped."""
        mock_glob.return_value = ['/fake/dc/bundle.json']
        
        mock_json_content = {
            "product_id": "888",
            "full_title": "Big Bundle",
            "is_adventure": False
        }
        mock_json_load.return_value = mock_json_content
        
        aggregator.aggregate()
        
        self.assertNotIn("888", aggregator.all_adventures_map)

if __name__ == '__main__':
    unittest.main()
