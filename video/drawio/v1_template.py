#!/usr/bin/env python3
"""Video 1: build the swimlane template in draw.io (Day 2, Session 3).   python3 v1_template.py [narrate|record|assemble|all]"""
import dvlib as V
from dvlib import GENERAL

NAME = "Day2_S3_Video1_Swimlane_Template"
LANES = ["Employee", "Line manager", "HR coordinator", "HR portal", "Team sheet"]
TAGS = [("REKEY", "blue"), ("WAIT", "purple"), ("READ", "green"), ("DRAFT", "yellow"), ("CHASE", "orange"), ("RUBBER", "grey"), ("JUDGE", "red")]


async def b_intro(d):
    await d.banner("Build a swimlane template", "draw.io, step by step")
    await d.pause(6.5); await d.banner("")


async def b_pool(d):
    await d.click(110, 123); await d.type("pool", 90); await d.key("Enter"); await d.pause(1.5)
    await d.move(27, 229); await d.pause(0.8)
    await d.drop("pool", (27, 229), 40, 80)
    await d.pause(0.6); await d.blank()
    await d.click(207, 123, 0.6); await d.p.keyboard.press('Escape')   # clear the search so the General shapes are back


async def lanes(d):
    g = await d.p.evaluate("""(id) => { const g = window.__ui.editor.graph; const c = g.model.getCell(id);
        const out = []; for (let i = 0; i < g.model.getChildCount(c); i++) out.push(g.model.getChildAt(c, i).id); return out; }""", d.ids["pool"])
    return g


async def b_dup(d):
    ls = await lanes(d); r = await d.rect(ls[-1])
    await d.click(r["x"] + 220, r["y"] + 60, 0.4)
    for _ in range(2):
        await d.pause(0.6); await d.key("Meta+d"); await d.pause(0.6)
    await d.blank()


async def b_widen(d):
    r = await d.rect("pool")
    await d.click(r["x"] + 9, r["y"] + r["h"] / 2, 0.5)
    await d.drag(r["x"] + r["w"], r["y"] + r["h"] / 2, r["x"] + r["w"] + 330, r["y"] + r["h"] / 2)
    await d.blank()


async def b_rename(d):
    ls = await lanes(d)
    for lane, text in zip(ls, LANES):
        r = await d.rect(lane)
        await d.rename((r["x"] + 10, r["y"] + r["h"] / 2), text)
    r = await d.rect("pool")
    await d.rename((r["x"] + 9, r["y"] + r["h"] / 2), "Process name")


async def b_trigger(d):
    await d.drop("trigger", GENERAL["rounded"], 40, 740); await d.type("Trigger"); await d.blank()
    await d.select("trigger"); await d.preset("orange"); await d.blank()


async def b_step(d):
    await d.drop("step", GENERAL["rounded"], 220, 740); await d.type("Verb + object, touch _ min"); await d.blank()


async def b_decision(d):
    await d.drop("decision", GENERAL["diamond"], 410, 730); await d.type("Yes / no?"); await d.blank()


async def b_connect(d):
    await d.connect("trigger", "step", "1 day")
    await d.connect("step", "decision")


async def b_tags(d):
    await d.drop("t0", GENERAL["rounded"], 40, 840)
    await d.resize("t0", -44, -32)
    await d.type(TAGS[0][0]); await d.blank(); await d.select("t0"); await d.preset(TAGS[0][1]); await d.blank()
    for i, (tag, col) in enumerate(TAGS[1:], 1):
        d.fast = i > 1
        await d.select(f"t{i - 1}" if i > 1 else "t0"); await d.key("Meta+d")
        nid = await d.p.evaluate(V.JS_SEL); d.ids[f"t{i}"] = nid
        x, y = await d.center(f"t{i}"); tx, ty = await d.screen(40 + i * 92 + 40, 840 + 15)   # centre of an 80x30 tag whose top-left is (40 + i*92, 840)
        await d.drag(x, y, tx, ty)
        await d.rename(f"t{i}", tag); await d.select(f"t{i}"); await d.preset(col); await d.blank()
    d.fast = False


async def b_title(d):
    await d.drop("title", GENERAL["text"], 40, 30)
    await d.type("Process: ...   Trigger: ...   End state: ...   Hand-offs: _"); await d.blank()
    await d.resize("title", 470, 0, handle=4); await d.blank()
    await d.pause(1.0)
    await d.menu("File", "Save as...")
    await d.pause(2.5); await d.p.keyboard.press("Escape"); await d.pause(0.5)


BEATS = [
    {"chip": "AI Administrator · Swimlane template", "do": b_intro,
     "say": "In this short video I'll build the swimlane template we use for every current-state map in this course. "
            "Open draw.io in your browser at app dot diagrams dot net, and start with a blank diagram."},
    {"chip": "1 · Insert a pool", "do": b_pool,
     "say": "First, the lanes. In the search box on the left, type pool, and drag the horizontal pool onto the page. "
            "A pool is a container, and each lane inside it belongs to one actor: a person, a team, or a system."},
    {"chip": "2 · Five lanes", "do": b_dup,
     "say": "Most of our processes need five lanes. Select the last lane and press Command D, or Control D on Windows, "
            "to duplicate it. Do it twice."},
    {"chip": "3 · Make it wide", "do": b_widen,
     "say": "Now make the pool wide enough for a whole process. Select the pool by its label on the left, "
            "and drag the handle on its right edge."},
    {"chip": "4 · Name the lanes", "do": b_rename,
     "say": "Rename the lanes. Double-click a lane label and type. People first: the person who starts the process, "
            "then everyone else who touches it. Then the systems, here the HR portal and a shared team sheet. "
            "Systems get lanes too, because typing into a system is a hand-off."},
    {"chip": "5 · Legend: trigger", "do": b_trigger,
     "say": "Below the pool, add a small legend, so everyone draws the same way. A rounded box for the trigger, "
            "coloured orange in the Style panel so it stands out."},
    {"chip": "6 · Legend: step", "do": b_step,
     "say": "A plain box for a step. Always a verb and an object, with the touch time written inside."},
    {"chip": "7 · Legend: decision", "do": b_decision,
     "say": "And a diamond for a decision: one yes or no question."},
    {"chip": "8 · Connect and add the wait", "do": b_connect,
     "say": "To connect two shapes, hover over the first one and drag one of its blue arrows onto the next. "
            "Then just type, and the text goes on the arrow. That is where the wait time lives."},
    {"chip": "9 · The seven tags", "do": b_tags,
     "say": "Finally, the seven pain-point tags. I make one small label, colour it, then duplicate it with Command D "
            "for the others: REKEY, WAIT, READ, DRAFT, CHASE, RUBBER, and JUDGE."},
    {"chip": "10 · Title and save", "do": b_title,
     "say": "Add a title line at the top for the process, the trigger, the end state and the number of hand-offs. "
            "Then save it with File, Save as, and keep the dot drawio file. That's your template. "
            "Make a copy of it for every process you map, and you're ready."},
]

if __name__ == "__main__":
    V.main(NAME, BEATS)
