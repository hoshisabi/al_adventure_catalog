import json
import os
import glob

def fix_hours_format_in_dc_files():
    dc_path = "f:/Users/decha/Documents/Projects/al_adventure_catalog/maintaindb/_dc/"
    json_files = glob.glob(os.path.join(dc_path, "*.json"))

    for file_path in json_files:
        with open(file_path, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data.get("hours"), (int, float)):
                    data["hours"] = str(int(data["hours"])) # Convert to string
                    f.seek(0) # Rewind to the beginning of the file
                    json.dump(data, f, indent=4, sort_keys=True)
                    f.truncate() # Truncate the rest of the file
                    print(f"Fixed hours in: {os.path.basename(file_path)}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")

if __name__ == "__main__":
    fix_hours_format_in_dc_files()