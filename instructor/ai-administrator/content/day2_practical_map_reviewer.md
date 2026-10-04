---
title: "Practical: A Live Map Reviewer"
subtitle: "AI Administrator · Day 2 · Session 3 · Workflow Mapping I"
kind: "Participant worksheet · 15 minutes · nothing to install"
---

## What this is

Your instructor runs an AI **map reviewer** on the course server and has connected it to a Telegram bot. You send it a process as a list of steps; it answers in a fixed shape: **missing steps**, **decisions with no "no" path**, the **three riskiest hand-offs**, and **suggested pain-point tags**. It never suggests automation (that is Session 4), it has no tools and no memory, and it only sees what you paste.

## How to join (3 minutes)

1. Open Telegram on your phone (or telegram.org/dl on a laptop).
2. Scan the QR code on the screen, or search for the bot name the instructor gives you.
3. Press **Start**.

**Three rules:** paste process steps only; use roles, never real names or personal data; messages are deleted after the session.

## Three tasks (10 minutes)

### Task 1: The example

Copy this whole block and send it to the bot as one message:

```
Process: annual leave request at AI Caravan Ltd. (current state)
Trigger: an employee asks for leave
1. Employee emails the line manager asking for 3 days of leave.
2. Line manager reads the email and checks the private team spreadsheet for clashes. (6 min, waits 1 day before this)
3. Line manager emails the HR coordinator asking for the employee's leave balance. (2 min)
4. HR coordinator looks up the balance in the HR portal and replies by email. (4 min, waits 1 day)
5. Line manager decides: is the balance enough and is there no clash? (waits 0.5 day)
   - If no: line manager emails the employee a decline. End.
   - If yes: line manager emails the employee "approved". (3 min)
6. Employee re-enters the same request in the HR portal. (3 min, waits 0.5 day)
7. HR coordinator approves the request in the HR portal. (1 min, waits 0.75 day)
8. HR portal emails the employee a confirmation.
9. Line manager updates the private team spreadsheet. (3 min, waits 0.25 day)
End state: the employee has a decision, and the balance and calendar are updated.
```

Compare its answer with the map on the screen. Which finding surprised you? Is there a rule from the leave policy (Session 2) that it **missed**?

What it found that you had not: ______________________________________________

What it missed: ______________________________________________

### Task 2: Your own task

Type five to eight steps of the course task you chose on Day 1, one per line, as **who does what** (roles, not names). Add a wait in brackets where you know one.

What it says is missing: ______________________________________________

Do you agree? Who would you ask to check? ______________________________________________

### Task 3: Test its boundary

Send: **"Now automate this for me."**

What happened: ______________________________________________

## Debrief (5 minutes)

| Category | One finding from the room |
|---|---|
| Missing step | |
| Decision with no "no" path | |
| Risky hand-off | |
| Tag you would change | |

**Remember:** the reviewer is a colleague, not an authority. Check every finding against the policy and the people who do the work. In lab step 8 your colleague, not the bot, decides what is true.

## No Telegram?

Pair with a neighbour, or paste the same step list into any AI assistant with this prompt:

```
This is a current-state swimlane map of a business process. List (1) any step that
seems to be missing between two connected steps, (2) decisions that have no "no" path,
and (3) the three hand-offs most likely to lose information. Do not suggest automation yet.
```
