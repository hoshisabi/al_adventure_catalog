import requests
import json
import os

WARHORN_APPLICATION_TOKEN = os.getenv("WARHORN_APPLICATION_TOKEN")
WARHORN_API_ENDPOINT = "https://warhorn.net/graphql"

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
