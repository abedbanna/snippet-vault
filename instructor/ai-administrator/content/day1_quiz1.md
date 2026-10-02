---
title: "Quiz Bank, Session 1: Foundations"
subtitle: "AI Administrator · Day 1 · Session 1 · Agents and Automation, Explained"
kind: "Instructor quiz bank with answer key"
---

Fifteen multiple-choice questions in the style of the final exam (40 MCQs, 60 minutes). One correct option each. Questions 1 to 5 are the module's own knowledge check and appear on the slides; 6 to 15 are additional. The **Outcome** tag names the curriculum "Key Outcomes" bullet each question assesses.

## Questions

**1.** Which statement best describes an agent, as opposed to an automation?
A. It runs on a schedule instead of a trigger
B. A language model decides the steps at run time
C. It always sends its output to a human
D. It cannot use external tools

**2.** Which of these is NOT one of the four building blocks of an agent?
A. Model
B. Tools
C. Memory
D. Dashboard

**3.** Sorting support emails into billing, technical and sales is best built as a...
A. Full autonomous agent
B. Workflow with an AI classification step
C. Manual task
D. Scheduled report

**4.** Why does an agent need an iteration limit?
A. To make it run faster
B. Because each loop costs tokens and a confused agent can keep going in the wrong direction
C. So it can use more tools
D. Because models forget after ten steps

**5.** Which task should generally stay with a person rather than be automated?
A. Creating accounts for a new hire
B. Summarising five trackers into a report draft
C. Approving a refund above the policy limit
D. Chasing late timesheets

**6.** A form submission that creates a spreadsheet row and sends a confirmation email is an example of...
A. An agent
B. A workflow with an AI step
C. An automation
D. A multi-agent system

**7.** In the think, act, observe loop, what happens in the "observe" step?
A. The model writes the final answer
B. The tool result is added to the agent's working memory
C. A human approves the next action
D. The instructions are rewritten

**8.** Which part of an agent does an administrator control most directly?
A. The model's training data
B. The instructions (system prompt) and the tools it is allowed to use
C. The size of the context window
D. The vendor's pricing

**9.** The rule of thumb taught in this session is to...
A. Use the most capable agent available for every task
B. Start with the least autonomous design that solves the problem, and add agency only where the path cannot be written in advance
C. Automate every task that takes more than ten minutes
D. Always keep a human in every step

**10.** "Tool quality is answer quality" means that...
A. Expensive tools give better answers
B. An agent only knows what its tools return, so a stale data source produces confident wrong answers
C. Agents should use as many tools as possible
D. Tools must be written in code

**11.** What does the ReAct pattern describe?
A. A model that reacts to user emotions
B. A loop in which the model reasons about the next step, takes an action, reads the result and reasons again
C. A fixed sequence of three tools
D. A method for training models faster

**12.** Compared with a full agent, a workflow with AI steps typically offers...
A. Less predictability and higher cost
B. Most of the benefit with most of the predictability, because the path is fixed and only one or two steps call a model
C. No use of a language model
D. Fully autonomous decision making

**13.** Which limitation of a bare language model is fixed by giving it tools?
A. It cannot write fluent text
B. It guesses at facts, numbers and live data instead of looking them up
C. It is too slow
D. It cannot follow instructions

**14.** Which limitation of a bare language model is fixed by giving it memory?
A. It forgets previous sessions and knows nothing of your organisation's documents
B. It cannot be shared with colleagues
C. It produces text one word at a time
D. It needs an internet connection

**15.** Where can a human be placed in an agent's loop? Choose the most complete answer.
A. Only at the very end, to read the final answer
B. Only at the start, to write the goal
C. Approving a tool call before it runs, reviewing the final answer, or being escalated to when the agent is unsure
D. Nowhere; agents are designed to run without people

## Answer key

| # | Answer | Why | Outcome |
|---|---|---|---|
| 1 | B | In an automation every step is fixed in advance; in an agent the model chooses which tool to use next and when to stop. | Automation and agents |
| 2 | D | The four parts are model, tools, memory and instructions. A dashboard is a way to monitor, not a part of the agent. | Automation and agents |
| 3 | B | The path is fixed (read, classify, route) and only one step needs a model: the workflow-with-AI-step pattern. | Workflow patterns |
| 4 | B | Without a limit a stuck agent burns money and may take more actions than intended. The limit is a basic control. | Controls and human oversight |
| 5 | C | Automation removes copying and chasing. Decisions involving money, people or legal exposure need human accountability. | Controls and human oversight |
| 6 | C | Every step was written in advance by the designer; no model decides anything. | Automation and agents |
| 7 | B | Think decides, act calls one tool, observe adds the result to working memory, then the loop repeats. | Automation and agents |
| 8 | B | Administrators rarely change the model; they write the instructions and decide which tools are permitted. | Automation and agents |
| 9 | B | Least autonomy that works; agency only where the path genuinely cannot be written down. | Workflow patterns |
| 10 | B | The agent's answers are only as good as what its tools return; fix the data source before blaming the model. | Connecting tools and information |
| 11 | B | ReAct = reason, then act, then observe, repeated until a final answer or a limit. | Automation and agents |
| 12 | B | A fixed automation with one or two model calls keeps predictability while adding reading and writing ability. | Workflow patterns |
| 13 | B | Next-word prediction is poor at arithmetic and live look-ups; tools (calculator, database, search) fix that. | Connecting tools and information |
| 14 | A | Memory, including a knowledge base of documents, is what lets an assistant know your organisation across sessions. | Automation and agents |
| 15 | C | A human can sit before a risky action, after the final answer, or as the escalation path when the agent is unsure. | Controls and human oversight |

## Notes for the instructor

- Questions 4, 5, 9 and 15 are the ones most often answered wrongly by participants who have seen impressive agent demos; use them for discussion.
- For a five-minute in-session check, use questions 1 to 5 (on the slides). For a homework quiz, use 6 to 15.
- The online module scores the first five questions in the browser: albanna-tutorials.com/ai-administrator/01_agents_and_automation.html
