import os
import glob
import json
import re

def main():
    json_files = glob.glob('maintaindb/_dc/*.json')
    updated_count = 0
    
    for filepath in json_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        full_title = data.get('full_title')
        code = data.get('code')
        original_title = data.get('title')
        
        # We only care about adventures that have a code and a full title
        if not data.get('is_adventure') or not code or not full_title:
            continue
            
        clean_title = full_title.strip()
        code_upper = code.upper()
        
        if clean_title.upper() in [code_upper, f"({code_upper})", f"[{code_upper}]", f"<{code_upper}>"]:
            title = full_title
        else:
            title = full_title
            dash_variants = ['\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2212']
            normalized_title_for_strip = title
            for dash_char in dash_variants:
                normalized_title_for_strip = normalized_title_for_strip.replace(dash_char, '-')
            
            safe_code = re.escape(code_upper)
            
            # 1. Strip from beginning
            start_pattern = r'^\s*[\(\[<]?\s*' + safe_code + r'\s*[\)\]>]?[\s\-:]*'
            match = re.search(start_pattern, normalized_title_for_strip, re.IGNORECASE)
            if match:
                title = title[match.end():].strip()
                normalized_title_for_strip = normalized_title_for_strip[match.end():].strip()

            # 2. Strip from end
            end_pattern = r'[\s\-:]*[\(\[<]?\s*' + safe_code + r'\s*[\)\]>]?\s*$'
            match = re.search(end_pattern, normalized_title_for_strip, re.IGNORECASE)
            if match:
                title = title[:match.start()].strip()
                
            if not title.strip(" ,:-"):
                title = full_title
            else:
                title = title.strip(" ,:-")

        if title != original_title:
            data['title'] = title
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            updated_count += 1
            # print(f"Updated {original_title} -> {title}")
            
    print(f"Successfully stripped codes from titles across {updated_count} JSON files.")

if __name__ == '__main__':
    main()
