# Suggested changes for generate_fixup_html.py
import json
import os
import glob
from adventure_model import Adventure # Import the Adventure dataclass

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
    <title>DMsGuild Adventures Needing Review</title>
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
    <p>The table below lists adventures that have been flagged for manual review or have potential data inconsistencies. Click the links to visit the DMsGuild page and manually verify/update the indicated fields.</p>
    <table>
        <thead>
            <tr>
                <th>Adventure Title</th>
                <th>Product ID</th>
                <th>Flags/Missing Fields</th>
                <th>DMsGuild Link</th>
                <th>JSON File</th>
            </tr>
        </thead>
        <tbody>
"""

    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                raw_json_data = json.load(f)
                adventure_obj = Adventure.from_json(raw_json_data) # Load into Adventure object

                # Condition for inclusion in the fixup list:
                # 1. 'needs_review' flag is True
                # 2. Or, if you want to highlight specific *formatting* issues not caught by needs_review,
                #    you could add checks here (e.g., if hours list contains non-string, or non-"X" / "X-Y" format)
                
                # For this tool, the primary trigger is the 'needs_review' flag set by the processing pipeline.
                if adventure_obj.needs_review:
                    # Collect specific reasons for review, or just state "Needs Review"
                    review_reasons = []
                    if not adventure_obj.title: review_reasons.append("Missing Title")
                    if not adventure_obj.authors: review_reasons.append("Missing Authors")
                    if not adventure_obj.hours: review_reasons.append("Missing Hours")
                    if not adventure_obj.tiers: review_reasons.append("Missing Tiers")
                    if not adventure_obj.campaigns: review_reasons.append("Missing Campaigns")
                    if not adventure_obj.level_ranges: review_reasons.append("Missing Level Ranges")
                    if not adventure_obj.price: review_reasons.append("Missing Price")
                    
                    if not review_reasons: # If needs_review is True but no obvious missing fields
                        review_reasons.append("General Review Flagged")

                    title = adventure_obj.full_title or adventure_obj.title or os.path.basename(file_path)
                    product_id = adventure_obj.product_id or "N/A"
                    dmsguild_url = adventure_obj.url or "#"
                    json_file_link = f"file:///{os.path.abspath(file_path).replace(os.sep, '/')}" # Absolute path for local link
                    
                    html_content += f"            <tr>\n"
                    html_content += f"                <td>{title}</td>\n"
                    html_content += f"                <td>{product_id}</td>\n"
                    html_content += f"                <td>{', '.join(review_reasons)}</td>\n"
                    html_content += f"                <td><a href=\"{dmsguild_url}\" target=\"_blank\">DMsGuild Page</a></td>\n"
                    html_content += f"                <td><a href=\"{json_file_link}\" target=\"_blank\">Open JSON</a></td>\n"
                    html_content += f"            </tr>\n"
            except json.JSONDecodeError as e:
                # Handle corrupted JSON files in the fixup tool
                print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")
                html_content += f"            <tr>\n"
                html_content += f"                <td>CORRUPTED JSON FILE</td>\n"
                html_content += f"                <td>{os.path.basename(file_path).replace('.json', '')}</td>\n"
                html_content += f"                <td>JSON Decode Error</td>\n"
                html_content += f"                <td>N/A</td>\n"
                html_content += f"                <td><a href=\"file:///{os.path.abspath(file_path).replace(os.sep, '/')}\" target=\"_blank\">Open JSON (Corrupted)</a></td>\n"
                html_content += f"            </tr>\n"
            except Exception as e:
                print(f"General error processing {os.path.basename(file_path)}: {e}")
                # You might want to add a generic error row as well

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