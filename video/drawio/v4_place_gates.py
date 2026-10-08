#!/usr/bin/env python3
"""Video 2 of Day 2, Session 4: place the approval gates on the future-state leave map.
Starts from page 2 of Day2_S4_Leave_Request_Future_State.drawio with the gates, the quarter-end rule and the decline end
taken out, then adds them back with real input. The result matches figures/d2s4_future.png and lab step 7.
python3 v4_place_gates.py [narrate|record|assemble|all|dry]"""
import xml.etree.ElementTree as ET
import dvlib as V

V.SESSION = "4"
NAME = "Day2_S4_Video2_Place_the_Gates"
SRC = "/Users/abedelkarimalbanna/albanna-portal/instructor/ai-administrator/out/day2/Session4/05_drawio_Files/Day2_S4_Leave_Request_Future_State.drawio"
TAKE_OUT = ("Approve?", "Last two weeks", "Gets the decision")
RED_GATE = "fillColor=#fee2e2;strokeColor=#dc2626;strokeWidth=3;fontStyle=1;"
RED_EDGE = "strokeColor=#dc2626;fontColor=#dc2626;"
FIND = {"D0": "All checks", "F3": "Prepares the", "F4": "Records leave", "E1": "Recorded and", "TITLE": "Leave request at AI Caravan"}


def lane_c(lane): return 60 + 140 * lane + 70
def col_c(x): return 150 + (x - 1.9) * 100


def page2_without_gates():
    """The future-state page as XML, minus the cells the video draws (and every arrow that touches them)."""
    root = ET.fromstring(open(SRC).read())
    model = root.findall("diagram")[1].find("mxGraphModel"); cells = model.find("root")
    gone = {c.get("id") for c in cells if c.get("vertex") and str(c.get("value", "")).startswith(TAKE_OUT)}
    for c in list(cells):
        if c.get("id") in gone or c.get("source") in gone or c.get("target") in gone:
            cells.remove(c)
    return ET.tostring(model, encoding="unicode")


async def prepare(d):
    await d.p.evaluate("""(xml) => { const ui = window.__ui; const m = mxUtils.parseXml(xml).documentElement;
        ui.editor.setGraphXml(m); ui.toggleFormatPanel(false); ui.hsplitPosition = 0; ui.refresh();
        const g = ui.editor.graph; g.zoomTo(Math.min((g.container.clientWidth - 40) / 2440, (g.container.clientHeight - 30) / 980)); }""",
                       page2_without_gates())
    await d.pause(1.0)
    for k, label in FIND.items():
        d.ids[k] = await d.find(label)
    missing = [k for k, v in d.ids.items() if not v]
    if missing: raise RuntimeError(f"cells not found: {missing}")


async def style(d, name, add):
    await d.select(name); await d.key("Meta+e"); await d.pause(0.7)
    await d.p.keyboard.press("Meta+ArrowDown"); await d.type(add, 30); await d.pause(0.3)
    box = await d.p.get_by_role("button", name="Apply").first.bounding_box()
    await d.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, 0.3); await d.blank()


async def clone(d, src, name, x, lane, text):
    """Select a shape, Command D, drag the copy so its centre lands on (column x, lane), type its label."""
    await d.select(src); await d.key("Meta+d"); await d.pause(0.3)
    d.ids[name] = await d.p.evaluate(V.JS_SEL)
    sx, sy = await d.center(name); tx, ty = await d.screen(col_c(x), lane_c(lane))
    await d.drag(sx, sy, tx, ty); await d.blank()
    await d.rename(name, text)


async def red_edge(d, eid):
    """Colour an arrow red through Edit Style (the edge is selected by clicking its label)."""
    xy = await d.p.evaluate("""(id) => { const g = window.__ui.editor.graph; const s = g.view.getState(g.model.getCell(id));
        const b = s.text.node.getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; }""", eid)
    await d.click(xy[0], xy[1], 0.35); await d.key("Meta+e"); await d.pause(0.7)
    await d.p.keyboard.press("Meta+ArrowDown"); await d.type(RED_EDGE, 30); await d.pause(0.3)
    box = await d.p.get_by_role("button", name="Apply").first.bounding_box()
    await d.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, 0.3); await d.blank()


async def b_intro(d):
    await d.banner("Place the approval gates", "from the scored candidates to the future-state map")
    await d.pause(6.5); await d.banner("")


async def b_open(d):
    await d.pause(1.0)
    for k in ("D0", "F3"):
        x, y = await d.center(k); await d.move(x, y + 40); await d.pause(1.4)


async def b_gate1(d):
    await clone(d, "D0", "G1", 14.65, 1, "Approve? (gate)")
    await style(d, "G1", RED_GATE)


async def b_feed(d):
    await d.connect("F3", "G1", "same day")


async def b_no(d):
    await clone(d, "E1", "N1", 19.35, 0, "Gets the decision with the reason")
    eid = await d.connect("G1", "N1", "No, with reason", side="u")
    await red_edge(d, eid)


async def b_quarter(d):
    await clone(d, "D0", "Q1", 17.0, 3, "Quarter end?")
    await d.connect("G1", "Q1", "Yes", side="d", into="l")
    await d.connect("Q1", "F4", "No")


async def b_gate2(d):
    await clone(d, "G1", "G2", 17.0, 2, "Approve? (gate)")
    await d.connect("Q1", "G2", "Yes", side="u")
    await d.connect("G2", "F4", "Yes")
    eid = await d.connect("G2", "N1", "No", side="u")
    await red_edge(d, eid)


async def b_export(d):
    await d.rename("TITLE", "Leave request at AI Caravan Ltd.: future state   ·   gates: line manager; department head at quarter end   ·   "
                            "routine request: 4 hand-offs, 4 min touch")
    await d.pause(1.0)
    await d.menu("File", "Export as", "PNG...")
    await d.pause(2.5); await d.p.keyboard.press("Escape"); await d.pause(0.5)


BEATS = [
    {"chip": "AI Administrator · Place the gates", "do": b_intro,
     "say": "In this video we finish the future state of the leave request. The automation does the preparation; "
            "now we decide exactly where a person stops it, and what happens when they say no."},
    {"chip": "The future state so far", "do": b_open,
     "say": "Here is the redesigned flow. The employee submits a form. The automation reads the balance, runs the notice "
            "and probation checks, reads the note and flags anything unusual, and anything that fails goes to HR. "
            "Then it prepares a decision card. Those were our build-first candidates. Nothing irreversible has happened yet."},
    {"chip": "1 · The gate, as late as possible", "do": b_gate1, "fast": True,
     "say": "The first irreversible step is recording the leave and telling the employee: from then on they book flights. "
            "So the gate goes just before it, in the manager's lane. I copy a diamond, call it Approve, and make it red and bold."},
    {"chip": "2 · The gate carries the evidence", "do": b_feed,
     "say": "The decision card feeds the gate, usually the same day. The manager sees the request, the balance, the notice check, "
            "the clashes and what the AI concluded, on one screen, with approve, edit or decline."},
    {"chip": "3 · Every gate has a no", "do": b_no, "fast": True,
     "say": "Every diamond needs a no. If the manager declines, the employee gets the decision with the reason. "
            "I colour that arrow red so the decline path is easy to see."},
    {"chip": "4 · The quarter-end rule", "do": b_quarter, "fast": True,
     "say": "The policy adds one rule: leave in the last two weeks of a quarter also needs the department head. "
            "That check, quarter end, is rule-based, so it sits in the Automation lane. No, and the leave is recorded straight away."},
    {"chip": "5 · A second gate, only when it applies", "do": b_gate2, "fast": True,
     "say": "Yes, and it goes to a second gate in the department head's lane, with its own no. This is not two gates in a row "
            "for the same decision: it is a different accountable person, and only when the policy says so."},
    {"chip": "6 · Name it and export", "do": b_export,
     "say": "Write the gates in the title and export a PNG for your M4 folder. A routine request is now four hand-offs, "
            "four minutes of work and a same-day answer, and every decision about a person's leave is still made by a person."},
]

if __name__ == "__main__":
    V.main(NAME, BEATS, prepare)
