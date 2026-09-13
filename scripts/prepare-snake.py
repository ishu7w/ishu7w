"""Provide a still contribution calendar and reduced-motion behavior for snk SVGs."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
for name in ['github-contribution-grid-snake.svg','github-contribution-grid-snake-dark.svg']:
    path=ROOT/'dist'/name
    source=path.read_text()
    ET.fromstring(source)
    source=source.replace('</svg>','<style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style></svg>')
    path.write_text(source)
    if name=='github-contribution-grid-snake-dark.svg':
        # The first frame shows the unconsumed calendar; disable all timeline movement.
        source=source.replace('</svg>','<style>*{animation:none!important}</style></svg>')
        (ROOT/'assets/contributions-static.svg').write_text(source)
print('Prepared animated and still contribution calendars.')
