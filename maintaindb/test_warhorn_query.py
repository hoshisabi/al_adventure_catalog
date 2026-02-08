import os
import json
try:
    from . import warhorn_api
except (ImportError, ValueError):
    import warhorn_api

def test_list_any():
    query = """
    query {
        globalScenarios(first: 5) {
            nodes {
                name
                slug
            }
        }
    }
    """
    result = warhorn_api.run_query(query)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_list_any()
