---
title: "Quiz Bank, Session 3: Workflow Mapping I"
subtitle: "AI Administrator · Day 2 · Session 3 · The Current State"
kind: "Instructor quiz bank with answer key"
---

Fifteen multiple-choice questions in the style of the final exam (40 MCQs, 60 minutes). One correct option each. Questions 1 to 5 are the module's own knowledge check; 6 to 15 are additional. The **Outcome** tag names the curriculum "Key Outcomes" bullet each question assesses.

## Questions

**1.** Why should a process be mapped before it is automated?
A. Because automation tools require a diagram file
B. Because automation freezes the process, including any workarounds and exceptions you have not seen
C. To make the project look professional
D. Because mapping replaces the need for testing

**2.** In a swimlane diagram, what does an arrow crossing from one lane to another represent?
A. A decision
B. A loop
C. A hand-off between actors
D. The end of the process

**3.** A process has 25 minutes of touch time and four days of elapsed time. What does this tell you?
A. The people are slow
B. Most of the time is waiting, so notifications and routing will help more than AI steps
C. It needs a full autonomous agent
D. It cannot be automated

**4.** Which pain-point tag marks a step you should protect rather than automate?
A. REKEY
B. CHASE
C. JUDGE
D. RUBBER

**5.** Which interview question is most likely to reveal the real process?
A. How does this process work?
B. What would you improve?
C. Walk me through the last one you handled
D. Do you follow the official procedure?

**6.** What does the "S" in SIPOC stand for?
A. Steps
B. Suppliers
C. Systems
D. Stakeholders

**7.** Why must the trigger of a process be written down before mapping?
A. It is required by the SIPOC template
B. Without a clear trigger an automation has nothing to listen for
C. It shortens the map
D. Triggers are always emails

**8.** How many steps should the "Process" column of a SIPOC usually contain?
A. One
B. Five to seven high-level steps
C. Every keystroke
D. At least twenty

**9.** Why do systems such as the HR portal or a shared spreadsheet get their own swimlane?
A. Systems cannot be drawn as steps
B. Typing into or waiting for a system is a hand-off that exposes REKEY and WAIT steps
C. draw.io requires it
D. To make the diagram wider

**10.** A decision diamond has three exits. What does that usually mean?
A. It is correct as drawn
B. It is probably two decisions and should be split
C. It should become a step
D. It should be removed

**11.** A manager re-types an approved request from an email into the HR portal. Which tag fits best?
A. JUDGE
B. DRAFT
C. REKEY
D. WAIT

**12.** HR approves every request in the portal after the manager has already decided, without reading it. Which tag fits?
A. RUBBER
B. READ
C. CHASE
D. JUDGE

**13.** Which fix matches a large WAIT on an arrow?
A. An AI drafting step
B. Notifications, routing or reminders with escalation
C. A larger language model
D. Hiring more staff

**14.** The official policy forbids private team spreadsheets, but the manager keeps one. What belongs on the current-state map?
A. Only the official steps
B. The spreadsheet, because the map shows what really happens
C. Nothing, because it breaks policy
D. A note to discipline the manager

**15.** An AI reviewer says a step is missing from your map. What should you do next?
A. Add it immediately
B. Ignore it; AI reviewers are unreliable
C. Check it against the policy and the people who do the work, then decide
D. Ask the AI to automate the step

## Answer key

| # | Answer | Why | Outcome |
|---|---|---|---|
| 1 | B | Automation makes a process rigid. Mapping first reveals the exceptions and workarounds that would otherwise be locked in or broken. | Workflow mapping |
| 2 | C | Lanes are actors; crossing lanes is a hand-off, and hand-offs are where waits and lost information accumulate. | Workflow mapping |
| 3 | B | Elapsed time far above touch time means the work queues. Waits are fixed with reminders, routing and escalation, not faster work. | Workflow mapping |
| 4 | C | JUDGE marks a real decision needing accountability. It stays with a person; automation prepares a better summary for them. | Controls and human oversight |
| 5 | C | A specific recent case contains the exceptions and workarounds that a general description leaves out. | Workflow mapping |
| 6 | B | Suppliers, Inputs, Process, Outputs, Customers. Suppliers provide the inputs. | Workflow mapping |
| 7 | B | Automation tools start on an event: an email, a form, a date. A process without a trigger cannot be listened for. | Workflow mapping |
| 8 | B | SIPOC fixes the boundaries; the detail comes later in the swimlane. Five to seven big steps is enough. | Workflow mapping |
| 9 | B | Entering data into a system or waiting for it is a hand-off like any other; showing it exposes REKEY and WAIT. | Workflow mapping |
| 10 | B | A decision is a yes/no question. Three exits usually hide two questions asked in sequence. | Workflow mapping |
| 11 | C | The same data typed into a second system is REKEY; an automation can copy it. | Workflow mapping |
| 12 | A | An approval that is always given without reading is RUBBER: delay that looks like control. | Controls and human oversight |
| 13 | B | Waits are attention problems. Routing and reminders fix them; AI steps fix touch time on reading and writing. | Workflow patterns |
| 14 | B | Map what happens, not what should. The workaround is the real process; leaving it off freezes a fiction. | Workflow mapping |
| 15 | C | An AI reviewer only knows what you pasted. Verify against a trusted source and the people who do the work. | Controls and human oversight |

## Notes for the instructor

- Questions 3, 13 and 14 are the ones participants most often get wrong; they expect AI to be the answer to slowness and expect the map to show the official process.
- For a five-minute in-session check, use questions 1 to 5. For homework, use 6 to 15.
- The online module scores questions 1 to 5 in the browser: albanna-tutorials.com/ai-administrator/03_workflow_mapping_current_state.html
