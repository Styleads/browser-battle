import os
import re

def fix_apply_now(file_path):
    if os.path.getsize(file_path) == 0:
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Find all <button> tags individually
    # Pattern: <button [attrs]>[content]</button>
    button_pattern = re.compile(r'(<button\s+)([^>]*?)(>)(.*?)(</button>)', re.IGNORECASE | re.DOTALL)
    
    def button_replacer(match):
        prefix = match.group(1)
        attrs = match.group(2)
        tag_start = match.group(3)
        tag_content = match.group(4)
        tag_end = match.group(5)
        
        # Check if "Apply Now" is in the tag content
        if re.search(r'Apply\s*Now', tag_content, re.IGNORECASE):
            # If it already has onclick, replace the destination
            if 'onclick' in attrs:
                new_attrs = re.sub(r'onclick\s*=\s*"[^"]*"', 'onclick="window.location.href=\'admissions.html\'"', attrs)
                if new_attrs == attrs: # Standard onclick not found
                    new_attrs = attrs + ' onclick="window.location.href=\'admissions.html\'"'
                attrs = new_attrs
            else:
                attrs = attrs + ' onclick="window.location.href=\'admissions.html\'"'
            
        return f"{prefix}{attrs}{tag_start}{tag_content}{tag_end}"

    content = button_pattern.sub(button_replacer, content)

    # 2. Handle <a> tags
    # Find all <a> tags individually
    link_tag_pattern = re.compile(r'(<a\s+)([^>]*?)(>)(.*?)(</a>)', re.IGNORECASE | re.DOTALL)
    
    def link_replacer(match):
        prefix = match.group(1)
        attrs = match.group(2)
        tag_start = match.group(3)
        tag_content = match.group(4)
        tag_end = match.group(5)
        
        # Check if "Apply Now" is in the tag content
        if re.search(r'Apply\s*Now', tag_content, re.IGNORECASE):
            # Update href in attributes
            if 'href="' in attrs:
                new_attrs = re.sub(r'href\s*=\s*"[^"]*"', 'href="admissions.html"', attrs)
                attrs = new_attrs
            else:
                attrs = attrs + ' href="admissions.html"'
                
        return f"{prefix}{attrs}{tag_start}{tag_content}{tag_end}"

    content = link_tag_pattern.sub(link_replacer, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in root: continue
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                if fix_apply_now(file_path):
                    print(f"Updated Apply Now in: {file_path}")
                    count += 1
    print(f"Total files updated: {count}")
