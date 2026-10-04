---
title: "Leave Request: Current-State Step List"
subtitle: "AI Administrator · Day 2 · Session 3 · worked example (fictional AI Caravan Ltd.)"
kind: "Paste-ready step list for the map reviewer and the live demo"
---

## The step list (copy everything in the box)

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

## What a good review finds (check against policy HR-POL-02)

| Category | Finding | Source in the policy |
|---|---|---|
| Missing step | Department-head approval for leave in the last two weeks of a quarter | Section 3, last paragraph |
| Missing step | Escalation to the HR coordinator when the manager has not answered after three working days | Section 3 |
| Missing step | Notice-period check: 2 working days for 1–2 days of leave, 10 working days for 3 or more | Section 3 |
| Missing step | Probation check for employees in their first three months | Section 2 |
| Decision without a "no" path | Step 7: HR's portal approval has no decline or "send back" path | (process design) |
| Risky hand-off | Step 3 to 4: balance requested and answered by email, outside the system of record | Section 7: the HR portal is the single record |
| Risky hand-off | Step 5 to 6: the approved details are re-typed by the employee and can differ from what was approved | (process design) |
| Risky hand-off | Step 8 to 9: the private spreadsheet is updated by hand and can drift from the portal | Section 7: no separate spreadsheets |
| Tags | REKEY (4, 6, 9), WAIT (before 2), READ (2), CHASE (3), DRAFT (5 reply), RUBBER (7), JUDGE (5 decision) | Session 3 tag vocabulary |

Totals: touch time 25 minutes; elapsed time about 4 working days; eight hand-offs.
