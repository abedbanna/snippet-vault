#!/usr/bin/env python3
"""Write the Day 2 Session 3 draw.io files: an empty swimlane template and the finished leave-request example.

The example uses the same steps, lanes, waits and tags as figures/d2s3_swimlane.png (tools/make_day2_figures.py).
Usage: python3 tools/make_day2_drawio.py out/day2/Session3/05_drawio_Files
"""
import sys, pathlib
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_day2_figures import LANES, STEPS, FLOWS, TAGS, TAG_COLOUR  # noqa: E402

LANE_H, LABEL_W, X0, Y0, SCALE, BW, BH = 140, 150, 20, 60, 100, 170, 76


class Doc:
    def __init__(self):
        self.cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']; self.n = 1

    def add(self, value, style, x=None, y=None, w=None, h=None, edge=False, src=None, tgt=None):
        self.n += 1; cid = f"c{self.n}"
        v = escape(value, {'"': "&quot;", "\n": "&#10;"})
        if edge:
            self.cells.append(f'<mxCell id="{cid}" value="{v}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">'
                              f'<mxGeometry relative="1" as="geometry"/></mxCell>')
        else:
            self.cells.append(f'<mxCell id="{cid}" value="{v}" style="{style}" vertex="1" parent="1">'
                              f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
        return cid

    def xml(self, name):
        return ('<mxfile host="app.diagrams.net"><diagram name="' + escape(name) + '"><mxGraphModel dx="1400" dy="800" grid="1" '
                'gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2400" '
                'pageHeight="900" math="0" shadow="0"><root>' + "".join(self.cells) + '</root></mxGraphModel></diagram></mxfile>\n')


LANE_STYLE = "swimlane;horizontal=0;startSize={s};fillColor={f};swimlaneFillColor={sf};strokeColor=#d1d5db;fontStyle=1;fontSize=12;html=1;"
STEP = "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#111111;strokeWidth=2;fontSize=13;"
TRIG = "rounded=1;arcSize=45;whiteSpace=wrap;html=1;fillColor=#fff7e6;strokeColor=#F7A11A;strokeWidth=2;fontSize=13;"
END = "rounded=1;arcSize=45;whiteSpace=wrap;html=1;fillColor=#f3f4f6;strokeColor=#111111;strokeWidth=2;fontSize=13;"
DATA = "rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#111111;dashed=1;strokeWidth=2;fontSize=13;"
DEC = "rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#111111;strokeWidth=2;fontSize=13;"
EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;endArrow=block;endFill=1;fontSize=13;fontStyle=1;"
TITLE = "text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=middle;"


def lanes(doc, names, width):
    for i, name in enumerate(names):
        doc.add(name, LANE_STYLE.format(s=46, f="#e5e7eb", sf="#ffffff" if i % 2 else "#f8fafc"),
                X0, Y0 + i * LANE_H, width, LANE_H)


def template(out):
    doc = Doc(); width = 2200
    doc.add("Process: ............   ·   Trigger: ............   ·   End state: ............   ·   hand-offs: __   (rename the lanes: people first, then systems)", TITLE, X0, 10, width, 40)
    lanes(doc, ["Actor 1", "Actor 2", "Actor 3", "System 1", "System 2"], width)
    ly = Y0 + 5 * LANE_H + 40
    doc.add("Legend", "text;html=1;fontSize=14;fontStyle=1;align=left;", X0, ly, 100, 30)
    t = doc.add("Trigger\n(what starts it)", TRIG, X0 + 110, ly, BW, BH)
    s = doc.add("Step: verb + object\ntouch __ min", STEP, X0 + 340, ly, BW, BH)
    d = doc.add("Decision?\n(yes / no)", DEC, X0 + 570, ly - 12, BW, BH + 24)
    e = doc.add("End state", END, X0 + 800, ly, BW, BH)
    doc.add("wait __", EDGE + "fontColor=#F7A11A;", edge=True, src=t, tgt=s)
    doc.add("", EDGE, edge=True, src=s, tgt=d)
    doc.add("yes", EDGE, edge=True, src=d, tgt=e)
    x = X0 + 1040
    for tag, col in TAG_COLOUR.items():
        doc.add(tag, f"rounded=1;arcSize=30;html=1;fillColor={col};strokeColor=none;fontColor=#ffffff;fontStyle=1;fontSize=12;", x, ly + 22, 80, 28)
        x += 88
    (out / "Day2_S3_Swimlane_Template.drawio").write_text(doc.xml("Current state (template)"))


def example(out):
    doc = Doc(); width = 2350
    ids, kinds = {}, {}
    lanes(doc, [l.replace("Team spreadsheet\n(manager's own)", "Team sheet (manager)").replace("\n", " ") for l in LANES], width)
    for k, (lane, x, txt, touch, kind) in STEPS.items():
        cx = X0 + LABEL_W + (x - 1.9) * SCALE * 1.0 - 20
        cy = Y0 + lane * LANE_H + LANE_H / 2
        label = txt + (f"\ntouch {touch} min" if touch else "")
        style = {"trigger": TRIG, "step": STEP, "end": END, "data": DATA, "decision": DEC}[kind]
        h = BH + 24 if kind == "decision" else BH
        ids[k] = doc.add(label, style, cx - BW / 2, cy - h / 2, BW, h); kinds[k] = kind
        for j, t in enumerate(TAGS.get(k, [])):
            doc.add(t, f"rounded=1;arcSize=30;html=1;fillColor={TAG_COLOUR[t]};strokeColor=none;fontColor=#ffffff;fontStyle=1;fontSize=11;",
                    cx + BW / 2 - 70, cy - h / 2 - 20, 70, 22)
    for a, b, lab, kind in FLOWS:
        st = EDGE
        if kind == "data": st += "dashed=1;strokeColor=#6b7280;startArrow=block;startFill=1;"
        if kind == "no": st += "strokeColor=#dc2626;fontColor=#dc2626;"
        if "day" in lab: st += "fontColor=#F7A11A;"
        doc.add(lab, st, edge=True, src=ids[a], tgt=ids[b])
    doc.add("Leave request at AI Caravan Ltd.: current state   ·   Trigger: employee asks for leave   ·   "
            "End: decision recorded, balance and calendar updated   ·   hand-offs: 8", TITLE, X0, 10, width, 40)
    doc.add("Total touch time 25 min   ·   total elapsed time about 4 working days (six queues)   ·   dashed = looking something up",
            "text;html=1;fontSize=13;fontColor=#6b7280;align=left;", X0, Y0 + 5 * LANE_H + 15, width, 30)
    (out / "Day2_S3_Leave_Request_Example.drawio").write_text(doc.xml("Leave request: current state"))


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out/day2/Session3/05_drawio_Files"); out.mkdir(parents=True, exist_ok=True)
    template(out); example(out)
    print("wrote", out / "Day2_S3_Swimlane_Template.drawio", out / "Day2_S3_Leave_Request_Example.drawio")
