files = ['library.html','nanolab.html','spiegel.html','sportcentrum.html','waieerauditorium.html','waieercanteen.html']
for f in files:
    with open(f, encoding='utf-8') as fp:
        c = fp.read()
    nav_ok = 'id="hamburger-btn"' in c
    footer_ok = 'University of Twente. The Digital' in c
    drawer_ok = 'id="mobile-drawer"' in c
    print(f'{f}: nav={nav_ok}, drawer={drawer_ok}, footer={footer_ok}')
