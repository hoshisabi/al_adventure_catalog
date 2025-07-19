import json
import os
import glob

def find_numeric_hours_in_dc_files():
    dc_path = "f:/Users/decha/Documents/Projects/al_adventure_catalog/maintaindb/_dc/"
    json_files = glob.glob(os.path.join(dc_path, "*.json"))

    found_issues = False
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data.get("hours"), (int, float)):
                    print(f"File: {os.path.basename(file_path)}, Hours: {data.get("hours")}")
                    found_issues = True
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")
    
    if not found_issues:
        print("No files found with numeric hours values in maintaindb/_dc/")

if __name__ == "__main__":
    find_numeric_hours_in_dc_files()