"""Dependency-free checks for the static GitHub Pages site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.h1_count = 0
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.h1_count += 1
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs['id'])
        if tag == 'img' and not attrs.get('alt'):
            self.errors.append('Image missing descriptive alt text')
        for key in ('src', 'href'):
            if key in attrs:
                self.links.append(attrs[key])

page = Page()
page.feed((ROOT / 'index.html').read_text())
assert page.h1_count == 1, 'Expected one primary heading'
for link in page.links:
    parts = urlsplit(link)
    if parts.scheme:
        assert parts.scheme in ('https', 'mailto'), f'Unexpected scheme: {link}'
    elif parts.path:
        assert (ROOT / parts.path).is_file(), f'Missing asset: {link}'
    elif parts.fragment:
        assert parts.fragment in page.ids, f'Missing anchor: {link}'
    else:
        raise AssertionError(f'Empty link: {link}')
for svg in (ROOT / 'assets').glob('*.svg'):
    ET.parse(svg)
assert (ROOT / 'CNAME').read_text().strip() == 'felixyangucas.com'
assert not page.errors, page.errors
print(f'PASS: {len(page.links)} links/assets, {len(page.ids)} unique IDs, SVG syntax, image alternatives, heading, custom domain')
