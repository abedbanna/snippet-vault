---
title: "Quiz Bank, Session 5: Automation Basics with n8n"
subtitle: "AI Administrator · Day 3 · Session 5 · Automation Basics with n8n"
kind: "Instructor quiz bank with answer key"
---

Fifteen multiple-choice questions in the style of the final exam (40 MCQs, 60 minutes). One correct option each. Questions 1 to 5 are the module's own knowledge check; 6 to 15 are additional and draw on what was tested live on 11 October 2026. The **Outcome** tag names the curriculum "Key Outcomes" bullet each question assesses.

## Questions

**1.** How many triggers does a workflow have?
A. None
B. Exactly one
C. One per action
D. As many as there are apps

**2.** A schedule trigger fetches 40 rows from a sheet. How many times does the next node run?
A. Once
B. 40 times, once per item
C. Twice
D. It depends on the credential

**3.** What is the single most effective habit for avoiding broken workflows?
A. Naming nodes in capitals
B. Running each node after adding it and reading its output panel
C. Using only Gmail nodes
D. Publishing before testing

**4.** Which credential practice is correct?
A. Paste the API key into a sticky note on the canvas
B. Use your personal login so it is easy to remember
C. Use a service account with the narrowest scope and store it in the credential store
D. Share one credential with everyone by e-mail

**5.** What is the purpose of an error workflow?
A. To stop all workflows when one fails
B. To run automatically when a workflow fails and notify someone with the execution link
C. To delete failed executions
D. To retry the workflow for ever

**6.** In n8n Cloud, what is the difference between the form's Test URL and Production URL?
A. There is none; they are aliases
B. The Test URL listens only after Execute is clicked; the Production URL works after the workflow is published
C. The Test URL is for mobile phones, the Production URL for laptops
D. The Production URL works only for the workspace owner

**7.** A Google Sheets node returns "403 Forbidden, the caller does not have permission". What is the most likely cause?
A. The sheet has too many columns
B. The n8n trial has expired
C. The Google account connected in n8n is not the account that owns the sheet, or a consent box was left unticked
D. The IF node before it compares text instead of numbers

**8.** A participant uploads an .xlsx file to Google Drive and n8n cannot list or read it. What should they do?
A. Rename it to .csv
B. Open it in Google Sheets and choose File, Save as Google Sheets, then use the new copy
C. Make the file public on the web
D. Switch the node to "Append or update"

**9.** A form's Amount field (type Number) is left blank. Testing showed n8n sends Amount = 0. Which guard catches the missing amount?
A. Amount is not empty
B. Amount exists
C. Amount is greater than 0
D. Amount is not equal to null

**10.** An IF node set to "is greater than 500" sends 900 to the false branch. What is the most likely cause?
A. Gmail is rate-limited
B. The condition uses a String operator instead of a Number operator
C. Retry On Fail is switched off
D. The workflow is not published

**11.** In the leave-request demo, which step remains with a person?
A. Looking up the balance
B. Checking the notice period
C. Approving or declining the leave
D. Logging the request in the sheet

**12.** Which statement about the n8n Cloud trial used in this course is correct?
A. It lasts 30 days with unlimited executions
B. It lasts 14 days and includes 1,000 executions; exported JSON lets you continue elsewhere
C. It never expires as long as you log in weekly
D. Test runs do not count as executions

**13.** Retry On Fail is set to Max. Tries 3 and Wait Between Tries 5000 ms. What happens when the Gmail server refuses once and then accepts?
A. The workflow stops immediately
B. Three e-mails are sent
C. n8n waits 5 seconds, tries again, and the run succeeds with one e-mail
D. The error workflow runs first, then the retry

**14.** In n8n 2.43 and later (released October 2026), what happens when you try to publish a workflow with an unconnected required input?
A. It publishes and skips the node
B. Publishing is blocked until the input is connected or filled in
C. The node is deleted automatically
D. The trial counter resets

**15.** Which platform choice reason is specific to n8n compared with Zapier?
A. It has triggers and actions
B. It can be self-hosted, so the data can stay inside the organisation
C. It can send e-mail
D. It works with Google Sheets

## Answer key

| # | Answer | Why | Outcome |
|---|---|---|---|
| 1 | **B** | Every workflow starts with one trigger; a second event needs a second workflow or a different trigger type. | Triggers and actions |
| 2 | **B** | Data flows as items; each following node runs once per item. | Items and data flow |
| 3 | **B** | Most failures are a missing or renamed field a few nodes back; reading each output catches it immediately. | Testing |
| 4 | **C** | Least privilege, a shared or service account, and the credential store; never secrets in fields or notes. | Credentials |
| 5 | **B** | The error workflow turns a silent failure into a notification with the execution link. | Error handling |
| 6 | **B** | The test URL listens for one submission after Execute; the production URL is live once published. | Test then publish |
| 7 | **C** | Seen live while preparing the session: wrong Google account (or unticked consent) gives 403. | Credentials |
| 8 | **B** | The Sheets node reads native Google Sheets only; an uploaded Office file must be saved as a Google Sheet. | Platform basics |
| 9 | **C** | A blank number arrives as 0, which is "not empty"; test greater than 0. | Conditions and guards |
| 10 | **B** | Compared as text, "900" sorts before "500"; use Number, is greater than (or type conversion). | Conditions |
| 11 | **C** | The workflow prepares the decision card; the manager decides (the gate is built on Day 5). | Mapping to the future state |
| 12 | **B** | 14 days, 1,000 executions; export JSON daily so work survives the trial. | Platform basics |
| 13 | **C** | Retry waits and tries again; one successful send means one e-mail. | Error handling |
| 14 | **B** | n8n 2.43.0 release notes: publishing is blocked for workflows with unconnected required inputs. | Test then publish |
| 15 | **B** | Self-hosting is n8n's distinguishing option; the others are common to every platform. | Platform comparison |
