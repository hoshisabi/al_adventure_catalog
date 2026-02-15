import os
import json
import re
import argparse
import sqlite3
from pathlib import Path

def load_catalog(catalog_path):
    with open(catalog_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('adventures', data)

def create_lookup_maps(catalog):
    title_to_id = {}
    code_to_id = {}
    
    for adv in catalog:
        adv_id = str(adv.get('i'))
        product_id = adv_id.split('-')[0]
        
        title = adv.get('n', '').lower()
        code = adv.get('c', '').lower()
        
        if title:
            title_to_id[title] = product_id
        if code:
            code_to_id[code] = product_id
            
    return title_to_id, code_to_id

def clean_name(name):
    name = os.path.splitext(name)[0]
    name = re.sub(r'[^a-zA-Z0-9\s-]', ' ', name)
    return ' '.join(name.split()).lower()

def match_path_to_adv(path, title_map, code_map):
    name = clean_name(path.name)
    parent_name = clean_name(path.parent.name)
    
    id_match = re.search(r'\b(\d{5,7})\b', name)
    if id_match:
        return id_match.group(1)

    for code, adv_id in code_map.items():
        if code in name or code in parent_name:
            return adv_id
            
    for title, adv_id in title_map.items():
        if title in name or title in parent_name:
            return adv_id
            
    return None

class GDriveResolver:
    def __init__(self, db_paths):
        self.db_paths = db_paths
        self.resolvers = []
        for db_path in db_paths:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                self.resolvers.append({
                    'path': db_path,
                    'conn': conn,
                    'cursor': cursor,
                    'cache': self._init_cache_for_db(cursor)
                })
            except Exception as e:
                print(f"Warning: Could not open database {db_path}: {e}")

    def _init_cache_for_db(self, cursor):
        # We'll cache item names to stable_ids and stable_ids to cloud_ids
        # Get all items that are not trashed and not tombstoned
        cursor.execute("SELECT local_title, stable_id FROM items WHERE trashed = 0 AND is_tombstone = 0")
        name_to_ids = {}
        for title, sid in cursor.fetchall():
            if title:
                name_to_ids.setdefault(title.lower(), []).append(sid)
        
        cursor.execute("SELECT stable_id, cloud_id FROM stable_ids")
        sid_to_cloud = dict(cursor.fetchall())
        
        cursor.execute("SELECT item_stable_id, parent_stable_id FROM stable_parents")
        child_to_parent = {}
        for cid, pid in cursor.fetchall():
            child_to_parent[cid] = pid
            
        return {
            'name_to_ids': name_to_ids,
            'sid_to_cloud': sid_to_cloud,
            'child_to_parent': child_to_parent
        }
            
    def get_cloud_id(self, local_path):
        filename = local_path.name
        
        for res in self.resolvers:
            cache = res['cache']
            possible_ids = cache['name_to_ids'].get(filename.lower(), [])
            
            if not possible_ids:
                continue
            
            if len(possible_ids) == 1:
                cloud_id = cache['sid_to_cloud'].get(possible_ids[0])
                if cloud_id: return cloud_id
                
            # If multiple files with same name, check parents
            path_parts = list(local_path.parts)
            for sid in possible_ids:
                current_sid = sid
                match = True
                # Check up to 3 levels of parents
                for i in range(len(path_parts) - 2, max(-1, len(path_parts) - 5), -1):
                    parent_sid = cache['child_to_parent'].get(current_sid)
                    if not parent_sid:
                        break
                    
                    # Get parent name
                    res['cursor'].execute("SELECT local_title FROM items WHERE stable_id = ?", (parent_sid,))
                    db_res = res['cursor'].fetchone()
                    if db_res and db_res[0].lower() != path_parts[i].lower():
                        # Special case: 'My Drive' might be represented differently
                        if db_res[0] == 'My Drive' and path_parts[i].lower() == 'my drive':
                            pass
                        else:
                            match = False
                            break
                    current_sid = parent_sid
                
                if match:
                    cloud_id = cache['sid_to_cloud'].get(sid)
                    if cloud_id: return cloud_id
                    
            # Fallback to first one in this DB if we found matches but didn't match parents exactly
            cloud_id = cache['sid_to_cloud'].get(possible_ids[0])
            if cloud_id: return cloud_id
                
        return None

def find_gdrive_dbs():
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        return []
    
    base_path = Path(local_app_data) / 'Google' / 'DriveFS'
    if not base_path.exists():
        return []
    
    dbs = []
    # DriveFS folders are usually long numeric strings
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name.isdigit():
            db_path = folder / 'metadata_sqlite_db'
            if db_path.exists():
                dbs.append(db_path)
    return dbs

def main():
    parser = argparse.ArgumentParser(description='Sync local Google Drive directory to private inventory')
    parser.add_argument('directory', help='Local directory to scan')
    parser.add_argument('--catalog', default='assets/data/catalog.json', help='Path to catalog.json')
    parser.add_argument('--output', default='local_inventory.json', help='Output filename')
    parser.add_argument('--use-gdrive', action='store_true', default=True, help='Try to resolve Google Drive share links')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory {args.directory} does not exist.")
        return

    print("Loading catalog...")
    catalog = load_catalog(args.catalog)
    title_map, code_map = create_lookup_maps(catalog)
    
    resolver = None
    if args.use_gdrive:
        db_paths = find_gdrive_dbs()
        if db_paths:
            print(f"Found {len(db_paths)} Google Drive metadata database(s).")
            try:
                resolver = GDriveResolver(db_paths)
            except Exception as e:
                print(f"Warning: Could not initialize Google Drive resolver: {e}")
        else:
            print("Warning: Could not find Google Drive metadata database. Will use file:// links.")

    inventory = {}
    total_files = 0
    matched_count = 0
    gdrive_count = 0
    
    print(f"Scanning {args.directory}...")
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            # Common adventure file types
            if file.lower().endswith(('.pdf', '.zip', '.rar', '.txt', '.json', '.gdoc', '.gsheet')):
                total_files += 1
                file_path = Path(root) / file
                
                adv_id = match_path_to_adv(file_path, title_map, code_map)
                if adv_id:
                    link = None
                    if resolver:
                        cloud_id = resolver.get_cloud_id(file_path)
                        if cloud_id:
                            link = f"https://drive.google.com/open?id={cloud_id}"
                            gdrive_count += 1
                    
                    if not link:
                        link = file_path.absolute().as_uri()
                    
                    inventory[adv_id] = link
                    matched_count += 1
                    # print(f"Matched: {file} -> {adv_id}")

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)
        
    print("\n--- Summary ---")
    print(f"Files scanned: {total_files}")
    print(f"Items matched: {matched_count}")
    print(f"Google Drive links resolved: {gdrive_count}")
    print(f"Saved to: {args.output}")
    print("\nYou can now import this file into the Private Inventory Manager.")

if __name__ == "__main__":
    main()
