#!/usr/bin/env python3
"""Generate a GitHub-compatible profile from public facts. No third-party stats service."""
import argparse
import collections
import datetime
import html
import json
from pathlib import Path
import subprocess
import textwrap
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / 'data/profile.json').read_text())
E = lambda value: html.escape(str(value), quote=True)
BG, FG, MUTED, LINE, CYAN, BLUE, PURPLE = '#0b1020', '#f1f5ff', '#b2c1d9', '#24334e', '#7dd9ed', '#8caeff', '#b7a0ff'

def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], text=True))

def fetch_stats():
    user = P['username']
    profile = api(f'users/{user}')
    repos, page = [], 1
    while True:
        chunk = api(f'users/{user}/repos?type=owner&per_page=100&page={page}')
        repos.extend(r for r in chunk if not r['private'])
        if len(chunk) < 100: break
        page += 1
    owned = [r for r in repos if not r['fork']]
    languages = collections.Counter()
    for r in owned:
        languages.update(api(f'repos/{user}/{r["name"]}/languages'))
    query = urllib.parse.quote(f'author:{user} is:pr is:merged is:public -user:{user}')
    merged = api(f'search/issues?q={query}&per_page=1')['total_count']
    stats = {'updated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'),
             'public_repositories': len(repos), 'original_repositories': len(owned),
             'stars': sum(r['stargazers_count'] for r in owned), 'followers': profile['followers'],
             'merged_upstream_prs': merged, 'language_bytes': dict(languages.most_common()),
             'source': f'https://api.github.com/users/{user}/repos',
             'scope': 'Public repositories only. Stars and language bytes exclude forks. Merged PRs exclude own repositories.'}
    # Refresh known public contributions without broadening the published data.
    states = {}
    for c in P['contributions']:
        parts = c['url'].split('/')
        pr = api(f'repos/{parts[3]}/{parts[4]}/pulls/{parts[6]}')
        states[c['url']] = 'Merged' if pr['merged'] else ('Open' if pr['state'] == 'open' else 'Closed')
    stats['contribution_states'] = states
    (ROOT / 'data/stats.json').write_text(json.dumps(stats, indent=2) + '\n')
    return stats

STYLE = f'''text{{font-family:Arial,Helvetica,sans-serif;fill:{FG}}}.muted{{fill:{MUTED}}}.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.signal{{stroke-dasharray:18 480;animation:flow 12s linear infinite}}.cursor{{animation:cursor 1.6s step-end infinite}}@keyframes flow{{to{{stroke-dashoffset:-996}}}}@keyframes cursor{{50%{{opacity:0}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.signal{{stroke-dasharray:none}}}}'''

def svg(path, w, h, title, body, css=''):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{E(title)}</title><style>{STYLE}{css}</style>{body}</svg>\n')

def text(x, y, content, size=18, color=FG, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" style="fill:{color}" {extra}>{E(content)}</text>'

def surface(w, h):
    return f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>'

def hero(mobile=False):
    w,h = (480,360) if mobile else (960,410)
    cx=w/2
    body=surface(w,h)
    body+='''<defs><radialGradient id="a"><stop stop-color="#233b62" stop-opacity=".8"/><stop offset="1" stop-color="#0b1020" stop-opacity="0"/></radialGradient><linearGradient id="s"><stop stop-color="#7dd9ed"/><stop offset=".5" stop-color="#8caeff"/><stop offset="1" stop-color="#b7a0ff"/></linearGradient></defs>'''
    body+=f'<ellipse cx="{cx}" cy="190" rx="{w*.48}" ry="200" fill="url(#a)"/>'
    # Data paths meet at the name; restrained motion is purely decorative.
    for side in (-1,1):
        for i in range(3):
            x=cx+side*(218 if mobile else 400)
            y=65+i*32
            d=f'M {cx+side*w/2} {y} H {x} Q {x-side*12} {y} {x-side*12} {y+12} V {h-65-i*18} H {cx+side*(205 if mobile else 372)}'
            body+=f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1"/><path class="signal" d="{d}" fill="none" stroke="url(#s)" stroke-width="1.5" style="animation-delay:-{i*3}s"/>'
    body+=text(cx,105 if mobile else 130,P['name'],60 if mobile else 88,extra='text-anchor="middle" font-weight="700" letter-spacing="-3"')
    body+=text(cx,144 if mobile else 177,'Computer Science & Engineering student',19 if mobile else 24,MUTED,'text-anchor="middle"')
    y=201 if mobile else 238
    css=''
    body+=text(cx,y,P['roles'][0],23 if mobile else 28,CYAN,'text-anchor="middle" class="fallback"')
    for i,role in enumerate(P['roles']):
        body+=f'<g class="role r{i}" opacity="0">'+text(cx,y,role,23 if mobile else 28,CYAN,'text-anchor="middle"')+'</g>'
        start=i*25
        # Each phrase gets a slow reveal, hold, and exit; static default stays useful.
        css+=f'@keyframes role{i}{{0%,100%{{opacity:0;clip-path:inset(0 100% 0 0)}}{start+.1}%{{opacity:1;clip-path:inset(0 100% 0 0)}}{start+8}%,{start+21}%{{opacity:1;clip-path:inset(0 0 0 0)}}{start+24}%{{opacity:0;clip-path:inset(0 0 0 0)}}}}'
    css+='@media(prefers-reduced-motion:no-preference){.fallback{opacity:0}' + ''.join(f'.r{i}{{animation:role{i} 24s linear infinite}}' for i in range(4)) + '}'
    body+=f'<path d="M {cx-80} {y+25} H {cx+80}" stroke="url(#s)" opacity=".7"/>'
    if mobile:
        body+=text(cx,277,'Learning the fundamentals.',19,MUTED,'text-anchor="middle"')+text(cx,305,'Building beyond the exercise.',19,MUTED,'text-anchor="middle"')
    else: body+=text(cx,316,P['statement'],23,MUTED,'text-anchor="middle"')
    svg('assets/hero-mobile.svg' if mobile else 'assets/hero.svg',w,h,'Ishu Patel — CSE student. Java, DSA, practical software and AI agents.',body,css)

def terminal():
    body=surface(640,276)
    body+=f'<path d="M 0 47 H 640" stroke="{LINE}"/>'
    for i,c in enumerate([BLUE,PURPLE,CYAN]):body+=f'<circle cx="{26+i*17}" cy="24" r="4" fill="{c}" opacity=".7"/>'
    body+=text(610,30,'current-focus.java',14,MUTED,'text-anchor="end" class="mono"')
    body+=text(26,84,'ishu@github:~$ current-focus',21,CYAN,'class="mono"')
    for i,(key,val) in enumerate(P['focus'].items()):
        body+=text(26,126+i*34,key,18,PURPLE,'class="mono"')+text(183,126+i*34,val,19,FG)
    body+=f'<rect class="cursor" x="580" y="239" width="10" height="19" fill="{CYAN}"/>'
    svg('assets/terminal.svg',640,276,'Current focus: '+ '; '.join(P['focus'].values()),body)
    b=surface(480,348)+text(24,40,'ishu@github:~$ current-focus',21,CYAN,'class="mono"')
    for i,(key,val) in enumerate(P['focus'].items()):
        b+=text(24,84+i*65,key.upper(),13,PURPLE,extra='letter-spacing="1"')+text(24,112+i*65,val,22)
    b+=f'<rect class="cursor" x="438" y="306" width="10" height="19" fill="{CYAN}"/>'
    svg('assets/terminal-mobile.svg',480,348,'Current focus: '+ '; '.join(P['focus'].values()),b)

def motif(kind):
    if kind=='timer':return '<circle cx="391" cy="75" r="26"/><path d="M391 56 V75 L405 83 M385 38 H397"/>'
    if kind=='heap':return '<path d="M391 46 L365 77 M391 46 L417 77 M365 77 L350 100 M365 77 L380 100"/><circle cx="391" cy="46" r="6"/><circle cx="365" cy="77" r="5"/><circle cx="417" cy="77" r="5"/>'
    if kind=='chart':return '<path d="M349 93 H430 M350 95 V42 M355 83 L373 65 L389 73 L411 45 L428 51"/>'
    return '<path d="M354 47 H376 L400 72 H429 M354 73 H376 L400 47 H429 M354 99 H376 L400 99 H429"/><circle cx="350" cy="47" r="4"/><circle cx="350" cy="73" r="4"/><circle cx="350" cy="99" r="4"/>'

def cards():
    for p in P['projects']:
        b=surface(460,234)
        b+=f'<g stroke="{BLUE}" stroke-width="1.5" fill="none" opacity=".8">{motif(p["motif"])}</g>'
        b+=text(26,47,p['name'],31,extra='font-weight="700" letter-spacing="-.8"')
        b+=text(26,76,p['category'],11,CYAN,extra='letter-spacing="1.2"')
        b+=text(26,122,p['description'],18,MUTED)+text(26,149,p['description2'],18,MUTED)
        b+=f'<path d="M26 173 H434" stroke="{LINE}"/>'
        b+=text(26,207,p['stack'],15,FG)+text(434,207,'↗',22,CYAN,'text-anchor="end"')
        svg(f'assets/project-cards/{p["slug"]}.svg',460,234,p['name']+': '+p['description']+' '+p['description2']+' '+p['stack'],b)
        b=surface(360,266)+text(24,45,p['name'],30,extra='font-weight="700" letter-spacing="-.8"')
        b+=text(24,76,p['category'],13,CYAN)
        for i,line in enumerate(textwrap.wrap(p['description']+' '+p['description2'],32)):
            b+=text(24,120+i*27,line,19,MUTED)
        b+=f'<path d="M24 214 H336" stroke="{LINE}"/>'
        b+=text(24,245,p['stack'],16)
        svg(f'assets/project-cards/{p["slug"]}-mobile.svg',360,266,p['name']+': '+p['description']+' '+p['description2']+' '+p['stack'],b)

def analytics(stats):
    b=surface(640,270)
    labels=[('Public repos',stats['public_repositories']),('Stars¹',stats['stars']),('Followers',stats['followers']),('Merged PRs²',stats['merged_upstream_prs'])]
    for i,(label,value) in enumerate(labels):
        x=25+i*155
        b+=text(x,56,value,35,FG,extra='font-weight="700"')+text(x,83,label,15,MUTED)
    b+=f'<path d="M25 107 H615" stroke="{LINE}"/>'
    b+=text(25,135,'Language mix · public non-fork code by bytes',17,FG)
    langs=list(stats['language_bytes'].items());total=sum(v for _,v in langs)
    colors=[BLUE,CYAN,PURPLE,'#d7b384','#9bc6ab','#d8a1c2']
    x=25
    for i,(name,value) in enumerate(langs[:5]):
        width=590*value/total if total else 0
        b+=f'<rect x="{x:.2f}" y="154" width="{width:.2f}" height="6" fill="{colors[i]}"/>';x+=width
    for i,(name,value) in enumerate(langs[:3]):
        b+=text(25+i*198,193,f'{name} {100*value/total:.1f}%',15,colors[i])
    b+=text(25,234,'GitHub API · '+stats['updated']+' UTC',13,MUTED)
    svg('assets/analytics.svg',640,270,'GitHub public statistics, updated '+stats['updated']+': '+', '.join(f'{n} {v}' for n,v in labels),b)
    b=surface(480,380)
    for i,(label,value) in enumerate(labels):
        x=26+(i%2)*232;y=58+(i//2)*92
        b+=text(x,y,value,36,extra='font-weight="700"')+text(x,y+28,label,23,MUTED)
    b+=f'<path d="M26 205 H454" stroke="{LINE}"/>'
    b+=text(26,236,'Language mix · code bytes¹',23)
    for i,(name,value) in enumerate(langs[:3]):
        b+=text(26,268+i*27,name,23,colors[i])+text(452,268+i*27,f'{100*value/total:.1f}%',23,colors[i],'text-anchor="end"')
    b+=text(26,357,'GitHub API · '+stats['updated']+' UTC',15,MUTED)
    svg('assets/analytics-mobile.svg',480,380,'GitHub public statistics, updated '+stats['updated'],b)

def accents():
    svg('assets/divider.svg',960,24,'Section divider',f'<path d="M0 12 H960" stroke="{LINE}"/><path class="signal" d="M0 12 H960" stroke="{BLUE}"/>')
    svg('assets/footer.svg',640,94,'Understand it. Build it. Make it better.',surface(640,94)+text(320,55,'Understand it. Build it. Make it better.',23,MUTED,'text-anchor="middle"')+f'<path class="signal" d="M70 78 H570" stroke="{CYAN}"/>')
    for label,file,w in [('Explore projects','projects',176),('Email Ishu','email',140),('GitHub','github',118)]:
        svg(f'assets/{file}-button.svg',w,40,label,f'<rect x=".5" y=".5" width="{w-1}" height="39" rx="8" fill="{BG}" stroke="{LINE}"/>'+text(w/2,26,label,15,CYAN,'text-anchor="middle"'))

def readme(stats):
    u=P['username'];content='''<!--
THESIS: A build signal connects learning, products, and upstream work.
OWN-WORLD: Ink navy panels, pale typography, cyan signals, blue geometry, restrained violet.
STORY: Meet Ishu; explore concrete projects; inspect public contributions; connect.
FIRST VIEWPORT: Centered animated name banner, short student identity, and two clear links.
FORM: User-pinned premium technical portfolio; seed 2000cf0b is overridden by the explicit brief.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md
Generated by scripts/generate-assets.py. Edit data/profile.json, then regenerate.
-->
<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/hero-mobile-static.svg" />
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/hero-static.svg" />
    <source media="(max-width: 600px)" srcset="assets/hero-mobile.svg" />
    <img src="assets/hero.svg" width="100%" alt="Ishu Patel — Computer Science & Engineering student. Learning Java and DSA, building useful software, and exploring AI agents." />
  </picture>
</p>
<p align="center">
  <a href="#selected-projects"><img src="assets/projects-button.svg" width="176" alt="Explore projects" /></a>
  <a href="mailto:EMAIL"><img src="assets/email-button.svg" width="140" alt="Email Ishu" /></a>
</p>

I'm **Ishu Patel**, a Computer Science & Engineering student working on Java, data structures, and software that solves practical problems. I build full-stack projects, explore AI agents, and contribute fixes to open-source Java tools. Hackathons give me a reason to turn an idea into something people can try.

### On my workbench

<p align="center"><picture><source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="assets/terminal-mobile-static.svg" /><source media="(prefers-reduced-motion: reduce)" srcset="assets/terminal-static.svg" /><source media="(max-width: 600px)" srcset="assets/terminal-mobile.svg" /><img src="assets/terminal.svg" width="640" alt="FOCUS" /></picture></p>

<details>
<summary>Current focus, in plain text</summary>

FOCUS_TEXT

</details>

### Tools I build with

STACK

**Exploring:** AI agents, LLM-assisted applications, and explainable decision systems.

<img src="assets/divider.svg" width="100%" alt="" />

## Selected projects

Small products, practical systems, and the ideas behind them. Cards open the source.

'''.replace('EMAIL',P['contact']['email']).replace('FOCUS_TEXT','\n'.join(f'- **{k.title()}:** {v}' for k,v in P['focus'].items())).replace('FOCUS',E('; '.join(P['focus'].values())))
    groups=[('Languages',[('java','Java'),('typescript','TypeScript'),('javascript','JavaScript')]),('Interface',[('react','React'),('nextjs','Next.js'),('vitejs','Vite'),('html5','HTML'),('css3','CSS')]),('Server & data',[('nodejs','Node.js'),('supabase','Supabase'),('postgresql','PostgreSQL')]),('Version control',[('git','Git'),('github','GitHub')])]
    stack=''
    for group,icons in groups:
        stack+=f'**{group}** — '+ ' · '.join(label for _,label in icons)+'\n\n<p>\n'
        stack+='\n'.join(f'  <img src="assets/icons/{key}.svg" width="32" height="32" alt="{label}" />' for key,label in icons)+'\n</p>\n\n'
    content=content.replace('STACK',stack.strip())
    for p in P['projects']:
        desc=E(p['name']+' — '+p['description']+' '+p['description2']+' '+p['stack'])
        content+=f'<a href="https://github.com/{u}/{p["slug"]}"><picture><source media="(max-width: 600px)" srcset="assets/project-cards/{p["slug"]}-mobile.svg" /><img src="assets/project-cards/{p["slug"]}.svg" width="400" alt="{desc}" /></picture></a>\n'
    content+='\n**Try the demos:** '+ ' · '.join(f'[{p["name"]}]({p["demo"]})' for p in P['projects'] if p['demo'])+'\n\n'
    content+='<details>\n<summary>Project details, in plain text</summary>\n\n'
    for p in P['projects']:content+=f'**[{p["name"]}](https://github.com/{u}/{p["slug"]})** — {p["description"]} {p["description2"]} Built with {p["stack"]}.\n\n'
    content+='</details>\n\n<img src="assets/divider.svg" width="100%" alt="" />\n\n## In the open\n\n'
    content+='<p align="center"><picture><source media="(max-width: 600px)" srcset="assets/analytics-mobile.svg" /><img src="assets/analytics.svg" width="640" alt="Public GitHub statistics; exact values and scope are available below." /></picture></p>\n\n'
    content+=f'<details>\n<summary>Numbers, sources & scope · updated {stats["updated"]}</summary>\n\n'
    content+=f'- **{stats["public_repositories"]}** public repositories, including forks.\n- **{stats["stars"]}** stars across public, non-fork repositories (¹).\n- **{stats["followers"]}** followers.\n- **{stats["merged_upstream_prs"]}** merged public pull requests outside my own repositories (²).\n'
    content+='- Language proportions measure code bytes across public non-fork repositories; they are not proficiency ratings.\n- [Snapshot and language totals](data/stats.json) · [GitHub profile](https://github.com/ishu7w)\n\n</details>\n\n'
    content+='''### A year of contributions

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/contributions-static.svg" />
  <source media="(prefers-color-scheme: dark)" srcset="dist/github-contribution-grid-snake-dark.svg" />
  <img src="dist/github-contribution-grid-snake.svg" width="100%" alt="Animated snake tracing my GitHub contribution calendar. View the accessible contribution history on my GitHub profile." />
</picture>

[Explore my contribution history](https://github.com/ishu7w?tab=overview) · Refreshed daily from GitHub.

### Java, DSA & real code

I'm learning data structures through Java and applying the same ideas in projects: a [max-heap delivery queue](https://github.com/ishu7w/logistics-delivery-system) and work on a [Java metro route planner](https://github.com/ishu7w/Delhi-Metro-Navigator). My focus is understanding the algorithm, the edge cases, and the tradeoffs.

### Beyond my own repositories

'''
    for c in P['contributions']:
        status=stats.get('contribution_states',{}).get(c['url'],c['status'])
        content+=f'- **[{c["project"]}]({c["url"]})** — {c["description"]}. *{status}.*\n'
    content+='\n<img src="assets/divider.svg" width="100%" alt="" />\n\n## Have a useful problem in mind?\n\nI’m interested in practical AI products, open-source Java work, and hackathon collaborations. Let’s build something people can try.\n\n<p align="center">\n'
    content+=f'<a href="mailto:{P["contact"]["email"]}"><img src="assets/email-button.svg" width="140" alt="Email Ishu at {P["contact"]["email"]}" /></a>\n<a href="https://github.com/{u}"><img src="assets/github-button.svg" width="118" alt="Ishu on GitHub" /></a>\n</p>\n'
    for key in ('linkedin','portfolio'):
        if P['contact'].get(key):content+=f'[{key.title()}]({P["contact"][key]})\n'
    content+='\n<p align="center"><img src="assets/footer.svg" width="640" alt="Understand it. Build it. Make it better." /></p>\n'
    for name,width,alt in [('divider','100%',''),('footer','640','Understand it. Build it. Make it better.')]:
        original=f'<img src="assets/{name}.svg" width="{width}" alt="{alt}" />'
        content=content.replace(original,f'<picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/{name}-static.svg" />{original}</picture>')
    (ROOT/'README.md').write_text(content)

def main():
    args=argparse.ArgumentParser();args.add_argument('--refresh',action='store_true');options=args.parse_args()
    stats=fetch_stats() if options.refresh else json.loads((ROOT/'data/stats.json').read_text())
    hero();hero(True);terminal();cards();analytics(stats);accents();readme(stats)
    for name in ('hero','hero-mobile','terminal','terminal-mobile','divider','footer'):
        source=(ROOT/f'assets/{name}.svg').read_text()
        source=source.replace('</svg>','<style>*{animation:none!important}.fallback{opacity:1!important}.role{display:none!important}</style></svg>')
        (ROOT/f'assets/{name}-static.svg').write_text(source)
    print('Generated README and custom SVG assets.')

if __name__=='__main__':main()
