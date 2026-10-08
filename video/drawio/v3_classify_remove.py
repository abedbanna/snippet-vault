#!/usr/bin/env python3
"""Video 1 of Day 2, Session 4: classify the Session 3 leave map, remove before automating, add the Automation lane.
Starts from the Session 3 example file; the result matches figures/d2s4_classified.png and lab steps 1 to 3.
python3 v3_classify_remove.py [narrate|record|assemble|all|dry]"""
import dvlib as V

V.SESSION = "4"
NAME = "Day2_S4_Video1_Classify_and_Remove"
SRC = "/Users/abedelkarimalbanna/albanna-portal/instructor/ai-administrator/out/day2/Session3/05_drawio_Files/Day2_S3_Leave_Request_Example.drawio"
TAGS = ["REKEY", "WAIT", "READ", "DRAFT", "CHASE", "RUBBER", "JUDGE"]
STEPS = {"T": "Emails manager:", "S1": "Reads email,", "S2": "Emails HR:", "S3": "Looks up balance,", "D1": "Balance OK",
         "S4": "Replies 'approved'", "S5": "Re-enters request", "S6": "Approves in portal", "S7": "Sends confirmation",
         "S8": "Updates team", "TITLE": "Leave request at AI Caravan", "TOTALS": "Total touch time",
         "PORTAL": "HR portal", "SHEET": "Team sheet"}
GREEN = "fillColor=#dcfce7;strokeColor=#16a34a;"
AMBER = "fillColor=#fef3c7;strokeColor=#d97706;"
RED = "fillColor=#fee2e2;strokeColor=#dc2626;"
AUTO_Y = 60 + 5 * 140 + 70           # centre of the new sixth lane, in diagram coordinates

JS_TAG = """([sid, tags]) => { const g = window.__ui.editor.graph, m = g.model; const s = m.getCell(sid).geometry;
  const out = []; for (const c of Object.values(m.cells)) { if (!c.vertex || !tags.includes(String(c.value))) continue;
    const q = c.geometry; if (q.x >= s.x && q.x <= s.x + s.width && q.y < s.y && q.y > s.y - 40) out.push(c.id); } return out; }"""
JS_ALLTAGS = """(tags) => Object.values(window.__ui.editor.graph.model.cells).filter(c => c.vertex && tags.includes(String(c.value))).map(c => c.id)"""


async def prepare(d):
    """Open the Session 3 map, hide both side panels and zoom so the whole page and a sixth lane fit (trimmed)."""
    await d.p.evaluate("""(xml) => { const ui = window.__ui; const m = mxUtils.parseXml(xml).getElementsByTagName('mxGraphModel')[0];
        ui.editor.setGraphXml(m); ui.toggleFormatPanel(false); ui.hsplitPosition = 0; ui.refresh();
        const g = ui.editor.graph; g.zoomTo(Math.min((g.container.clientWidth - 40) / 2400, (g.container.clientHeight - 30) / 940));
        g.scrollCellToVisible(g.model.getCell('c2')); }""", open(SRC).read())
    await d.pause(1.0)
    for k, label in STEPS.items():
        d.ids[k] = await d.find(label)
    missing = [k for k, v in d.ids.items() if not v]
    if missing: raise RuntimeError(f"cells not found: {missing}")


async def style(d, name, add):
    """Edit > Edit Style (Command E) and append to the style, as a participant would."""
    await d.select(name); await d.key("Meta+e"); await d.pause(0.7)
    await d.p.keyboard.press("Meta+ArrowDown"); await d.type(add, 35); await d.pause(0.3)
    box = await d.p.get_by_role("button", name="Apply").first.bounding_box()
    await d.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, 0.3); await d.blank()


async def shift_select(d, ids):
    await d.blank()
    for i, cid in enumerate(ids):
        x, y = await d.center(cid)
        if i: await d.p.keyboard.down("Shift")
        await d.click(x, y, 0.25)
        if i: await d.p.keyboard.up("Shift")


async def move_to(d, name, y_diagram):
    """Drag a shape straight down (or up) to a lane, keeping its column."""
    x, y = await d.center(name); r = await d.p.evaluate("(id) => window.__ui.editor.graph.model.getCell(id).geometry", d.ids[name])
    tx, ty = await d.screen(r["x"] + r["width"] / 2, y_diagram)
    await d.select(name); await d.drag(x, y, tx, ty); await d.blank()


async def b_intro(d):
    await d.banner("Classify and remove", "the Session 3 map, redrawn one step at a time")
    await d.pause(6.5); await d.banner("")


async def b_open(d):
    await d.pause(2.0)
    x, y = await d.center("TITLE"); await d.move(x - 300, y); await d.pause(1.5)
    x, y = await d.center("TOTALS"); await d.move(x - 300, y); await d.pause(1.0)


async def b_green(d):
    for k in ("S3", "S4", "S7"):
        await style(d, k, GREEN)


async def b_amber(d):
    await style(d, "S1", AMBER)


async def b_red(d):
    await style(d, "D1", RED)


async def b_remove(d):
    ids = [d.ids[k] for k in ("S2", "S5", "S6", "S8")]
    for k in ("S2", "S5", "S6", "S8"):
        ids += await d.p.evaluate(JS_TAG, [d.ids[k], TAGS])
    await shift_select(d, ids); await d.pause(1.0)
    await d.key("Meta+Delete"); await d.pause(0.8)          # Delete All: the boxes and their arrows


async def b_trigger(d):
    await d.rename("T", "Submits leave form in the HR portal (2 min)")
    await d.rename("SHEET", "Team calendar")


async def b_lane(d):
    await d.select("TOTALS"); await d.key("Delete")
    await shift_select(d, await d.p.evaluate(JS_ALLTAGS, TAGS)); await d.key("Delete")
    r = await d.rect("PORTAL")
    await d.click(r["x"] + r["w"] * 0.62, r["y"] + r["h"] / 2, 0.4)
    await d.key("Meta+d"); await d.pause(0.4)
    d.ids["AUTO"] = await d.p.evaluate(V.JS_SEL)
    g = await d.p.evaluate("(id) => window.__ui.editor.graph.model.getCell(id).geometry", d.ids["AUTO"])
    x, y = await d.screen(g["x"] + g["width"] * 0.62, g["y"] + g["height"] / 2)
    tx, ty = await d.screen(g["x"] - 10 + g["width"] * 0.62, AUTO_Y)
    await d.drag(x, y, tx, ty)
    await d.key("Meta+Shift+b"); await d.blank()             # To Back: the new lane must not cover the arrows
    r = await d.rect("AUTO")
    await d.rename((r["x"] + 10, r["y"] + r["h"] / 2), "Automation\nowner: HR")


async def b_move(d):
    for k in ("S1", "S3", "S4", "S7"):
        await move_to(d, k, AUTO_Y)
    d.ids["L1"] = await d.find("Team calendar lookup")         # slide the lookup aside, off the trigger's arrow
    x, y = await d.center("L1"); await d.click(x + 45, y, 0.3); await d.drag(x + 45, y, x - 105, y); await d.blank()   # grab right of the arrow


async def b_reconnect(d):
    await d.connect("S1", "S3")
    await d.connect("S4", "S7")


async def b_title(d):
    await d.rename("TITLE", "Leave request: classified, removed, Automation lane added   ·   "
                            "removed: e-mail chase, re-entry, HR click (RUBBER), private sheet")
    await d.pause(1.0)


BEATS = [
    {"chip": "AI Administrator · Classify and remove", "do": b_intro,
     "say": "In this video I take the leave-request map from Session 3 and start the future state. "
            "Three steps: classify every box, remove what should not exist, and give the machine its own lane."},
    {"chip": "Start from the current state", "do": b_open,
     "say": "This is the Session 3 map: twenty-five minutes of work, about four days of waiting, eight hand-offs. "
            "Work on a copy: right-click the page tab and choose Duplicate, so the current state stays as it was."},
    {"chip": "1 · Green: rule-based", "do": b_green, "fast": True,
     "say": "For every box, one question: could I write the rule in one sentence, with no usually? "
            "Looking up the balance, yes. Sending the decision with a template, yes. The confirmation, yes. "
            "Those turn green. I add the colour with Command E, Edit Style."},
    {"chip": "2 · Amber: AI-judged", "do": b_amber,
     "say": "Reading the employee's note is different. A person does it in seconds, but nobody can list every exception. "
            "That is AI-judged, so it is amber."},
    {"chip": "3 · Red: human-only", "do": b_red,
     "say": "The manager's decision is red. Someone has to be accountable for the team. That one stays human."},
    {"chip": "4 · Remove before you automate", "do": b_remove, "fast": True,
     "say": "Now remove before you automate. The email chase to HR goes, because the balance can be read from the portal. "
            "The employee typing the request again goes. HR's approval click goes: it is never refused, so it is a rubber stamp. "
            "And the private team sheet goes; the policy forbids it anyway. Four boxes deleted, not automated."},
    {"chip": "5 · Simplify the trigger", "do": b_trigger,
     "say": "The trigger stays the same request, but simpler: one leave form in the HR portal instead of an email. "
            "And the team calendar now lives in the portal, not in the manager's own sheet."},
    {"chip": "6 · Add the Automation lane", "do": b_lane, "fast": True,
     "say": "The tags have done their job, so I clear them. Then I duplicate a lane, drag it to the bottom, and call it Automation. "
            "Write the owner on the lane: the HR coordinator answers when it fails."},
    {"chip": "7 · Move the machine's steps", "do": b_move, "fast": True,
     "say": "Green and amber steps move into the Automation lane, in the same order. "
            "What stays in the human lanes is the point of the exercise: the employee's form and the manager's decision."},
    {"chip": "8 · Close the gaps", "do": b_reconnect,
     "say": "Deleting boxes left two gaps in the flow, so I reconnect them: note to balance, decision email to confirmation."},
    {"chip": "9 · Write down what you removed", "do": b_title,
     "say": "Last, write in the title what you removed, so nobody puts it back by accident. "
            "In the next video we score the candidates and place the approval gate."},
]

if __name__ == "__main__":
    V.main(NAME, BEATS, prepare)
