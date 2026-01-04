import json
import os
import glob

def find_missing_html():
    dc_path = os.path.join(os.path.dirname(__file__), "_dc")
    dmsguildinfo_path = os.path.join(os.path.dirname(__file__), "dmsguildinfo")
    processed_path = os.path.join(dmsguildinfo_path, "processed")
    output_file = os.path.join("missing_html.html")

    json_files = glob.glob(os.path.join(dc_path, "*.json"))
    
    html_files = set()
    print("--- Loading HTML files ---")
    for path in [dmsguildinfo_path, processed_path]:
        path_exists = os.path.exists(path)
        print(f"Checking path: {path} (exists: {path_exists})")
        # Search recursively for HTML files
        files_found = glob.glob(os.path.join(path, "**", "*.html"), recursive=True)
        print(f"  Found {len(files_found)} HTML files in this path (recursive)")
        for i, filepath in enumerate(files_found):
            filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
            if i < 5: # Print first 5 for verification
                print(f"  Loaded HTML file: {filename_no_ext}")
            html_files.add(filename_no_ext)
    print(f"--- Loaded {len(html_files)} total HTML files ---")

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adventures with Missing HTML</title>
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
    <h1>Adventures with Missing HTML</h1>
    <p>The table below lists adventures that have a JSON file in the <code>_dc</code> directory but do not have a corresponding HTML file in the <code>dmsguildinfo</code> or <code>dmsguildinfo/processed</code> directories.</p>
    <table>
        <thead>
            <tr>
                <th>Adventure Title</th>
                <th>DMsGuild Link</th>
                <th>JSON File</th>
            </tr>
        </thead>
        <tbody>
"""

    missing_count = 0
    non_numeric_product_ids = []
    for file_path in json_files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if data.get("is_adventure") == True:
                    product_id = data.get("product_id")
                    
                    # If product_id is missing from JSON, use filename as fallback
                    if product_id is None:
                        # Extract numeric part from filename (e.g., "230970.json" -> "230970")
                        filename_no_ext = os.path.splitext(filename)[0]
                        product_id = filename_no_ext

                    # Check if product_id is numeric (either int or numeric string)
                    is_numeric = False
                    numeric_product_id = None
                    
                    if product_id is not None:
                        if isinstance(product_id, int):
                            is_numeric = True
                            numeric_product_id = product_id
                        elif isinstance(product_id, str):
                            # Handle product IDs with non-numeric suffixes (e.g., "200609-2" or "200609_2")
                            # We want to extract the first continuous numeric part
                            import re
                            match = re.search(r'(\d+)', product_id)
                            if match:
                                is_numeric = True
                                numeric_product_id = int(match.group(1))
                    
                    if is_numeric and numeric_product_id is not None:
                        html_filename = f"dmsguildinfo-{numeric_product_id}"
                        if html_filename not in html_files:
                            missing_count += 1
                            title = data.get("full_title", os.path.basename(file_path))
                            dmsguild_url = data.get("url", "#")
                            json_file_link = f"file:///{file_path.replace('\\', '/')}"
                            
                            html_content += f"""            <tr>
                        <td>{title}</td>
                        <td><a href=\"{dmsguild_url}\" target=\"_blank\">DMsGuild Page</a></td>
                        <td><a href=\"{json_file_link}\" target=\"_blank\">Open JSON</a></td>
                    </tr>
"""
                    elif product_id:
                        # Product ID exists but is not numeric
                        non_numeric_product_ids.append({
                            "title": data.get("full_title", os.path.basename(file_path)),
                            "product_id": product_id,
                            "json_file_link": f"file:///{file_path.replace('\\', '/')}"
                        })
                        print(f'Skipping non-numeric product_id: {product_id}')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")

    html_content += f"""        </tbody>
    </table>
    <p>Found {missing_count} adventures with missing HTML files.</p>

    <h2>Adventures with Non-Numeric Product IDs</h2>
    <p>The table below lists adventures that have a JSON file in the <code>_dc</code> directory but contain a non-numeric product ID. These should be audited and fixed.</p>
    <table>
        <thead>
            <tr>
                <th>Adventure Title</th>
                <th>Product ID</th>
                <th>JSON File</th>
            </tr>
        </thead>
        <tbody>
"""
    for adventure in non_numeric_product_ids:
        html_content += f"""            <tr>
                <td>{adventure['title']}</td>
                <td>{adventure['product_id']}</td>
                <td><a href=\"{adventure['json_file_link']}\" target=\"_blank\">Open JSON</a></td>
            </tr>
"""

    html_content += f"""        </tbody>
    </table>
    <p>Found {len(non_numeric_product_ids)} adventures with non-numeric product IDs.</p>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated missing_html.html at: {output_file}")
    print(f"Found {missing_count} adventures with missing HTML files.")

if __name__ == "__main__":
    find_missing_html()
