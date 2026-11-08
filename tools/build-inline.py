"""Build a self-contained UI with bounded, verified previews; full media loads on demand."""
from pathlib import Path
from PIL import Image
import io,base64,json,re
root=Path(__file__).resolve().parents[1]
previews={}
for p in sorted((root/'assets/thumbs').glob('*.webp')):
 source=root/'assets'/p.name
 if not source.is_file():source=root/'assets'/(p.stem+'.jpg')
 if not source.is_file():source=p
 im=Image.open(source).convert('RGB');im.thumbnail((280,280));out=io.BytesIO();im.save(out,format='WEBP',quality=40,method=6);raw=out.getvalue();assert raw;Image.open(io.BytesIO(raw)).verify();previews[p.stem+'.jpg']='data:image/webp;base64,'+base64.b64encode(raw).decode()
script=(root/'script.js').read_text()
works=json.loads(re.search(r'const works=(\[.*?\]);',script)[1])
for w in works:
 assert w['file'].rsplit('.',1)[0]+'.jpg' in previews
 Image.open(root/'assets'/w['file']).verify()
html=(root/'index.template.html').read_text()
html=re.sub(r'assets/(?:thumbs/)?([\w-]+)\.(?:webp|jpg)(?:\?v=\d+)?',lambda m:previews[m[1]+'.jpg'],html)
html=re.sub(r'<link rel="stylesheet"[^>]+>',lambda m:'<style>'+(root/'style.css').read_text()+'</style>',html)
data='<script type="application/json" id="preview-data">'+json.dumps(previews,separators=(',',':'))+'</script>'
html=re.sub(r'<script defer src="script.js[^\"]*"></script>',lambda m:data+'<script>'+script.replace('</script','<\\/script')+'</script>',html)
(root/'index.html').write_text(html)
print(f'Built {len(previews)} verified inline previews; HTML {len(html.encode()):,} bytes')
