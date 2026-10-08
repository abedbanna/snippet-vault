"""draw.io screencast driver for the AI Administrator Day 2 videos.

A video is a list of beats: {"say": narration, "do": async fn(d), "chip": optional step label}.
  1. narrate(): one ElevenLabs request per beat in Dr. Albanna's cloned voice (cached: never billed twice).
  2. record(): Playwright opens the real draw.io editor (app.diagrams.net) at 1920x1080 and performs every action with
     real mouse and keyboard input, paced so each beat lasts at least as long as its narration. A cursor overlay and a
     step chip are drawn in the page because headless recordings show no pointer.
  3. assemble(): trims the page-load seconds, lays each beat's audio at its recorded start, burns captions from the
     narration timings, writes out/<name>/<name>.mp4.
The draw.io editor object is reached only to READ positions (where to aim the mouse); every visible change is input.
"""
import asyncio, json, math, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import narrate  # noqa: E402  (video/narrate.py)

VOICE = "0f6a8dmX40t9NZBAo3ci"          # Kareem, Dr. Albanna's cloned voice
MODEL = "eleven_multilingual_v2"
OUT = os.path.join(HERE, "out")
GAP = 0.6                              # seconds of breathing room after each beat
URL = "https://app.diagrams.net/?splash=0&lang=en"
SESSION = "3"                          # shown on the title banner; a video script may set V.SESSION

HOOK = """
(() => {
  const t = setInterval(() => {
    if (window.EditorUi && !EditorUi.__hooked) { EditorUi.__hooked = true;
      const orig = EditorUi.prototype.init;
      EditorUi.prototype.init = function() { window.__ui = this; return orig.apply(this, arguments); };
      clearInterval(t); } }, 1);
  const add = () => {
    if (document.getElementById('__cur')) return;
    const c = document.createElement('div'); c.id = '__cur';
    c.innerHTML = '<svg width="26" height="30" viewBox="0 0 26 30"><path d="M2 2 L2 24 L8 18 L12 28 L16 26 L12 17 L21 17 Z" fill="#111" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></svg>';
    c.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;transform:translate(-2px,-2px);transition:none';
    document.body.appendChild(c);
    const chip = document.createElement('div'); chip.id = '__chip';
    chip.style.cssText = 'position:fixed;left:50%;transform:translateX(-50%);top:112px;z-index:2147483646;pointer-events:none;background:#111;color:#fff;font:600 22px Inter,Helvetica,Arial,sans-serif;padding:10px 18px;border-radius:10px;border-left:6px solid #F7A11A;box-shadow:0 6px 20px rgba(0,0,0,.25);display:none;max-width:640px';
    document.body.appendChild(chip);
    const ban = document.createElement('div'); ban.id = '__ban';
    ban.style.cssText = 'position:fixed;inset:0;z-index:2147483645;pointer-events:none;display:none;align-items:center;justify-content:center;background:rgba(255,255,255,.94)';
    document.body.appendChild(ban);
    const mv = e => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; };
    ['mousemove','pointermove','mousedown','mouseup'].forEach(k => document.addEventListener(k, mv, true));
    document.addEventListener('mousedown', e => { const r = document.createElement('div');
      r.style.cssText = `position:fixed;left:${e.clientX-18}px;top:${e.clientY-18}px;width:36px;height:36px;border-radius:50%;border:3px solid #F7A11A;z-index:2147483646;pointer-events:none;opacity:.9;transition:transform .45s ease-out,opacity .45s ease-out`;
      document.body.appendChild(r); requestAnimationFrame(() => { r.style.transform = 'scale(1.8)'; r.style.opacity = '0'; });
      setTimeout(() => r.remove(), 500); }, true);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', add); else add();
})();
"""

JS_RECT = """(id) => { const g = window.__ui.editor.graph; const c = g.model.getCell(id); const s = g.view.getState(c);
  const cn = g.container; const r = cn.getBoundingClientRect();
  return {x: r.left + s.x - cn.scrollLeft, y: r.top + s.y - cn.scrollTop, w: s.width, h: s.height}; }"""
JS_SEL = "() => { const c = window.__ui.editor.graph.getSelectionCell(); return c ? c.id : null }"
JS_TOSCREEN = """([x, y]) => { const g = window.__ui.editor.graph; const v = g.view; const cn = g.container; const r = cn.getBoundingClientRect();
  return [r.left + (x + v.translate.x) * v.scale - cn.scrollLeft, r.top + (y + v.translate.y) * v.scale - cn.scrollTop]; }"""
JS_FIND = """(label) => { const g = window.__ui.editor.graph; const m = g.model; const out = [];
  const walk = c => { const n = m.getChildCount(c); for (let i = 0; i < n; i++) { const k = m.getChildAt(c, i);
    if (String(k.value || '').replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim().startsWith(label)) out.push(k.id); walk(k); } };
  walk(m.getRoot()); return out[0] || null; }"""

# Format panel style presets (vertex selected, Style tab): row 1 white, grey, blue, green; row 2 orange, yellow, red, purple
PRESET = {"white": (1735, 171), "grey": (1777, 171), "blue": (1819, 171), "green": (1861, 171),
          "orange": (1735, 201), "yellow": (1777, 201), "red": (1819, 201), "purple": (1861, 201)}
GENERAL = {"rect": (36, 290), "rounded": (74, 290), "text": (112, 290), "diamond": (150, 329)}


class D:
    """Helpers that act on the page with real input. `fast` shortens movement and typing for time-lapse beats."""

    def __init__(self, page):
        self.p, self.fast, self.ids, self.cx, self.cy = page, False, {}, 960, 540

    async def pause(self, s):
        await self.p.wait_for_timeout(int(1000 * s * (0.35 if self.fast else 1)))

    async def move(self, x, y):
        dist = math.hypot(x - self.cx, y - self.cy)
        steps = max(4, int(dist / (90 if self.fast else 28)))
        await self.p.mouse.move(x, y, steps=steps); self.cx, self.cy = x, y

    async def click(self, x, y, pause=0.25):
        await self.move(x, y); await self.p.mouse.click(x, y); await self.pause(pause)

    async def dblclick(self, x, y):
        await self.move(x, y); await self.p.mouse.dblclick(x, y); await self.pause(0.35)

    async def drag(self, x1, y1, x2, y2):
        await self.move(x1, y1); await self.p.mouse.down(); await self.pause(0.15)
        await self.move(x2, y2); await self.pause(0.15); await self.p.mouse.up(); await self.pause(0.35)

    async def type(self, text, delay=55):
        await self.p.keyboard.type(text, delay=int(delay * (0.35 if self.fast else 1)))

    async def key(self, k):
        await self.p.keyboard.press(k); await self.pause(0.3)

    async def rect(self, name):
        return await self.p.evaluate(JS_RECT, self.ids.get(name, name))

    async def center(self, name):
        r = await self.rect(name); return r["x"] + r["w"] / 2, r["y"] + r["h"] / 2

    async def screen(self, x, y):
        return await self.p.evaluate(JS_TOSCREEN, [x, y])

    async def find(self, label):
        return await self.p.evaluate(JS_FIND, label)

    async def blank(self):
        """Finish editing and clear the selection with the keyboard, so the pointer stays where the work is
        (Escape applies the label in draw.io; Cmd+Shift+A is Select None)."""
        await self.p.keyboard.press("Escape"); await self.pause(0.15)
        await self.p.keyboard.press("Meta+Shift+a"); await self.pause(0.15)

    # ---- shapes --------------------------------------------------------------------------------------------
    async def drop(self, name, src, x, y):
        """Drag a sidebar shape (screen xy) so its top-left lands at diagram coordinates (x, y). Returns the cell id."""
        sx, sy = await self.screen(x, y)
        await self.drag(src[0], src[1], sx, sy)
        cid = await self.p.evaluate(JS_SEL); self.ids[name] = cid; return cid

    async def label(self, text):
        """Type into the selected (just dropped) shape, then click away."""
        await self.type(text); await self.pause(0.2); await self.blank()

    async def rename(self, name_or_xy, text):
        if isinstance(name_or_xy, tuple): x, y = name_or_xy
        else: x, y = await self.center(name_or_xy)
        await self.dblclick(x, y); await self.p.keyboard.press("Meta+a"); await self.type(text); await self.pause(0.2); await self.blank()

    async def select(self, name):
        x, y = await self.center(name); await self.click(x, y, 0.35)

    async def sizers(self):
        return await self.p.evaluate("""() => { const g = window.__ui.editor.graph; const c = g.getSelectionCell();
            const h = c && g.selectionCellsHandler.getHandler(c);
            return h && h.sizers ? h.sizers.map(s => { const b = s.node.getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; }) : []; }""")

    async def resize(self, name, dx, dy, handle=7):
        """Select `name` and drag one of its resize handles (7 = bottom-right, 4 = right-middle) by (dx, dy) pixels."""
        await self.select(name); hs = await self.sizers(); x, y = hs[handle]
        await self.drag(x, y, x + dx, y + dy)

    async def preset(self, colour):
        await self.click(*PRESET[colour], 0.35)

    async def connect(self, a, b, label=None, side="r", into=None):
        """Hover a, drag its blue hover arrow onto b, optionally type a label on the new edge."""
        ra = await self.rect(a); x, y = ra["x"] + ra["w"] / 2, ra["y"] + ra["h"] / 2
        arrows = []
        for attempt in range(3):   # the hover arrows need ~0.7 s to appear, even in fast beats
            await self.move(x + 6 * attempt, y); await self.p.wait_for_timeout(800 + 400 * attempt)
            arrows = await self.p.evaluate("""([cx, cy, w, h]) => [...document.querySelectorAll('img')].map(i => {
            const r = i.getBoundingClientRect(); return {x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width}; })
            .filter(a => a.w > 8 && a.w < 40 && Math.abs(a.x - cx) < w / 2 + 45 && Math.abs(a.y - cy) < h / 2 + 45)""",
                                         [x, y, ra["w"], ra["h"]])
            if arrows: break
        pick = {"r": max(arrows, key=lambda a: a["x"]), "l": min(arrows, key=lambda a: a["x"]),
                "d": max(arrows, key=lambda a: a["y"]), "u": min(arrows, key=lambda a: a["y"])}[side] if arrows else None
        if not pick: raise RuntimeError(f"no hover arrows on {a}")
        # drop on the midpoint of the side facing the source: draw.io pins the arrow wherever it is released inside a
        # shape (even the centre), so release it on the border instead
        rb = await self.rect(b); dy = (rb["y"] + rb["h"] / 2) - y; dx = (rb["x"] + rb["w"] / 2) - x
        # (5 px inside it: exactly on the border the pointer is over the lane behind, and the arrow is left dangling)
        if abs(dy) > 30: bx, by = rb["x"] + rb["w"] / 2, (rb["y"] + 5 if dy > 0 else rb["y"] + rb["h"] - 5)
        else: bx, by = (rb["x"] + 5 if dx > 0 else rb["x"] + rb["w"] - 5), rb["y"] + rb["h"] / 2
        if into == "l": bx, by = rb["x"] + 5, rb["y"] + rb["h"] / 2          # force the side of the target it enters
        elif into == "t": bx, by = rb["x"] + rb["w"] / 2, rb["y"] + 5
        await self.move(pick["x"], pick["y"]); await self.p.mouse.down(); await self.pause(0.15)
        await self.move(bx, by); await self.p.wait_for_timeout(450); await self.p.mouse.up()   # let draw.io highlight the target shape; await self.pause(0.4)
        eid = await self.p.evaluate(JS_SEL)
        if label:
            await self.type(label); await self.pause(0.2)
        await self.blank(); return eid

    async def menu(self, *path):
        tops = {"File": (81, 48), "Edit": (120, 48), "View": (165, 48), "Arrange": (222, 48), "Extras": (284, 48)}
        await self.click(*tops[path[0]], 0.4)
        for item in path[1:]:
            loc = self.p.locator(".mxPopupMenu .mxPopupMenuItem", has_text=item).first
            box = await loc.bounding_box()
            await self.move(box["x"] + 40, box["y"] + box["height"] / 2); await self.pause(0.5)
            if item == path[-1]: await self.p.mouse.click(box["x"] + 40, box["y"] + box["height"] / 2); await self.pause(0.4)

    async def chip(self, text):
        await self.p.evaluate("(t) => { const c = document.getElementById('__chip'); if (!t) { c.style.display='none'; return; } c.textContent = t; c.style.display = 'block'; }", text or "")

    async def banner(self, title, sub=""):
        html = ("" if not title else
                f"<div style='text-align:center;font-family:Inter,Helvetica,Arial,sans-serif'>"
                f"<div style='font:700 26px Inter,Helvetica,Arial;color:#F7A11A;letter-spacing:.06em'>AI ADMINISTRATOR · DAY 2 · SESSION {SESSION}</div>"
                f"<div style='font:800 64px Inter,Helvetica,Arial;color:#111;margin:18px 0'>{title}</div>"
                f"<div style='font:500 30px Inter,Helvetica,Arial;color:#4b5563'>{sub}</div>"
                f"<div style='font:500 22px Inter,Helvetica,Arial;color:#6b7280;margin-top:40px'>Dr. Abdulkarim Albanna · IEEE CS AI Caravan 2026</div></div>")
        await self.p.evaluate("(h) => { const b = document.getElementById('__ban'); b.innerHTML = h; b.style.display = h ? 'flex' : 'none'; }", html)


# ---------------------------------------------------------------------------------------------------------------
def outdir(name):
    d = os.path.join(OUT, name); os.makedirs(os.path.join(d, "audio"), exist_ok=True); return d


SYNC = [(255, 0, 0), (0, 200, 0), (0, 0, 255)]   # beat i shows SYNC[i % 3]; the end shows yellow
MARK = """(rgb) => { let m = document.getElementById('__sync'); if (!m) { m = document.createElement('div'); m.id = '__sync';
    m.style.cssText = 'position:fixed;right:0;bottom:0;width:8px;height:8px;z-index:2147483647;pointer-events:none';
    document.body.appendChild(m); } m.style.background = 'rgb(' + rgb.join(',') + ')'; }"""


FOOTER = "0xf1f3f4"   # paints over the sync marker in the output


def sync_times(webm, n):
    """Read the corner marker from the recording: the true start of each beat and the end, in webm seconds.
    (Headless screencasts fall behind wall-clock time under load, so wall-clock beat times drift.)"""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", webm, "-vf", "fps=30,crop=4:4:1914:1074,scale=1:1",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    want = SYNC + [(255, 255, 0)]
    cls = []
    for k in range(0, len(raw), 3):
        px = raw[k:k + 3]; dist = [sum((a - b) ** 2 for a, b in zip(px, c)) for c in want]
        cls.append(dist.index(min(dist)) if min(dist) < 9000 else -1)
    out, f = [], 0
    for i in range(n + 1):
        target = 3 if i == n else i % 3
        while f < len(cls) and cls[f] != target: f += 1
        if f == len(cls): raise RuntimeError(f"sync marker {i} not found")
        out.append(f / 30)
    return out[:n], out[n]


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def narrate_all(name, beats):
    d = outdir(name); billed = 0
    for i, b in enumerate(beats, 1):
        mp3 = os.path.join(d, "audio", f"beat_{i:02d}.mp3"); aj = mp3.replace(".mp3", ".align.json")
        tj = mp3.replace(".mp3", ".txt")
        if os.path.exists(mp3) and os.path.exists(aj) and os.path.exists(tj) and open(tj).read() == b["say"]:
            continue
        al = narrate.speak(b["say"], VOICE, mp3, model_id=MODEL)
        json.dump(al, open(aj, "w")); open(tj, "w").write(b["say"]); billed += len(b["say"])
    print(f"narration ready ({billed} characters billed this run)")


async def record(name, beats, prepare=None):
    from playwright.async_api import async_playwright
    d = outdir(name); vd = os.path.join(d, "raw"); shutil.rmtree(vd, ignore_errors=True)
    durs = [duration(os.path.join(d, "audio", f"beat_{i:02d}.mp3")) for i in range(1, len(beats) + 1)]
    async with async_playwright() as p:
        br = await p.chromium.launch(headless=True)
        ctx = await br.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=vd,
                                   record_video_size={"width": 1920, "height": 1080})
        await ctx.add_init_script(HOOK)
        page = await ctx.new_page(); t_video0 = time.monotonic()
        await page.goto(URL, wait_until="networkidle", timeout=120000)
        await page.wait_for_function("() => window.__ui && window.__ui.editor && window.__ui.editor.graph", timeout=60000)
        await page.wait_for_timeout(1500)
        dd = D(page)
        if prepare: await prepare(dd)
        starts = []
        for i, b in enumerate(beats):
            await page.evaluate(MARK, list(SYNC[i % 3]))
            t0 = time.monotonic(); starts.append(t0 - t_video0)
            dd.fast = bool(b.get("fast"))
            if "chip" in b: await dd.chip(b["chip"])
            print(f"beat {i + 1}/{len(beats)} ({durs[i]:.1f}s) {b['say'][:60]}...", flush=True)
            await b["do"](dd)
            left = durs[i] + GAP - (time.monotonic() - t0)
            if left > 0: await page.wait_for_timeout(int(left * 1000))
        end = time.monotonic() - t_video0 + 1.0
        await page.evaluate(MARK, [255, 255, 0])
        await page.wait_for_timeout(1500)
        await ctx.close(); await br.close()
    webm = [f for f in os.listdir(vd) if f.endswith(".webm")][0]
    json.dump({"webm": os.path.join(vd, webm), "starts": starts, "end": end, "durs": durs}, open(os.path.join(d, "timeline.json"), "w"), indent=1)
    print("recorded", os.path.join(vd, webm))


def assemble(name, beats):
    d = outdir(name); tl = json.load(open(os.path.join(d, "timeline.json")))
    starts, end = sync_times(tl["webm"], len(beats))
    tl["starts"] = starts; off = starts[0]; total = end + 1.0 - off
    print("sync starts", [round(x - off, 1) for x in starts], "end", round(end - off, 1))
    cues = []
    for i, b in enumerate(beats, 1):
        al = json.load(open(os.path.join(d, "audio", f"beat_{i:02d}.align.json")))
        cues += narrate.cues_from_alignment(al, offset=tl["starts"][i - 1] - off, max_chars=90)
    srt = narrate.write_srt(cues, os.path.join(d, f"{name}.srt"))
    inputs = ["-ss", f"{off:.3f}", "-t", f"{total:.3f}", "-i", tl["webm"]]   # the 8 px marker sits in the bottom-right corner, under the footer
    fl, mix = [], []
    for i in range(1, len(beats) + 1):
        inputs += ["-i", os.path.join(d, "audio", f"beat_{i:02d}.mp3")]
        ms = int((tl["starts"][i - 1] - off) * 1000)
        fl.append(f"[{i}:a]adelay={ms}|{ms},apad[a{i}]"); mix.append(f"[a{i}]")
    style = ("FontName=Helvetica,FontSize=11,PrimaryColour=&H00FFFFFF,BackColour=&HB0000000,BorderStyle=4,Outline=0,"
             "Shadow=0,MarginV=10,Alignment=2")
    fl.append(f"{''.join(mix)}amix=inputs={len(beats)}:normalize=0:duration=longest,atrim=0:{total:.3f}[aout]")
    fl.append(f"[0:v]fps=30,drawbox=x=1908:y=1068:w=12:h=12:color={FOOTER}:t=fill,subtitles={srt}:force_style='{style}'[vout]")
    out = os.path.join(d, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fl), "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], check=True)
    print(out, f"{duration(out):.1f}s")
    return out


async def dry(name, beats, prepare=None, shots=True):
    """Run every action with no audio and no recording; save a screenshot after each beat."""
    from playwright.async_api import async_playwright
    d = outdir(name); sd = os.path.join(d, "dry"); shutil.rmtree(sd, ignore_errors=True); os.makedirs(sd)
    async with async_playwright() as p:
        br = await p.chromium.launch(headless=True)
        ctx = await br.new_context(viewport={"width": 1920, "height": 1080}); await ctx.add_init_script(HOOK)
        page = await ctx.new_page(); await page.goto(URL, wait_until="networkidle", timeout=120000)
        await page.wait_for_function("() => window.__ui && window.__ui.editor && window.__ui.editor.graph", timeout=60000)
        await page.wait_for_timeout(1500); dd = D(page)
        if prepare: await prepare(dd)
        for i, b in enumerate(beats, 1):
            dd.fast = bool(b.get("fast"))
            if "chip" in b: await dd.chip(b["chip"])
            t = time.monotonic(); await b["do"](dd)
            print(f"beat {i}: {time.monotonic() - t:.1f}s actions", flush=True)
            if shots: await page.screenshot(path=os.path.join(sd, f"beat_{i:02d}.png"))
        edges = await page.evaluate("""() => { const g = window.__ui.editor.graph; return Object.values(g.model.cells).filter(c => c.edge)
            .map(c => [c.id, c.source && c.source.id, c.target && c.target.id, c.style]); }""")
        json.dump({"ids": dd.ids, "edges": edges}, open(os.path.join(sd, "model.json"), "w"), indent=1)
        await br.close()


def main(name, beats, prepare=None):
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step == "dry": asyncio.run(dry(name, beats, prepare)); return
    if step in ("narrate", "all"): narrate_all(name, beats)
    if step in ("record", "all"): asyncio.run(record(name, beats, prepare))
    if step in ("assemble", "all"): assemble(name, beats)
