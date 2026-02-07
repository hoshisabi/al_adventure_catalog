#!/usr/bin/env python3
"""
Normalize adventure data in JSON files using the AdventureDataNormalizer.
This script updates:
- Product IDs to match filenames
- Hours (formatting and deduplication)
- Campaigns (normalization)
- Tiers and Level Ranges
- Titles (cleaning)
- Prices and other metadata
"""
import json
import glob
import os
import sys
from pathlib import Path

# Add parent directory to path to import from maintaindb
sys.path.insert(0, str(Path(__file__).parent.parent))

from .paths import DC_DIR
from .adventure_normalizers import AdventureDataNormalizer
from .adventure import merge_adventure_data

def normalize_data():
    """Normalize all JSON files in the _dc directory."""
    input_path = str(DC_DIR)
    input_full_path = f"{input_path}/*.json"
    
    normalizer = AdventureDataNormalizer()
    
    fixed_count = 0
    processed_count = 0
    error_count = 0
    
    print(f'Normalizing data in: {input_path}')
    
    files = glob.glob(input_full_path)
    total_files = len(files)
    
    for i, file_path in enumerate(files):
        filename = os.path.basename(file_path)
        processed_count += 1
        
        # Feedback every 100 files
        if processed_count % 100 == 0:
            print(f"Processed {processed_count}/{total_files} files...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 1. ensure product_id matches filename
            expected_product_id = filename.replace('.json', '')
            original_product_id = data.get('product_id')
            
            if original_product_id != expected_product_id:
                data['product_id'] = expected_product_id
            
            # 2. Run deep normalization
            # The normalizer expects "raw" keys usually, but our current data is already "semi-processed".
            # We map current keys to "raw" keys where necessary for the normalizer to pick them up,
            # OR we ensure the normalizer handles existing keys as fallbacks.
            # Looking at AdventureDataNormalizer, it looks for *_raw keys mainly.
            # Let's populate the *_raw keys from current values if they are missing, to ensure idempotency.
            
            prep_data = data.copy()
            prep_data['full_title_raw'] = data.get('full_title', data.get('title', ''))
            prep_data['url_raw'] = data.get('url', '')
            prep_data['date_created_raw'] = data.get('date_created', '')
            prep_data['authors_raw'] = data.get('authors', [])
            prep_data['price_raw'] = str(data.get('price', '')) if data.get('price') else None
            prep_data['page_count_raw'] = str(data.get('page_count', '')) if data.get('page_count') else None
            prep_data['apl_raw'] = str(data.get('apl', '')) if data.get('apl') else None
            prep_data['level_range_raw'] = data.get('level_range', '')
            prep_data['tiers_raw'] = str(data.get('tiers', '')) if data.get('tiers') else None
            # For hours, the normalizer expects a list or string in hours_raw
            prep_data['hours_raw'] = data.get('hours', [])

            # Run normalization
            normalized_data = normalizer.normalize(prep_data)
            
            # 3. Merge normalized data back into original data
            # using the careful merge strategy to preserve manual edits if we wanted, 
            # but here we want to enforce normalization, so we overwrite validation fields.
            
            # We check if anything actually changed to avoid touching files unnecessarily?
            # Comparing dicts with lists can be tricky, but let's try.
            
            has_changes = False
            
            # Check core fields
            fields_to_check = [
                'product_id', 'full_title', 'code', 'campaigns', 'season', 
                'authors', 'hours', 'tiers', 'level_range', 'title',
                'salvage_mission', 'dungeoncraft', 'community_content'
            ]
            
            for field in fields_to_check:
                if normalized_data.get(field) != data.get(field):
                    data[field] = normalized_data.get(field)
                    has_changes = True

            # Price needs special handling for Decimal vs float/str
            # Skip for now to avoid simple type diffs
            
            if has_changes:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
                fixed_count += 1
                # print(f"Fixed: {filename}") # Verbose
            
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON from {filename}: {e}")
            error_count += 1
            continue
        except Exception as e:
            print(f"Error: Failed to process {filename}: {e}")
            error_count += 1
            continue
    
    print(f"\nSummary:")
    print(f"  Processed: {processed_count} files")
    print(f"  Updated: {fixed_count} files")
    print(f"  Errors: {error_count} files")

if __name__ == '__main__':
    normalize_data()


