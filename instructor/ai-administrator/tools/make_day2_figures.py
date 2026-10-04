#!/usr/bin/env python3
"""Draw the course-made figures for Day 2 Session 3 (workflow mapping) into figures/d2s3_*.png.

The running example is the leave-request process at the fictional AI Caravan Ltd. (content/day1_policy_leave.md),
mapped as it really runs: requests by email, a manager's private team spreadsheet, balances chased from HR.
Style follows the decks: white background, black text, IEEE orange (#F7A11A) only for accents.
Usage: python3 tools/make_day2_figures.py
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch, Rectangle

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
ORANGE, BLACK, GREY, LIGHT, RED, GREEN = "#F7A11A", "#111111", "#6b7280", "#f3f4f6", "#dc2626", "#16a34a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})

LANES = ["Employee", "Line manager", "HR coordinator", "HR portal", "Team spreadsheet\n(manager's own)"]
LANE_H, LABEL_W = 1.15, 1.9


def lane_y(i):
    return (len(LANES) - 1 - i) * LANE_H + LANE_H / 2


# steps: id -> (lane, x, text, touch_minutes, kind)
STEPS = {
    "T":  (0, 2.9, "Emails manager:\n'Can I take 3 days?'", 3, "trigger"),
    "S1": (1, 5.25, "Reads email,\nchecks clashes", 6, "step"),
    "L1": (4, 5.25, "Team calendar\nlookup", None, "data"),
    "S2": (1, 7.6, "Emails HR: 'What\nis her balance?'", 2, "step"),
    "S3": (2, 9.95, "Looks up balance,\nreplies by email", 4, "step"),
    "L3": (3, 9.95, "Balance\nrecord", None, "data"),
    "D1": (1, 12.3, "Balance OK\nand no clash?", None, "decision"),
    "N1": (0, 12.3, "Gets 'no' email\n(end)", None, "end"),
    "S4": (1, 14.65, "Replies 'approved'\nby email", 3, "step"),
    "S5": (0, 17.0, "Re-enters request\nin HR portal", 3, "step"),
    "S6": (2, 19.35, "Approves\nin portal", 1, "step"),
    "S7": (3, 21.7, "Sends confirmation\n(end)", None, "end"),
    "S8": (1, 21.7, "Updates team\nspreadsheet", 3, "step"),
}
FLOWS = [
    ("T", "S1", "1 day", "main"), ("S1", "L1", "", "data"), ("S1", "S2", "", "main"),
    ("S2", "S3", "1 day", "main"), ("S3", "L3", "", "data"), ("S3", "D1", "0.5 day", "main"),
    ("D1", "N1", "No", "no"), ("D1", "S4", "Yes", "main"), ("S4", "S5", "0.5 day", "main"),
    ("S5", "S6", "0.75 day", "main"), ("S6", "S7", "", "main"), ("S7", "S8", "0.25 day", "main"),
]
TAGS = {"T": ["WAIT"], "S1": ["READ"], "S2": ["CHASE"], "S3": ["REKEY"], "D1": ["JUDGE"], "S4": ["DRAFT"],
        "S5": ["REKEY"], "S6": ["RUBBER"], "S8": ["REKEY"]}
TAG_COLOUR = {"REKEY": "#2563eb", "WAIT": "#9333ea", "READ": "#0891b2", "DRAFT": "#ca8a04", "CHASE": "#ea580c",
              "RUBBER": "#6b7280", "JUDGE": GREEN}
BOX_W, BOX_H, DEC_W, DEC_H = 1.78, 0.78, 0.82, 0.48


def _edge(k, side):
    lane, x, _, _, kind = STEPS[k]; y = lane_y(lane)
    hw = DEC_W if kind == "decision" else BOX_W / 2
    hh = DEC_H if kind == "decision" else BOX_H / 2
    return {"r": (x + hw, y), "l": (x - hw, y), "t": (x, y + hh), "b": (x, y - hh)}[side]


def _label(ax, x, y, text, colour):
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5, fontweight="bold", color=colour,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=6)


def draw_swimlane(path, tagged=False, title=None):
    width = 22.7
    fig, ax = plt.subplots(figsize=(19.5, 7.6))
    top = len(LANES) * LANE_H
    for i, name in enumerate(LANES):
        y0 = (len(LANES) - 1 - i) * LANE_H
        ax.add_patch(Rectangle((0, y0), width, LANE_H, facecolor="white" if i % 2 else LIGHT, edgecolor="#d1d5db", lw=1))
        ax.add_patch(Rectangle((0, y0), LABEL_W, LANE_H, facecolor="#e5e7eb", edgecolor="#d1d5db", lw=1))
        ax.text(LABEL_W / 2, y0 + LANE_H / 2, name, ha="center", va="center", fontsize=12, fontweight="bold", color=BLACK)
    handoffs = 0
    for a, b, lab, kind in FLOWS:
        la, xa, *_ = STEPS[a]; lb, xb, *_ = STEPS[b]
        ya, yb = lane_y(la), lane_y(lb)
        col = RED if kind == "no" else (GREY if kind == "data" else BLACK)
        ls = "--" if kind == "data" else "-"
        if la != lb and kind != "data": handoffs += 1
        if abs(xa - xb) < 1e-6:                                  # vertical
            p1 = _edge(a, "b" if yb < ya else "t"); p2 = _edge(b, "t" if yb < ya else "b")
            pts = [p1, p2]; lx, ly = xa + (0.42 if kind != "no" else 0.3), (p1[1] + p2[1]) / 2
        elif la == lb:                                           # same lane
            p1, p2 = _edge(a, "r"), _edge(b, "l"); pts = [p1, p2]; lx, ly = (p1[0] + p2[0]) / 2, ya + 0.26
        else:                                                    # elbow through the gap
            p1, p2 = _edge(a, "r"), _edge(b, "l"); xm = (p1[0] + p2[0]) / 2
            pts = [p1, (xm, p1[1]), (xm, p2[1]), p2]; lx, ly = xm, (p1[1] + p2[1]) / 2
        xs, ys = zip(*pts)
        ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color=col, lw=1.6, ls=ls, zorder=2,
                solid_joinstyle="miter")
        ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=16, lw=1.6, color=col, ls=ls, zorder=3))
        if kind == "data":
            ax.add_patch(FancyArrowPatch(pts[1], pts[0], arrowstyle="-|>", mutation_scale=12, lw=1.2, color=col, ls=ls, zorder=3))
        if lab:
            _label(ax, lx, ly, lab, ORANGE if "day" in lab else (RED if kind == "no" else BLACK))
    pos = {}
    for k, (lane, x, txt, touch, kind) in STEPS.items():
        y = lane_y(lane); pos[k] = (x, y)
        if kind == "decision":
            ax.add_patch(Polygon([(x, y + DEC_H), (x + DEC_W, y), (x, y - DEC_H), (x - DEC_W, y)],
                                 closed=True, facecolor="white", edgecolor=BLACK, lw=1.7, zorder=4))
            ax.text(x, y, txt, ha="center", va="center", fontsize=10, zorder=5)
            continue
        rs = 0.36 if kind in ("trigger", "end") else 0.06
        fc = {"trigger": "#fff7e6", "end": "#f3f4f6", "step": "white", "data": "white"}[kind]
        ec = ORANGE if kind == "trigger" else BLACK
        ax.add_patch(FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H, boxstyle=f"round,pad=0.0,rounding_size={rs}",
                                    facecolor=fc, edgecolor=ec, lw=1.7, ls="--" if kind == "data" else "-", zorder=4))
        ax.text(x, y + (0.1 if touch else 0), txt, ha="center", va="center", fontsize=10, zorder=5)
        if touch:
            ax.text(x, y - 0.25, f"touch {touch} min", ha="center", va="center", fontsize=8.8, color=GREY, zorder=5)
    if tagged:
        for k, tags in TAGS.items():
            x, y = pos[k]
            tx, ty = (x + BOX_W / 2, y + BOX_H / 2 + 0.04) if STEPS[k][4] != "decision" else (x + DEC_W, y + DEC_H - 0.05)
            ax.text(tx, ty, " ".join(tags), ha="right", va="bottom", fontsize=9, fontweight="bold", color="white",
                    bbox=dict(boxstyle="round,pad=0.22", fc=TAG_COLOUR[tags[0]], ec="none"), zorder=7)
    ax.set_xlim(-0.05, width + 0.05); ax.set_ylim(-0.7, top + 0.6); ax.axis("off")
    total_touch = sum(v[3] for v in STEPS.values() if v[3])
    ax.text(0.05, top + 0.3, title or "Leave request at AI Caravan Ltd.: current state, as it really runs", fontsize=15,
            fontweight="bold", va="center", color=BLACK)
    ax.text(width, top + 0.3, f"hand-offs: {handoffs}", fontsize=13, fontweight="bold", va="center", ha="right", color=ORANGE)
    ax.text(0.05, -0.4, f"Total touch time {total_touch} min   ·   total elapsed time about 4 working days (six queues, orange)   ·   "
            "dashed = looking something up", fontsize=11, color=GREY, va="center")
    plt.tight_layout(); fig.savefig(path, dpi=160, facecolor="white"); plt.close(fig)
    return handoffs, total_touch


def box(ax, x, y, w, h, txt, fc="white", ec=BLACK, fs=11, ls="-", bold=False, rounding=0.06):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0.02,rounding_size={rounding}",
                                facecolor=fc, edgecolor=ec, lw=1.6, ls=ls))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", color=BLACK)


def arrow(ax, p1, p2, col=BLACK, lab=None, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=15, lw=1.6, color=col, ls=ls))
    if lab:
        ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 0.17, lab, ha="center", fontsize=9.5, color=col, fontweight="bold")


def draw_freeze(path):
    fig, ax = plt.subplots(figsize=(15, 6.2))
    ax.text(0.1, 5.55, "The process people describe", fontsize=15, fontweight="bold")
    xs = [1.3, 4.3, 7.3]
    for x, t in zip(xs, ["Employee submits\nin HR portal", "Manager approves\nin portal", "Confirmation\nsent"]):
        box(ax, x, 4.6, 2.3, 0.9, t)
    for a, b in zip(xs, xs[1:]): arrow(ax, (a + 1.15, 4.6), (b - 1.15, 4.6))
    ax.text(9.2, 4.6, "3 steps · looks ready\nto automate", fontsize=11.5, va="center", color=GREY)
    ax.plot([0.1, 14.8], [3.7, 3.7], color="#d1d5db", lw=1)
    ax.text(0.1, 3.25, "The process that actually runs", fontsize=15, fontweight="bold")
    xs2 = [1.3, 3.7, 6.1, 8.5, 10.9, 13.3]
    t2 = ["Email to manager", "Check private\nteam sheet", "Ask HR for\nbalance by email", "Approve\nby email",
          "Re-type into\nHR portal", "Update the\nteam sheet"]
    hidden = [True, True, True, True, False, True]
    for x, t, h in zip(xs2, t2, hidden):
        box(ax, x, 2.2, 2.0, 0.9, t, fc="#fff7e6" if h else "white", ec=ORANGE if h else BLACK)
    for a, b in zip(xs2, xs2[1:]): arrow(ax, (a + 1.0, 2.2), (b - 1.0, 2.2))
    ax.add_patch(FancyBboxPatch((0.25, 0.55), 0.5, 0.35, boxstyle="round,pad=0.02,rounding_size=0.05", fc="#fff7e6", ec=ORANGE, lw=1.6))
    ax.text(0.95, 0.72, "steps nobody mentioned: workarounds an automation of the top line would break or freeze",
            fontsize=11.5, va="center")
    ax.set_xlim(0, 15); ax.set_ylim(0.2, 6); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_sipoc(path):
    fig, ax = plt.subplots(figsize=(15, 6.4))
    cols = [("S", "Suppliers", ["Employees", "Line managers", "HR coordinator", "HR portal"]),
            ("I", "Inputs", ["Leave request", "Leave balance", "Team calendar", "Leave policy HR-POL-02"]),
            ("P", "Process", ["Request", "Check balance and clashes", "Manager decides", "Record in HR portal", "Confirm"]),
            ("O", "Outputs", ["Approved or declined\nrequest", "Updated balance", "Updated calendar"]),
            ("C", "Customers", ["Employee", "Team", "Payroll"])]
    w = 2.75
    for i, (L, name, items) in enumerate(cols):
        x = 0.35 + i * (w + 0.18)
        ax.add_patch(Rectangle((x, 3.75), w, 0.95, fc=ORANGE if L == "P" else "#111111", ec="none"))
        ax.text(x + 0.25, 4.22, L, color="white", fontsize=26, fontweight="bold", va="center")
        ax.text(x + 0.85, 4.22, name, color="white", fontsize=14, fontweight="bold", va="center")
        ax.add_patch(Rectangle((x, 0.6), w, 3.15, fc="white", ec="#d1d5db", lw=1.2))
        for j, it in enumerate(items):
            ax.text(x + 0.18, 3.38 - j * 0.6, ("%d. " % (j + 1) if L == "P" else "• ") + it, fontsize=11.5, va="top")
    ax.text(0.35, 5.6, "Trigger:", fontsize=13, fontweight="bold"); ax.text(1.55, 5.6, "an employee asks for annual leave (today: an email; officially: the HR portal)", fontsize=13)
    ax.text(0.35, 5.1, "End state:", fontsize=13, fontweight="bold"); ax.text(1.75, 5.1, "the employee has a recorded decision and the balance and calendar are updated", fontsize=13)
    ax.set_xlim(0, 15); ax.set_ylim(0.4, 6); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_notation(path):
    fig, ax = plt.subplots(figsize=(15, 4.6))
    cx = [1.8, 5.6, 9.4, 13.0]
    box(ax, cx[0], 2.6, 2.4, 0.95, "Email arrives", fc="#fff7e6", ec=ORANGE, rounding=0.4)
    box(ax, cx[1], 2.6, 2.4, 0.95, "Check leave\nbalance")
    d = 0.75
    ax.add_patch(Polygon([(cx[2], 2.6 + d), (cx[2] + 1.35, 2.6), (cx[2], 2.6 - d), (cx[2] - 1.35, 2.6)], closed=True, fc="white", ec=BLACK, lw=1.6))
    ax.text(cx[2], 2.6, "Balance\nenough?", ha="center", va="center", fontsize=11)
    arrow(ax, (cx[3] - 1.4, 2.6), (cx[3] + 1.4, 2.6)); ax.text(cx[3], 2.85, "2 days", ha="center", fontsize=13, fontweight="bold", color=ORANGE)
    labs = [("Trigger", "What starts the process.\nRounded, far left."), ("Step", "One action: a verb\nand an object."),
            ("Decision", "A yes/no question with\nlabelled exits."), ("Wait", "Write on the arrow how long\nthe work sits before the next step.")]
    for x, (h, t) in zip(cx, labs):
        ax.text(x, 1.25, h, ha="center", fontsize=14, fontweight="bold"); ax.text(x, 0.55, t, ha="center", va="center", fontsize=11, color=GREY)
    ax.set_xlim(0, 15); ax.set_ylim(0, 3.6); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_touch_wait(path):
    fig, ax = plt.subplots(figsize=(15, 4.4))
    steps = [("Email", 3, 1.0), ("Read, check", 6, 0), ("Ask HR", 2, 1.0), ("HR lookup", 4, 0.5), ("Decide, reply", 3, 0.5),
             ("Re-enter", 3, 0.75), ("Approve", 1, 0.25), ("Update sheet", 3, 0)]
    # working day = 8 h = 480 min; draw on a day axis
    t = 0.0
    for name, touch, wait in steps:
        tw = touch / 480
        ax.add_patch(Rectangle((t, 1.0), max(tw, 0.012), 0.8, fc=BLACK, ec="none"))
        t += tw
        if wait:
            ax.add_patch(Rectangle((t, 1.0), wait, 0.8, fc="#fde7c2", ec=ORANGE, lw=1))
            ax.text(t + wait / 2, 1.4, f"waiting {wait:g} day" if wait >= 0.5 else f"{wait:g} d", ha="center", va="center", fontsize=10.5, color="#92400e")
            t += wait
    for d in range(0, 5):
        ax.plot([d, d], [0.9, 1.9], color="#9ca3af", lw=1, zorder=3); ax.text(d, 0.72, f"day {d}", ha="center", fontsize=10, color=GREY)
    ax.text(0, 2.35, "25 minutes of work (black slivers) spread over about 4 working days (orange queues)", fontsize=14, fontweight="bold")
    ax.text(0, 0.25, "Waits are fixed by notifications, routing and reminders. Touch time on reading and writing is fixed by AI steps.",
            fontsize=12, color=GREY)
    ax.set_xlim(-0.1, 4.2); ax.set_ylim(0, 2.7); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_tags(path):
    fig, ax = plt.subplots(figsize=(15, 5.4))
    rows = [("REKEY", "Same data typed into a second system", "Automation copies it"),
            ("WAIT", "Work sits for hours or days for no reason but attention", "Notifications, reminders, routing"),
            ("READ", "A person reads free text to decide or extract something", "AI classification or extraction step"),
            ("DRAFT", "A person writes near-identical text repeatedly", "AI drafting step, human sends"),
            ("CHASE", "Someone reminds someone else to act", "Scheduled reminders with escalation"),
            ("RUBBER", "An approval that is always given without reading", "Remove it, or make it an exception check"),
            ("JUDGE", "A real decision needing judgement or accountability", "Keep human; give them a better summary")]
    ax.text(0.2, 7.55, "Tag", fontsize=12.5, fontweight="bold", color=GREY); ax.text(2.0, 7.55, "Meaning", fontsize=12.5, fontweight="bold", color=GREY)
    ax.text(9.4, 7.55, "Typical fix", fontsize=12.5, fontweight="bold", color=GREY)
    for i, (t, m, f) in enumerate(rows):
        y = 6.8 - i * 1.0
        ax.text(0.2, y, t, fontsize=12, fontweight="bold", color="white", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc=TAG_COLOUR[t], ec="none"))
        ax.text(2.0, y, m, fontsize=13, va="center"); ax.text(9.4, y, f, fontsize=13, va="center",
                                                               fontweight="bold" if t == "JUDGE" else "normal", color=GREEN if t == "JUDGE" else BLACK)
        ax.plot([0.1, 14.9], [y - 0.5, y - 0.5], color="#e5e7eb", lw=1)
    ax.set_xlim(0, 15); ax.set_ylim(0, 8); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    h, tt = draw_swimlane(FIG / "d2s3_swimlane.png")
    draw_swimlane(FIG / "d2s3_tagged.png", tagged=True, title="The same map, tagged with pain points")
    draw_freeze(FIG / "d2s3_freeze.png")
    draw_sipoc(FIG / "d2s3_sipoc.png")
    draw_notation(FIG / "d2s3_notation.png")
    draw_touch_wait(FIG / "d2s3_touch_wait.png")
    draw_tags(FIG / "d2s3_tags.png")
    print(f"figures written; hand-offs {h}, touch {tt} min")
