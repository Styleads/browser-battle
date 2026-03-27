import os
import re

replacements = {
    'Campus': 'campus.html',
    'Placements': 'placements.html',
    'Notable Alumni': 'alumni.html',
    'Academics': 'academics.html',
    'Admissions': 'admissions.html',
    'Homepage': 'index.html'
}

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in html_files:
    file_path = os.path.abspath(filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for label, target in replacements.items():
        # This regex looks for:
        # 1. <a
        # 2. optional stuff
        # 3. href="#" or href=""
        # 4. optional stuff
        # 5. >
        # 6. any content containing the label (including icons and nested divs)
        # 7. </a>
        
        # We use a pattern that matches the <a> tag until its closing </a>
        # ensuring the label is inside.
        pattern = re.compile(rf'(<a\s+[^>]*?href\s*=\s*")(#?)("[^>]*?>.*?{label}.*?</a>)', re.IGNORECASE | re.DOTALL)
        
        def rep(match):
            if match.group(2) in ['#', '']:
                return match.group(1) + target + match.group(3)
            return match.group(0)
            
        new_content = pattern.sub(rep, new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
