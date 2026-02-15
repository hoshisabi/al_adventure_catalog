
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure PROJECT_ROOT is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maintaindb import process_rss

class TestRSSParser(unittest.TestCase):

    def test_extract_product_id(self):
        """Test extraction of product ID from URLs."""
        url = "https://www.dmsguild.com/product/123456/Some-Title"
        self.assertEqual(process_rss._extract_product_id(url), "123456")

        url_no_title = "https://www.dmsguild.com/product/987654/"
        self.assertEqual(process_rss._extract_product_id(url_no_title), "987654")

        # Test invalid or missing ID
        self.assertIsNone(process_rss._extract_product_id("https://google.com"))
        self.assertIsNone(process_rss._extract_product_id(None))

    def test_parse_pub_date(self):
        """Test parsing of RSS pubDate format to YYYYMMDD."""
        # Standard RSS date format
        rss_date = "Wed, 01 Jan 2025 12:00:00 GMT"
        self.assertEqual(process_rss.parse_pub_date(rss_date), "20250101")

        # Invalid date
        self.assertIsNone(process_rss.parse_pub_date("Not a date"))
        self.assertIsNone(process_rss.parse_pub_date(None))

    @patch('maintaindb.process_rss.requests.get')
    def test_parse_dmsguild_rss_remote(self, mock_get):
        """Test parsing a remote RSS feed with mocked response."""
        # Mock XML content
        rss_content = """<?xml version="1.0"?>
        <rss version="2.0">
            <channel>
                <title>DMs Guild</title>
                <item>
                    <title>Test Adventure</title>
                    <link>https://www.dmsguild.com/product/111111/Test-Adventure</link>
                    <description>A test description</description>
                    <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>
        """
        mock_response = MagicMock()
        mock_response.text = rss_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        products = process_rss.parse_dmsguild_rss("http://fake-url.com/rss")
        
        self.assertEqual(len(products), 1)
        pid, title, authors, desc, pubdate, link = products[0]
        
        self.assertEqual(pid, "111111")
        self.assertEqual(title, "Test Adventure")
        self.assertEqual(desc, "A test description")
        self.assertEqual(pubdate, "Mon, 01 Jan 2024 10:00:00 GMT")

    def test_parse_price_from_description_local(self):
        """
        Test the inner function _parse_price_from_description by accessing it 
        via a test wrapper or by simulating the main loop logic if needed.
        Since it's defined inside main(), we can duplicate the logic here to verify the regex 
        or we can refactor the code. Ideally we refactor, but for now we'll rely on testing 
        the regex patterns directly as they appear in the file.
        """
        import re
        
        # Regex from process_rss.py
        price_regex = r"Price: \$\s*([\d.]+)"
        
        desc = "Some text. Price: $4.99"
        match = re.search(price_regex, desc)
        self.assertTrue(match)
        self.assertEqual(match.group(1), "4.99")
        
        desc_bold = "<b>Price: $19.95</b>"
        match = re.search(r"Price(?:</b>)?\s*:\s*\$\s*([\d.]+)", desc_bold)
        self.assertTrue(match)
        self.assertEqual(match.group(1), "19.95")

if __name__ == '__main__':
    unittest.main()
