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
        for i, filepath in enumerate(glob.glob(os.path.join(path, "*.html"))):
            filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
            if i < 5: # Print first 5 for verification
                print(f"Loaded HTML file: {filename_no_ext}")
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
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if data.get("is_adventure") == True:
                    product_id = data.get("product_id")
                    if product_id and isinstance(product_id, int):
                        html_filename = f"dmsguildinfo-{product_id}"
                        print(f'Checking for: {html_filename}')  # Diagnostic print
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
                        print(f'Skipping non-integer product_id: {product_id}')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {os.path.basename(file_path)}: {e}")

    html_content += f"""        </tbody>
    </table>
    <p>Found {missing_count} adventures with missing HTML files.</p>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated missing_html.html at: {output_file}")
    print(f"Found {missing_count} adventures with missing HTML files.")

if __name__ == "__main__":
    find_missing_html()
