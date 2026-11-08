"""Build a standalone page with compact previews; full-size works stay external."""
from pathlib import Path
import base64
import io
import json
import re
from PIL import Image

root = Path(__file__).resolve().parents[1]
previews = {}
for path in sorted((root / 'assets/thumbs').glob('*.jpg')):
    image = Image.open(path).convert('RGB')
    image.thumbnail((480, 360))
    output = io.BytesIO()
    image.save(output, format='WEBP', quality=52, method=6)
    previews[path.name] = 'data:image/webp;base64,' + base64.b64encode(output.getvalue()).decode()

script = (root / 'script.js').read_text()
works = json.loads(re.search(r'const works=(\[.*?\]);', script).group(1))
required = {re.sub(r'\.[^.]+$', '.jpg', work['file']) for work in works}
required |= {'hero-cover.jpg', 'film-poster.jpg'}
assert required <= previews.keys(), required - previews.keys()
html = (root / 'index.template.html').read_text()
html = re.sub(r'assets/(?:thumbs/)?([^"/]+\.(?:jpg))(?:\?v=\d+)?', lambda m: previews[m[1]], html)
css = (root / 'style.css').read_text()
html = re.sub(r'<link rel="stylesheet" href="style.css[^\"]*">', lambda _: '<style>' + css + '</style>', html)
data = '<script type="application/json" id="preview-data">' + json.dumps(previews, separators=(',', ':')) + '</script>'
html = re.sub(r'<script src="script.js[^\"]*"></script>', lambda _: data + '<script>' + script.replace('</script', '<\\/script') + '</script>', html)
(root / 'index.html').write_text(html)
print(f'Built {len(previews)} embedded previews; HTML {len(html.encode()):,} bytes')
