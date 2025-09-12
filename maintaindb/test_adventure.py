import unittest
from bs4 import BeautifulSoup
from maintaindb.adventure import (
    extract_data_from_html, sanitize_filename, str_to_int, get_patt_first_matching_group
)
class TestAdventureExtraction(unittest.TestCase):

    def test_extract_simple_hours_from_html(self):
        # Sample HTML content from dmsguildinfo-463522.html
        html_content = """
        <div class="alpha omega prod-content">
            At the height of the Battle of Kalaman, an opportunity to honor an oath-decades unfulfilled presents itself! If Ansalon’s heroes can press deep into the heart of the enemy and topple a flame-fueled destructive force, they might repel the Red Dragon Army, defend The Beacon of the East, and reuinite mother and child. 
            This is a 2 hour adventure for Tier 2 (Levels 5-10) characters and was designed under the Dungeoncraft program guidance. 
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        # For testing, we can pass a dummy product_id and existing_data
        extracted_data = extract_data_from_html(parsed_html, "463522", existing_data={})
        self.assertEqual(extracted_data['hours'], "2")

    def test_extract_word_hours_from_html(self):
        # Sample HTML content from dmsguildinfo-463522.html
        html_content = """
        <div class="alpha omega prod-content">
            At the height of the Battle of Kalaman, an opportunity to honor an oath-decades unfulfilled presents itself! If Ansalon’s heroes can press deep into the heart of the enemy and topple a flame-fueled destructive force, they might repel the Red Dragon Army, defend The Beacon of the East, and reuinite mother and child. 
            This is a four-hour adventure for Tier 2 (Levels 5-10) characters and was designed under the Dungeoncraft program guidance. 
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        # For testing, we can pass a dummy product_id and existing_data
        extracted_data = extract_data_from_html(parsed_html, "463522", existing_data={})
        self.assertEqual(extracted_data['hours'], "4")

    def test_extract_hour_range_from_html(self):
        # Sample HTML
        html_content = """
        <div class="alpha omega prod-content">
        This is a 3-7-hour adventure for levels 100-101.
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        with self.subTest("Numeric range"):
            extracted_data = extract_data_from_html(parsed_html, "463522", existing_data={})
            self.assertEqual(extracted_data['hours'], "3-7")

        html_content = """
        <div class="alpha omega prod-content">
        This is a two to four hour adventure for levels 100-101.
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        with self.subTest("Word range with 'to'"):
            extracted_data = extract_data_from_html(parsed_html, "463522", existing_data={})
            self.assertEqual(extracted_data['hours'], "2-4")

        html_content = """
        <div class="alpha omega prod-content">
        This is a two-to-four-hour adventure for levels 100-101.
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        with self.subTest("Word range with 'to' and dashes"):
            extracted_data = extract_data_from_html(parsed_html, "463522", existing_data={})
            self.assertEqual(extracted_data['hours'], "2-4")

        html_content = """
        <div class="alpha omega prod-content">
        This adventure will take 1 hour.
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        with self.subTest("Single hour"):
            extracted_data = extract_data_from_html(parsed_html, "463522", existing_data={})
            self.assertEqual(extracted_data['hours'], "1")

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("My Awesome Adventure!"), "My-Awesome-Adventure.json")
        self.assertEqual(sanitize_filename("Another Adventure (Part 2)"), "Another-Adventure-Part-2.json")
        self.assertEqual(sanitize_filename("Special Chars: @#$%^&*()"), "Special-Chars.json")
        self.assertEqual(sanitize_filename("  Leading and Trailing Spaces  "), "Leading-and-Trailing-Spaces.json")
        self.assertEqual(sanitize_filename("File with-dashes-and_underscores"), "File-with-dashes-and_underscores.json")
        self.assertEqual(sanitize_filename("Ünicode Fïle Ñame"), "Unicode-File-Name.json")
        self.assertEqual(sanitize_filename("A.B.C.D.html"), "A-B-C-D.json") # All periods in base name should become dashes
        self.assertEqual(sanitize_filename("Test.json"), "Test.json") # Already has .json
        self.assertEqual(sanitize_filename("Test.txt"), "Test.json") # Changes extension to .json

    def test_str_to_int_conversion(self):
        self.assertEqual(str_to_int("four"), 4)
        self.assertEqual(str_to_int("4"), 4)
        self.assertEqual(str_to_int("10"), 10)
        self.assertIsNone(str_to_int("invalid"))
        self.assertIsNone(str_to_int(None))

    def test_get_patt_first_matching_group(self):
        text = "This is Tier 2 and APL 5."
        self.assertEqual(get_patt_first_matching_group(r"Tier ?([1-4])", text), "2")
        self.assertEqual(get_patt_first_matching_group(r"APL ?(\d+)", text), "5")
        self.assertIsNone(get_patt_first_matching_group(r"NonExistentPattern", text))

    def test_deduce_tier_from_level_range(self):
        html_content = """
        <meta name="description" content="A Two-Hour Spelljammer Dungeoncraft Adventure for&nbsp;Level 1-4 Characters. Optimized for&nbsp;Average Party Level&nbsp;(APL) 3.">
        <div class="alpha omega prod-content">
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        extracted_data = extract_data_from_html(parsed_html, "dummy_id", existing_data={})
        self.assertEqual(extracted_data['tiers'], 1)

    def test_extract_apl_and_tier_from_526753_html(self):
        html_content = """
        <meta name="description" content="PS-DC-STRAT-TALES-06 Dungeon &amp; A Dragon - Rescue the princess. Slay the dragon. Save the kingdom.\n\nA Four-Hour Adventure for Tier 4 Characters. Optimized for APL ">
        <div class="alpha omega prod-content">
        A Four-Hour Adventure for Tier 4 Characters. Optimized for APL 18.
        </div>
        """
        parsed_html = BeautifulSoup(html_content, 'html.parser')
        extracted_data = extract_data_from_html(parsed_html, "526753", existing_data={})
        self.assertEqual(extracted_data['apl'], 18)
        self.assertEqual(extracted_data['tiers'], 4)

if __name__ == '__main__':
    unittest.main()
