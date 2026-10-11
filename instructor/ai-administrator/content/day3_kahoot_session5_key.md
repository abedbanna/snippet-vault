---
title: "Kahoot: Automation Basics with n8n"
subtitle: "AI Administrator · Day 3 · Session 5 · 20 questions"
kind: "Instructor answer key for the Kahoot import file"
---

## How to import

1. In Kahoot, choose **Create**, then **Import spreadsheet** (the 'Add question' menu offers 'Import spreadsheet').
2. Upload **Day3_S5_Kahoot.xlsx**. All 20 questions arrive as quiz questions with a 20-second timer.
3. Set the kahoot's cover title and run it in the room at the end of the session, or as a homework challenge.

## Design notes

Written against the "longest answer is right" habit: on every question the four options are within a few characters of each other in length, the correct answer is spread evenly over positions A to D, and no option is "all of the above". Question text under 120 characters, answers under 75, as Kahoot requires.

Correct answers by position A, B, C, D: 5, 5, 5, 5.

## Questions and answers

| # | Question | A | B | C | D | Correct |
|---|---|---|---|---|---|---|
| 1 | How many triggers does one n8n workflow have? | Exactly one | None at all | One per node | One per app | **A** |
| 2 | A sheet node returns 40 rows. How often does the next Gmail node run? | Once | 40 times | Twice | Never | **B** |
| 3 | In n8n, one form submission arrives as... | Forty items | A sheet row | One item | An e-mail | **C** |
| 4 | Which node is the start event of the leave request demo? | Gmail: Send | IF node | Code node | Form Trigger | **D** |
| 5 | What does the n8n Cloud trial give you? | 14 days, 1,000 runs | 30 days, unlimited | 7 days, 100 runs | 1 year, 10,000 runs | **A** |
| 6 | At the end of every session you should... | Delete the workflow | Export the JSON | Change your password | Unpublish everything | **B** |
| 7 | What does a red triangle on a node usually mean? | It ran successfully | It is an AI step | Something to fill in | It is published | **C** |
| 8 | The test form URL works... | Forever | Only after Publish | For everyone | After you click Execute | **D** |
| 9 | Which URL do real users get after you publish? | The production URL | The test URL | The editor URL | The webhook log URL | **A** |
| 10 | Sheets node error '403, the caller does not have permission'. Most likely cause? | The sheet is empty | Wrong Google account | Too many columns | The IF node is wrong | **B** |
| 11 | Your sheet shows a green XLSX badge. Before n8n can read it you... | Rename the file | Share it publicly | Save as Google Sheets | Delete the header row | **C** |
| 12 | Where should a Google password or API key live? | In a sticky note | In the node's text | In the e-mail body | In the credential store | **D** |
| 13 | A blank Number field on an n8n form arrives as... | 0 | an error | the word null | the text 'empty' | **A** |
| 14 | So the guard for a missing amount should test... | Amount is not empty | Amount is greater than 0 | Amount exists | Amount equals null | **B** |
| 15 | The IF says 900 is not greater than 500. What is wrong? | Gmail is offline | The trial expired | It compares as text | The sheet is full | **C** |
| 16 | Retry On Fail with 3 tries and 5000 ms means... | Three e-mails sent | Wait 3 seconds once | Run 5,000 times | Up to 3 tries, 5 s apart | **D** |
| 17 | What does an error workflow do? | Alerts you on failure | Deletes failed runs | Retries for ever | Stops all workflows | **A** |
| 18 | Where do you see every past run, with its data? | The Templates page | The Executions tab | The Admin Panel | The trial banner | **B** |
| 19 | In the leave demo, who approves or declines the leave? | The IF node | The HR coordinator | The line manager | The Code node | **C** |
| 20 | Which Session 4 step stays human in the demo workflow? | Look up the balance | Log the request | E-mail the card | The manager's decision | **D** |
