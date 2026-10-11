---
title: "Leave-Request Demo: Setup and Run Sheet"
subtitle: "AI Administrator · Day 3 · Session 5 · Automation Basics with n8n"
kind: "Instructor setup sheet · tested 11 October 2026"
---

## What you are running

The Session 4 first build as a real n8n workflow: **S5 Demo - Leave request** (`workflows/Day3_S5_Leave_Request_Demo.json`, 8 nodes and a sticky note). A leave form feeds a balance lookup in Google Sheets, a policy check (fictional policy HR-POL-02: 1 to 2 days need 2 working days' notice, 3 or more need 10; Friday and Saturday are the weekend; the last two weeks of a quarter also need the department head), and an IF. Requests that pass are logged as **Pending manager** and a decision card is e-mailed to the manager; requests that fail are logged as **Flagged for HR** with the reason, and HR is e-mailed. Nothing is approved or declined automatically.

No bot, no server and no API keys this session. Everything runs in your own n8n Cloud trial.

## Once, a few days before Session 5

### 1. Open your n8n trial

Sign up at n8n.io/pricing, **Start free trial** (n8n Cloud, no credit card). Open it **no more than a few days before** the session: the trial lasts 14 days and must still be active on the last n8n day of the course. Note your workspace address (`yourname.app.n8n.cloud`).

### 2. Make the Google Sheet

1. Upload `Day3_S5_Leave_Demo_Sheet.xlsx` to Google Drive and open it in Google Sheets.
2. **File, Save as Google Sheets.** The uploaded copy has a green **XLSX** badge; n8n cannot read it (you get "403" or an empty list). Use the new native copy and note its link.
3. Do this in **the Google account you will connect in n8n**. In our test the sheet was first created in a different account and n8n returned *403 Forbidden, the caller does not have permission*.
4. Tab **Balances**: the four fictional employees (Lina Haddad has 2 days left, Omar Khalil 21, Sara Nasser 15). Tab **Requests**: headers only.

### 3. Import the workflow

In n8n: **Overview, Build a workflow**, then the three-dots menu next to the name, **Import, From file**, choose `Day3_S5_Leave_Request_Demo.json`. The workflow renames itself **S5 Demo - Leave request**. Red triangles on the Sheets and Gmail nodes are expected: no credentials yet.

### 4. Connect Google

1. Open **Look up balance**, Credential, **Sign in with Google**. On Google's consent screen choose the account that owns the sheet and **tick every box**. n8n names it "Google Sheets account".
2. Open **Flag to HR**, Credential, **Sign in with Google** again for Gmail ("Gmail account").
3. The other Sheets and Gmail nodes pick up the same credentials. If not, choose them from the Credential list.

### 5. Point the nodes at your sheet

1. In **Look up balance**: Document **By URL**, paste the sheet link; Sheet **From list**, choose **Balances** (if the list loads, access is right); Filters, **Add Filter**, Column **Email**, Value `{{ $json['Work email'] }}` in **Expression** mode (the toggle above the field; in Fixed mode it is matched as plain text).
2. In **Log request** and **Log flagged request**: the same link, Sheet **Requests**. The column mapping is already set.
3. In **Flag to HR**: change To from `hr@example.com` to your own address for the demo.

Changing the document resets the sheet and filter fields, so do it in this order: document, sheet, filter.

### 6. Test three times

Click **Execute workflow** (bottom centre), open the form's **Test URL** (in the form node, Form URLs) and submit:

| Test | Full name | Work email | Manager email | Type | First day | Last day | Expected |
|---|---|---|---|---|---|---|---|
| 1 | Omar Khalil | omar.khalil@aicaravan.example | your address | Annual leave | 15 Nov | 17 Nov | Pending manager; decision card in your inbox |
| 2 | Sara Nasser | sara.nasser@aicaravan.example | your address | Annual leave | the day after tomorrow | same day | Flagged for HR: 1 working day notice, policy needs 2 |
| 3 | Lina Haddad | lina.haddad@aicaravan.example | your address | Annual leave | 15 Nov | 17 Nov | Flagged for HR: asks for 3 days but only 2 remain |

Click **Execute workflow** again before each submission: the test URL listens for one submission only. Check the **Requests** tab (Reason and Status columns) and the **Executions** tab (three green runs).

### 7. Reset

Delete the three test rows from **Requests** so the sheet is empty for the live demo. Keep the Executions; they are useful if the live run fails.

## On the day

- Open the editor in its own browser window, zoomed to 125%, and the sheet in a second tab on **Requests**.
- Run test 1 live, then 2 and 3 if time allows (minute 35 to 55 in the deck).
- If Google fails live: show the **Executions** tab from your preparation runs and the screenshots in the deck. Keep the timing.

## After the session

- Export the workflow (menu, **Export JSON**) and keep it with this package.
- Share `Day3_S5_Request_Intake_Solution.json` (the lab solution) in the chat or by e-mail. Participants import it with Import, From file and connect their own Google account.

## What was verified on 11 October 2026

On n8n Cloud (trial, "Publish" editor): import from file, the form test URL, Google Sheets Get row(s) with a filter, the Code node, IF, Sheets Append row and Gmail Send on both branches; the three tests above produced the expected rows and e-mails. The lab solution produced *New*, *New* and *Incomplete* for amounts 200, 900 and blank, after one correction: **an empty number field arrives as 0**, so the guard must test *Amount is greater than 0*, not *is not empty*.
