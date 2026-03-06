import json
from pathlib import Path

def fix_specific_codes():
    base_dir = Path("f:/Users/decha/Documents/Projects/al_adventure_catalog")
    dc_dir = base_dir / "maintaindb" / "_dc"
    
    fixes = {
        "456972": "SJ-DC-PANDORA-JWEI-03A",
        "456970": "SJ-DC-PANDORA-JWEI-03B"
    }
    
    for pid, new_code in fixes.items():
        file_path = dc_dir / f"{pid}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            old_code = data.get("code")
            data["code"] = new_code
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            print(f"Updated {pid}.json: code changed from {old_code} to {new_code}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    fix_specific_codes()
