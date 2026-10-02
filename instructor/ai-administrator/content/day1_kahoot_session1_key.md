---
title: "Kahoot: Agents and Automation, Explained"
subtitle: "AI Administrator · Day 1 · Session 1 · 30 questions"
kind: "Instructor answer key for the Kahoot import file"
---

## How to import

1. In Kahoot, choose **Create**, then **Import spreadsheet** (the 'Add question' menu offers 'Import spreadsheet').
2. Upload **Day1_S1_Kahoot.xlsx**. All 30 questions arrive as quiz questions with a 20-second timer.
3. Set the kahoot's cover title and run it in the room at the end of the session, or as a homework challenge.

## Design notes

Written against the "longest answer is right" habit: on every question the four options are within a few characters of each other in length, the correct answer is spread evenly over positions A to D, and no option is "all of the above". Question text under 120 characters, answers under 75, as Kahoot requires.

Correct answers by position A, B, C, D: 7, 8, 6, 9.

## Questions and answers

| # | Question | A | B | C | D | Correct |
|---|---|---|---|---|---|---|
| 1 | Who decides the steps in an automation? | The model, while it runs | The designer, in advance | The person using it | The tool it calls | **B** |
| 2 | Who decides the steps in an agent? | The designer, in advance | The person using it | The model, while it runs | The spreadsheet | **C** |
| 3 | A form submission creates a sheet row and sends a confirmation email. This is... | An automation | An agent | A multi-agent | A chatbot | **A** |
| 4 | 'Find out why this invoice was rejected and prepare a corrected version' is a task for... | A fixed script | A daily report | A form | An agent | **D** |
| 5 | Which is NOT one of the four parts of an agent? | Memory | Tools | Dashboard | Instructions | **C** |
| 6 | Which part of an agent is the system prompt? | Instructions | Memory | Tools | The model | **A** |
| 7 | Which part lets an agent send an email or create a ticket? | Instructions | Memory | The model | Tools | **D** |
| 8 | Which part makes an assistant seem to know your organisation? | Tools | Memory | The model | The loop | **B** |
| 9 | What does a language model actually do? | Predicts the next word | Searches a database | Runs a fixed script | Copies a web page | **A** |
| 10 | In the agent loop, what happens in the 'observe' step? | It writes the goal | It asks a person | It reads the tool result | It picks a model | **C** |
| 11 | What is the correct order of the agent loop? | Act, think, observe | Think, act, observe | Observe, act, stop | Act, stop, think | **B** |
| 12 | The ReAct pattern means... | React to user mood | Reason, then act | Run a fixed script | Reply, then exit | **B** |
| 13 | Why does an agent need an iteration limit? | To run much faster | To use more tools | Each loop costs money | Models tire quickly | **C** |
| 14 | 'Tool quality is answer quality' means... | Buy only the costly tools | Use many tools at once | Tools must be coded first | Agents know only tool output | **D** |
| 15 | Most useful office systems are... | Fully autonomous agents | Workflows with AI steps | Manual checklists | Chatbots only | **B** |
| 16 | Sorting support emails into billing, technical and sales is best built as... | A workflow with AI step | A full autonomous agent | A scheduled report | A manual task | **A** |
| 17 | Compiling a weekly status report from five trackers is best built as... | A full agent task | A manual phone call | A workflow with AI step | A paper form | **C** |
| 18 | Researching three suppliers and preparing a comparison table is best built as... | An agent with tools | A simple automation | A scheduled email | A manual task | **A** |
| 19 | Approving a refund above the policy limit should be... | A full agent task | An automation | An AI step | Kept with a person | **D** |
| 20 | The rule of thumb for choosing a design is... | Most autonomy first | Least autonomy that works | Always use an agent | Never use a model | **B** |
| 21 | Automation reliably removes which kind of work? | Deciding and judging | Approving budgets | Copying and chasing | Hiring new staff | **C** |
| 22 | Decisions about money, people or law should... | Go to the agent | Stay with a person | Be automated | Be skipped | **B** |
| 23 | The context window is... | The model's permanent disk | A tab in the web browser | The list of allowed tools | All the model sees right now | **D** |
| 24 | What fixes a bare model's habit of guessing numbers and live facts? | A longer prompt | A faster model | A friendly tone | Giving it tools | **D** |
| 25 | What fixes a bare model forgetting yesterday's conversation? | Adding memory | A bigger screen | More tools | A new vendor | **A** |
| 26 | How does a model ask for a tool? | It runs the code by itself | It emails the administrator | It cannot ask for anything | It writes a structured request | **D** |
| 27 | Where can a human sit in the agent loop? | Only at the very start | Only at the very end | Nowhere in the loop at all | Before an action or at the end | **D** |
| 28 | An agent that is confused will typically... | Stop with an error | Keep going wrongly | Ask for a budget | Shut itself down | **B** |
| 29 | OpenClaw and Hermes are examples of... | Spreadsheet add-on tools | Email hosting providers | Project tracking boards | Always-on personal agents | **D** |
| 30 | What is the lab deliverable for this session? | A ten-row task inventory | A working n8n flow | A policy document | A slide deck | **A** |
