---
title: "Lab 3: Map Your Process as It Runs Today"
subtitle: "AI Administrator · Day 2 · Session 3 · Workflow Mapping I: The Current State"
kind: "Participant lab handout"
---

## Objective

Draw the course task you chose on Day 1 exactly as it happens today: who does what, how long each step takes, how long the work waits between steps, and where it hurts. This map is the input to Session 4 (the future state) and to the automation you build on Day 3.

**Time:** about one hour, including a 15-minute conversation with a colleague. Started in the session, finished at home. **Due:** before Session 4.

## What you need

- Your **M1-task-inventory** from Day 1, with the chosen course task highlighted.
- **draw.io** (also called diagrams.net): app.diagrams.net in a browser, or the free desktop app. Miro, Lucidchart, PowerPoint or paper and sticky notes also work; the steps are identical.
- The template **Day2_S3_Swimlane_Template.drawio** (shared in the chat) and, for reference, the finished example **Day2_S3_Leave_Request_Example.drawio**.
- An AI assistant, or the map reviewer bot from the practical.
- Fifteen minutes with one colleague who does part of the process.

## Steps

### 1. Write the SIPOC, the trigger and the end state

At the top of a new page write, in one sentence each:

- **Trigger:** what starts the process (an email arrives, a form is submitted, the first of the month).
- **End state:** how you know it is finished.

Then fill a five-column SIPOC:

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| Who provides the inputs? | What arrives to start or feed it? | Five to seven big steps, no detail | What leaves it? | Who receives the outputs? |

### 2. Interview one colleague

Spend fifteen minutes with someone who does part of the process. Use these openers and write down every exception they mention:

```
1. Walk me through the last one you handled, from the moment it arrived.
2. What did you have to look up, and where?
3. Who did you wait for, and how long?
4. When does this go wrong, and what do you do then?
5. Is there a step you do that isn't in the official process?
```

Do not propose fixes during the conversation. Ask for the real email, sheet or form and take a screenshot with permission.

### 3. Create the swimlanes

Open the template (or insert a pool from the shape panel: search "swimlane"). Make **one lane per actor**, including systems (email, HR system, a shared spreadsheet) as lanes of their own. Put the trigger at the far left.

### 4. Add steps, decisions and hand-offs

- One rectangle per action, written as a verb and an object: "Check leave balance".
- One diamond per decision, a yes/no question with **both** exits labelled.
- Connect them in order. Every arrow that crosses a lane is a **hand-off**. Count them and write the number in the title.

### 5. Add the two numbers

- Inside each step: **touch time** in minutes (actual work).
- On each arrow: the typical **wait** before the next step starts.
- At the bottom: total touch time and total elapsed time.

### 6. Tag the pain points

Add a small coloured label to each step. A step may carry more than one.

| Tag | Meaning | Typical fix (Session 4) |
|---|---|---|
| REKEY | Same data typed into a second system | Automation copies it |
| WAIT | Work sits for hours or days for no reason but attention | Notifications, reminders, routing |
| READ | A person reads free text to decide or extract something | AI classification or extraction step |
| DRAFT | A person writes near-identical text repeatedly | AI drafting step, human sends |
| CHASE | Someone reminds someone else to act | Scheduled reminders with escalation |
| RUBBER | An approval that is always given without reading | Remove it, or make it an exception check |
| JUDGE | A real decision needing judgement or accountability | Keep human; give them a better summary |

### 7. Ask for a review

Send your step list to the **map reviewer bot**, or export the map as PNG and give it to your assistant with this prompt (paste a text list of the steps if your assistant does not accept images):

```
This is a current-state swimlane map of a business process. List (1) any step that
seems to be missing between two connected steps, (2) decisions that have no "no" path,
and (3) the three hand-offs most likely to lose information. Do not suggest automation yet.

[paste your step list, or upload the PNG]
```

Check each finding against the policy or the people who do the work before you change the map.

### 8. Confirm with your colleague

Show your colleague the map for five minutes and correct anything they push back on. Save as **M3-current-state**.

## Deliverable

The current-state swimlane, as PNG and as the draw.io file, with:

- SIPOC, trigger and end state;
- touch time on every step, wait on every arrow, both totals;
- pain-point tags, and the hand-off count in the title;
- five lines on what the colleague interview changed.

Save it as **M3-current-state** and bring it to Session 4.

## Stuck?

- **"My process has no clear trigger."** What happened just before you started the last one: an email, a date, a call? If there is truly nothing, write that down; it is a finding.
- **"I am mapping what the procedure says."** Ask yourself when you last followed it exactly. Map the last real case, workarounds included.
- **"I do not know the wait times."** Estimate from the last three cases and write "about". Order of magnitude (hours or days) is what matters.
- **"draw.io is blocked."** Paper and sticky notes, one row per actor, then a photo.

## For the instructor: quick rubric

| Check | Pass looks like |
|---|---|
| Boundaries | Trigger, end state and a five-column SIPOC with 5 to 7 process steps |
| Lanes | Every actor and every system has a lane; steps sit in the right lane |
| Decisions | Diamonds with both exits labelled |
| Numbers | Touch time on every step, wait on every arrow, totals at the bottom |
| Tags | Every step tagged; at least one JUDGE step identified, or a reason why none exists |
| Reality | At least one workaround or exception from the interview appears on the map |
| Confirmed | Five lines on what the colleague changed |

Reference: Module 3 online, with the knowledge check scored in the browser:
albanna-tutorials.com/ai-administrator/03_workflow_mapping_current_state.html
