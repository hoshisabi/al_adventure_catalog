#!/usr/bin/env python3
"""
Fix product_id in JSON files to match their filenames.
If a file is named '533675-13.json', the product_id should be '533675-13', not '533675'.
"""
import json
import glob
import os
import sys
from pathlib import Path

# Add parent directory to path to import from maintaindb
sys.path.insert(0, str(Path(__file__).parent.parent))

from maintaindb.paths import DC_DIR

def fix_product_ids():
    """Fix product_id in JSON files to match their filenames."""
    input_path = str(DC_DIR)
    input_full_path = f"{input_path}/*.json"
    
    fixed_count = 0
    skipped_count = 0
    
    print(f'Reading all files at: {input_path}')
    
    for file_path in glob.glob(input_full_path):
        filename = os.path.basename(file_path)
        # Extract expected product_id from filename (remove .json extension)
        expected_product_id = filename.replace('.json', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            current_product_id = data.get('product_id')
            
            # Skip if product_id already matches filename
            if current_product_id == expected_product_id:
                skipped_count += 1
                continue
            
            # Update product_id to match filename
            data['product_id'] = expected_product_id
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            print(f"Fixed: {filename} - product_id changed from '{current_product_id}' to '{expected_product_id}'")
            fixed_count += 1
            
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON from {filename}: {e}")
            continue
        except Exception as e:
            print(f"Error: Failed to process {filename}: {e}")
            continue
    
    print(f"\nSummary:")
    print(f"  Fixed: {fixed_count} files")
    print(f"  Skipped (already correct): {skipped_count} files")

if __name__ == '__main__':
    fix_product_ids()

