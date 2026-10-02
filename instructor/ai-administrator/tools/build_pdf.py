#!/usr/bin/env python3
"""Render branded PDFs: instructor guide (from the session YAML) and participant handouts / quiz banks (from markdown).

Usage:
  build_pdf.py guide content/day1_session1.yaml out/day1/Day1_S1_Instructor_Guide.pdf
  build_pdf.py md    content/day1_lab1.md       out/day1/Day1_S1_Lab_Handout.pdf

Markdown -> HTML via pandoc; HTML -> PDF via headless Google Chrome. White pages, black text, logo strip header.
"""
import sys, re, html, pathlib, subprocess, tempfile, base64, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGO = base64.b64encode((ROOT / "brand" / "header_strip.png").read_bytes()).decode()

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #111; font-size: 10.5pt; line-height: 1.45; }
.strip { text-align: center; margin-bottom: 6mm; } .strip img { height: 15mm; }
h1 { font-size: 22pt; margin: 0 0 2mm 0; } .sub { color: #666; font-size: 11pt; margin-bottom: 1mm; }
.kind { color: #666; font-size: 9.5pt; margin-bottom: 6mm; padding-bottom: 3mm; border-bottom: 2px solid #F7A11A; }
h2 { font-size: 14pt; margin: 8mm 0 2mm 0; padding-bottom: 1mm; border-bottom: 1px solid #ddd; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 5mm 0 1.5mm 0; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm 0; font-size: 9.5pt; page-break-inside: auto; }
th, td { border: 1px solid #ccc; padding: 1.6mm 2.2mm; vertical-align: top; text-align: left; }
th { background: #f2f2f2; } tr { page-break-inside: avoid; }
pre { background: #f5f5f5; border: 1px solid #ddd; padding: 3mm; font-size: 9pt; white-space: pre-wrap; page-break-inside: avoid; }
code { font-family: Menlo, 'Courier New', monospace; font-size: 9pt; }
ul, ol { margin: 1mm 0 3mm 0; padding-left: 6mm; } li { margin-bottom: 1mm; }
.notes { font-size: 9.5pt; color: #222; } .slide { margin-bottom: 3.5mm; page-break-inside: avoid; }
.slide .t { font-weight: 600; } .slide .l { color: #666; font-size: 9pt; }
.footer { color: #666; font-size: 8.5pt; margin-top: 8mm; border-top: 1px solid #ddd; padding-top: 2mm; }
blockquote { margin: 2mm 0; padding: 2mm 4mm; border-left: 3px solid #F7A11A; background: #fafafa; }
"""


def wrap(title, subtitle, kind, body, footer):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><div class="strip"><img src="data:image/png;base64,{LOGO}"></div>
<h1>{html.escape(title)}</h1><div class="sub">{html.escape(subtitle)}</div><div class="kind">{html.escape(kind)}</div>
{body}<div class="footer">{html.escape(footer)}</div></body></html>"""


def to_pdf(html_text, out_path):
    out_path = pathlib.Path(out_path); out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = pathlib.Path(td) / "page.html"; src.write_text(html_text)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out_path}", f"file://{src}"], check=True, capture_output=True, timeout=120)
    print(out_path, out_path.stat().st_size // 1024, "KB")


def md_to_html(md_text):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html"], input=md_text, text=True, capture_output=True, check=True).stdout


def build_md(md_path, out_path):
    text = pathlib.Path(md_path).read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S); fm = yaml.safe_load(m.group(1)); body = m.group(2)
    footer = "IEEE CS Region 8 AI Caravan 2026 · AI Administrator track · Course materials by Dr. Abdulkarim Al-Banna · albanna-tutorials.com"
    to_pdf(wrap(fm["title"], fm["subtitle"], fm["kind"], md_to_html(body), footer), out_path)


def esc(x): return html.escape(str(x))


def build_guide(yaml_path, out_path):
    doc = yaml.safe_load(pathlib.Path(yaml_path).read_text()); meta = doc["meta"]; slides = doc["slides"]
    parts = []
    parts.append("<h2>Session at a glance</h2><table><tr><th>Day / session</th><td>Day %s · Session %s · %s minutes</td></tr>"
                 "<tr><th>Lead instructors</th><td>%s</td></tr><tr><th>Online module</th><td>%s</td></tr><tr><th>Deck</th><td>%s</td></tr></table>"
                 % (meta["day"], meta["session"], meta["duration_min"], esc(", ".join(meta["instructors"])), esc(meta["module_url"]),
                    esc(f"Day{meta['day']}_S{meta['session']}_{meta['short']}.pptx, {sum(2 if s['layout']=='quiz' else 1 for s in slides)} slides, speaker notes included")))
    parts.append("<h2>Learning objectives</h2><ul>" + "".join(f"<li>{esc(o)}</li>" for o in meta["objectives"]) + "</ul>")
    # run of show from section slides
    secs = [s for s in slides if s["layout"] == "section" and "minute" in s]
    rows = []
    for i, s in enumerate(secs):
        end = s["minute"] + s.get("duration", 0)
        rows.append(f"<tr><td>{s['minute']} to {end}</td><td>{esc(s['title'])}</td><td>{esc(s.get('subtitle',''))}</td></tr>")
    # break: find the gap
    parts.append("<h2>Run of show</h2><table><tr><th style='width:16%'>Minutes</th><th style='width:34%'>Block</th><th>Focus</th></tr>"
                 + "".join(rows) + "</table><p class='notes'>The welcome, objectives and run-of-show slides take the first minutes before Section 1. "
                 "The break is planned at the midpoint (see the run-of-show slide in the deck). Cuts if running behind are listed under Troubleshooting.</p>")
    parts.append("<h2>Materials checklist</h2><ul>" + "".join(f"<li>{esc(m)}</li>" for m in meta["materials"]) + "</ul>")
    parts.append("<h2>Before the session</h2><ul>" + "".join(f"<li>{esc(m)}</li>" for m in meta["prep"]) + "</ul>")
    d = meta["demo"]
    parts.append(f"<h2>{esc(d['title'])}</h2><ol>" + "".join(f"<li>{esc(x)}</li>" for x in d["steps"]) + "</ol>")
    # slide by slide
    out = ["<h2>Slide-by-slide talking points</h2><p class='notes'>Slide numbers match the deck. Quiz questions occupy two slides each (question, then answer).</p>"]
    n = 0
    for s in slides:
        n += 1; lay = s["layout"]
        label = {"section": "Section", "figure": "Figure", "figures": "Figures", "table": "Table", "two_col": "Two columns",
                 "callout": "Callout", "prompt": "Prompt text", "steps": "Steps", "quiz": "Quiz", "references": "References",
                 "articles": "Latest articles", "title": "Title", "bullets": "Bullets", "qr": "Join (QR)"}[lay]
        if lay == "quiz":
            body = f"<div class='slide'><div class='t'>{n}–{n+1}. {esc(s['title'])} <span class='l'>· Quiz</span></div><div class='notes'>Q: {esc(s['question'])}<br>Answer: {'ABCD'[s['answer']]}. {esc(s['why'])}</div></div>"
            n += 1
        else:
            extra = ""
            if lay in ("figure",): extra = f" <span class='l'>· figure: {esc(s['figure'])}</span>"
            if lay == "section" and "minute" in s: extra = f" <span class='l'>· minute {s['minute']}</span>"
            note = esc((s.get("notes") or "").strip())
            body = f"<div class='slide'><div class='t'>{n}. {esc(s['title'])} <span class='l'>· {label}</span>{extra}</div>" + (f"<div class='notes'>{note}</div>" if note else "") + "</div>"
        out.append(body)
    parts.append("".join(out))
    if meta.get("practical_setup"):
        ps = meta["practical_setup"]
        parts.append(f"<h2>{esc(ps['title'])}</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in ps["points"]) + "</ul>"
                     f"<p class='notes'>Full step-by-step instructions, persona text and fallbacks: <b>{esc(ps['sheet'])}</b> (in this package).</p>")
    parts.append("<h2>Troubleshooting and cuts</h2><table><tr><th style='width:38%'>If</th><th>Then</th></tr>"
                 + "".join(f"<tr><td>{esc(t['issue'])}</td><td>{esc(t['fix'])}</td></tr>" for t in meta["troubleshooting"]) + "</table>")
    arts = [s for s in slides if s["layout"] == "articles"]
    if arts:
        parts.append("<h2>Latest articles used on the slides</h2><ul>" + "".join(
            f"<li><b>{esc(a['title'])}</b>. {esc(a['source'])}, {esc(a['date'])}. {esc(a['url'])}<br><span class='notes'>{esc(a['takeaway'])}</span></li>"
            for s in arts for a in s["items"]) + "</ul>")
    parts.append("<h2>References</h2><ol>" + "".join(f"<li>{esc(r)}</li>" for r in meta["references"]) + "</ol>"
                 f"<p class='notes'>{esc(meta['figure_credit'])}. Figures reused from the course tutorial albanna-tutorials.com/llm_agents.html with credit.</p>")
    footer = "IEEE CS Region 8 AI Caravan 2026 · AI Administrator track · Instructor guide prepared by Dr. Abdulkarim Al-Banna · albanna-tutorials.com"
    to_pdf(wrap(meta["title"], f"Instructor guide · Day {meta['day']} · Session {meta['session']}", meta["subtitle"], "".join(parts), footer), out_path)


if __name__ == "__main__":
    kind, src, dst = sys.argv[1:4]
    (build_guide if kind == "guide" else build_md)(src, dst)
