import os, re
import sys

target_files = ['library.html', 'nanolab.html', 'spiegel.html', 'sportcentrum.html', 'waieerauditorium.html', 'waieercanteen.html']

try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()

    nav_match = re.search(r'<!-- Top Navigation Shell -->(.*?)</nav>', index_html, re.DOTALL)
    drawer_match = re.search(r'<div class="mobile-only font-headline" id="mobile-drawer">(.*?)</div>\n    <!-- Main Body Container -->', index_html, re.DOTALL)
    footer_match = re.search(r'<!-- Footer -->(.*?)</footer>', index_html, re.DOTALL)

    if not nav_match or not footer_match:
        print("Failed to find nav or footer in index.html")
        sys.exit(1)

    nav_content = nav_match.group(0)
    drawer_content = f'<div class="mobile-only font-headline" id="mobile-drawer">{drawer_match.group(1)}</div>' if drawer_match else ''
    footer_content = footer_match.group(0)

    # Style block for the mobile menu
    style_match = re.search(r'<style>\n        @media \(max-width: 1024px\).*?</style>', index_html, re.DOTALL)
    style_content = style_match.group(0) if style_match else ''

    script_content = """
    <script>
        function showPage(pageId) {
            if(pageId === 'main-homepage') { window.location.href = 'index.html'; }
        }
        function showHomepage() { window.location.href = 'index.html'; }
        const hamburgerBtn = document.getElementById('hamburger-btn');
        const mobileDrawer = document.getElementById('mobile-drawer');
        if (hamburgerBtn && mobileDrawer) {
            hamburgerBtn.addEventListener('click', () => {
                mobileDrawer.classList.toggle('active');
            });
        }
    </script>
"""

    for filename in target_files:
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We need to replace only the outermost/main <nav> element. Usually at the top.
        # So we can search for `<nav ...>` and then `</nav>`. But `<nav` might be nested. 
        # But in these templates, the TopNavBar is usually the first `<nav` in the document.
        new_nav = nav_content + '\n    ' + drawer_content
        
        # Using a regex to replace the text between <!-- TopNavBar --> and the VERY FIRST </nav> after it, or if missing, the FIRST <nav> ... </nav> overall.
        match = re.search(r'<!-- TopNavBar -->\s*<nav[^>]*>.*?</nav>', content, flags=re.DOTALL)
        if match:
            content = content[:match.start()] + new_nav + content[match.end():]
        else:
            # First nav
            match2 = re.search(r'<nav[^>]*>.*?</nav>', content, flags=re.DOTALL)
            if match2:
                content = content[:match2.start()] + new_nav + content[match2.end():]

        # Same for footer
        footer_m = re.search(r'<!-- Footer -->\s*<footer[^>]*>.*?</footer>', content, flags=re.DOTALL)
        if footer_m:
            content = content[:footer_m.start()] + footer_content + content[footer_m.end():]
        else:
            footer_m2 = re.search(r'<footer[^>]*>.*?</footer>', content, flags=re.DOTALL)
            if footer_m2:
                content = content[:footer_m2.start()] + footer_content + content[footer_m2.end():]

        # Add style if not present
        if '@media (max-width: 1024px)' not in content and style_content:
            content = content.replace('</head>', '\n    ' + style_content + '\n</head>')
            
        # Add script if not present
        if 'hamburgerBtn' not in content:
            content = content.replace('</body>', script_content + '\n</body>')
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {filename}.')

except Exception as e:
    import traceback
    traceback.print_exc()
