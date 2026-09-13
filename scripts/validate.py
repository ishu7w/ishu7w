"""Validate generated assets, references, SVG safety, and profile facts."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
readme=(ROOT/'README.md').read_text()
assert not re.search(r'<(?:script|style|iframe|table)\b',readme,re.I)
assert not re.search(r'\s(?:style|on\w+)\s*=',readme,re.I)
for path in re.findall(r'(?:src|srcset)="([^"]+)"',readme):
    assert not path.startswith(('http:','https:')),f'External image: {path}'
    assert (ROOT/path).is_file(),f'Missing asset: {path}'
for tag in re.findall(r'<img\b[^>]+>',readme):assert 'alt=' in tag
for path in ROOT.rglob('*.svg'):
    tree=ET.fromstring(path.read_text());assert 'viewBox' in tree.attrib,path
    for el in tree.iter():
        assert el.tag.split('}')[-1] not in ('script','foreignObject','image'),path
        assert not any(k.lower().startswith('on') for k in el.attrib),path
    assert path.stat().st_size<250000,(path,'oversized SVG')
p=json.loads((ROOT/'data/profile.json').read_text());s=json.loads((ROOT/'data/stats.json').read_text())
assert p['username']=='ishu7w'
assert all(v>=0 for v in s['language_bytes'].values())
assert all(isinstance(s[k],int) and s[k]>=0 for k in ['public_repositories','stars','followers','merged_upstream_prs'])
assert readme.count('<details>')==readme.count('</details>')
assert readme.count('<picture>')==readme.count('</picture>')
print(f'Validated README, {len(list(ROOT.rglob("*.svg")))} SVGs, all image references, and public statistics.')
