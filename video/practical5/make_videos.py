#!/usr/bin/env python3
"""Day 3 Session 5 videos (n8n): three narrated walkthroughs built from REAL n8n Cloud screenshots.

  1. Day3_S5_Video1_Open_Your_Workspace   sign-up and the trial rules
  2. Day3_S5_Video2_Leave_Request_Demo    the Session 4 first build running (backup for the live demo)
  3. Day3_S5_Video3_Lab_Request_Intake    the lab, node by node

Screens: instructor/ai-administrator/figures/d3s5_shot_*.jpg and shots/v*_*.jpg, captured 11 October 2026 on the
course trial workspace (personal e-mail addresses blurred). Each frame = the screen fitted into 1920x858, an orange
box on the control being discussed, and the Session 3/4 title band. Narration: ElevenLabs, same voice as Session 4.
Usage: python3 make_videos.py [--voice] [--only 1,2,3] [--slides]
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "..", "instructor", "ai-administrator", "figures")
SH = os.path.join(HERE, "shots")
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
W, H, TOP = 1920, 1080, 858
ORANGE, INK, GREY = (244, 160, 27), (17, 17, 17), (90, 90, 90)
F = "/System/Library/Fonts/Supplemental/"
bold = lambda s: ImageFont.truetype(F + "Arial Bold.ttf", s)
reg = lambda s: ImageFont.truetype(F + "Arial.ttf", s)
FOOT = "Real screens from n8n Cloud (trial workspace), 11 Oct 2026 · AI Caravan Ltd. and its staff are fictional"
SESSION = "IEEE CS Region 8 AI Caravan 2026 · AI Administrator · Day 3 · Session 5"


def src(name):
    for p in (os.path.join(FIG, name + ".jpg"), os.path.join(FIG, name + ".png"), os.path.join(SH, name + ".jpg")):
        if os.path.exists(p): return p
    raise SystemExit("missing screen: " + name)


def frame(name, title, sub, box=None):
    shot = Image.open(src(name)).convert("RGB")
    s = min(W / shot.width, TOP / shot.height); sw, sh = int(shot.width * s), int(shot.height * s)
    im = Image.new("RGB", (W, H), (233, 235, 238)); x0, y0 = (W - sw) // 2, (TOP - sh) // 2
    im.paste(shot.resize((sw, sh), Image.LANCZOS), (x0, y0)); d = ImageDraw.Draw(im)
    if box:
        a, b, c, e = box
        d.rounded_rectangle([x0 + a * s - 8, y0 + b * s - 8, x0 + c * s + 8, y0 + e * s + 8], 14, outline=ORANGE, width=7)
    d.rectangle([0, TOP, W, H], fill="white"); d.rectangle([0, TOP, W, TOP + 3], fill=(221, 220, 225))
    d.rectangle([60, 897, 70, 1017], fill=ORANGE)
    d.text((100, 912), title, font=bold(38), fill=INK)
    d.text((100, 966), sub, font=reg(31), fill=(40, 40, 40))
    tw = d.textlength(FOOT, font=reg(22)); d.text((W - 18 - tw, 1040), FOOT, font=reg(22), fill=GREY)
    return im


def card(title, lines):
    im = Image.new("RGB", (W, H), (252, 252, 252)); d = ImageDraw.Draw(im)
    d.rectangle([120, 300, 260, 308], fill=ORANGE)
    d.text((120, 335), title, font=bold(64), fill=INK)
    for i, l in enumerate(lines): d.text((120, 440 + i * 58), l, font=reg(38), fill=GREY)
    d.text((120, 990), SESSION, font=reg(28), fill=GREY)
    return im


# (kind, screen or card lines, title, subtitle, box in screenshot pixels, narration)
V1 = ("Day3_S5_Video1_Open_Your_Workspace", [
    ("card", ["About two minutes. Do it together with the group.", "You need a laptop and an e-mail inbox you can open now."],
     "Open your n8n workspace", None, None,
     "Let's open your n8n workspace. It takes about two minutes. You need a laptop, and an e-mail inbox you can open right now."),
    ("v1_pricing", None, "1 · n8n.io/pricing", "Start free trial: n8n Cloud, no credit card required", (161, 601, 428, 647),
     "Go to n8n dot i o, slash pricing, and click Start free trial. This is n8n Cloud, and no credit card is required."),
    ("card", ["Your e-mail address and a password.", "Open the verification e-mail: check spam and Promotions.",
              "Nothing after two minutes? Raise your hand in Zoom."], "2 · Register and verify", None, None,
     "Register with your e-mail address and a password, then open the verification e-mail. If it is not there, check spam "
     "and the Promotions tab. Still nothing after two minutes? Raise your hand in Zoom, and the co-host will help you in a breakout room."),
    ("v1_dashboard", None, "3 · Your workspace", "Your workspace name, the trial days left, and Open instance", (329, 280, 521, 445),
     "Your workspace gets its own name and address. The dashboard shows how many trial days are left. Click Open instance."),
    ("d3s5_shot_01_instance_ready", None, "4 · Your instance is ready", "Click Start automating", (595, 124, 972, 163),
     "After about a minute you see: your instance is ready. Click Start automating."),
    ("d3s5_shot_02_trial_onboarding", None, "5 · Two questions, and the clock", "Answer or skip. Top left: 14 days left, 0 of 1000 executions",
     (8, 10, 268, 34),
     "n8n asks two short questions; answer them or skip. Notice the counter at the top left: fourteen days left, "
     "and zero of one thousand executions. Every test run counts as one."),
    ("d3s5_shot_03_overview", None, "6 · You are in", "Stop here and wait for the group", (998, 345, 1182, 500),
     "You are in. From here, Build a workflow opens an empty canvas. Stop at this page and wait for the group."),
    ("d3s5_shot_07_menu_export", None, "Every session: Export JSON", "The three-dots menu next to the workflow name", (346, 365, 543, 397),
     "One habit for the whole course. At the end of every session, open the three-dots menu next to the workflow name, "
     "and choose Export JSON. Import, From file, loads it back into any n8n workspace."),
    ("card", ["14 days, then the workspace is deleted.", "1,000 executions; every test run counts.",
              "Export JSON at the end of every session."], "Three rules for the trial", None, None,
     "Three rules for the trial. It lasts fourteen days, and then the workspace is deleted. It allows one thousand executions. "
     "And you export your workflows at the end of every session."),
])

V2 = ("Day3_S5_Video2_Leave_Request_Demo", [
    ("card", ["Session 4's first build, as a real n8n workflow.", "Three test runs: one passes, two go to HR."],
     "The leave request runs", None, None,
     "In Session 4 you chose the first automation for the leave request. Here it is, running in n8n. "
     "We will submit three requests: one passes the checks, and two go to HR."),
    ("d3s5_map_to_nodes", None, "One step, one node", "The Automation lane from Session 4, read as n8n nodes", None,
     "Each step in the Automation lane becomes one node. The form is the trigger. Looking up the balance is a Google Sheets node. "
     "The policy checks and the decision are a code step and an IF. Logging and e-mails are Sheets and Gmail. "
     "And the manager's decision stays with the manager."),
    ("d3s5_shot_06_leave_canvas_unconnected", None, "The workflow", "Red triangles: credentials and the sheet link still to fill in",
     (130, 330, 1045, 515),
     "This is the workflow right after importing it. The red triangles mean something is missing: here, the Google credentials "
     "and the link to the sheet. Until they are filled in, the workflow cannot be published."),
    ("d3s5_shot_09_form_node", None, "The trigger is a form", "Test URL while testing; Production URL after Publish", (597, 160, 975, 280),
     "The trigger is an n8n form. It has two addresses: the test URL, which listens while you test, and the production URL, "
     "which works for everyone once the workflow is published."),
    ("d3s5_shot_11_test_form_filled", None, "Submit a request", "Annual leave, 15 to 17 November: 3 working days", None,
     "Click Execute workflow, open the test form, and submit a request: annual leave from the fifteenth to the seventeenth of November."),
    ("d3s5_shot_13_form_output_json", None, "One item, seven fields", "The output panel shows exactly what arrived", (995, 155, 1545, 450),
     "Open the form node and read its output. One submission is one item, with seven fields. These fields are what the next nodes use."),
    ("d3s5_shot_17_code_policy_checks", None, "The policy checks", "Notice: 2 working days for 1 to 2 days of leave, 10 for longer; then the balance",
     (490, 320, 1080, 620),
     "The policy checks follow the leave policy, one sentence at a time. One or two days of leave need two working days of notice; "
     "three or more need ten. And the request must fit the remaining balance."),
    ("d3s5_shot_14_if_node_empty", None, "All checks pass?", "True goes to the manager; false goes to HR", (513, 190, 1075, 226),
     "The IF node asks one question: did all checks pass? True goes to the manager. False goes to HR."),
    ("d3s5_shot_20_run_pass_green", None, "Run 1: checks pass", "Logged as Pending manager; the decision card is e-mailed", (383, 160, 1045, 400),
     "The first request passes. Every node turns green, with one item on each arrow. The request is logged as pending, "
     "and the manager receives a decision card."),
    ("d3s5_shot_21_run_flagged_executions", None, "Runs 2 and 3: flagged for HR", "Short notice, and not enough balance. Every run is kept in Executions",
     (64, 203, 317, 447),
     "Two more requests: one with only one day's notice, and one asking for three days when only two remain. Both take the false path "
     "and go to HR, not to the manager. On the left, the Executions list keeps every run, with its data."),
    ("d3s5_shot_23_sheet_rows_status", None, "The record", "Reason and Status, written by the workflow", (683, 182, 1075, 242),
     "And the sheet holds the record: one request pending the manager, and two flagged for HR, each with its reason in plain words."),
    ("card", ["The workflow prepares; it never approves.", "Next: a reminder (later) and an AI step (Session 6)."],
     "The manager still decides", None, None,
     "Notice what the workflow does not do. It prepares, and it never approves or declines: the manager still decides. "
     "A reminder comes later, and Session 6 adds an AI step."),
])

V3 = ("Day3_S5_Video3_Lab_Request_Intake", [
    ("card", ["Form, sheet, IF, two e-mails, a guard.", "Execute step after every node, and read its output."],
     "Lab: request intake", None, None,
     "Now you build your first workflow: a request form, logged to a sheet, with an IF, two e-mails, and a guard. "
     "After every node, click Execute step and read the output."),
    ("v3_canvas", None, "The finished workflow", "Seven nodes; build them in this order", (540, 280, 1490, 680),
     "This is where you will end up: seven nodes. Build them in this order, testing as you go."),
    ("card", ["A Google Sheet called Requests with seven headers:", "Timestamp, Name, Email, Department, Amount, Description, Status.",
              "A native Google Sheet, in the same Google account as n8n."], "1 · The sheet", None, None,
     "Step one: a Google Sheet called Requests, with seven column headers. It must be a native Google Sheet, "
     "in the same Google account you connect to n8n."),
    ("d3s5_shot_05_trigger_picker", None, "2 · The trigger", "Add first step, then On form submission", (1196, 525, 1568, 585),
     "Step two: create a workflow, click Add first step, and choose On form submission."),
    ("v3_form_node", None, "2 · Five fields", "Name, Email, Department, Amount as a number, Description", (597, 535, 972, 725),
     "Add five fields: Name, Email, a Department dropdown, Amount as a number, and Description."),
    ("d3s5_shot_24_lab_form", None, "2 · Execute step, then submit once", "Leave Email and Amount optional: the guard will need them", None,
     "Click Execute step, open the test URL, and submit one request. Leave Email and Amount optional. The guard in step six needs that."),
    ("v3_search_sheets", None, "3 · Log the row", "Plus, then search Google Sheets", (1210, 178, 1553, 216),
     "Step three: add a Google Sheets node."),
    ("v3_sheets_append", None, "3 · Append Row", "Sign in with Google, choose your sheet, map each column, Status = New", (597, 160, 975, 540),
     "Choose Append Row. Sign in with Google, using the account that owns your sheet. Pick the sheet, and map each column. "
     "For Status, type the fixed value: New."),
    ("v3_amount_if", None, "4 · Branch on amount", "IF: Amount, Number, is greater than 500", (513, 190, 1075, 252),
     "Step four: an IF node. Amount, a Number operator, is greater than, five hundred. Make sure it is a Number operator, not text."),
    ("v3_gmail", None, "5 · Two e-mails", "Gmail Send on each branch; To = Email, body with Name and Amount", (597, 355, 975, 480),
     "Step five: a Gmail node on each branch. Send it to the requester's e-mail, with a subject, and a short message using Name and Amount."),
    ("v3_complete_if", None, "6 · The guard", "Email is not empty AND Amount is greater than 0", (513, 190, 1075, 326),
     "Step six: a guard, right after the form. Email is not empty, and Amount is greater than zero."),
    ("card", ["A blank number field arrives as 0, not as empty.", "'Is not empty' lets it through, logs it and sends an e-mail.",
              "Test the empty case on purpose."], "Why greater than 0?", None, None,
     "Why greater than zero? We tested it: a blank number field arrives as zero, not as empty. A check for not empty lets it through. "
     "Always test the empty case on purpose."),
    ("v3_edit_fields", None, "6 · Mark it incomplete", "Edit Fields: Status = Incomplete, then append the row. No e-mail", (620, 275, 970, 368),
     "On the false side of the guard, an Edit Fields node sets Status to Incomplete, and a second Sheets node logs the row. No e-mail is sent."),
    ("d3s5_shot_16_retry_on_fail", None, "7 · Retry On Fail", "On each Gmail node: 3 tries, 5000 ms apart", (595, 245, 975, 400),
     "Step seven: open each Gmail node's Settings, and turn on Retry On Fail: three tries, five seconds apart."),
    ("v3_search_error_trigger", None, "7 · An error notifier", "A second workflow: Error Trigger, then Gmail to you", (1196, 238, 1568, 300),
     "Then make a second workflow, the error notifier: an Error Trigger, followed by a Gmail node to yourself."),
    ("v3_settings_error_wf", None, "7 · Attach it", "Workflow menu, Settings, Error Workflow", (290, 226, 1272, 266),
     "Back in the lab workflow, open Settings from the workflow menu, and choose the error notifier as the Error Workflow."),
    ("d3s5_shot_26_lab_run_incomplete", None, "8 · Test three times", "200, 900 and blank: New, New, Incomplete", (340, 270, 1010, 470),
     "Step eight: test three times: an amount of two hundred, nine hundred, and one left blank. Here, the blank one takes the incomplete path."),
    ("d3s5_shot_25_lab_sheet_rows", None, "8 · Check the sheet", "Three rows; two e-mails", (630, 180, 730, 238),
     "Check the sheet: three rows, new, new, and incomplete. And two e-mails in your inbox."),
    ("card", ["Publish (top right), and copy the production URL.", "Then the three-dots menu, Export JSON."],
     "8 · Publish and export", None, None,
     "Finally, click Publish, and copy the production form address. Then export your workflow as JSON. Well done: that is your first automation."),
])

VIDEOS = {1: V1, 2: V2, 3: V3}
VOICE, MODEL, GAP = "0f6a8dmX40t9NZBAo3ci", "eleven_multilingual_v2", 0.8
voice = "--voice" in sys.argv
only = [int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")] if "--only" in sys.argv else [1, 2, 3]
if voice:
    sys.path.insert(0, os.path.dirname(HERE)); import narrate   # video/narrate.py (key in ~/.albanna-elevenlabs-key)


def audio_len(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


billed = 0
for k in only:
    name, slides = VIDEOS[k]
    D = os.path.join(OUT, name); AUD = os.path.join(D, "audio"); os.makedirs(AUD, exist_ok=True)
    lst, cues, t = [], [], 0.0
    for i, (kind, lines, title, sub, box, say) in enumerate(slides):
        im = card(title, lines) if kind == "card" else frame(kind, title, sub, box)
        p = os.path.join(D, f"slide_{i:02d}.png"); im.save(p); dur = 6.0
        if voice:
            mp3, tj, aj = (os.path.join(AUD, f"s{i:02d}{e}") for e in (".mp3", ".txt", ".align.json"))
            if not (os.path.exists(mp3) and os.path.exists(tj) and open(tj).read() == say):
                al = narrate.speak(say, VOICE, mp3, model_id=MODEL)
                json.dump(al, open(aj, "w")); open(tj, "w").write(say); billed += len(say)
            lead = 0.5 if i == 0 else 0.3
            dur = round(lead + audio_len(mp3) + GAP, 2)
            cues += narrate.cues_from_alignment(json.load(open(aj)), offset=t + lead, max_chars=90); t += dur
        lst.append((p, dur))
    if "--slides" in sys.argv: continue
    with open(os.path.join(D, "list.txt"), "w") as f:
        for p, dur in lst: f.write(f"file '{p}'\nduration {dur}\n")
        f.write(f"file '{lst[-1][0]}'\n")
    mp4 = os.path.join(OUT, name + ".mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(D, "list.txt")]
    if voice:
        starts, t0 = [], 0.0
        for _, dur in lst: starts.append(t0); t0 += dur
        fl = []
        for i in range(len(lst)):
            cmd += ["-i", os.path.join(AUD, f"s{i:02d}.mp3")]; ms = int((starts[i] + (0.5 if i == 0 else 0.3)) * 1000)
            fl.append(f"[{i + 1}:a]adelay={ms}|{ms},apad[a{i}]")
        fl.append("".join(f"[a{i}]" for i in range(len(lst))) + f"amix=inputs={len(lst)}:normalize=0:duration=longest,atrim=0:{t0:.2f}[aout]")
        cmd += ["-filter_complex", ";".join(fl), "-map", "0:v", "-map", "[aout]", "-c:a", "aac", "-b:a", "160k"]
        narrate.write_srt(cues, mp4.replace(".mp4", ".srt"))
    cmd += ["-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True); print(mp4, f"{sum(d for _, d in lst):.0f}s")
if voice: print(f"narration: {billed} characters billed this run")
