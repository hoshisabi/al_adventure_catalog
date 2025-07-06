import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from word2number import w2n

def get_patt_first_matching_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        for group in matches.groups():
            if group:
                return group
    return None

def __str_to_int(value):
    if not value:
        return None

    try:
        number = int(value)
        return number
    except ValueError:
        try:
            number = w2n.word_to_num(value)
            return number
        except Exception:
            return None
    except Exception:
        return None

def fetch_dmsguild_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Successfully fetched {url}. Status code: {response.status_code}")
        
        root = ET.fromstring(response.text)
        items = root.findall('.//item')
        print(f"Number of items in feed: {len(items)}")
        
        if items:
            print("\nExtracted details from the first 5 items:")
            for i, item in enumerate(items[:5]): # Check first 5 items
                title = item.find('title').text
                description_html = item.find('description').text
                
                soup = BeautifulSoup(description_html, 'html.parser')
                description_text = soup.get_text()

                hours = get_patt_first_matching_group(r"(?i)(two|four|\d)+(?:hour|to|through|\+|-|\s+)*(?:(\d|two|four|eight|\s)+)*Hour", description_text)
                hours = __str_to_int(hours)
                tier = get_patt_first_matching_group(r"Tier ?([1-4])", description_text)
                tier = __str_to_int(tier)
                apl = get_patt_first_matching_group(r"APL ?(\d+)", description_text)
                apl = __str_to_int(apl)
                level_range = get_patt_first_matching_group(r"(?i)(?:levels ?)?(\d+)(?:nd|th)?(?:[ -]|through|to)*(\d+)(?:nd|th)?[- ](?:level)?", description_text)

                print(f"\n--- Item {i+1}: {title} ---")
                print(f"  Hours: {hours}")
                print(f"  Tier: {tier}")
                print(f"  APL: {apl}")
                print(f"  Level Range: {level_range}")

        else:
            print("No items found in the RSS feed.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML from {url}: {e}")

if __name__ == "__main__":
    fetch_dmsguild_data("https://www.dmsguild.com/rss.php?filters=45470_0_0_0_0_0_0_0_0&src=fid45470&affiliate_id=171040")