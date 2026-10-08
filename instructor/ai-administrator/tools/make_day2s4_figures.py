#!/usr/bin/env python3
"""Draw the course-made figures for Day 2 Session 4 (workflow mapping II, the future state) into figures/d2s4_*.png.

Same running example as Session 3: annual-leave requests at the fictional AI Caravan Ltd. (content/day1_policy_leave.md).
The current-state steps come from make_day2_figures.py; this script classifies them, redraws the process as a future
state with an Automation lane and an approval gate, and plots the scored candidates (CANDIDATES, also used by
make_day2s4_sheets.py so the slides, the spreadsheet and the draw.io file agree).
Usage: python3 tools/make_day2s4_figures.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch, Rectangle
from make_day2_figures import (STEPS as CUR_STEPS, FLOWS as CUR_FLOWS, LANES as CUR_LANES, ORANGE, BLACK, GREY, LIGHT,
                               RED, GREEN, box, arrow, draw_swimlane)  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
AMBER, GREEN_BG, AMBER_BG, RED_BG = "#d97706", "#dcfce7", "#fef3c7", "#fee2e2"
CAT = {"rule": (GREEN, GREEN_BG, "Rule-based"), "ai": (AMBER, AMBER_BG, "AI-judged"), "human": (RED, RED_BG, "Human-only")}

# Classification of the Session 3 current-state steps (ids from make_day2_figures.STEPS).
# value: (category, action, one-line reason)
CLASSIFY = {
    "T":  ("rule", "simplify", "Becomes a portal form: dates and type in fields, not an email"),
    "S1": ("ai", "keep", "Reading a free-text note needs judgement; checking the calendar does not"),
    "S2": ("rule", "remove", "CHASE: disappears once the balance is read from the HR portal"),
    "S3": ("rule", "automate", "Balance lookup: a rule you can write in one sentence"),
    "D1": ("human", "keep", "JUDGE: the manager is accountable for the team"),
    "S4": ("rule", "automate", "Fixed template once the decision is made"),
    "S5": ("rule", "remove", "REKEY: the form already holds the request"),
    "S6": ("rule", "remove", "RUBBER: always approved, never read; deleted, not automated"),
    "S7": ("rule", "automate", "Confirmation: a fixed template"),
    "S8": ("rule", "remove", "REKEY into a private sheet the policy forbids (Section 7)"),
}

# Scored candidates for the leave process (the M4-scoring example).
# name, steps, minutes saved per run, runs per month, reversibility, money, people, legal/data, decision
CANDIDATES = [
    ("Record approved leave in portal and team calendar", "S5, S8, S7", 6, 60, 1, 0, 0, 1,
     "Build first, fully automatic"),
    ("Look up balance and run the policy checks", "S2, S3", 6, 60, 0, 0, 1, 1,
     "Build first, fully automatic"),
    ("Prepare the manager's decision card", "S1", 4, 60, 0, 0, 1, 1,
     "Build first; flags go to HR, not to the AI"),
    ("Remind the manager, escalate to HR at 3 days", "S2 (CHASE)", 2, 20, 0, 0, 1, 0,
     "Batch later: add it to candidate 1, it is cheap"),
    ("Auto-approve 1-day requests with no clash", "D1", 2, 20, 2, 1, 2, 1,
     "Later: notify the manager, with undo"),
    ("Auto-decline requests that fail notice", "D1", 2, 10, 3, 1, 3, 2,
     "Leave alone: give the manager the check instead"),
]
VALUE_HIGH, RISK_HIGH = 4.0, 8          # thresholds used by the matrix and the spreadsheet


def value(c):
    return round(c[2] * c[3] / 60, 1)


def risk(c):
    return sum(c[4:8])


def quadrant(v, r):
    if v >= VALUE_HIGH:
        return "Build first" if r < RISK_HIGH else "Build with a gate"
    return "Batch later" if r < RISK_HIGH else "Leave alone"


# ------------------------------------------------------------------------------------------------- classification map
def draw_classified(path):
    """The Session 3 map with every step coloured by category and the removed steps struck through."""
    lanes = CUR_LANES
    LANE_H, LABEL_W, width = 1.15, 1.9, 22.7
    BOX_W, BOX_H, DEC_W, DEC_H = 1.78, 0.78, 0.82, 0.48
    fig, ax = plt.subplots(figsize=(19.5, 7.6))
    top = len(lanes) * LANE_H
    ly = lambda i: (len(lanes) - 1 - i) * LANE_H + LANE_H / 2  # noqa: E731
    for i, name in enumerate(lanes):
        y0 = (len(lanes) - 1 - i) * LANE_H
        ax.add_patch(Rectangle((0, y0), width, LANE_H, facecolor="white" if i % 2 else LIGHT, edgecolor="#d1d5db", lw=1))
        ax.add_patch(Rectangle((0, y0), LABEL_W, LANE_H, facecolor="#e5e7eb", edgecolor="#d1d5db", lw=1))
        ax.text(LABEL_W / 2, y0 + LANE_H / 2, name, ha="center", va="center", fontsize=12, fontweight="bold")
    for a, b, lab, kind in CUR_FLOWS:
        la, xa, *_ = CUR_STEPS[a]; lb, xb, *_ = CUR_STEPS[b]
        ya, yb = ly(la), ly(lb)
        col = "#c4c9d1"
        if abs(xa - xb) < 1e-6:
            pts = [(xa, ya), (xb, yb)]
        elif la == lb:
            pts = [(xa, ya), (xb, yb)]
        else:
            xm = (xa + xb) / 2; pts = [(xa, ya), (xm, ya), (xm, yb), (xb, yb)]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=col, lw=1.4, ls="--" if kind == "data" else "-", zorder=1)
    for k, (lane, x, txt, touch, kind) in CUR_STEPS.items():
        y = ly(lane)
        if kind == "data":
            ax.add_patch(FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor="white", edgecolor=GREY, lw=1.2, ls="--", zorder=4))
            ax.text(x, y, txt, ha="center", va="center", fontsize=10, color=GREY, zorder=5)
            continue
        if k not in CLASSIFY:
            ax.add_patch(FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H, boxstyle="round,pad=0,rounding_size=0.36",
                                        facecolor="#f3f4f6", edgecolor=GREY, lw=1.2, zorder=4))
            ax.text(x, y, txt, ha="center", va="center", fontsize=10, color=GREY, zorder=5)
            continue
        cat, action, _ = CLASSIFY[k]
        ec, fc, _ = CAT[cat]
        if action == "remove":
            fc, ec = "white", "#9ca3af"
        if kind == "decision":
            ax.add_patch(Polygon([(x, y + DEC_H), (x + DEC_W, y), (x, y - DEC_H), (x - DEC_W, y)], closed=True,
                                 facecolor=fc, edgecolor=ec, lw=2.2, zorder=4))
        else:
            ax.add_patch(FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor=fc, edgecolor=ec, lw=2.2, ls="--" if action == "remove" else "-", zorder=4))
        ax.text(x, y, txt, ha="center", va="center", fontsize=10, zorder=5, color="#9ca3af" if action == "remove" else BLACK)
        if action == "remove":
            ax.plot([x - BOX_W / 2 + 0.1, x + BOX_W / 2 - 0.1], [y - BOX_H / 2 + 0.1, y + BOX_H / 2 - 0.1], color=RED, lw=2.4, zorder=6)
            ax.text(x, y - BOX_H / 2 - 0.12, "REMOVE", ha="center", va="top", fontsize=9, fontweight="bold", color=RED, zorder=6)
        elif action == "simplify":
            ax.text(x, y - BOX_H / 2 - 0.12, "SIMPLIFY: a form", ha="center", va="top", fontsize=9, fontweight="bold", color=GREEN, zorder=6)
    ax.set_xlim(-0.05, width + 0.05); ax.set_ylim(-0.75, top + 0.6); ax.axis("off")
    ax.text(0.05, top + 0.3, "Step 1 and 2: classify every step, then remove before you automate", fontsize=15, fontweight="bold", va="center")
    lx = 0.05
    for cat in ("rule", "ai", "human"):
        ec, fc, lab = CAT[cat]
        ax.add_patch(FancyBboxPatch((lx, -0.58), 0.45, 0.3, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, lw=2))
        ax.text(lx + 0.6, -0.43, lab, fontsize=11.5, va="center"); lx += 2.6
    ax.plot([lx, lx + 0.45], [-0.58, -0.28], color=RED, lw=2.4)
    ax.text(lx + 0.6, -0.43, "removed: deleted, not automated (four of nine steps)", fontsize=11.5, va="center")
    plt.tight_layout(); fig.savefig(path, dpi=160, facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------------------------------------- future-state map
FUT_LANES = ["Employee", "Line manager", "Department head", "Automation\n(owner: HR coordinator)", "HR coordinator", "HR portal\nand team calendar"]
# id -> (lane, x, text, touch, kind, category)
FUT_STEPS = {
    "F0": (0, 2.9, "Submits leave form\nin the HR portal", 2, "trigger", "human"),
    "F1": (3, 5.25, "Reads balance;\nchecks notice,\nprobation, clashes", None, "step", "rule"),
    "L1": (5, 5.25, "Balance and\ncalendar", None, "data", None),
    "F2": (3, 7.6, "Reads the note;\nflags anything\nnot routine", None, "step", "ai"),
    "D0": (3, 9.95, "All checks\npass?", None, "decision", "rule"),
    "X1": (4, 9.95, "Resolves the\nexception", 5, "step", "human"),
    "F3": (3, 12.3, "Prepares the\ndecision card", None, "step", "rule"),
    "G1": (1, 14.65, "Approve?\n(gate)", 2, "gate", "human"),
    "Q1": (3, 17.0, "Last two weeks\nof a quarter?", None, "decision", "rule"),
    "G2": (2, 17.0, "Approve?\n(gate)", 2, "gate", "human"),
    "F4": (3, 19.35, "Records leave,\nupdates calendar,\nsends confirmation", None, "step", "rule"),
    "E1": (5, 21.7, "Recorded and\nconfirmed (end)", None, "end", None),
    "N1": (0, 19.35, "Gets the decision\nwith the reason", None, "end", None),
}
FUT_FLOWS = [
    ("F0", "F1", "", "main"), ("F1", "L1", "", "data"), ("F1", "F2", "", "main"), ("F2", "D0", "", "main"),
    ("D0", "X1", "No", "no"), ("D0", "F3", "Yes", "main"), ("F3", "G1", "same day", "main"),
    ("G1", "Q1", "Yes", "main"), ("Q1", "G2", "Yes", "main"), ("Q1", "F4", "No", "main"), ("G2", "F4", "Yes", "corner"),
    ("F4", "E1", "", "main"),
]
FUT_TOUCH_ROUTINE = 4         # employee form 2 + manager decision 2 (no exception, not quarter end)
FUT_HANDOFFS_ROUTINE = 4      # employee->automation, automation->manager, manager->automation, automation->portal


def draw_future(path):
    lanes = FUT_LANES
    LANE_H, LABEL_W, width = 1.08, 2.25, 23.0
    BOX_W, BOX_H, DEC_W, DEC_H = 1.86, 0.8, 0.86, 0.46
    fig, ax = plt.subplots(figsize=(19.5, 8.6))
    top = len(lanes) * LANE_H
    ly = lambda i: (len(lanes) - 1 - i) * LANE_H + LANE_H / 2  # noqa: E731
    for i, name in enumerate(lanes):
        y0 = (len(lanes) - 1 - i) * LANE_H
        auto = name.startswith("Automation")
        ax.add_patch(Rectangle((0, y0), width, LANE_H, facecolor="#fffaf0" if auto else ("white" if i % 2 else LIGHT),
                               edgecolor=ORANGE if auto else "#d1d5db", lw=2 if auto else 1, zorder=0))
        ax.add_patch(Rectangle((0, y0), LABEL_W, LANE_H, facecolor="#fde7c2" if auto else "#e5e7eb", edgecolor="#d1d5db", lw=1))
        ax.text(LABEL_W / 2, y0 + LANE_H / 2, name, ha="center", va="center", fontsize=11.5, fontweight="bold")

    def edge(k, side):
        lane, x, _, _, kind, _ = FUT_STEPS[k]; y = ly(lane)
        hw = DEC_W if kind in ("decision", "gate") else BOX_W / 2
        hh = DEC_H if kind in ("decision", "gate") else BOX_H / 2
        return {"r": (x + hw, y), "l": (x - hw, y), "t": (x, y + hh), "b": (x, y - hh)}[side]

    for a, b, lab, kind in FUT_FLOWS:
        la, xa, *_ = FUT_STEPS[a]; lb, xb, *_ = FUT_STEPS[b]
        ya, yb = ly(la), ly(lb)
        col = RED if kind == "no" else (GREY if kind == "data" else BLACK)
        ls = "--" if kind == "data" else "-"
        if kind == "corner":
            p1, p2 = edge(a, "r"), edge(b, "t" if yb < ya else "b")
            pts = [p1, (xb, ya), p2]; lx, lyy = (p1[0] + xb) / 2, ya + 0.22
        elif abs(xa - xb) < 1e-6:
            p1 = edge(a, "b" if yb < ya else "t"); p2 = edge(b, "t" if yb < ya else "b")
            pts = [p1, p2]; lx, lyy = xa + 0.35, (p1[1] + p2[1]) / 2
        elif la == lb:
            p1, p2 = edge(a, "r"), edge(b, "l"); pts = [p1, p2]; lx, lyy = (p1[0] + p2[0]) / 2, ya + 0.24
        else:
            p1, p2 = edge(a, "r"), edge(b, "l"); xm = (p1[0] + p2[0]) / 2
            pts = [p1, (xm, p1[1]), (xm, p2[1]), p2]; lx, lyy = xm, (p1[1] + p2[1]) / 2
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=col, lw=1.6, ls=ls, zorder=2)
        ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=16, lw=1.6, color=col, ls=ls, zorder=3))
        if kind == "data":
            ax.add_patch(FancyArrowPatch(pts[1], pts[0], arrowstyle="-|>", mutation_scale=12, lw=1.2, color=col, ls=ls, zorder=3))
        if lab:
            ax.text(lx, lyy, lab, ha="center", va="center", fontsize=9.5, fontweight="bold",
                    color=ORANGE if "day" in lab else (RED if kind == "no" else BLACK),
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=6)
    # decline path from gate 1 to the employee
    g = FUT_STEPS["G1"]; n = FUT_STEPS["N1"]
    p1 = (g[1], ly(g[0]) + DEC_H); p2 = (n[1] - BOX_W / 2, ly(n[0]))
    ax.plot([p1[0], p1[0], p2[0]], [p1[1], p2[1], p2[1]], color=RED, lw=1.6, zorder=2)
    ax.add_patch(FancyArrowPatch((p1[0] + 0.5, p2[1]), p2, arrowstyle="-|>", mutation_scale=16, lw=1.6, color=RED, zorder=3))
    ax.text(p1[0] + 0.3, (p1[1] + p2[1]) / 2, "No, with reason", fontsize=9.5, fontweight="bold", color=RED, va="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=6)
    g2 = FUT_STEPS["G2"]                                         # department head's "no" joins the same decline path
    ax.plot([g2[1], g2[1]], [ly(g2[0]) + DEC_H, p2[1]], color=RED, lw=1.6, zorder=2)
    ax.text(g2[1] + 0.12, ly(1), "No", fontsize=9.5, fontweight="bold", color=RED, va="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=6)
    # escalation timer on the manager gate
    ax.text(g[1] - 1.75, ly(g[0]), "reminder at 2 working days,\nHR at 3 (policy, Section 3)", fontsize=8.8,
            color="#92400e", ha="right", va="center", style="italic", zorder=6)
    for k, (lane, x, txt, touch, kind, cat) in FUT_STEPS.items():
        y = ly(lane)
        ec, fc = (CAT[cat][0], CAT[cat][1]) if cat else (BLACK, "#f3f4f6")
        if kind in ("decision", "gate"):
            ax.add_patch(Polygon([(x, y + DEC_H), (x + DEC_W, y), (x, y - DEC_H), (x - DEC_W, y)], closed=True,
                                 facecolor=fc, edgecolor=ec, lw=2.4 if kind == "gate" else 1.8, zorder=4))
            ax.text(x, y, txt, ha="center", va="center", fontsize=9.6, zorder=5, fontweight="bold" if kind == "gate" else "normal")
            continue
        if kind == "data":
            ax.add_patch(FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor="white", edgecolor=GREY, lw=1.3, ls="--", zorder=4))
            ax.text(x, y, txt, ha="center", va="center", fontsize=10, color=GREY, zorder=5)
            continue
        rs = 0.36 if kind in ("trigger", "end") else 0.06
        if kind == "trigger":
            ec = ORANGE
        ax.add_patch(FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H, boxstyle=f"round,pad=0,rounding_size={rs}",
                                    facecolor=fc, edgecolor=ec, lw=1.9, zorder=4))
        ax.text(x, y + (0.1 if touch else 0), txt, ha="center", va="center", fontsize=9.6, zorder=5)
        if touch:
            ax.text(x, y - 0.27, f"touch {touch} min", ha="center", va="center", fontsize=8.6, color=GREY, zorder=5)
    ax.set_xlim(-0.05, width + 0.05); ax.set_ylim(-0.75, top + 0.6); ax.axis("off")
    ax.text(0.05, top + 0.3, "Leave request at AI Caravan Ltd.: future state", fontsize=15, fontweight="bold", va="center")
    ax.text(width, top + 0.3, f"routine request: {FUT_HANDOFFS_ROUTINE} hand-offs, {FUT_TOUCH_ROUTINE} min touch, decided the same day",
            fontsize=12.5, fontweight="bold", va="center", ha="right", color=ORANGE)
    lx = 0.05
    for cat in ("rule", "ai", "human"):
        ec, fc, lab = CAT[cat]
        ax.add_patch(FancyBboxPatch((lx, -0.6), 0.45, 0.3, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, lw=2))
        ax.text(lx + 0.6, -0.45, lab, fontsize=11, va="center"); lx += 2.4
    ax.text(lx, -0.45, "Gates (bold diamonds) sit just before the irreversible step: recording the leave and telling the employee.",
            fontsize=11, va="center", color=GREY)
    plt.tight_layout(); fig.savefig(path, dpi=160, facecolor="white"); plt.close(fig)


# ------------------------------------------------------------------------------------------------- other figures
def draw_before_after(path):
    fig, ax = plt.subplots(figsize=(15, 5.6))
    rows = [("Steps people do", "9", "3 (form, decision, exceptions)"),
            ("Touch time, routine request", "25 min", f"{FUT_TOUCH_ROUTINE} min"),
            ("Elapsed time, routine request", "about 4 working days", "same day, if the manager answers"),
            ("Hand-offs", "8", f"{FUT_HANDOFFS_ROUTINE}"),
            ("Private team spreadsheet", "yes (policy breach)", "no: the portal calendar is the record"),
            ("Department-head approval at quarter end", "missing", "a second gate, only when it applies"),
            ("What stays human", "everything", "the decision, the exceptions")]
    ax.text(0.2, 6.55, "", fontsize=13)
    ax.text(6.1, 6.55, "Current state (Session 3)", fontsize=14, fontweight="bold", ha="center", color=GREY)
    ax.text(11.4, 6.55, "Future state (Session 4)", fontsize=14, fontweight="bold", ha="center", color=ORANGE)
    for i, (a, b, c) in enumerate(rows):
        y = 5.75 - i * 0.82
        ax.text(0.2, y, a, fontsize=13.5, va="center", fontweight="bold")
        ax.text(6.1, y, b, fontsize=13.5, va="center", ha="center", color=GREY)
        ax.text(11.4, y, c, fontsize=13.5, va="center", ha="center")
        ax.plot([0.1, 14.9], [y - 0.41, y - 0.41], color="#e5e7eb", lw=1)
    ax.set_xlim(0, 15); ax.set_ylim(0, 7); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_three_way(path):
    fig, ax = plt.subplots(figsize=(15, 6.2))
    cols = [("rule", "Could I write the rule?\nYes, in one sentence,\nwith no 'usually'.",
             ["Read the balance from the portal", "Notice: 2 days for 1-2 days of leave", "Reminder after 2 working days",
              "Record leave, send the template"], "Plain automation nodes\n(Day 3, Module 5)"),
            ("ai", "A trained person decides\nin seconds by reading,\nbut I cannot list the exceptions.",
             ["Read the employee's note", "Flag 'not routine' (sick child,\nhospital, a wedding abroad)",
              "Summarise the request for\nthe manager"], "An AI step inside the\nautomation (Day 3, Module 6)"),
            ("human", "Someone must be accountable,\nor it is hard to undo.",
             ["Approve or decline the leave", "Department head at quarter end", "Resolve an exception",
              "Anything about pay, job or health"], "An approval gate or a task\n(Day 5, Module 10)")]
    w = 4.75
    for i, (cat, test, ex, built) in enumerate(cols):
        ec, fc, lab = CAT[cat]
        x = 0.2 + i * (w + 0.2)
        ax.add_patch(Rectangle((x, 5.0), w, 0.85, fc=ec, ec="none"))
        ax.text(x + w / 2, 5.42, lab, color="white", fontsize=17, fontweight="bold", ha="center", va="center")
        ax.add_patch(Rectangle((x, 0.3), w, 4.7, fc=fc, ec=ec, lw=1.5))
        ax.text(x + 0.2, 4.8, test, fontsize=12, va="top", fontweight="bold")
        for j, e in enumerate(ex):
            ax.text(x + 0.2, 3.35 - j * 0.58 - (0.25 if j and "\n" in ex[j - 1] else 0), "• " + e, fontsize=11.5, va="top")
        ax.text(x + 0.2, 0.55, built, fontsize=11, va="bottom", color=GREY, style="italic")
    ax.set_xlim(0, 15); ax.set_ylim(0.2, 6); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_risk_questions(path):
    fig, ax = plt.subplots(figsize=(15, 6.0))
    rows = [("Reversibility", "If it goes wrong, how hard is it to undo?", "Internal draft, easily corrected",
             "Sent to a person, paid out, deleted"),
            ("Money", "What is the largest amount involved?", "None", "Above the manager's own limit"),
            ("People", "Does it affect someone's job, pay, access or wellbeing?", "No", "Directly and significantly"),
            ("Legal and data", "Contracts, regulation, personal data?", "None", "Personal data or a legal duty")]
    ax.text(0.2, 6.55, "Question", fontsize=12.5, fontweight="bold", color=GREY)
    ax.text(7.55, 6.55, "Scores 0", fontsize=12.5, fontweight="bold", color=GREEN)
    ax.text(11.3, 6.55, "Scores 3", fontsize=12.5, fontweight="bold", color=RED)
    for i, (h, q, z, t) in enumerate(rows):
        y = 5.8 - i * 1.0
        ax.text(0.2, y + 0.16, h, fontsize=14, fontweight="bold", va="center")
        ax.text(0.2, y - 0.22, q, fontsize=11.5, va="center", color=GREY)
        ax.text(7.55, y, z, fontsize=12.5, va="center"); ax.text(11.3, y, t, fontsize=12.5, va="center")
        ax.plot([0.1, 14.9], [y - 0.5, y - 0.5], color="#e5e7eb", lw=1)
    bands = [(0, 4, GREEN, GREEN_BG, "0 to 3: fully automatic"), (4, 8, AMBER, AMBER_BG, "4 to 7: notify a person, with undo"),
             (8, 13, RED, RED_BG, "8 to 12: approval gate every time")]
    x0, sc = 0.2, 14.6 / 13
    for a, b, ec, fc, lab in bands:
        ax.add_patch(Rectangle((x0 + a * sc, 0.55), (b - a) * sc, 0.75, fc=fc, ec=ec, lw=1.5))
        ax.text(x0 + (a + b) / 2 * sc, 0.92, lab, ha="center", va="center", fontsize=12, fontweight="bold", color=ec)
    for v in range(0, 13):
        ax.text(x0 + (v + 0.5) * sc, 0.33, str(v), ha="center", fontsize=9.5, color=GREY)
    ax.text(0.2, 1.62, "Total risk 0 to 12 (add the four scores):", fontsize=12.5, fontweight="bold")
    ax.set_xlim(0, 15); ax.set_ylim(0.1, 6.9); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_matrix(path):
    fig, ax = plt.subplots(figsize=(13.5, 7.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8)
    regions = [(0, RISK_HIGH, VALUE_HIGH, 8, GREEN_BG, "Build first"), (RISK_HIGH, 12, VALUE_HIGH, 8, AMBER_BG, "Build with a gate"),
               (0, RISK_HIGH, 0, VALUE_HIGH, "#f3f4f6", "Batch later"), (RISK_HIGH, 12, 0, VALUE_HIGH, RED_BG, "Leave alone")]
    for x0, x1, y0, y1, fc, lab in regions:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec="white", lw=3, zorder=0))
        ax.text(x0 + 0.15, y1 - 0.2, lab, fontsize=14, fontweight="bold", va="top", color=BLACK, zorder=1)
    seen = {}
    for n, c in enumerate(CANDIDATES, 1):
        v, r = value(c), risk(c)
        k = seen[(v, r)] = seen.get((v, r), -1) + 1           # nudge candidates with identical scores apart
        r = r + 0.45 * k
        ax.scatter([r], [v], s=420, color=BLACK, zorder=3)
        ax.text(r, v, str(n), color="white", ha="center", va="center", fontsize=12, fontweight="bold", zorder=4)
    leg = [f"{n}. {c[0]}  ({value(c):g} h, risk {risk(c)})" for n, c in enumerate(CANDIDATES, 1)]
    ax.text(12.3, 7.6, "Leave-process candidates", fontsize=13, fontweight="bold", va="top")
    for i, t in enumerate(leg):
        ax.text(12.3, 6.9 - i * 0.62, t, fontsize=11, va="top")
    ax.set_xlabel("Risk (0 to 12)  →", fontsize=13); ax.set_ylabel("Value: hours saved per month  →", fontsize=13)
    ax.set_xticks(range(0, 13)); ax.set_yticks(range(0, 9))
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    plt.subplots_adjust(left=0.07, right=0.56, top=0.95, bottom=0.1)
    fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


def draw_gate(path):
    fig, ax = plt.subplots(figsize=(15, 5.8))
    xs = [1.4, 4.0, 6.6]
    for x, t in zip(xs, ["Read balance,\nrun the checks", "Flag anything\nnot routine", "Prepare the\ndecision card"]):
        box(ax, x, 4.4, 2.2, 0.95, t, fc=GREEN_BG if "Flag" not in t else AMBER_BG, ec=GREEN if "Flag" not in t else AMBER)
    for a, b in zip(xs, xs[1:]): arrow(ax, (a + 1.1, 4.4), (b - 1.1, 4.4))
    gx, d = 9.3, 0.75
    ax.add_patch(Polygon([(gx, 4.4 + d), (gx + 1.25, 4.4), (gx, 4.4 - d), (gx - 1.25, 4.4)], closed=True, fc=RED_BG, ec=RED, lw=2.6))
    ax.text(gx, 4.4, "Manager:\napprove?", ha="center", va="center", fontsize=12, fontweight="bold")
    arrow(ax, (xs[-1] + 1.1, 4.4), (gx - 1.25, 4.4))
    box(ax, 12.9, 4.4, 2.6, 0.95, "Record leave,\ntell the employee", fc="#111111", ec="#111111")
    ax.texts[-1].set_color("white")
    arrow(ax, (gx + 1.25, 4.4), (12.9 - 1.3, 4.4), lab="Yes")
    ax.text(12.9, 5.15, "irreversible: the employee books flights", ha="center", fontsize=10.5, color=RED, fontweight="bold")
    ax.text(4.0, 5.3, "the automation does all the preparation", ha="center", fontsize=11, color=GREY)
    # evidence card
    ax.add_patch(FancyBboxPatch((5.6, 0.3), 7.4, 2.75, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=BLACK, lw=1.6))
    ax.text(5.85, 2.82, "What the manager sees at the gate (the evidence)", fontsize=12.5, fontweight="bold", va="top")
    lines = ["Request: 3 days, 12 to 14 November · employee in Finance", "Balance: 9 days left · notice 12 working days (needs 10): OK",
             "Clashes: 1 of 6 people in the team already off on 13 November", "AI note check: routine ('family visit') · not quarter end"]
    for i, t in enumerate(lines):
        ax.text(5.85, 2.3 - i * 0.42, t, fontsize=11, va="top")
    for i, (t, c) in enumerate([("Approve", GREEN), ("Edit", AMBER), ("Decline with reason", RED)]):
        ax.text(5.85 + i * 1.75 + (0 if i < 2 else 0), 0.45, t, fontsize=11, fontweight="bold", color="white", va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", fc=c, ec="none"))
    ax.plot([gx, gx], [4.4 - d, 3.1], color=GREY, lw=1.2, ls=":")
    rules = ["1. As late as possible, before the irreversible step", "2. One gate per irreversible action",
             "3. The gate carries the evidence"]
    for i, t in enumerate(rules):
        ax.text(0.2, 2.75 - i * 0.62, t, fontsize=12.5, va="top", fontweight="bold" if i == 0 else "normal")
    ax.set_xlim(0, 15); ax.set_ylim(0.1, 5.7); ax.axis("off")
    plt.tight_layout(); fig.savefig(path, dpi=170, facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    draw_classified(FIG / "d2s4_classified.png")
    draw_future(FIG / "d2s4_future.png")
    draw_before_after(FIG / "d2s4_before_after.png")
    draw_three_way(FIG / "d2s4_three_way.png")
    draw_risk_questions(FIG / "d2s4_risk.png")
    draw_matrix(FIG / "d2s4_matrix.png")
    draw_gate(FIG / "d2s4_gate.png")
    for n, c in enumerate(CANDIDATES, 1):
        print(n, c[0], f"value {value(c):g} h", f"risk {risk(c)}", quadrant(value(c), risk(c)), "|", c[8])
