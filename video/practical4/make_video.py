#!/usr/bin/env python3
"""Day 2 Session 4 practical video: the live risk challenger (Hermes profile riskreview).
The three answers in replies/ are the challenger's real replies, recorded on the course server with
`hermes -p riskreview -z` on 9 October 2026 (Session 3 was running on @aicaravan_bot, so Telegram itself was not used).
They are drawn here as a Telegram-style chat and composed into captioned 1920x1080 slides in the Session 3 style.
Usage: python3 make_video.py [--voice]  ->  out/Day2_S4_Practical_Risk_Challenger.mp4"""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
REP = os.path.join(HERE, "replies")
W, H, TOP = 1920, 1080, 858
ORANGE, INK, GREY = (244, 160, 27), (17, 17, 17), (90, 90, 90)
F = "/System/Library/Fonts/Supplemental/"
bold = lambda s: ImageFont.truetype(F + "Arial Bold.ttf", s)
reg = lambda s: ImageFont.truetype(F + "Arial.ttf", s)
FOOT = "Real replies from the live risk challenger (Hermes Agent, @aicaravan_bot), 9 Oct 2026 · shown as a Telegram chat"
SESSION = "IEEE CS Region 8 AI Caravan 2026 · AI Administrator · Day 2 · Session 4"

# Telegram-style chat geometry
WALL, OUTB, INB = (198, 222, 177), (239, 253, 222), (255, 255, 255)
CHAT_X, CHAT_W, BUB_MAX, FS, LH, PAD = 360, 1200, 1000, 25, 34, 22
HEAD_H = 76


def replies():
    raw = open(os.path.join(REP, "all.txt")).read().split("=== ")[1:]
    return {int(r.split("\n", 1)[0]): r.split("\n", 1)[1].strip() for r in raw}


def wrap(text, width_px, font):
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append(""); continue
        words, line = para.split(" "), ""
        for w in words:
            t = (line + " " + w).strip()
            if font.getlength(t) <= width_px: line = t
            else: out.append(line); line = w
        out.append(line)
    return out


def chat_tall(msgs):
    """Render all messages on one tall canvas; returns the image and each message's (top, bottom)."""
    f = reg(FS); spans = []; y = 24
    blocks = []
    for side, text in msgs:
        lines = wrap(text, BUB_MAX - 2 * PAD, f)
        h = len(lines) * LH + 2 * PAD + 18
        w = min(BUB_MAX, max(f.getlength(l) for l in lines if l) + 2 * PAD + 70) if any(lines) else 200
        blocks.append((side, lines, w, h, y)); spans.append((y, y + h)); y += h + 18
    im = Image.new("RGB", (CHAT_W, y + 24), WALL); d = ImageDraw.Draw(im)
    for side, lines, w, h, y0 in blocks:
        x0 = CHAT_W - 30 - w if side == "out" else 30
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 18, fill=OUTB if side == "out" else INB)
        for i, l in enumerate(lines):
            d.text((x0 + PAD, y0 + PAD + i * LH), l, font=f, fill=INK)
        stamp = "00:12"
        sw = reg(18).getlength(stamp)
        d.text((x0 + w - PAD - sw, y0 + h - 30), stamp, font=reg(18), fill=(79, 174, 78) if side == "out" else (150, 150, 150))
    return im, spans


def screen(msgs, focus="end", start_at=None):
    """A chat window 'scrolled' so the last message ends at the bottom (focus='end'), or so message start_at
    begins at the top (focus='top')."""
    tall, spans = chat_tall(msgs)
    view = TOP - HEAD_H - 70
    if focus == "end": y0 = max(0, tall.height - view)
    else: y0 = max(0, spans[start_at][0] - 20)
    y0 = min(y0, max(0, tall.height - view))
    if tall.height <= view:                                  # short chat: messages sit at the bottom, as in Telegram
        crop = Image.new("RGB", (CHAT_W, view), WALL); crop.paste(tall, (0, view - tall.height))
    else:
        crop = tall.crop((0, y0, CHAT_W, y0 + view))
    im = Image.new("RGB", (W, TOP), (233, 235, 238)); d = ImageDraw.Draw(im)
    d.rectangle([CHAT_X, 0, CHAT_X + CHAT_W, TOP], fill=WALL)
    im.paste(crop, (CHAT_X, HEAD_H))
    d.rectangle([CHAT_X, 0, CHAT_X + CHAT_W, HEAD_H], fill="white")
    d.ellipse([CHAT_X + 20, 12, CHAT_X + 72, 64], fill=(64, 167, 227))
    d.text((CHAT_X + 34, 22), "AI", font=bold(24), fill="white")
    d.text((CHAT_X + 90, 12), "AI Caravan bot", font=bold(26), fill=INK)
    d.text((CHAT_X + 90, 44), "bot · risk challenger", font=reg(20), fill=(112, 117, 121))
    d.rectangle([CHAT_X, TOP - 70, CHAT_X + CHAT_W, TOP], fill="white")
    d.text((CHAT_X + 30, TOP - 50), "Write a message...", font=reg(24), fill=(160, 160, 160))
    return im


def frame(chat, title, sub):
    im = Image.new("RGB", (W, H), "white"); im.paste(chat, (0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, TOP, W, TOP + 3], fill=(221, 220, 225))
    d.rectangle([60, 897, 70, 1017], fill=ORANGE)
    d.text((100, 912), title, font=bold(38), fill=INK)
    d.text((100, 966), sub, font=reg(31), fill=(40, 40, 40))
    tw = d.textlength(FOOT, font=reg(24)); d.text((W - 18 - tw, 1038), FOOT, font=reg(24), fill=GREY)
    return im


def card(title, lines):
    im = Image.new("RGB", (W, H), (252, 252, 252)); d = ImageDraw.Draw(im)
    d.rectangle([120, 300, 260, 308], fill=ORANGE)
    d.text((120, 335), title, font=bold(64), fill=INK)
    for i, l in enumerate(lines): d.text((120, 440 + i * 58), l, font=reg(38), fill=GREY)
    d.text((120, 990), SESSION, font=reg(28), fill=GREY)
    return im


R = replies()
S1, S2, S3 = (open(os.path.join(REP, f"task{t}_sent.txt")).read().strip() for t in (1, 2, 3))
T1 = [("out", S1)]; T1r = T1 + [("in", R[1])]
T2 = T1r + [("out", S2)]; T2r = T2 + [("in", R[2])]
T3 = T2r + [("out", S3)]; T3r = T3 + [("in", R[3])]

SLIDES = [
    ("card", "A live risk challenger", ["Send a scoring sheet; it argues with your risk scores.",
                                        "Three tasks: the example, your own sheet, and its boundary."]),
    (screen(T1), "Task 1 · The example", "The leave scoring sheet from the worksheet; two rows are wrong on purpose"),
    (screen(T1r, "top", 1), "Task 1 · Challenge each row", "One concrete failure per row; rows 4 and 5 raised to 8"),
    (screen(T1r), "Task 1 · Remove, first build, one question", "Row 5 is a rubber stamp: delete it. First build: the policy checks"),
    (screen(T2), "Task 2 · Your own sheet", "Three candidates from office-supplies ordering, with value and risk"),
    (screen(T2r), "Task 2 · The challenge", "Placing the order commits money: raise to 8, gate just before it"),
    (screen(T3r), "Task 3 · Test its boundary", "\"Is it safe? Build it for me.\" It declines: people decide; building is Day 3"),
    ("card", "A colleague, not an authority", ["Decide whether each failure can really happen in your process,",
                                               "and write your reason in the Notes column either way."]),
]
SAY = [
    "In this practical you send an automation scoring sheet to a live AI risk challenger. It argues with your risk scores, "
    "one row at a time. Three tasks: the example, your own sheet, and a test of its limits.",
    "Open the course bot and paste the leave-request scoring sheet from the worksheet as one message. "
    "Five candidates, each with its value in hours and four risk scores. Two of the rows are wrong on purpose.",
    "For every row it names one concrete failure. Rows one to three hold. Row four, auto-approving one-day leave, "
    "it raises to eight: it bypasses the manager's sign-off in Section 3 of the policy. "
    "And row five, automating HR's approval click, also goes up.",
    "Then the key finding: row five should not be automated at all. It is a rubber stamp, so delete it. "
    "Its first build is the balance and policy checks, and it ends with one question for the process owner.",
    "Task two: your own sheet. Three candidates from your future-state map, each with its value and the four scores. "
    "Here, ordering office supplies.",
    "It spots that placing the order commits money to a supplier and cannot easily be undone, so it raises that row to eight, "
    "and puts the approval gate just before the purchase. It also calls row one a rekey step to remove.",
    "Task three: test its boundary. Ask whether candidate one is safe, and to build it in n8n. "
    "It declines. It challenges scores; people decide, and building is Day 3.",
    "Remember, the challenger is a colleague, not an authority. For each challenge, decide whether that failure "
    "can really happen in your process, and write your reason down.",
]
VOICE, MODEL, GAP = "0f6a8dmX40t9NZBAo3ci", "eleven_multilingual_v2", 0.9
voice = "--voice" in sys.argv
if voice:
    sys.path.insert(0, os.path.dirname(HERE)); import narrate   # video/narrate.py (ElevenLabs key in ~/.albanna-elevenlabs-key)
    AUD = os.path.join(OUT, "audio"); os.makedirs(AUD, exist_ok=True); billed = 0; cues = []; t = 0.0
DUR = [5.5, 7, 9, 9, 6, 9, 7, 6]


def audio_len(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


lst = []
for i, (src, title, sub) in enumerate(SLIDES):
    im = card(title, sub) if isinstance(src, str) else frame(src, title, sub)
    p = os.path.join(OUT, f"slide_{i:02d}.png"); im.save(p); dur = DUR[i]
    if voice:
        mp3, tj, aj = (os.path.join(AUD, f"s{i:02d}{e}") for e in (".mp3", ".txt", ".align.json"))
        if not (os.path.exists(mp3) and os.path.exists(tj) and open(tj).read() == SAY[i]):
            al = narrate.speak(SAY[i], VOICE, mp3, model_id=MODEL)
            json.dump(al, open(aj, "w")); open(tj, "w").write(SAY[i]); billed += len(SAY[i])
        lead = 0.5 if i == 0 else 0.3
        dur = round(lead + audio_len(mp3) + GAP, 2)
        cues += narrate.cues_from_alignment(json.load(open(aj)), offset=t + lead, max_chars=90); t += dur
    lst.append((p, dur))
if "--slides" in sys.argv: sys.exit(0)
with open(os.path.join(OUT, "list.txt"), "w") as f:
    for p, dur in lst: f.write(f"file '{p}'\nduration {dur}\n")
    f.write(f"file '{lst[-1][0]}'\n")
mp4 = os.path.join(OUT, "Day2_S4_Practical_Risk_Challenger.mp4")
cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt")]
if voice:
    starts, t0 = [], 0.0
    for _, dur in lst: starts.append(t0); t0 += dur
    fl = []
    for i in range(len(lst)):
        cmd += ["-i", os.path.join(AUD, f"s{i:02d}.mp3")]; ms = int((starts[i] + (0.5 if i == 0 else 0.3)) * 1000)
        fl.append(f"[{i + 1}:a]adelay={ms}|{ms},apad[a{i}]")
    fl.append("".join(f"[a{i}]" for i in range(len(lst))) + f"amix=inputs={len(lst)}:normalize=0:duration=longest,atrim=0:{t0:.2f}[aout]")
    cmd += ["-filter_complex", ";".join(fl), "-map", "0:v", "-map", "[aout]", "-c:a", "aac", "-b:a", "160k"]
    narrate.write_srt(cues, mp4.replace(".mp4", ".srt")); print(f"narration: {billed} characters billed this run")
cmd += ["-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", mp4]
subprocess.run(cmd, check=True)
print(mp4)
