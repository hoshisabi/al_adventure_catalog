import json
import requests
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def audit_links():
    private_inventory_path = Path('private_inventory.json')
    report_path = Path('link_audit_report.json')
    
    if not private_inventory_path.exists():
        print(f"Error: {private_inventory_path} not found.")
        return

    with open(private_inventory_path, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    results = []
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    def check_link(item):
        prod_id, url = item
        try:
            # HEAD first
            response = session.head(url, timeout=15, allow_redirects=True)
            
            if response.status_code in [405, 403]:
                response = session.get(url, timeout=15, stream=True)
            
            status_code = response.status_code
            final_url = response.url
            
            # Heuristics for Google Drive
            status = "Valid"
            if status_code == 404:
                status = "Broken (404)"
            elif "accounts.google.com/v3/signin" in final_url:
                status = "Access Denied (Requires Login)"
            elif "ServiceLogin" in final_url:
                status = "Access Denied (Requires Login)"
            elif status_code != 200:
                status = f"Error: {status_code}"
            
            return {
                "product_id": prod_id,
                "url": url,
                "status_code": status_code,
                "status": status,
                "final_url": final_url
            }
        except Exception as e:
            return {
                "product_id": prod_id,
                "url": url,
                "status": f"Failed: {str(e)}",
                "status_code": None
            }

    print(f"Auditing {len(inventory)} links...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_link, inventory.items()))

    # Summary logic
    valid_count = sum(1 for r in results if r['status'] == "Valid")
    denied_count = sum(1 for r in results if "Access Denied" in r['status'])
    broken_count = sum(1 for r in results if "Broken" in r['status'] or "Failed" in r['status'])
    other_count = len(results) - valid_count - denied_count - broken_count

    report = {
        "summary": {
            "total": len(results),
            "valid": valid_count,
            "access_denied": denied_count,
            "broken": broken_count,
            "other_errors": other_count
        },
        "details": results
    }

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nAudit Complete!")
    print(f"Valid: {valid_count}")
    print(f"Access Denied (Login Required): {denied_count}")
    print(f"Broken/Failed: {broken_count}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    audit_links()
