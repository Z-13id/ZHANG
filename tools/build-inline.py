"""Build the lightweight page; thumbnails stay external and load on demand."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
html=(root/'index.template.html').read_text()
(root/'index.html').write_text(html)
print(f'Built lightweight HTML: {len(html.encode()):,} bytes')
