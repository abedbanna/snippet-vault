#!/usr/bin/env python3
"""Video 2: map the leave-request example on the swimlane template (Day 2, Session 3).
Same steps, waits and tags as figures/d2s3_swimlane.png.   python3 v2_leave_request.py [narrate|record|assemble|all|dry]"""
import dvlib as V

NAME = "Day2_S3_Video2_Leave_Request_Map"
TPL = "/Users/abedelkarimalbanna/albanna-portal/instructor/ai-administrator/out/day2/Day2_S3_Swimlane_Template.drawio"
LANES = ["Employee", "Line manager", "HR coordinator", "HR portal", "Team sheet (manager)"]
# template cells: c2 title, c3-c7 lanes, c9 trigger, c10 step, c11 decision, c12 end, c16-c22 tags
LEGEND = {"trigger": "c9", "step": "c10", "decision": "c11", "end": "c12"}
TAG = {t: f"c{16 + i}" for i, t in enumerate(["REKEY", "WAIT", "READ", "DRAFT", "CHASE", "RUBBER", "JUDGE"])}


def col(c): return 96 + 240 * c
def lane_top(i): return 60 + 140 * i


async def prepare(d):
    """Open the template, hide both side panels and zoom so the whole page fits (trimmed from the video)."""
    await d.p.evaluate("""(xml) => { const ui = window.__ui; const m = mxUtils.parseXml(xml).getElementsByTagName('mxGraphModel')[0];
        ui.editor.setGraphXml(m); ui.toggleFormatPanel(false); ui.hsplitPosition = 0; ui.refresh();
        const g = ui.editor.graph; g.zoomTo((g.container.clientWidth - 40) / 2260); }""", open(TPL).read())
    await d.pause(1.0)


async def clone(d, src, name, c, lane, text=None, kind="step"):
    """Select a shape, duplicate it with Command D, drag the copy to column c of the lane, then type its label."""
    w, h = (170, 100) if kind == "decision" else (170, 76)
    await d.select(src); await d.key("Meta+d"); await d.pause(0.3)
    d.ids[name] = await d.p.evaluate(V.JS_SEL)
    x, y = await d.center(name); tx, ty = await d.screen(col(c) + w / 2, lane_top(lane) + 70)
    await d.drag(x, y, tx, ty); await d.blank()
    if text: await d.rename(name, text)


async def tag(d, t, step):
    """Copy a tag from the legend onto the top-right corner of a step."""
    await d.select(TAG[t]); await d.key("Meta+d"); await d.pause(0.2)
    nid = await d.p.evaluate(V.JS_SEL); x, y = await d.center(nid)
    r = await d.rect(step); tx, ty = r["x"] + r["w"] - 20, r["y"]
    await d.drag(x, y, tx, ty); await d.blank()


async def dashed(d, name):
    """Edit > Edit Style (Command E): add dashed=1 to the style."""
    await d.select(name); await d.key("Meta+e"); await d.pause(0.8)
    await d.p.keyboard.press("Meta+ArrowDown"); await d.type("dashed=1;"); await d.pause(0.5)
    box = await d.p.get_by_role("button", name="Apply").first.bounding_box()
    await d.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, 0.4); await d.blank()


async def b_intro(d):
    await d.banner("Map the leave request", "from the template to a finished current-state map")
    await d.pause(7.0); await d.banner("")


async def b_lanes(d):
    for i, text in enumerate(LANES):
        r = await d.rect(f"c{3 + i}")
        await d.rename((r["x"] + 14, r["y"] + r["h"] / 2), text)


async def b_trigger(d):
    await clone(d, LEGEND["trigger"], "T", 0, 0, "Emails manager: can I take 3 days? (3 min)", "trigger")


async def b_step1(d):
    await clone(d, LEGEND["step"], "S1", 1, 1, "Reads email, checks clashes (6 min)")


async def b_wait1(d):
    await d.connect("T", "S1", "1 day")


async def b_lookup(d):
    await clone(d, "S1", "L1", 1, 4, "Team calendar lookup")
    await dashed(d, "L1")
    await d.connect("S1", "L1", side="d")


async def b_hr(d):
    await clone(d, "S1", "S2", 2, 1, "Emails HR: what is her balance? (2 min)")
    await d.connect("S1", "S2")
    await clone(d, "S2", "S3", 3, 2, "Looks up balance, replies by email (4 min)")
    await d.connect("S2", "S3", "1 day")
    await clone(d, "L1", "L3", 3, 3, "Balance record")
    await d.connect("S3", "L3", side="d")


async def b_decision(d):
    await clone(d, LEGEND["decision"], "D1", 4, 1, "Balance OK? No clash?", "decision")
    await d.connect("S3", "D1", "0.5 day")
    await clone(d, LEGEND["end"], "N1", 4, 0, "Gets a no email (end)")
    await d.connect("D1", "N1", "No", side="u")
    await clone(d, "S2", "S4", 5, 1, "Replies approved by email (3 min)")
    await d.connect("D1", "S4", "Yes")


async def b_rest(d):
    await clone(d, "S4", "S5", 6, 0, "Re-enters request in HR portal (3 min)")
    await d.connect("S4", "S5", "0.5 day")
    await clone(d, "S3", "S6", 7, 2, "Approves in portal (1 min)")
    await d.connect("S5", "S6", "0.75 day")
    await clone(d, "N1", "S7", 8, 3, "Sends confirmation (end)")
    await d.connect("S6", "S7")
    await clone(d, "S4", "S8", 8, 1, "Updates team sheet (3 min)")
    await d.connect("S7", "S8", "0.25 day", side="u")


async def b_tags(d):
    for t, s in [("WAIT", "T"), ("READ", "S1"), ("CHASE", "S2"), ("REKEY", "S3"), ("JUDGE", "D1"), ("DRAFT", "S4"),
                 ("REKEY", "S5"), ("RUBBER", "S6"), ("REKEY", "S8")]:
        await tag(d, t, s)


async def b_count(d):
    await d.rename("c2", "Leave request: current state · Trigger: employee asks for leave · End: decision recorded · "
                         "hand-offs: 8 · touch 25 min · elapsed about 4 days")
    await d.pause(1.0)
    await d.menu("File", "Export as", "PNG...")
    await d.pause(2.5); await d.p.keyboard.press("Escape"); await d.pause(0.5)


BEATS = [
    {"chip": "AI Administrator · Leave request map", "do": b_intro,
     "say": "In this video I take the template and map a real process: the annual leave request at AI Caravan Limited, "
            "the same example we use in the slides. Watch how each step lands in the lane of the person who does it."},
    {"chip": "1 · Name the lanes", "do": b_lanes,
     "say": "I've opened a copy of the template and zoomed out so the whole page fits. First, the lanes: the employee, "
            "the line manager and the HR coordinator. Then the two systems: the HR portal and the manager's own team sheet."},
    {"chip": "2 · The trigger", "do": b_trigger,
     "say": "Every map starts with the trigger. I select the trigger in the legend, press Command D to copy it, "
            "drag the copy into the employee lane, and type what starts the process, with its touch time."},
    {"chip": "3 · First step", "do": b_step1,
     "say": "Then the steps. One box per step, a verb and an object, in the lane of whoever does it. "
            "The line manager reads the email and checks for clashes. Six minutes."},
    {"chip": "4 · The wait goes on the arrow", "do": b_wait1,
     "say": "Connect the two and type the wait on the arrow. The email sits in the inbox for a day before anyone reads it."},
    {"chip": "5 · A lookup", "do": b_lookup,
     "say": "Checking the team sheet is a lookup, not a step, so it goes in the team sheet lane with a dashed border. "
            "Command E opens the style, and I add dashed equals one."},
    {"chip": "6 · Ask HR", "do": b_hr, "fast": True,
     "say": "Same pattern for the next steps. The manager emails HR for the balance: two minutes, then a day of waiting. "
            "HR looks it up in the portal and replies: four minutes."},
    {"chip": "7 · A decision has two exits", "do": b_decision, "fast": True,
     "say": "Now the decision: is the balance enough, and is there no clash? Every decision needs two exits. "
            "No, and the employee gets a decline by email. Yes, and the manager replies, approved."},
    {"chip": "8 · The part nobody sees", "do": b_rest, "fast": True,
     "say": "Then the part nobody sees. The employee types the same request again into the HR portal. "
            "HR approves it there, the portal sends a confirmation, and the manager updates the team sheet by hand."},
    {"chip": "9 · Tag the pain points", "do": b_tags, "fast": True,
     "say": "Now tag the pain points, copying tags from the legend. Waiting for the manager is WAIT. Reading the email, READ. "
            "Asking HR for the balance, CHASE. Typing the same data again, REKEY, three times. "
            "The decision is JUDGE: real human judgement, which we protect."},
    {"chip": "10 · Count and export", "do": b_count,
     "say": "Finally, count. Eight hand-offs, twenty-five minutes of touch time, and about four working days from start to end. "
            "Write that in the title, and export a PNG for your report. That gap between minutes and days "
            "is exactly what Session 4 works on."},
]

if __name__ == "__main__":
    V.main(NAME, BEATS, prepare)
