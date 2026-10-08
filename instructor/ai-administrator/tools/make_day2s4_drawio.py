#!/usr/bin/env python3
"""Write the Day 2 Session 4 draw.io file: the leave-request example in two pages, the current state classified
(green rule-based, amber AI-judged, red human-only, removed steps struck through) and the future state with the
Automation lane and the approval gates. Same steps as figures/d2s4_classified.png and d2s4_future.png.
Usage: python3 tools/make_day2s4_drawio.py out/day2/Session4/05_drawio_Files
"""
import sys, pathlib
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_day2_drawio import Doc, LANE_STYLE, EDGE, TITLE, X0, Y0, LABEL_W, BW, BH  # noqa: E402
from make_day2_figures import LANES, STEPS, FLOWS  # noqa: E402
from make_day2s4_figures import CLASSIFY, FUT_LANES, FUT_STEPS, FUT_FLOWS  # noqa: E402

LANE_H, SCALE = 140, 100
COL = {"rule": ("#dcfce7", "#16a34a"), "ai": ("#fef3c7", "#d97706"), "human": ("#fee2e2", "#dc2626"), None: ("#f3f4f6", "#111111")}


def shape(cat, kind, removed=False):
    fc, sc = COL[cat]
    if removed:
        fc, sc = "#ffffff", "#9ca3af"
    base = f"whiteSpace=wrap;html=1;fillColor={fc};strokeColor={sc};strokeWidth={3 if kind == 'gate' else 2};fontSize=13;"
    if kind in ("decision", "gate"):
        return "rhombus;" + base + ("fontStyle=1;" if kind == "gate" else "")
    if kind == "data":
        return "rounded=1;arcSize=8;dashed=1;" + base.replace(f"fillColor={fc}", "fillColor=#ffffff")
    if kind in ("trigger", "end"):
        return "rounded=1;arcSize=45;" + base + ("strokeColor=#F7A11A;" if kind == "trigger" else "")
    return "rounded=1;arcSize=8;" + base + ("dashed=1;fontColor=#9ca3af;" if removed else "")


def lanes(doc, names, width, auto_index=None):
    for i, name in enumerate(names):
        st = LANE_STYLE.format(s=46, f="#fde7c2" if i == auto_index else "#e5e7eb",
                               sf="#fffaf0" if i == auto_index else ("#ffffff" if i % 2 else "#f8fafc"))
        if i == auto_index:
            st = st.replace("strokeColor=#d1d5db", "strokeColor=#F7A11A")
        doc.add(name.replace("\n", " "), st, X0, Y0 + i * LANE_H, width, LANE_H)


def legend(doc, y, extra):
    x = X0
    for cat, lab in (("rule", "Rule-based"), ("ai", "AI-judged"), ("human", "Human-only")):
        doc.add(lab, f"rounded=1;html=1;fillColor={COL[cat][0]};strokeColor={COL[cat][1]};strokeWidth=2;fontSize=12;", x, y, 120, 30)
        x += 135
    doc.add(extra, "text;html=1;fontSize=13;fontColor=#6b7280;align=left;", x + 10, y, 1500, 30)


def classified():
    doc = Doc(); width = 2350; ids = {}
    lanes(doc, [l.replace("Team spreadsheet\n(manager's own)", "Team sheet (manager)") for l in LANES], width)
    for k, (lane, x, txt, touch, kind) in STEPS.items():
        cx = X0 + LABEL_W + (x - 1.9) * SCALE - 20; cy = Y0 + lane * LANE_H + LANE_H / 2
        cat, action, why = CLASSIFY.get(k, (None, None, ""))
        removed = action == "remove"
        k2 = "decision" if kind == "decision" else kind
        h = BH + 24 if kind == "decision" else BH
        label = txt + (f"\ntouch {touch} min" if touch else "")
        ids[k] = doc.add(label, shape(cat, k2, removed), cx - BW / 2, cy - h / 2, BW, h)
        if removed:
            doc.add("REMOVE", "text;html=1;fontSize=11;fontStyle=1;fontColor=#dc2626;align=center;", cx - BW / 2, cy + h / 2, BW, 20)
        elif action == "simplify":
            doc.add("SIMPLIFY: a form", "text;html=1;fontSize=11;fontStyle=1;fontColor=#16a34a;align=center;", cx - BW / 2, cy + h / 2, BW, 20)
    for a, b, lab, kind in FLOWS:
        st = EDGE + "strokeColor=#9ca3af;fontColor=#9ca3af;" + ("dashed=1;" if kind == "data" else "")
        doc.add(lab, st, edge=True, src=ids[a], tgt=ids[b])
    doc.add("Step 1 and 2: classify every step (green rule, amber AI-judged, red human-only), then remove before you automate",
            TITLE, X0, 10, width, 40)
    legend(doc, Y0 + 5 * LANE_H + 15, "Dashed grey = removed, not automated: the e-mail chase, the re-entry, the RUBBER approval, the private sheet.")
    return doc


def future():
    doc = Doc(); width = 2400; ids = {}
    lanes(doc, FUT_LANES, width, auto_index=3)
    for k, (lane, x, txt, touch, kind, cat) in FUT_STEPS.items():
        cx = X0 + LABEL_W + (x - 1.9) * SCALE - 20; cy = Y0 + lane * LANE_H + LANE_H / 2
        h = BH + 30 if kind in ("decision", "gate") else BH
        label = txt + (f"\ntouch {touch} min" if touch else "")
        ids[k] = doc.add(label, shape(cat, kind), cx - BW / 2, cy - h / 2, BW, h)
    for a, b, lab, kind in FUT_FLOWS:
        st = EDGE
        if kind == "data": st += "dashed=1;strokeColor=#6b7280;startArrow=block;startFill=1;"
        if kind == "no": st += "strokeColor=#dc2626;fontColor=#dc2626;"
        if "day" in lab: st += "fontColor=#F7A11A;"
        doc.add(lab, st, edge=True, src=ids[a], tgt=ids[b])
    red = EDGE + "strokeColor=#dc2626;fontColor=#dc2626;"
    doc.add("No, with reason", red, edge=True, src=ids["G1"], tgt=ids["N1"])
    doc.add("No, with reason", red, edge=True, src=ids["G2"], tgt=ids["N1"])
    g = FUT_STEPS["G1"]
    doc.add("reminder at 2 working days, HR at 3 (policy, Section 3)",
            "text;html=1;fontSize=12;fontStyle=2;fontColor=#92400e;align=right;",
            X0 + LABEL_W + (g[1] - 1.9) * SCALE - 20 - BW / 2 - 330, Y0 + LANE_H + LANE_H / 2 - 15, 320, 30)
    doc.add("Leave request at AI Caravan Ltd.: future state   ·   Trigger: leave form submitted   ·   "
            "End: recorded and confirmed, or declined with a reason   ·   routine request: 4 hand-offs, 4 min touch",
            TITLE, X0, 10, width, 40)
    legend(doc, Y0 + 6 * LANE_H + 15, "Bold diamonds are approval gates: as late as possible, just before recording the leave and telling the employee.")
    return doc


def page(doc, name, pid):
    x = doc.xml(name)
    body = x[x.index("<diagram"):x.index("</mxfile>")]
    return body.replace("<diagram ", f'<diagram id="{pid}" ', 1)


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out/day2/Session4/05_drawio_Files"); out.mkdir(parents=True, exist_ok=True)
    f = out / "Day2_S4_Leave_Request_Future_State.drawio"
    f.write_text('<mxfile host="app.diagrams.net">' + page(classified(), "1 Current state, classified", "p1")
                 + page(future(), "2 Future state", "p2") + "</mxfile>\n")
    print("wrote", f)
