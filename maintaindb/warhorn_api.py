import requests
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file (needed when using uv instead of pipenv)
load_dotenv()

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
        text = scenario_data["blurb"]
        # Primary pattern: handle numeric and word forms with ranges (borrowed from adventure.py)
        # We don't have str_to_int here easily without circular imports, so we use a simpler version
        # or just a better regex.
        
        # Numeric range or single: "4 hours", "2-4 hours", "4-hour"
        match = re.search(r'(\d+)(?:\s*[-/to]\s*(\d+))?\s*[-h]*(?:hour|hours|hr)', text, re.IGNORECASE)
        if match:
            if match.group(2):
                hours = f"{match.group(1)}-{match.group(2)}"
            else:
                hours = match.group(1)
        else:
            # Word-based single: "Four-Hour", "Two hours"
            words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8}
            for word, num in words.items():
                if re.search(rf'\b{word}-?hour', text, re.IGNORECASE):
                    hours = str(num)
                    break

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

def fetch_warhorn_scenario_data(title):
    """
    Searches for a scenario on Warhorn and returns extracted data.
    """
    if not WARHORN_APPLICATION_TOKEN:
        return None

    expected_slug = generate_warhorn_slug(title)

    warhorn_query = """
        query ($searchQuery: String!) {
            globalScenarios(query: $searchQuery) {
                nodes {
                    name
                    blurb
                    author
                    minLevel
                    maxLevel
                    campaign {
                        name
                    }
                    gameSystem {
                        name
                    }
                    tags {
                        name
                    }
                    slug
                }
            }
        }
    """
    
    try:
        result = run_query(warhorn_query, {"searchQuery": title})
        
        if result and result.get("data") and result["data"].get("globalScenarios") and result["data"]["globalScenarios"].get("nodes"):
            # Prioritize exact slug match
            nodes = result["data"]["globalScenarios"]["nodes"]
            warhorn_scenario = None
            for node in nodes:
                if node.get("slug") == expected_slug:
                    warhorn_scenario = node
                    break
            
            # Fallback to first result
            if not warhorn_scenario:
                warhorn_scenario = nodes[0]
                
            return {
                "raw": warhorn_scenario,
                "extracted": _extract_data_from_warhorn(warhorn_scenario)
            }
    except Exception as e:
        print(f"Error fetching Warhorn data for '{title}': {e}")
        
    return None

def fetch_warhorn_scenarios_batched(titles):
    """
    Searches for multiple scenarios on Warhorn in a single batched GraphQL query.
    Returns a dictionary mapping titles to their extracted data.
    """
    if not WARHORN_APPLICATION_TOKEN or not titles:
        return {}

    query_parts = []
    variables = {}
    
    # Process each title in the batch
    for i, title in enumerate(titles):
        alias = f"r{i}"
        var_name = f"q{i}"
        query_parts.append(f"""
            {alias}: globalScenarios(query: ${var_name}) {{
                nodes {{
                    name
                    blurb
                    author
                    minLevel
                    maxLevel
                    campaign {{
                        name
                    }}
                    gameSystem {{
                        name
                    }}
                    tags {{
                        name
                    }}
                    slug
                }}
            }}
        """)
        variables[var_name] = title
        
    full_query = "query (" + ", ".join([f"${v}: String!" for v in variables.keys()]) + ") {\n" + "\n".join(query_parts) + "\n}"
    
    try:
        result = run_query(full_query, variables)
        
        batched_results = {}
        if result and result.get("data"):
            data = result["data"]
            for i, title in enumerate(titles):
                alias = f"r{i}"
                nodes = data.get(alias, {}).get("nodes", [])
                if nodes:
                    # Try to find a node with a matching name or slug
                    warhorn_scenario = None
                    # 1. Try exact slug match
                    expected_slug = generate_warhorn_slug(title)
                    for node in nodes:
                        if node.get("slug") == expected_slug:
                            warhorn_scenario = node
                            break
                    
                    # 2. Try exact name match (case-insensitive)
                    if not warhorn_scenario:
                        for node in nodes:
                            if node.get("name") and node["name"].lower() == title.lower():
                                warhorn_scenario = node
                                break
                    
                    # 3. Try if the title is contained in the node name (or vice versa)
                    if not warhorn_scenario:
                        for node in nodes:
                            if node.get("name") and (title.lower() in node["name"].lower() or node["name"].lower() in title.lower()):
                                warhorn_scenario = node
                                break

                    # 4. Fallback to first result
                    if not warhorn_scenario:
                        warhorn_scenario = nodes[0]
                    
                    batched_results[title] = {
                        "raw": warhorn_scenario,
                        "extracted": _extract_data_from_warhorn(warhorn_scenario)
                    }
                else:
                    batched_results[title] = None
        return batched_results
    except Exception as e:
        print(f"Error fetching batched Warhorn data: {e}")
        return {title: None for title in titles}

if __name__ == "__main__":
    try:
        result = run_query(query_fields_query)
        if result and result.get("data") and result["data"].get("__type"):
            fields = [f['name'] for f in result["data"]["__type"]["fields"]]
            print(f"Query fields: {fields}")
        else:
            print(f"Raw result: {json.dumps(result, indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except KeyError as e:
        print(f"Error parsing API response: Missing key {e}. Response: {result}")
