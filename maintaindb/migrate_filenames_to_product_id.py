"""
Migration script to rename JSON adventure files from title-based to product_id-based filenames.

This script:
1. Reads all JSON files in the _dc directory
2. Extracts product_id from each file (from product_id field or URL if missing/non-numeric)
3. Updates the product_id field in the JSON file if extracted from URL
4. Renames files from title-based names (e.g., "DDAL07-11-A-Lesson-in-Love.json") 
   to product_id-based names (e.g., "232624.json")
5. Handles edge cases like missing product_id, already-migrated files, and duplicates
6. Generates a conflict report file (migration_report.json) listing all conflicts that need resolution

Usage:
    python -m maintaindb.migrate_filenames_to_product_id [--dry-run] [--force]
    
    --dry-run: Show what would be renamed without actually renaming files
    --force: Overwrite existing files if there's a conflict (use with caution)

After running the migration, check migration_report.json in the _dc directory for:
- conflicts: Files that couldn't be migrated because target already exists, or duplicate product_ids
- missing_product_id_files: Files that couldn't be migrated because they lack a product_id field
- remaining_old_format_files: Complete list of all files still in old format after migration
  (this includes conflicts + missing product_id files, plus any files that failed to migrate)

Note: "conflicts" only counts specific conflict types. "remaining_old_format_files" shows ALL
files that still need attention, which may be more than the conflict count.
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

from .paths import DC_DIR

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


def is_product_id_filename(filename):
    """
    Check if filename is already in product_id format.
    Formats: "232624.json" or "232624-02.json" (with optional part number suffix)
    """
    base_name = Path(filename).stem
    # Check if it's just a product_id (all digits)
    if base_name.isdigit():
        return True
    # Check if it's product_id-part format (e.g., "232624-02")
    if '-' in base_name:
        parts = base_name.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return True
    return False




def extract_product_id_from_url(url):
    """
    Extract product_id from a DMsGuild URL.
    
    Pattern: https://www.dmsguild.com/product/{product_id}/...
    Returns the numeric product_id as a string, or None if not found.
    """
    if not url or not isinstance(url, str):
        return None
    
    # Match pattern: /product/{numbers}/ 
    match = re.search(r'/product/(\d+)/', url)
    if match:
        return match.group(1)
    return None


def extract_product_id_from_data(data, file_path=None, update_file=False):
    """
    Extract product_id from JSON data dictionary.
    
    Tries multiple sources:
    1. Direct product_id field (if numeric)
    2. URL field (extracts from /product/{id}/ pattern)
    
    Args:
        data: JSON data dictionary
        file_path: Optional path to file (only needed if update_file=True)
        update_file: If True and product_id is extracted from URL, update the JSON file
        
    Returns:
        Product ID as string, or None if not found
    """
    # First, try the product_id field directly
    product_id = data.get('product_id')
    
    # Check if product_id is valid (should be numeric string or number)
    if product_id is not None:
        # Convert to string and check if it's numeric
        product_id_str = str(product_id).strip()
        if product_id_str.isdigit():
            return product_id_str
    
    # If product_id is missing or non-numeric, try extracting from URL
    url = data.get('url')
    if url:
        extracted_id = extract_product_id_from_url(url)
        if extracted_id:
            # Update the file if requested
            if update_file and file_path:
                data['product_id'] = extracted_id
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, sort_keys=True)
                    logger.debug(f"Updated product_id in {file_path.name} to {extracted_id} from URL")
                except Exception as e:
                    logger.warning(f"Failed to update product_id in {file_path.name}: {e}")
            return extracted_id
    
    return None


def migrate_filenames(dry_run=False, force=False):
    """
    Migrate all JSON files from title-based to product_id-based filenames.
    
    Args:
        dry_run: If True, only show what would be renamed without actually renaming
        force: If True, overwrite existing files on conflict (use with caution)
    """
    dc_path = Path(DC_DIR)
    
    if not dc_path.exists():
        logger.error(f"Directory does not exist: {dc_path}")
        return
    
    # Find all JSON files
    json_files = list(dc_path.glob('*.json'))
    logger.info(f"Found {len(json_files)} JSON files to process")
    
    # Track statistics and conflicts
    stats = {
        'already_migrated': 0,
        'missing_product_id': 0,
        'successful_migrations': 0,
        'skipped_conflicts': 0,
        'errors': 0,
        'product_id_to_files': defaultdict(list),  # Track duplicates
        'conflicts': [],  # Track conflicts for reporting
        'missing_product_id_files': []  # Track files missing product_id
    }
    
    # Initialize list for tracking remaining old format files
    remaining_old_format_files = []
    
    # First pass: collect all mappings
    migrations = []
    for file_path in json_files:
        filename = file_path.name
        
        # Skip if already in product_id format
        if is_product_id_filename(filename):
            stats['already_migrated'] += 1
            continue
        
        # Read JSON file once to extract both product_id and code
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read {filename}: {e}")
            stats['errors'] += 1
            continue
        
        # Extract product_id (try to update from URL if missing/non-numeric)
        product_id = extract_product_id_from_data(data, file_path=file_path, update_file=True)
        
        if not product_id:
            logger.warning(f"Skipping {filename}: cannot extract product_id from JSON or URL")
            stats['missing_product_id'] += 1
            stats['missing_product_id_files'].append(filename)
            continue
        
        # Create filename using product_id
        # Note: The script recognizes manually created part-number filenames (e.g., "545950-02.json")
        # via is_product_id_filename(), but only creates standard {product_id}.json format
        new_filename = f"{product_id}.json"
        new_file_path = dc_path / new_filename
        
        # Track product_id -> files mapping to detect duplicates
        stats['product_id_to_files'][product_id].append(filename)
        
        migrations.append({
            'old_path': file_path,
            'new_path': new_file_path,
            'product_id': product_id,
            'old_filename': filename,
            'new_filename': new_filename
        })
    
    # Check for duplicate product_ids (same product_id in multiple files)
    # Also check if target files already exist (already migrated files)
    duplicates = {pid: files for pid, files in stats['product_id_to_files'].items() 
                  if len(files) > 1}
    if duplicates:
        logger.warning(f"Found {len(duplicates)} product_ids with multiple source files:")
        for product_id, files in duplicates.items():
            logger.warning(f"  Product ID {product_id} appears in: {', '.join(files)}")
            logger.warning(f"    This will result in conflicts when migrating to {product_id}.json")
            # Add to conflicts for reporting
            stats['conflicts'].append({
                'type': 'duplicate_product_id',
                'product_id': product_id,
                'source_files': files,
                'target_filename': f"{product_id}.json",
                'action': 'needs_manual_resolution'
            })
    
    # Second pass: perform migrations
    logger.info(f"\n{'DRY RUN - ' if dry_run else ''}Processing {len(migrations)} files to migrate...")
    
    for migration in migrations:
        old_path = migration['old_path']
        new_path = migration['new_path']
        product_id = migration['product_id']
        old_filename = migration['old_filename']
        new_filename = migration['new_filename']
        
        # Check if target file already exists
        if new_path.exists() and old_path != new_path:
            conflict_info = {
                'type': 'target_file_exists',
                'old_filename': old_filename,
                'new_filename': new_filename,
                'product_id': product_id,
                'existing_file': new_filename,
                'resolved': force
            }
            
            if force:
                logger.warning(f"Target {new_filename} exists, overwriting (--force enabled)")
                conflict_info['action'] = 'overwritten'
            else:
                logger.warning(f"Skipping {old_filename}: target {new_filename} already exists (use --force to overwrite)")
                stats['skipped_conflicts'] += 1
                conflict_info['action'] = 'skipped'
                stats['conflicts'].append(conflict_info)
                continue
            
            stats['conflicts'].append(conflict_info)
        
        # Perform rename
        try:
            if dry_run:
                logger.info(f"Would rename: {old_filename} -> {new_filename} (product_id: {product_id})")
            else:
                old_path.rename(new_path)
                logger.info(f"Renamed: {old_filename} -> {new_filename} (product_id: {product_id})")
            stats['successful_migrations'] += 1
        except Exception as e:
            logger.error(f"Error renaming {old_filename} to {new_filename}: {e}")
            stats['errors'] += 1
    
    # After migration, identify all files that remain in old format
    if not dry_run:
        for file_path in dc_path.glob('*.json'):
            filename = file_path.name
            if not is_product_id_filename(filename):
                remaining_old_format_files.append(filename)
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("Migration Summary:")
    logger.info(f"  Total files found: {len(json_files)}")
    logger.info(f"  Already migrated (product_id format): {stats['already_migrated']}")
    logger.info(f"  Successfully migrated: {stats['successful_migrations']}")
    logger.info(f"  Missing product_id (cannot migrate): {stats['missing_product_id']}")
    logger.info(f"  Skipped due to conflicts: {stats['skipped_conflicts']}")
    logger.info(f"  Errors during migration: {stats['errors']}")
    if not dry_run and remaining_old_format_files:
        logger.info(f"  Files still in old format: {len(remaining_old_format_files)}")
        logger.info(f"    → See migration_report.json for complete list")
    
    if duplicates:
        logger.warning(f"\n⚠️  Found {len(duplicates)} product_ids with multiple files - manual review needed!")
    
    # Generate conflict report file (always generate if there are issues, or if files remain in old format)
    if stats['conflicts'] or stats['missing_product_id_files'] or remaining_old_format_files:
        report_file = dc_path / 'migration_report.json'
        report_data = {
            'summary': {
                'total_files_processed': len(json_files),
                'already_migrated': stats['already_migrated'],
                'missing_product_id': stats['missing_product_id'],
                'successful_migrations': stats['successful_migrations'],
                'skipped_conflicts': stats['skipped_conflicts'],
                'errors': stats['errors'],
                'remaining_old_format_files': len(remaining_old_format_files) if not dry_run else 0
            },
            'conflicts': stats['conflicts'],
            'missing_product_id_files': stats['missing_product_id_files'],
            'remaining_old_format_files': remaining_old_format_files if not dry_run else []
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"\n📄 Migration report saved to: {report_file}")
            logger.info(f"   Review this file to see which files need manual resolution")
            if stats['conflicts']:
                logger.info(f"   Found {len(stats['conflicts'])} conflict(s) that need attention")
            if stats['missing_product_id_files']:
                logger.info(f"   Found {len(stats['missing_product_id_files'])} file(s) missing product_id")
            if remaining_old_format_files:
                logger.warning(f"   ⚠️  Found {len(remaining_old_format_files)} file(s) still in old format")
                logger.info(f"      Check 'remaining_old_format_files' in the report for complete list")
        except Exception as e:
            logger.error(f"Failed to write conflict report: {e}")
    elif not dry_run:
        # No conflicts, so remove any old report file
        report_file = dc_path / 'migration_report.json'
        if report_file.exists():
            try:
                report_file.unlink()
                logger.info(f"\n✓ No conflicts found. Removed old migration_report.json")
            except Exception:
                pass
    
    if dry_run:
        logger.info("\nThis was a dry run. Use without --dry-run to perform actual migration.")
    else:
        logger.info(f"\nMigration complete! Processed {len(json_files)} files.")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate JSON adventure files from title-based to product_id-based filenames",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be renamed without actually renaming files'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing files if there is a conflict (use with caution)'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("DRY RUN MODE: No files will be modified\n")
    
    migrate_filenames(dry_run=args.dry_run, force=args.force)


if __name__ == '__main__':
    main()

