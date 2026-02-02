import os
import json
from pathlib import Path

def migrate_json_files():
    dc_dir = Path('_dc')
    if not dc_dir.exists():
        print(f"Directory {dc_dir} not found.")
        return

    json_files = list(dc_dir.glob('*.json'))
    print(f"Found {len(json_files)} JSON files to process.")

    count = 0
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'module_name' in data:
                del data['module_name']
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, sort_keys=True)
                count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Successfully migrated {count} files (removed 'module_name').")

if __name__ == '__main__':
    migrate_json_files()
