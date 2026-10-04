#!/usr/bin/env python3
"""Day 2 Session 3 practical video: the live map reviewer on @aicaravan_bot.
Composes Telegram Web captures (frames/) into captioned 1920x1080 slides in the Day 1 practical style, then ffmpeg.
Usage: python3 make_video.py  ->  out/Day2_S3_Practical_Map_Reviewer.mp4"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
W, H, TOP = 1920, 1080, 858          # screenshot area 0..858, caption bar below (as Day 1)
ORANGE, INK, GREY = (244, 160, 27), (17, 17, 17), (90, 90, 90)
F = "/System/Library/Fonts/Supplemental/"
bold = lambda s: ImageFont.truetype(F + "Arial Bold.ttf", s)
reg = lambda s: ImageFont.truetype(F + "Arial.ttf", s)
FOOT = "Live agent: Hermes Agent on Telegram · @aicaravan_bot"
CHATLIST_W = 372                     # px of the Telegram Web chat list in the 1551-wide captures (blurred)

SLIDES = [
    ("card", "A live map reviewer", ["Send a process as a list of steps; get a review in a fixed shape.",
                                     "Three tasks: the example, your own task, and its boundary."], 5.5),
    ("01_typed.jpg", "Task 1 · The example", "Paste the whole leave-request step list as one message", 6),
    ("02_sent.jpg", "Task 1 · The example", "Nine steps, with touch time and waits in brackets", 4),
    ("03_review_top.jpg", "Task 1 · The review", "Missing steps checked against the leave policy (Sections 3 and 7)", 9),
    ("04_review_end.jpg", "Task 1 · The review", "Riskiest hand-offs, suggested tags, and one question for a colleague", 9),
    ("05_task2_typed.jpg", "Task 2 · Your own task", "Five to eight steps: roles, not names; waits in brackets", 6),
    ("06_task2_review.jpg", "Task 2 · The review", "A missing hand-off to finance, and two approvals with no \"no\" path", 9),
    ("07_task3_typed.jpg", "Task 3 · Test its boundary", "\"Now automate this for me.\"", 4.5),
    ("08_task3_reply.jpg", "Task 3 · The boundary holds", "Automation is Session 4; today it only reviews the current state", 7),
    ("card", "A colleague, not an authority", ["Check every finding against the policy and the people who do the work.",
                                               "What did it miss? (Hint: the three-day escalation in Section 3.)"], 6),
]


def card(title, lines):
    im = Image.new("RGB", (W, H), (252, 252, 252)); d = ImageDraw.Draw(im)
    d.rectangle([120, 300, 260, 308], fill=ORANGE)
    d.text((120, 335), title, font=bold(64), fill=INK)
    for i, l in enumerate(lines): d.text((120, 440 + i * 58), l, font=reg(38), fill=GREY)
    d.text((120, 990), "IEEE CS Region 8 AI Caravan 2026 · AI Administrator · Day 2 · Session 3", font=reg(28), fill=GREY)
    return im


def shot(path, title, sub):
    src = Image.open(os.path.join(HERE, "frames", path)).convert("RGB")
    src.paste(src.crop((0, 0, CHATLIST_W, src.height)).filter(ImageFilter.GaussianBlur(14)), (0, 0))
    s = TOP / src.height; fg = src.resize((round(src.width * s), TOP), Image.LANCZOS)
    im = Image.new("RGB", (W, H), "white")
    im.paste(src.resize((W, TOP)).filter(ImageFilter.GaussianBlur(30)), (0, 0))   # soft fill for the side margins
    im.paste(fg, ((W - fg.width) // 2, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, TOP, W, TOP + 3], fill=(221, 220, 225))
    d.rectangle([60, 897, 70, 1017], fill=ORANGE)
    d.text((100, 912), title, font=bold(38), fill=INK)
    d.text((100, 966), sub, font=reg(31), fill=(40, 40, 40))
    tw = d.textlength(FOOT, font=reg(25)); d.text((W - 18 - tw, 1036), FOOT, font=reg(25), fill=GREY)
    return im


lst = []
for i, (src, title, sub, dur) in enumerate(SLIDES):
    im = card(title, sub) if src == "card" else shot(src, title, sub)
    p = os.path.join(OUT, f"slide_{i:02d}.png"); im.save(p); lst.append((p, dur))
with open(os.path.join(OUT, "list.txt"), "w") as f:
    for p, dur in lst: f.write(f"file '{p}'\nduration {dur}\n")
    f.write(f"file '{lst[-1][0]}'\n")
mp4 = os.path.join(OUT, "Day2_S3_Practical_Map_Reviewer.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt"),
                "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", mp4], check=True)
print(mp4)
