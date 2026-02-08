"""
Generates a `fixup.html` report for identifying missing or malformed adventure data.

This script scans all adventure JSON files in `_dc/` and checks for:
- Missing critical data (hours, tiers, campaigns).
- Missing source HTML files in `dmsguildinfo/` (unless suppressed).
- Non-standard adventure codes.
- Explicit `needs_review` flags.

Output:
- `_site/fixup.html`: An HTML report with links to DMsGuild and local JSON files.
"""
import json
import os
import glob
import sys
import re
import time
import argparse

try:
    from . import warhorn_api
    from .adventure_utils import get_campaigns_from_code
except (ImportError, ValueError):
    import warhorn_api
    from adventure_utils import get_campaigns_from_code

def is_standard_code(code):
    """
    Check if a code matches standard patterns.
    Returns True if the code is recognized, False if it's non-standard.
    """
    if not code:
        return True  # No code is not non-standard, it's just missing
    
    # Use adventure_utils to check if it's a known campaign code
    if get_campaigns_from_code(code):
        return True
        
    code_upper = code.upper()
    
    # Fallback for some patterns that might not be in get_campaigns_from_code yet
    # DDIA codes (e.g., DDIA-MORD, DDIA-VOLO, DDIA-MORD-01, DDIA05)
    if re.match(r'^DDIA-[A-Z]+(?:-\d{1,2})?$|^DDIA\d{1,2}$', code_upper):
        return True
    
    # If we get here, the code is not recognized by any standard pattern
    return False

def generate_fixup_html(enable_warhorn=False, limit=None):
    """
    Main function to generate the fixup HTML report.
    
    Checks each adventure JSON for:
    1. `hours`: Must be non-empty string or number.
    2. `tiers`: Must be 1-4 (numeric) or range (string).
    3. `campaigns`: Must be a non-empty list.
    4. `missing_source_html`: Checks if a corresponding file exists in `dmsguildinfo/`.
       Can be suppressed with `suppress_missing_html: true` in JSON.
    5. `non-standard_code`: Checks if the code matches known patterns.
    6. `needs_review`: Explicit flag in JSON.
    
    Args:
        enable_warhorn (bool): If True, perform an audit against Warhorn API.
        limit (int): If set, only process this many files.
    """
    dc_path = os.path.join(os.path.dirname(__file__), "_dc")
    dmsguildinfo_path = os.path.join(os.path.dirname(__file__), "dmsguildinfo")
    processed_path = os.path.join(dmsguildinfo_path, "processed")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "_site") # Output to _site for Jekyll
    output_file = os.path.join(output_dir, "fixup.html")
    json_files = glob.glob(os.path.join(dc_path, "*.json"))
    
    if limit:
        json_files = json_files[:limit]
        
    total_files = len(json_files)
    processed_count = 0
    issues_found = 0

    # Loading HTML files for existence check
    html_files = set()
    for path in [dmsguildinfo_path, processed_path]:
        if os.path.exists(path):
            files_found = glob.glob(os.path.join(path, "**", "*.html"), recursive=True)
            for filepath in files_found:
                filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
                html_files.add(filename_no_ext)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fixup DMsGuild URLs</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f2f2; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>DMsGuild Adventures Needing Review</h1>
    <p>The table below lists adventures that may have missing or malformed data, or are missing their source HTML file.</p>
    <table>
        <thead>
            <tr>
                <th>Adventure Title</th>
                <th>Issues</th>
                <th>DMsGuild Link</th>
                <th>Warhorn Audit</th>
                <th>JSON File</th>
            </tr>
        </thead>
        <tbody>
"""

    adventures_to_review = []

    for file_path in json_files:
        processed_count += 1
        if processed_count % 100 == 0:
            print(f"Checking files: {processed_count}/{total_files}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            is_adventure = data.get("is_adventure") == True
            if not is_adventure:
                continue

            needs_review = bool(data.get("needs_review"))
            suppress_missing_html = bool(data.get("suppress_missing_html"))
            
            # Check for missing HTML
            product_id = data.get("product_id")
            missing_html = False
            
            # Determine expected HTML filename
            expected_html_filename = None
            if product_id:
                 # Check if product_id is numeric or has numeric part
                numeric_part = None
                if isinstance(product_id, int):
                    numeric_part = str(product_id)
                elif isinstance(product_id, str):
                    match = re.search(r'(\d+)', product_id)
                    if match:
                        numeric_part = match.group(1)
                
                if numeric_part:
                    expected_html_filename = f"dmsguildinfo-{numeric_part}"
            
            # If we couldn't determine an expected filename from product_id, try from JSON filename as fallback
            if not expected_html_filename:
                 filename_no_ext = os.path.splitext(os.path.basename(file_path))[0]
                 match = re.search(r'(\d+)', filename_no_ext)
                 if match:
                     expected_html_filename = f"dmsguildinfo-{match.group(1)}"

            if expected_html_filename and expected_html_filename not in html_files:
                if not suppress_missing_html:
                    missing_html = True

            
            if is_adventure or needs_review or missing_html:
                issues = []

                # Include needs_review marker explicitly if set
                if needs_review:
                    issues.append("needs_review")
                
                if missing_html:
                    issues.append("<span class='error'>missing_source_html</span>")
                
                # Check hours
                # Accept string like "4" or "2-4" or list of such strings, and also numeric types (int/float)
                hours_val = data.get("hours")
                hours_missing = False
                if hours_val in (None, ""):
                    hours_missing = True
                elif isinstance(hours_val, list):
                    # non-empty list is fine
                    if len(hours_val) == 0:
                        hours_missing = True
                elif isinstance(hours_val, str):
                    # non-empty string is fine
                    pass
                elif isinstance(hours_val, (int, float)):
                    # numeric value like 4 or 4.0 is fine
                    pass
                else:
                    # Other types unexpected
                    hours_missing = True
                if hours_missing:
                    issues.append("hours")
                
                # Check tiers
                # Accept either a numeric tier (1-4) or a string/range like "3-4"
                tiers_val = data.get("tiers")
                tiers_missing = False
                if tiers_val is None:
                    tiers_missing = True
                else:
                    # valid if int/float 1-4
                    if isinstance(tiers_val, (int, float)):
                        if not (1 <= int(tiers_val) <= 4):
                            tiers_missing = True
                    elif isinstance(tiers_val, str):
                        # Accept "1", "2", "3-4", etc.
                        if not (re.fullmatch(r"\d+", tiers_val) or re.fullmatch(r"\d+-\d+", tiers_val)):
                            tiers_missing = True
                    else:
                        tiers_missing = True
                if tiers_missing:
                    issues.append("tiers")
                    
                # Check campaigns (should be a list)
                if not data.get("campaigns") or not isinstance(data.get("campaigns"), list) or len(data.get("campaigns")) == 0:
                    issues.append("campaigns")
                
                # Check for non-standard codes (worth human review)
                code = data.get("code")
                if code and not is_standard_code(code):
                    issues.append("non-standard_code")

                # For needs_review=True, include the row even if the above fields look present
                # Only show if there are actual issues or if marked for review
                if needs_review or issues:
                    title = data.get("full_title", os.path.basename(file_path))
                    dmsguild_url = data.get("url", "#")
                    json_file_link = f"file:///{file_path.replace('\\', '/')}"
                    
                    adventures_to_review.append({
                        'title': title,
                        'issues': issues,
                        'url': dmsguild_url,
                        'json_file_link': json_file_link,
                        'code': data.get("code"),
                        'level_range': data.get("level_range"),
                        'hours': data.get("hours")
                    })
                    issues_found += 1
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")
        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {e}")

    # Optional: Fetch data from Warhorn using batching
    warhorn_data_map = {}
    if enable_warhorn and warhorn_api.WARHORN_APPLICATION_TOKEN:
        batch_size = 20
        all_titles = [a['title'] for a in adventures_to_review]
        total_batches = (len(all_titles) + batch_size - 1) // batch_size
        
        print(f"\nStarting Warhorn audit for {len(all_titles)} adventures...")
        for i in range(0, len(all_titles), batch_size):
            batch_titles = all_titles[i:i+batch_size]
            current_batch = i // batch_size + 1
            print(f"  [Warhorn Audit] Fetching batch {current_batch}/{total_batches} ({len(batch_titles)} titles)...")
            
            batch_results = warhorn_api.fetch_warhorn_scenarios_batched(batch_titles)
            warhorn_data_map.update(batch_results)
            
            # Add a small delay between batches to be respectful
            if current_batch < total_batches:
                time.sleep(1.0)

    # Generate HTML table rows
    for adv in adventures_to_review:
        title = adv['title']
        issues = adv['issues']
        dmsguild_url = adv['url']
        json_file_link = adv['json_file_link']
        code = adv['code']
        
        warhorn_search_url = f"https://warhorn.net/organized-play/p/dnd-adventurers-league?q={code or title}"
        warhorn_info = f"<a href=\"{warhorn_search_url}\" target=\"_blank\">Search Warhorn</a>"
        
        if enable_warhorn and warhorn_api.WARHORN_APPLICATION_TOKEN:
            wh_data = warhorn_data_map.get(title)
            if wh_data:
                ext = wh_data["extracted"]
                wh_suggestions = []
                if ext["hours"] and ext["hours"] != adv.get("hours"):
                    wh_suggestions.append(f"Hours: {ext['hours']}")
                if ext["level_range"] and ext["level_range"] != adv.get("level_range"):
                    wh_suggestions.append(f"Levels: {ext['level_range']}")
                
                if wh_suggestions:
                    warhorn_info += "<br><span style='font-size: 0.8em; color: green;'>Warhorn suggests:<br>" + "<br>".join(wh_suggestions) + "</span>"
                else:
                    warhorn_info += "<br><span style='font-size: 0.8em; color: gray;'>Warhorn data matches</span>"
            elif enable_warhorn:
                warhorn_info += "<br><span style='font-size: 0.8em; color: #dc3545;'>No data found</span>"

        html_content += f"            <tr>\n"
        html_content += f"                <td>{title}</td>\n"
        html_content += f"                <td>{', '.join(issues)}</td>\n"
        html_content += f"                <td><a href=\"{dmsguild_url}\" target=\"_blank\">DMsGuild Page</a></td>\n"
        html_content += f"                <td>{warhorn_info}</td>\n"
        html_content += f"                <td><a href=\"{json_file_link}\" target=\"_blank\">Open JSON</a></td>\n"
        html_content += f"            </tr>\n"

    html_content += """        </tbody>
    </table>
</body>
</html>
"""

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\nDone! Processed {total_files} files.")
    print(f"Found {issues_found} adventures needing review.")
    print(f"Generated fixup.html at: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fixup.html report for adventure data.")
    parser.add_argument("--warhorn", action="store_true", help="Enable auditing against Warhorn API (requires WARHORN_APPLICATION_TOKEN)")
    parser.add_argument("--limit", type=int, help="Limit the number of files processed (useful for testing)")
    args = parser.parse_args()
    
    generate_fixup_html(enable_warhorn=args.warhorn, limit=args.limit)
