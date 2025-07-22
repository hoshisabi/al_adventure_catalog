import requests
import json
import os

WARHORN_APPLICATION_TOKEN = os.getenv("WARHORN_APPLICATION_TOKEN")
WARHORN_API_ENDPOINT = "https://warhorn.net/graphql"

def generate_warhorn_slug(title):
    """
    Generates a Warhorn-style slug from a given title.
    """
    # Convert to lowercase
    slug = title.lower()
    # Replace spaces and non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def _extract_data_from_warhorn(scenario_data):
    # Extract data from Warhorn scenario data
    hours = None
    if scenario_data.get("blurb"):
        hours_match = re.search(r'(\d+)(?:-(\d+))?\s*[-h]*(?:hour|hours|hr)', scenario_data["blurb"], re.IGNORECASE)
        if hours_match:
            if hours_match.group(2):
                hours = f"{hours_match.group(1)}-{hours_match.group(2)}"
            else:
                hours = hours_match.group(1)

    return {
        "hours": hours,
        "apl": scenario_data.get("minLevel"), # Warhorn has min/max level, not APL directly
        "tiers": None, # Need to derive this from minLevel/maxLevel if possible
        "level_range": f"{scenario_data.get('minLevel')}-{scenario_data.get('maxLevel')}",
        "season": None, # Warhorn doesn't seem to have a direct season field
    }


def run_query(query, variables=None):
    headers = {
        "Authorization": f"Bearer {WARHORN_APPLICATION_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(WARHORN_API_ENDPOINT, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Query to inspect the fields of the 'Query' type
query_fields_query = """
    query {
        __type(name: "Query") {
            name
            fields {
                name
                args {
                    name
                    type {
                        name
                        kind
                    }
                }
                type {
                    name
                    kind
                }
            }
        }
    }
"""

if __name__ == "__main__":
    try:
        result = run_query(query_fields_query)
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except KeyError as e:
        print(f"Error parsing API response: Missing key {e}. Response: {result}")
