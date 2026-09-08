"""Place each lesson video directly beneath the section it teaches.

    python3 tools/gen_videos.py            # update every module that has uploads
    python3 tools/gen_videos.py --dry-run
    python3 tools/gen_videos.py --course vibe_coding   # one video per module, under "What you'll learn"

A student reads a section, then finds its video waiting at the bottom of it. Only
lessons actually uploaded appear, so re-run this after each upload batch — every block
is delimited by markers and replaced in place, never duplicated.
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "video"))
import assemble_v2 as A

COURSES = {
    "deep_learning": dict(state="~/.albanna-youtube-uploaded.json", src="deep_learning",
                          heading="Watch this lesson", label="lesson"),
    "vibe_coding": dict(state="~/.albanna-youtube-uploaded.vibe.json", src="vibe-coding",
                        heading="Watch this module", label="module"),
}
COURSE = "deep_learning"
STATE = os.path.expanduser(COURSES[COURSE]["state"])
SRC = os.path.join(ROOT, "src", COURSES[COURSE]["src"])
THUMBS = os.path.join(SRC, "images", "video")
VIDEO_OUT = os.path.join(ROOT, "video", "out", COURSE)
FFMPEG, FFPROBE = A.FFMPEG, A.FFPROBE


def set_course(course):
    global COURSE, STATE, SRC, THUMBS, VIDEO_OUT
    COURSE = course
    c = COURSES[course]
    STATE = os.path.expanduser(c["state"])
    SRC = os.path.join(ROOT, "src", c["src"])
    THUMBS = os.path.join(SRC, "images", "video")
    VIDEO_OUT = os.path.join(ROOT, "video", "out", course)
    if course != "deep_learning":
        A.configure(1, None, None, course)   # script-derived registry (one lesson per module)

# which page section each lesson belongs under. Two lessons may share an anchor —
# they then stack in lesson order beneath it.
PLACEMENT = {
    "01_linear_algebra": {1: "properties", 2: "tensors", 3: "matrices",
                          4: "inverse2x2", 5: "norms", 6: "svd"},
    "02_numerical_computation": {1: "gd", 2: "critical", 3: "hessian", 4: "step",
                                 5: "conditioning", 6: "constrained", 7: "floats",
                                 8: "cancellation", 9: "stable-softmax",
                                 10: "bughunting"},
    "03_nn_foundations": {1: "why", 2: "feedforward", 3: "cost", 4: "lab"},
    "04_activation_functions": {1: "step-linear", 2: "tanh", 3: "leaky", 4: "swish",
                                5: "choose", 6: "summary"},
    "05_xor_mcculloch_pitts": {1: "mp", 2: "mp", 3: "build", 4: "verify"},
    "06_backpropagation": {1: "what", 2: "chain", 3: "forward", 4: "backward",
                           5: "lab"},
    # module 7's lessons each cover a run of numbered sections, so they sit under the
    # last one in their range: lesson 1 is s1-s3, lesson 2 is s4-s5, and so on
    "07_optimization_regularization": {1: "s3", 2: "s5", 3: "s7", 4: "s10", 5: "s12",
                                       6: "s14", 7: "s16"},
    "08_convolutional_networks": {1: "why", 2: "convolution", 3: "dims", 4: "pooling",
                                  5: "pytorch"},
    "09_sequence_models": {1: "need", 2: "what-are-rnns", 3: "example", 4: "problems",
                           5: "bilstm"},
}


def duration(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    try:
        s = int(float(r.stdout.strip()))
    except ValueError:
        return ""
    return f"{s // 60}:{s % 60:02d}"


def thumbnail(mod, cfg):
    src = os.path.join(VIDEO_OUT, mod, "lessons_v2", cfg["slug"], "thumbnail.png")
    if not os.path.exists(src):
        return None
    os.makedirs(THUMBS, exist_ok=True)
    name = f"{mod}_{cfg['slug']}.jpg"
    dst = os.path.join(THUMBS, name)
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src,
                        "-vf", "scale=640:360", "-q:v", "4", dst], check=True)
    return f"images/video/{name}"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def block_for(mod, n, cfg, vid):
    d = os.path.join(VIDEO_OUT, mod, "lessons_v2", cfg["slug"])
    thumb = thumbnail(mod, cfg)
    dur = duration(os.path.join(d, "video.mp4"))
    c = COURSES[COURSE]
    label = esc(f"Play {c['label']} {n}: {cfg['title']}")
    img = f'<img src="{thumb}" alt="" loading="lazy" width="640" height="360">' if thumb else ""
    return (
        f'            <!-- lesson-video:{n}:start -->\n'
        '            <div class="lesson-video">\n'
        f'                <h4><i class="fa-solid fa-circle-play"></i> {c["heading"]} '
        f'&mdash; {esc(cfg["title"])}{f" <span>{dur}</span>" if dur else ""}</h4>\n'
        f'                <button class="video-thumb" data-yt="{vid}" aria-label="{label}">\n'
        f'                    {img}\n'
        '                    <span class="video-play" aria-hidden="true">'
        '<i class="fa-solid fa-play"></i></span>\n'
        '                </button>\n'
        '            </div>\n'
        f'            <!-- lesson-video:{n}:end -->')


def section_span(doc, anchor):
    """Start/end offsets of a top-level section div. Inner divs are indented deeper,
    so the first 8-space close after the opening tag is the section's own."""
    m = re.search(r'<div class="section fade-up" id="%s">' % re.escape(anchor), doc)
    if not m:
        return None
    close = re.search(r"\n        </div>\n", doc[m.end():])
    if not close:
        return None
    return m.end() + close.start()


def apply(page, mod, uploaded):
    doc = open(page, encoding="utf-8").read()
    orig = doc
    placed, missing = [], []

    # drop the old single block and its TOC entry, if this page still has them
    doc = re.sub(r"\s*<!-- lesson-videos:start -->.*?<!-- lesson-videos:end -->", "",
                 doc, flags=re.S)
    doc = re.sub(r'\s*<a class="toc-item" href="#videos">[^<]*</a>', "", doc)
    # and any previously placed per-lesson blocks, so this is idempotent
    doc = re.sub(r"\n *<!-- lesson-video:\d+:start -->.*?<!-- lesson-video:\d+:end -->",
                 "", doc, flags=re.S)

    for n, cfg in sorted(A.MODULES[mod].items()):
        vid = uploaded.get(f"{mod}/{n}")
        if not vid:
            continue
        # screencast courses: one video per module, under "What you'll learn"
        anchor = PLACEMENT.get(mod, {}).get(n) if COURSE == "deep_learning" else "objectives"
        if not anchor:
            missing.append(n); continue
        at = section_span(doc, anchor)
        if at is None:
            missing.append(n); continue
        doc = doc[:at] + "\n" + block_for(mod, n, cfg, vid) + doc[at:]
        placed.append((n, anchor))

    return (doc, placed, missing, doc != orig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--course", default="deep_learning", choices=sorted(COURSES))
    a = ap.parse_args()
    set_course(a.course)

    state = json.load(open(STATE))
    uploaded = {k: v for k, v in state.items() if k != "_playlist"}
    for mod in sorted({k.split("/")[0] for k in uploaded}):
        page = os.path.join(SRC, f"{mod}.html")
        if not os.path.exists(page):
            print(f"  ! no page for {mod}"); continue
        doc, placed, missing, changed = apply(page, mod, uploaded)
        if not a.dry_run and changed:
            open(page, "w", encoding="utf-8").write(doc)
        print(f"  {mod}: {len(placed)} placed"
              + (f", {len(missing)} unplaced {missing}" if missing else "")
              + ("  [dry run]" if a.dry_run else ""))
        for n, anchor in placed:
            print(f"      lesson {n} -> #{anchor}")


if __name__ == "__main__":
    main()
