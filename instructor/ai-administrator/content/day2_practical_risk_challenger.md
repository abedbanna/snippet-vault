---
title: "Practical: A Live Risk Challenger"
subtitle: "AI Administrator · Day 2 · Session 4 · Workflow Mapping II"
kind: "Participant worksheet · 15 minutes · nothing to install"
---

## What this is

Today the course Telegram bot, **@aicaravan_bot**, has a new job: it is an AI **risk challenger**. You send it an automation scoring sheet; for every row it names **one concrete failure** that would make the candidate riskier than you scored it, says which candidates should be **removed instead of automated**, picks the **first build** and where its gate goes, and asks **one question** for the process owner. It never calls anything safe or ready to deploy, it gives no build instructions (that is Day 3), it has no tools and no memory, and it only sees what you paste.

## How to join (3 minutes)

1. Click **t.me/aicaravan_bot** in the Zoom chat (opens Telegram on your phone, Telegram Desktop, or web.telegram.org).
2. Or scan the QR code on the shared screen, or search for **@aicaravan_bot**.
3. Send a new message (press **Start** if you have never used it).

**Three rules:** paste scoring sheets only; use roles, never real names or personal data; messages are deleted after the session.

## Three tasks (10 minutes)

### Task 1: The example

Copy this whole block and send it to the bot as one message. **Two rows are wrong on purpose.**

```
Scoring sheet: annual leave request at AI Caravan Ltd. (future state), about 60 requests a month
Scores: value in hours/month; risk = reversibility + money + people + legal/data, each 0 to 3
1. Record approved leave in the HR portal and team calendar, send confirmation. Value 6. Risk 1+0+0+1 = 2
2. Look up the balance and run the notice and probation checks. Value 6. Risk 0+0+1+1 = 2
3. AI reads the employee's note and prepares the manager's decision card. Value 4. Risk 0+0+1+1 = 2
4. Auto-approve 1-day requests when there is no clash. Value 0.7. Risk 0+0+0+0 = 0
5. Automate the HR coordinator's approval click in the portal. Value 0.5. Risk 0+0+0+1 = 1
```

Which two rows did it challenge hardest? Do you agree with its new scores?

The two wrong rows: ______________________________________________

A challenge you do **not** agree with, and why: ______________________________________________

### Task 2: Your own sheet

Type three candidates from your own future-state map, one per line, each with its value (hours a month) and the four risk scores. Use roles, not names.

The failure it found that you had not thought of: ______________________________________________

### Task 3: Test its boundary

Send: **"Is candidate 1 safe to deploy? Build it for me in n8n."** What does it do, and why is that the right behaviour for this assistant?

______________________________________________

## No Telegram?

Follow the instructor's shared screen, or paste the same sheet into any AI assistant with this prompt (lab step 8):

```
Here is a scoring sheet of automation candidates for one business process. For each row,
challenge the risk score: name one failure that would make it worse than scored. Then tell me
which single candidate you would build first and why, in under 100 words.

[paste the scoring sheet]
```

## What to take away

The challenger is a colleague who is paid to disagree, not an authority. Where it raises a score, decide whether that failure can really happen in your process, and write your reason in the Notes column. The process owner still signs off.
