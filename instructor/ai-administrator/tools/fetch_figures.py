#!/usr/bin/env python3
"""Download the figures hot-linked by src/llm_agents.html into figures/ and write figures/manifest.json."""
import re, json, html, pathlib, urllib.request, sys
HERE = pathlib.Path(__file__).resolve().parent.parent
SRC = HERE.parents[1] / "src" / "llm_agents.html"
OUT = HERE / "figures"; OUT.mkdir(exist_ok=True)
page = SRC.read_text()
seen = {}
for m in re.finditer(r'<img[^>]+>', page):
    tag = m.group(0)
    src = re.search(r'src="([^"]+)"', tag); alt = re.search(r'alt="([^"]*)"', tag)
    if not src: continue
    src = html.unescape(src.group(1)); alt = html.unescape(alt.group(1)) if alt else pathlib.Path(src).stem
    slug = re.sub(r'[^a-z0-9]+', '-', alt.lower()).strip('-')
    if not src.startswith('http'): slug = 'local-' + pathlib.Path(src).stem   # e.g. local-book
    if slug in seen: continue
    if src.startswith('http'):
        dest = OUT / f"{slug}.png"
        if not dest.exists():
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r: dest.write_bytes(r.read())
    else:
        local = HERE.parents[1] / "src" / src.lstrip('/')
        dest = OUT / f"{slug}{local.suffix}"
        if not dest.exists(): dest.write_bytes(local.read_bytes())
    seen[slug] = {"alt": alt, "file": dest.name, "source": src}
    print(f"{slug:40s} {dest.stat().st_size//1024:5d} KB")
(OUT / "manifest.json").write_text(json.dumps(seen, indent=2))
print(len(seen), "figures")
