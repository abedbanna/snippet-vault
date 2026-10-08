---
title: "Lab 4: Redesign Your Process and Choose the First Build"
subtitle: "AI Administrator · Day 2 · Session 4 · Workflow Mapping II: Designing the Future State"
kind: "Participant lab handout"
---

## Objective

Redraw your Session 3 map as it will run once an automation exists, score every automation candidate on value and risk, and choose the first one you will build on Day 3, with its approval gate marked.

**Time:** about one hour, including fifteen minutes with the colleague from Session 3. Started in the session, finished at home. **Due:** before Day 3.

## What you need

- Your **M3-current-state** map (draw.io file and PNG) from Session 3.
- **draw.io** (app.diagrams.net or the desktop app). For reference: **Day2_S4_Leave_Request_Future_State.drawio** (page 1 the current state classified, page 2 the future state).
- **Day2_S4_M4_Scoring_Template.xlsx** (open in Excel, or in Google Sheets with File, Import, Upload). For reference: **Day2_S4_M4_Scoring_Example.xlsx**, the leave process scored.
- The risk challenger bot (@aicaravan_bot, while it runs) or any AI assistant.
- Fifteen minutes with your colleague from Session 3.

## Steps

### 1. Classify each step

Duplicate the current-state page in draw.io (right-click the page tab, Duplicate). Colour each step:

| Colour | Category | Test |
|---|---|---|
| Green | Rule-based | You can write the complete rule in one sentence with no "usually" |
| Amber | AI-judged | A trained person decides in seconds by reading, but you cannot list the exceptions |
| Red | Human-only | Someone must be accountable, or the consequence is hard to reverse |

Write one sentence per amber or red step explaining why it is not green. Where you hesitate, choose the more conservative colour. Your Session 3 tags help: REKEY, WAIT and CHASE usually become green, READ and DRAFT amber (or green if a fixed template is enough), JUDGE red.

### 2. Remove before automating

Delete every RUBBER approval and every REKEY step that disappears once two systems are connected. Note what you removed, and why, in a text box on the page. Removing is not automating: a step that adds nothing should not be kept alive by a machine.

### 3. Add the Automation lane

Insert a new lane called **Automation** and write its **owner** on it (the role that answers when it fails). Move the green and amber steps into it, keeping their order. What remains in the human lanes should be red steps and the gate. Keep the same trigger and end state as the current state.

### 4. Build the scoring sheet

In the template, one row per **candidate** (one or more adjacent green or amber steps that would form a single automation):

| Column | What to enter |
|---|---|
| Candidate, Steps included | A short name; the step numbers from your map |
| Minutes saved per run | Touch time removed, **minus** any time a person still spends reviewing |
| Runs per month | How often the process runs |
| Reversibility, Money, People, Legal/data | Each 0 to 3 (table below) |
| Value, Risk total, Quadrant, Mode | Calculated for you |
| Decision, Notes | Your call, and why |

| Question | 0 | 3 |
|---|---|---|
| Reversibility: if it goes wrong, how hard is it to undo? | Internal draft, easily corrected | Sent to a person, paid out, deleted |
| Money: the largest amount involved | None | Above the manager's own approval limit |
| People: job, pay, access or wellbeing | No | Directly and significantly |
| Legal and data: contracts, regulation, personal data | None | Personal data or a regulatory duty |

Risk total 0 to 3: may run fully automatically. 4 to 7: runs, but a person is notified and can undo. 8 to 12: stops at an approval gate every time.

### 5. Score with a colleague

Fill the sheet with the colleague from Session 3. Where you disagree on a risk score, take the higher one and write why in Notes.

### 6. Plot and choose

Sort by quadrant (high value is 4 hours a month or more, high risk is 8 or more):

| | Low risk | High risk |
|---|---|---|
| **High value** | Build first | Build with a gate |
| **Low value** | Batch later | Leave alone |

Pick one **high value, low risk** candidate as your first build. If none exists, pick the highest-value candidate with risk 7 or below and plan its gate.

### 7. Mark the gate and write the ROI

On the future-state map, place the approval gate diamond (in a human lane) immediately **before the first irreversible action** of your chosen candidate. "Yes" continues the automation; "no" returns the item with a reason. If your candidate has no irreversible step, draw a notification point where a person sees what ran and can undo it, and write "no gate: nothing irreversible" as a decision.

In the sheet, add an ROI line as a range with its assumptions:

```
Hours saved per month x loaded hourly cost - monthly tool cost - maintenance (1 hour a month)
Example: 50 to 70 requests x 5 to 7 min = about 4 to 8 hours a month;
at JOD 10 an hour, minus JOD 15 tool and JOD 10 maintenance = about JOD 15 to 60 a month net.
```

### 8. Stress-test

Send your scoring sheet to the **risk challenger bot**, or paste it into your assistant:

```
Here is a scoring sheet of automation candidates for one business process. For each row,
challenge the risk score: name one failure that would make it worse than scored. Then tell me
which single candidate you would build first and why, in under 100 words.

[paste your scoring sheet]
```

Decide for each challenge whether the failure is real in your process. Change the score or write in Notes why not.

## Deliverable

Saved as **M4-future-state**:

- the future-state map (Automation lane with its owner, colours, removed steps noted, the gate);
- the M4-scoring sheet with the ROI range and its assumptions;
- one sentence: "My first build is ..., and its approval rule is ...".

Bring it to Day 3: you build that candidate in n8n.

## On Day 3: n8n

You build your chosen candidate in **n8n** on Day 3. **Do not sign up in advance.** At the start of Day 3 everyone opens the free **14-day n8n Cloud trial** together, in the session, with the instructor: nothing to install. The trial counts from the moment you sign up, so opening it on Day 3 keeps it running for the days that follow. Bring an e-mail address you can open during the session.

## Stuck?

- **"Everything is red."** Look inside each red box: reading, typing, looking up, reminding. The decision is human; the preparation around it rarely is.
- **"Everything is amber."** Apply the one-sentence test again. A plain rule is cheaper and more predictable than a model.
- **"My best candidate scores 9 on risk."** Build the preparation and keep the decision human: the gate goes just before the irreversible step. Or choose a smaller first build.
- **"I do not know the runs per month."** Count the last four weeks and write "about". Order of magnitude is what matters.

## For the instructor: quick rubric

| Check | Pass looks like |
|---|---|
| Classified | Every step coloured; one sentence for each amber and red step |
| Removed | At least one RUBBER or REKEY step removed with a reason, or a reason why none exists |
| Lane | An Automation lane with an owner; trigger and end state unchanged |
| Scored | One row per candidate; review time subtracted; the higher score taken where colleagues disagreed |
| Chosen | One first build that matches the quadrant rule |
| Gate | A diamond before the first irreversible action, both exits labelled, or an explicit "no gate" decision |
| ROI | A range with stated assumptions, not a single number |

Reference: Module 4 online, with the knowledge check scored in the browser:
albanna-tutorials.com/ai-administrator/04_workflow_mapping_future_state.html
