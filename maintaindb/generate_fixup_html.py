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

def is_standard_code(code):
    """
    Check if a code matches standard patterns.
    Returns True if the code is recognized, False if it's non-standard.
    
    This checks against the standard code prefixes without importing the full adventure_utils
    module to avoid dependency issues.
    """
    if not code:
        return True  # No code is not non-standard, it's just missing
    
    code_upper = code.upper()
    
    # Standard DC campaign prefixes (from DC_CAMPAIGNS)
    dc_prefixes = [
        'DL-DC', 'EB-DC', 'EB-SM', 'FR-DC', 'PS-DC', 'SJ-DC', 'WBW-DC',
        'DC-POA', 'PO-BK', 'BMG-DRW', 'BMG-DL', 'BMG-MOON', 'CCC-', 'RV-DC'
    ]
    for prefix in dc_prefixes:
        if code_upper.startswith(prefix.upper()):
            return True
    
    # Standard DDAL/DDEX/DDHC/DDIA prefixes (from DDAL_CAMPAIGN)
    ddal_prefixes = [
        'DDAL', 'DDEX', 'DDHC', 'DDIA', 'DDALEL', 'DDALBG', 'DDALDR', 'DDALDRW',
        'DDEP', 'DDAL04', 'DDAL00', 'DDEX1', 'DDEX2', 'DDEX3', 'DDEX4',
        'AL', 'CCC', 'SJA'
    ]
    for prefix in ddal_prefixes:
        prefix_upper = prefix.upper()
        # Handle prefixes like DDAL4/DDAL04, DDEX1/DDEX01
        if prefix.endswith('0') and len(prefix) > 1:
            # Check if code starts with prefix minus the last '0'
            prefix_minus_zero = prefix_upper[:-1]
            if code_upper.startswith(prefix_minus_zero):
                # Check if next char after prefix is a digit
                if len(code_upper) > len(prefix_minus_zero) and code_upper[len(prefix_minus_zero):len(prefix_minus_zero)+1].isdigit():
                    return True
        # Handle exact matches or prefixes
        elif code_upper.startswith(prefix_upper):
            return True
    
    # Check for other standard patterns
    import re
    # DDIA codes (e.g., DDIA-MORD, DDIA-VOLO, DDIA-MORD-01, DDIA05)
    if re.match(r'^DDIA-[A-Z]+(?:-\d{1,2})?$|^DDIA\d{1,2}$', code_upper):
        return True
    # Ravenloft Module Hunt
    if re.match(r'^RMH-\d+', code_upper):
        return True
    
    # If we get here, the code is not recognized by any standard pattern
    return False

def generate_fixup_html():
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
    """
    dc_path = os.path.join(os.path.dirname(__file__), "_dc")
    dmsguildinfo_path = os.path.join(os.path.dirname(__file__), "dmsguildinfo")
    processed_path = os.path.join(dmsguildinfo_path, "processed")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "_site") # Output to _site for Jekyll
    output_file = os.path.join(output_dir, "fixup.html")
    json_files = glob.glob(os.path.join(dc_path, "*.json"))

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
                <th>JSON File</th>
            </tr>
        </thead>
        <tbody>
"""

    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
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
                        
                        html_content += f"            <tr>\n"
                        html_content += f"                <td>{title}</td>\n"
                        html_content += f"                <td>{', '.join(issues)}</td>\n"
                        html_content += f"                <td><a href=\"{dmsguild_url}\" target=\"_blank\">DMsGuild Page</a></td>\n"
                        html_content += f"                <td><a href=\"{json_file_link}\" target=\"_blank\">Open JSON</a></td>\n"
                        html_content += f"            </tr>\n"
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")

    html_content += """        </tbody>
    </table>
</body>
</html>
"""

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated fixup.html at: {output_file}")

if __name__ == "__main__":
    generate_fixup_html()
