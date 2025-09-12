import json
import os
import glob

def generate_fixup_html():
    dc_path = os.path.join(os.path.dirname(__file__), "_dc")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "_site") # Output to _site for Jekyll
    output_file = os.path.join(output_dir, "fixup.html")
    json_files = glob.glob(os.path.join(dc_path, "*.json"))

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
    </style>
</head>
<body>
    <h1>DMsGuild Adventures Needing Review</h1>
    <p>The table below lists adventures that may have missing or malformed data. Click the links to visit the DMsGuild page and manually verify/update the indicated fields.</p>
    <table>
        <thead>
            <tr>
                <th>Adventure Title</th>
                <th>Missing/Malformed Fields</th>
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
                needs_review = bool(data.get("needs_review"))
                if is_adventure or needs_review:
                    missing_fields = []

                    # Include needs_review marker explicitly if set
                    if needs_review:
                        missing_fields.append("needs_review")
                    
                    # Check hours
                    # Accept string like "4" or "2-4" or list of such strings
                    hours_val = data.get("hours")
                    hours_missing = False
                    if hours_val in (None, ""):
                        hours_missing = True
                    elif isinstance(hours_val, list):
                        if len(hours_val) == 0:
                            hours_missing = True
                    elif isinstance(hours_val, str):
                        # non-empty string is fine
                        pass
                    else:
                        # Other types unexpected
                        hours_missing = True
                    if hours_missing:
                        missing_fields.append("hours")
                    
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
                            import re
                            if not (re.fullmatch(r"\d+", tiers_val) or re.fullmatch(r"\d+-\d+", tiers_val)):
                                tiers_missing = True
                        else:
                            tiers_missing = True
                    if tiers_missing:
                        missing_fields.append("tiers")
                        
                    # Check campaigns (should be a list)
                    if not data.get("campaigns") or not isinstance(data.get("campaigns"), list) or len(data.get("campaigns")) == 0:
                        missing_fields.append("campaigns")

                    # For needs_review=True, include the row even if the above fields look present
                    if needs_review or missing_fields:
                        title = data.get("full_title", os.path.basename(file_path))
                        dmsguild_url = data.get("url", "#")
                        json_file_link = f"file:///{file_path.replace('\\', '/')}"
                        
                        html_content += f"            <tr>\n"
                        html_content += f"                <td>{title}</td>\n"
                        html_content += f"                <td>{', '.join(missing_fields) if missing_fields else 'needs_review' if needs_review else ''}</td>\n"
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
