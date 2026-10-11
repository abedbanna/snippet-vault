---
title: "Lab 5: Request Intake, Your First Workflow"
subtitle: "AI Administrator · Day 3 · Session 5 · Automation Basics with n8n"
kind: "Participant lab handout"
---

## Objective

Build the classic first automation: a request form whose submissions are logged to a Google Sheet and acknowledged by e-mail, with a branch that flags large requests, a guard for incomplete requests, and retry and error handling. You will reuse these four node types (Form, Google Sheets, IF, Gmail) in every later module.

**Time:** 40 minutes in breakout rooms. Finish at home before Session 6 if needed. **Deliverable:** below.

## What you need

- Your **n8n Cloud** workspace (opened at the start of this session).
- A **Google account** with Sheets and Gmail. The sheet and the n8n connection must use **the same account**.
- **Day3_S5_Requests_Template.xlsx** (optional: you can type the headers yourself).

Words used by today's n8n: **Execute step** runs one node, **Execute workflow** runs the whole workflow once, **Publish** makes it live. Older guides, including the module page, say "Test step" and "Activate"; they mean the same.

## Steps

### 1. Prepare the sheet

In Google Sheets create a sheet called **Requests** with this header row:

| Timestamp | Name | Email | Department | Amount | Description | Status |
|---|---|---|---|---|---|---|

If you upload the template instead, open it and choose **File, Save as Google Sheets**. A green **XLSX** badge next to the name means n8n cannot read it yet.

### 2. Create the workflow and the trigger

In n8n: **Overview, Build a workflow**. Rename it **M5 Request intake** (click the name at the top). Click **Add first step**, choose **On form submission**. Give the form a title and add five fields:

| Field | Type | Required |
|---|---|---|
| Name | Text | yes |
| Email | Email | no |
| Department | Dropdown: Finance, HR, IT, Operations | yes |
| Amount | Number | no |
| Description | Textarea | no |

Leave Email and Amount optional on purpose: step 6 catches requests that leave them blank.

Click **Execute step**, open the **Test URL**, submit one sample request, and read the **output panel**: one item with your five fields.

### 3. Log the row

Add a **Google Sheets** node, operation **Append Row**. Credential: **Sign in with Google**, choose the account that owns your sheet, and **tick every box** on Google's consent screen. Select your spreadsheet and the **Requests** sheet. Map each column by dragging the matching field from the input panel on the left. For **Status** type the fixed value `New`. For **Timestamp** you can drag **submittedAt**. Execute the step and check that a row appears.

### 4. Branch on amount

Add an **IF** node after the Sheets node. Condition: drag **Amount**, choose **Number, is greater than**, value `500`. Test with two submissions, one above and one below 500, and check which output (**true** or **false**) each item leaves by.

### 5. Two confirmation e-mails

On the **true** branch add **Gmail, Send a message**. To: drag **Email**. Subject: `Request received - needs approval`. Email type **Text**, body for example:

```
Hello {Name},
We have received your request for {Amount}. Because it is above 500 it will be
reviewed by a manager before processing. We will confirm within two working days.
Regards,
Operations
```

Replace `{Name}` and `{Amount}` by dragging the fields in. On the **false** branch add a second Gmail node, subject `Request received - being processed`. Use **Sign in with Google** for the Gmail credential.

### 6. Guard against incomplete requests

Insert an **IF** node directly after the form, called **Complete?**, with two conditions joined by **AND**:

- **Email**, String, **is not empty**
- **Amount**, Number, **is greater than** `0`

Connect its **true** output to the Sheets node from step 3. On the **false** output add **Edit Fields (Set)** that sets **Status** to `Incomplete` (keep the other fields), then a second **Google Sheets, Append row** so the incomplete request is still logged. No e-mail leaves from this branch.

**Why "greater than 0" and not "is not empty":** we tested it. When Amount is left blank, the n8n form sends **Amount = 0**, which is not empty. A guard on "not empty" lets it through, logs it as New and sends an e-mail.

### 7. Retry and an error notification

Open each Gmail node, tab **Settings**: switch on **Retry On Fail**, Max. Tries `3`, Wait Between Tries `5000` ms.

Then create a second workflow, **Error notifier**: trigger **Error Trigger**, then **Gmail, Send a message** to yourself with the failed workflow's name and the execution link (drag them from the Error Trigger output). Publish it. Back in **M5 Request intake**: the three-dots menu, **Settings**, **Error workflow**, choose **Error notifier**, save.

### 8. Test end to end, then publish

Click **Execute workflow** before each test (the test URL listens for one submission at a time) and submit three requests:

| Test | Amount | Expected row | Expected e-mail |
|---|---|---|---|
| Complete and small | 200 | Status New | "being processed" |
| Complete and large | 900 | Status New | "needs approval" |
| Amount left blank | (blank) | Status Incomplete | none |

Check the sheet has three rows with the right statuses and that you received two e-mails. Then click **Publish** (top right), copy the form's **Production URL**, and open the **Executions** tab to see your runs.

Finally: the three-dots menu, **Export JSON**. Keep the file.

## Deliverable

Saved as **M5-request-intake**:

1. A screenshot of the published workflow canvas.
2. The production form URL.
3. A screenshot of the Requests sheet showing the three test rows.
4. A screenshot of the Executions list.
5. The exported JSON file.

## If you are stuck

| Symptom | Likely cause |
|---|---|
| "403 Forbidden, the caller does not have permission" in a Sheets node | n8n is connected to a different Google account than the sheet's owner, or a consent box was unticked. Credential, Switch account. |
| The spreadsheet does not appear in the list | Same cause, or the file is an uploaded .xlsx (Save as Google Sheets). |
| "Form Submitted" but nothing in the editor | You did not click Execute workflow (or Execute step) before submitting. |
| 900 goes to the false branch | The IF uses a String operator. Choose Number, is greater than. |
| Publish is greyed out | A node still shows a red triangle: a missing credential or a required field. |
| Two e-mails for one request | Two nodes connected to the same output by mistake. Check the arrows. |

The solution workflow (**Day3_S5_Request_Intake_Solution.json**) is shared after the session. Import it with **Import, From file**, then connect your own Google account in its Sheets and Gmail nodes and paste your sheet link.
