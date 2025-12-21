#!/usr/bin/env python3
"""
Analyze CSV files to find adventures missing from _dc directory and extract seed information.

This script:
1. Reads all CSV files in _data directory
2. Extracts product IDs from URLs
3. Identifies adventures that don't have corresponding JSON files
4. Extracts seed information where available
5. Optionally updates existing JSON files with seed information
"""

import csv
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter

# Paths
DATA_DIR = Path(__file__).parent.parent / "_data"
DC_DIR = Path(__file__).parent / "_dc"
OUTPUT_REPORT = Path(__file__).parent.parent / "missing_adventures_report.html"

# CSV files to process
CSV_FILES = [
    "_data/DDALDM.csv",
    "_data/orig_adventures.csv",
    "_data/adventures.csv",
    "_data/DC-PoA List and Story Seeds Used - By Title.csv",
    "_data/SJ-DC List and Story Seeds Used - By Title.csv",
    "_data/WBW-DC List and Story Seeds Used - By Title.csv",
]


def extract_product_id_from_url(url: str) -> Optional[str]:
    """Extract product ID from DMsGuild URL."""
    if not url or url == "" or url.startswith("Not Available") or url.startswith("Coming Soon"):
        return None
    
    # Pattern: /product/123456/ or /product/123456?...
    match = re.search(r'/product/(\d+)', url)
    if match:
        return match.group(1)
    
    # Alternative pattern: product_info.php?products_id=123456
    match = re.search(r'products_id=(\d+)', url)
    if match:
        return match.group(1)
    
    return None


def read_csv_file(file_path: Path) -> List[Dict]:
    """Read a CSV file and return list of dictionaries."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return data


def get_existing_json_files() -> Set[str]:
    """Get set of all product IDs that have JSON files."""
    json_files = set()
    if DC_DIR.exists():
        for file in DC_DIR.glob("*.json"):
            product_id = file.stem  # filename without extension
            json_files.add(product_id)
    return json_files


def extract_code_from_row(row: Dict, code_columns: List[str]) -> Optional[str]:
    """Extract adventure code from row using various column names."""
    for col in code_columns:
        if col in row and row[col] and row[col].strip():
            return row[col].strip()
    return None


def analyze_csv_files() -> Tuple[Dict[str, Dict], Dict[str, str]]:
    """
    Analyze all CSV files and return:
    1. Dictionary mapping product_id -> adventure info
    2. Dictionary mapping code -> seed name
    """
    product_info = {}  # product_id -> {code, title, url, seed, source_file}
    code_to_seed = {}  # code -> seed name
    
    existing_json_files = get_existing_json_files()
    
    for csv_file in CSV_FILES:
        file_path = Path(__file__).parent.parent / csv_file
        if not file_path.exists():
            print(f"Warning: {csv_file} not found")
            continue
        
        print(f"Processing {csv_file}...")
        rows = read_csv_file(file_path)
        
        # Determine column names for this CSV
        if "DDALDM.csv" in csv_file:
            url_col = "URL"
            code_cols = ["Code"]
            seed_cols = ["Seed"]
            title_cols = ["Title"]
        elif "orig_adventures.csv" in csv_file:
            url_col = "URL"
            code_cols = ["Code"]
            seed_cols = []  # No seed column
            title_cols = ["Title"]
        elif "adventures.csv" in csv_file:
            url_col = "URL"
            code_cols = ["Code"]
            seed_cols = ["Seed"]
            title_cols = ["Title"]
        elif "DC-PoA" in csv_file:
            url_col = None  # May not have URL column
            code_cols = ["DC Code"]
            seed_cols = ["Seed Name"]
            title_cols = ["DC Name"]
        elif "SJ-DC" in csv_file:
            url_col = None
            code_cols = ["Adventure Code"]
            seed_cols = ["Seed Name"]
            title_cols = ["Adventure Name"]
        elif "WBW-DC" in csv_file:
            url_col = None
            code_cols = ["Code"]
            seed_cols = ["Seed Name"]
            title_cols = ["DC Name"]
        else:
            print(f"Unknown CSV format: {csv_file}")
            continue
        
        for row in rows:
            # Extract code
            code = extract_code_from_row(row, code_cols)
            
            # Extract seed
            seed = None
            for seed_col in seed_cols:
                if seed_col in row and row[seed_col] and row[seed_col].strip():
                    seed = row[seed_col].strip()
                    break
            
            # Store code -> seed mapping
            if code and seed:
                code_to_seed[code] = seed
            
            # Extract product ID from URL
            product_id = None
            if url_col and url_col in row:
                product_id = extract_product_id_from_url(row[url_col])
            
            if product_id:
                # Extract title
                title = None
                for title_col in title_cols:
                    if title_col in row and row[title_col] and row[title_col].strip():
                        title = row[title_col].strip()
                        break
                
                # Store product info
                if product_id not in product_info:
                    product_info[product_id] = {
                        'product_id': product_id,
                        'code': code,
                        'title': title,
                        'url': row.get(url_col, '') if url_col else '',
                        'seed': seed,
                        'source_files': []
                    }
                else:
                    # Merge information
                    if seed and not product_info[product_id]['seed']:
                        product_info[product_id]['seed'] = seed
                    if code and not product_info[product_id]['code']:
                        product_info[product_id]['code'] = code
                    if title and not product_info[product_id]['title']:
                        product_info[product_id]['title'] = title
                
                product_info[product_id]['source_files'].append(csv_file)
    
    return product_info, code_to_seed


def find_missing_adventures(product_info: Dict[str, Dict]) -> List[Dict]:
    """Find adventures in CSV that don't have JSON files."""
    existing_json_files = get_existing_json_files()
    missing = []
    
    for product_id, info in product_info.items():
        if product_id not in existing_json_files:
            missing.append(info)
    
    return missing


def update_json_with_seeds(code_to_seed: Dict[str, str], dry_run: bool = True):
    """Update existing JSON files with seed information from CSV."""
    updated_count = 0
    skipped_count = 0
    
    if not DC_DIR.exists():
        print(f"Directory {DC_DIR} does not exist")
        return updated_count, skipped_count
    
    for json_file in DC_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get code from JSON
            code = data.get('code')
            if not code:
                continue
            
            # Check if seed already exists
            if 'seed' in data and data['seed']:
                skipped_count += 1
                continue
            
            # Look up seed by code
            seed = code_to_seed.get(code)
            if seed:
                if not dry_run:
                    data['seed'] = seed
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                
                print(f"{'Would update' if dry_run else 'Updated'} {json_file.name} (code: {code}) with seed: {seed}")
                updated_count += 1
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    return updated_count, skipped_count


def is_seed_required_code(code: str) -> Tuple[bool, Optional[str]]:
    """Check if code belongs to POA, WBW, or SJ campaigns that require seeds.
    Returns (is_required, season_name) tuple."""
    if not code:
        return False, None
    
    code_upper = code.upper()
    
    # POA patterns
    if 'POA' in code_upper or code_upper.startswith('DC-POA'):
        return True, 'Icewind Dale (DC-POA)'
    
    # WBW patterns
    if 'WBW' in code_upper or code_upper.startswith('WBW-DC') or code_upper.startswith('DC-WBW'):
        return True, 'Wild Beyond the Witchlight (WBW-DC)'
    
    # SJ patterns
    if code_upper.startswith('SJ-DC') or code_upper.startswith('DC-SJ'):
        return True, 'Spelljammer (SJ-DC)'
    
    return False, None


def generate_report(product_info: Dict[str, Dict], missing: List[Dict], code_to_seed: Dict[str, str]):
    """Generate an HTML report file with clickable links."""
    existing_json_files = get_existing_json_files()
    
    # Count how many could be updated with seeds
    could_update_seeds = []
    
    # Find POA/WBW/SJ adventures missing seeds
    seed_required_missing_seeds = []
    seed_stats_by_season = defaultdict(lambda: defaultdict(int))  # season -> seed -> count
    
    for json_file in Path(DC_DIR).glob("*.json"):
        try:
            product_id = json_file.stem
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            code = data.get('code')
            if not code:
                continue
            
            # Check if this code requires a seed
            is_required, season_name = is_seed_required_code(code)
            
            # Track seed usage statistics
            seed = data.get('seed')
            if seed and season_name:
                seed_stats_by_season[season_name][seed] += 1
            
            # Check if it needs seed update from CSV
            if code and not seed and code in code_to_seed:
                could_update_seeds.append({
                    'product_id': product_id,
                    'code': code,
                    'title': data.get('title', data.get('full_title', 'N/A')),
                    'seed': code_to_seed[code],
                    'url': data.get('url', '')
                })
            
            # Check if seed-required adventure is missing seed
            if is_required and not seed:
                seed_required_missing_seeds.append({
                    'product_id': product_id,
                    'code': code,
                    'title': data.get('title', data.get('full_title', 'N/A')),
                    'url': data.get('url', ''),
                    'season': season_name
                })
        except Exception as e:
            pass
    
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Missing Adventures Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .stat-box {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 200px;
        }
        .stat-box h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        .stat-box .number {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        .section {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
            position: sticky;
            top: 0;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .product-id {
            font-family: monospace;
            font-weight: bold;
            color: #2c3e50;
        }
        .code {
            font-family: monospace;
            color: #27ae60;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .url-link {
            word-break: break-all;
        }
        .seed {
            font-style: italic;
            color: #7f8c8d;
        }
        .warning {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .info {
            background-color: #d1ecf1;
            border: 1px solid #0c5460;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .chart-container {
            position: relative;
            height: 400px;
            margin: 20px 0;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .season-stats {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .season-stats h3 {
            color: #2c3e50;
            margin-top: 0;
        }
        .seed-list {
            margin-top: 15px;
        }
        .seed-item {
            padding: 8px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
        }
        .seed-count {
            font-weight: bold;
            color: #3498db;
        }
    </style>
</head>
<body>
""")
        
        f.write(f"""
    <div class="header">
        <h1>Missing Adventures Report</h1>
        <p>Generated from CSV files analysis</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <h3>Total in CSV</h3>
            <div class="number">{len(product_info)}</div>
        </div>
        <div class="stat-box">
            <h3>Missing JSON Files</h3>
            <div class="number">{len(missing)}</div>
        </div>
        <div class="stat-box">
            <h3>Seed Mappings</h3>
            <div class="number">{len(code_to_seed)}</div>
        </div>
        <div class="stat-box">
            <h3>Could Update Seeds</h3>
            <div class="number">{len(could_update_seeds)}</div>
        </div>
        <div class="stat-box">
            <h3>POA/WBW/SJ Missing Seeds</h3>
            <div class="number">{len(seed_required_missing_seeds)}</div>
        </div>
    </div>
""")
        
        if missing:
            f.write(f"""
    <div class="section">
        <h2>Missing Adventures ({len(missing)})</h2>
        <p>These adventures are in CSV files but don't have corresponding JSON files. Click the URL to download the HTML file for processing.</p>
        <table>
            <thead>
                <tr>
                    <th>Product ID</th>
                    <th>Code</th>
                    <th>Title</th>
                    <th>Seed</th>
                    <th>DMsGuild URL</th>
                    <th>Source Files</th>
                </tr>
            </thead>
            <tbody>
""")
            for info in sorted(missing, key=lambda x: x.get('product_id', '')):
                url = info.get('url', '')
                if not url or url.startswith('Not Available') or url.startswith('Coming Soon'):
                    url_display = url if url else 'N/A'
                    url_link = '#'
                else:
                    url_display = url
                    url_link = url
                
                f.write(f"""
                <tr>
                    <td class="product-id">{info['product_id']}</td>
                    <td class="code">{info.get('code', 'N/A')}</td>
                    <td>{info.get('title', 'N/A')}</td>
                    <td class="seed">{info.get('seed', 'N/A') if info.get('seed') else '—'}</td>
                    <td><a href="{url_link}" target="_blank" class="url-link">{url_display}</a></td>
                    <td>{', '.join(info.get('source_files', []))}</td>
                </tr>
""")
            
            f.write("""
            </tbody>
        </table>
    </div>
""")
        else:
            f.write("""
    <div class="section">
        <h2>Missing Adventures</h2>
        <div class="info">
            <p>✓ No missing adventures found! All adventures in CSV files have corresponding JSON files.</p>
        </div>
    </div>
""")
        
        if could_update_seeds:
            f.write(f"""
    <div class="section">
        <h2>Adventures That Could Be Updated With Seeds ({len(could_update_seeds)})</h2>
        <p>These JSON files exist but don't have seed information. Run the script with <code>--update-seeds</code> to update them.</p>
        <table>
            <thead>
                <tr>
                    <th>Product ID</th>
                    <th>Code</th>
                    <th>Title</th>
                    <th>Seed (from CSV)</th>
                    <th>DMsGuild URL</th>
                </tr>
            </thead>
            <tbody>
""")
            for info in sorted(could_update_seeds, key=lambda x: x.get('code') or ''):
                url = info.get('url', '')
                if url:
                    url_display = url
                    url_link = url
                else:
                    url_display = 'N/A'
                    url_link = '#'
                f.write(f"""
                <tr>
                    <td class="product-id">{info['product_id']}</td>
                    <td class="code">{info.get('code', 'N/A')}</td>
                    <td>{info.get('title', 'N/A')}</td>
                    <td class="seed">{info.get('seed', 'N/A')}</td>
                    <td><a href="{url_link}" target="_blank" class="url-link">{url_display}</a></td>
                </tr>
""")
            
            f.write("""
            </tbody>
        </table>
    </div>
""")
        
        # POA/WBW/SJ adventures missing seeds
        if seed_required_missing_seeds:
            f.write(f"""
    <div class="section">
        <h2>POA/WBW/SJ Adventures Missing Seeds ({len(seed_required_missing_seeds)})</h2>
        <div class="warning">
            <p><strong>Warning:</strong> These adventures belong to campaigns that require seeds (DC-POA, WBW-DC, or SJ-DC), but they don't have seed information. They should have seeds!</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Product ID</th>
                    <th>Code</th>
                    <th>Title</th>
                    <th>Season</th>
                    <th>DMsGuild URL</th>
                </tr>
            </thead>
            <tbody>
""")
            for info in sorted(seed_required_missing_seeds, key=lambda x: (x.get('season', ''), x.get('code', ''))):
                url = info.get('url', '')
                if url:
                    url_display = url
                    url_link = url
                else:
                    url_display = 'N/A'
                    url_link = '#'
                f.write(f"""
                <tr>
                    <td class="product-id">{info['product_id']}</td>
                    <td class="code">{info.get('code', 'N/A')}</td>
                    <td>{info.get('title', 'N/A')}</td>
                    <td>{info.get('season', 'N/A')}</td>
                    <td><a href="{url_link}" target="_blank" class="url-link">{url_display}</a></td>
                </tr>
""")
            
            f.write("""
            </tbody>
        </table>
    </div>
""")
        
        # Seed Statistics by Season
        if seed_stats_by_season:
            f.write("""
    <div class="section">
        <h2>Seed Usage Statistics by Season</h2>
        <p>Pie charts showing how popular each seed is for POA, WBW, and SJ campaigns.</p>
        <div class="charts-grid">
""")
            
            # Generate charts for each season
            chart_id = 0
            colors = [
                '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', 
                '#1abc9c', '#e67e22', '#34495e', '#16a085', '#27ae60',
                '#c0392b', '#8e44ad', '#2980b9', '#d35400', '#7f8c8d'
            ]
            
            for season_name, seed_counts in sorted(seed_stats_by_season.items()):
                if not seed_counts:
                    continue
                
                # Prepare data for chart
                seeds = list(seed_counts.keys())
                counts = list(seed_counts.values())
                total = sum(counts)
                
                # Generate colors for this chart
                chart_colors = []
                for i in range(len(seeds)):
                    chart_colors.append(colors[i % len(colors)])
                
                canvas_id = f"chart_{chart_id}"
                chart_id += 1
                
                f.write(f"""
            <div class="season-stats">
                <h3>{season_name}</h3>
                <p><strong>Total adventures with seeds: {total}</strong></p>
                <div class="chart-container">
                    <canvas id="{canvas_id}"></canvas>
                </div>
                <div class="seed-list">
""")
                
                # List seeds with counts, sorted by count descending
                sorted_seeds = sorted(seed_counts.items(), key=lambda x: x[1], reverse=True)
                for seed, count in sorted_seeds:
                    percentage = (count / total * 100) if total > 0 else 0
                    f.write(f"""
                    <div class="seed-item">
                        <span>{seed}</span>
                        <span class="seed-count">{count} ({percentage:.1f}%)</span>
                    </div>
""")
                
                f.write("""
                </div>
            </div>
""")
                
                # Generate JavaScript for this chart
                f.write(f"""
            <script>
                (function() {{
                    const ctx_{canvas_id} = document.getElementById('{canvas_id}');
                    new Chart(ctx_{canvas_id}, {{
                        type: 'pie',
                        data: {{
                            labels: {json.dumps(seeds)},
                            datasets: [{{
                                data: {json.dumps(counts)},
                                backgroundColor: {json.dumps(chart_colors)}
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: true,
                            plugins: {{
                                legend: {{
                                    position: 'right',
                                    labels: {{
                                        font: {{
                                            size: 12
                                        }},
                                        boxWidth: 15,
                                        padding: 10
                                    }}
                                }},
                                tooltip: {{
                                    callbacks: {{
                                        label: function(context) {{
                                            const label = context.label || '';
                                            const value = context.parsed || 0;
                                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                            return label + ': ' + value + ' (' + percentage + '%)';
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }});
                }})();
            </script>
""")
            
            f.write("""
        </div>
    </div>
""")
        
        # Summary of seeds
        with_seed = [info for info in product_info.values() if info.get('seed')]
        if with_seed:
            f.write(f"""
    <div class="section">
        <h2>All Adventures With Seed Information ({len(with_seed)})</h2>
        <p>Complete list of code-to-seed mappings found in CSV files.</p>
        <table>
            <thead>
                <tr>
                    <th>Code</th>
                    <th>Seed Name</th>
                    <th>Product ID</th>
                    <th>Title</th>
                </tr>
            </thead>
            <tbody>
""")
            for info in sorted(with_seed, key=lambda x: x.get('code') or ''):
                f.write(f"""
                <tr>
                    <td class="code">{info.get('code', 'N/A')}</td>
                    <td class="seed">{info.get('seed', 'N/A')}</td>
                    <td class="product-id">{info.get('product_id', 'N/A')}</td>
                    <td>{info.get('title', 'N/A')}</td>
                </tr>
""")
            
            f.write("""
            </tbody>
        </table>
    </div>
""")
        
        f.write("""
</body>
</html>
""")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze CSV files for missing adventures and seeds')
    parser.add_argument('--update-seeds', action='store_true', 
                       help='Update existing JSON files with seed information (default: dry-run)')
    parser.add_argument('--no-report', action='store_true',
                       help='Skip generating report file')
    
    args = parser.parse_args()
    
    print("Analyzing CSV files...")
    product_info, code_to_seed = analyze_csv_files()
    
    print(f"\nFound {len(product_info)} adventures with product IDs in CSV files")
    print(f"Found {len(code_to_seed)} code-to-seed mappings")
    
    print("\nFinding missing adventures...")
    missing = find_missing_adventures(product_info)
    print(f"Found {len(missing)} missing JSON files")
    
    if missing:
        print("\nMissing adventures:")
        for info in missing[:10]:  # Show first 10
            print(f"  {info['product_id']}: {info.get('code', 'N/A')} - {info.get('title', 'N/A')}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
    
    print("\nUpdating JSON files with seed information...")
    updated, skipped = update_json_with_seeds(code_to_seed, dry_run=not args.update_seeds)
    
    mode = "DRY RUN" if not args.update_seeds else "LIVE"
    print(f"\n{mode} Results:")
    print(f"  Would update/Updated: {updated} files")
    print(f"  Skipped (already has seed): {skipped} files")
    
    if not args.no_report:
        print("\nGenerating report...")
        generate_report(product_info, missing, code_to_seed)
        print(f"Report saved to: {OUTPUT_REPORT}")
    
    if missing:
        print(f"\nWARNING: Found {len(missing)} adventures in CSV files that don't have JSON files")
        print(f"   See {OUTPUT_REPORT} for details")
    
    if not args.update_seeds and updated > 0:
        print(f"\nTIP: Run with --update-seeds to actually update {updated} JSON files with seed information")


if __name__ == "__main__":
    main()

