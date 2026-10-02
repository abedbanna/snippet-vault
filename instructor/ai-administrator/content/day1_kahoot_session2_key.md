---
title: "Kahoot: Prompting for Operators"
subtitle: "AI Administrator · Day 1 · Session 2 · 20 questions"
kind: "Instructor answer key for the Kahoot import file"
---

## How to import

1. In Kahoot, choose **Create**, then **Import spreadsheet** (the 'Add question' menu offers 'Import spreadsheet').
2. Upload **Day1_S2_Kahoot.xlsx**. All 20 questions arrive as quiz questions with a 20-second timer.
3. Set the kahoot's cover title and run it in the room at the end of the session, or as a homework challenge.

## Design notes

Written against the "longest answer is right" habit: on every question the four options are within a few characters of each other in length, the correct answer is spread evenly over positions A to D, and no option is "all of the above". Question text under 120 characters, answers under 75, as Kahoot requires.

Correct answers by position A, B, C, D: 5, 4, 6, 5.

## Questions and answers

| # | Question | A | B | C | D | Correct |
|---|---|---|---|---|---|---|
| 1 | A prompt is best thought of as... | A work instruction | A friendly chat | A search query | A password | **A** |
| 2 | Which of these is NOT one of the five parts of a working prompt? | Role | Context | Signature | Constraints | **C** |
| 3 | A prompt gives a different shape of answer every run. Which part is probably missing? | Output format | Role | Greeting | Context | **A** |
| 4 | What is the standard a prompt must meet before it goes inside an automation? | It sounds polite | It is under 50 words | It is written in English | It repeats the same shape | **D** |
| 5 | Which line turns a confident wrong answer into a flag a person can act on? | Be very accurate | If unclear, say unclear | Answer quickly | Use bullet points | **B** |
| 6 | 'Category must be one of: billing, technical, sales, other' is an example of... | A role statement | A few-shot example | Stating allowed values | A greeting | **C** |
| 7 | Few-shot prompting means... | Showing worked examples | Asking several times | Using very short prompts | Splitting across models | **A** |
| 8 | Why do examples work better than descriptions? | Models copy patterns well | Examples are shorter | Models ignore rules | Examples cost less | **A** |
| 9 | How many test inputs does the module ask you to collect for a classifier? | Three | Five | Ten | Fifty | **C** |
| 10 | Two of ten test emails are mislabelled. The right fix is to... | Add 'be more accurate' | Delete the two emails | Add a constraint or example | Use a longer prompt | **C** |
| 11 | After fixing a prompt, what do you re-run? | Only the failed rows | All ten rows | A brand new set | Nothing, it is fixed | **B** |
| 12 | Why keep the ten-row test set after the prompt works? | To prove the work | Models and prompts change | It has no further use | To train the model | **B** |
| 13 | ChatGPT Projects, Claude Projects, Gems and Copilot agents all let you... | Train your own model from scratch | Send emails on your behalf | Run n8n workflows for you | Save instructions with files | **D** |
| 14 | A department assistant built from a Project with documents has which agent parts? | Model, instructions, memory | Model and tools only | Tools and memory only | Instructions only | **A** |
| 15 | 'Data goes where the model goes' is a warning about... | Slow internet connections | Prompts that are too long | Using two models at once | Uploading sensitive documents | **D** |
| 16 | Hallucination is when the model... | Refuses to answer | Answers too slowly | Produces a plausible fact | Repeats the question | **C** |
| 17 | Which is NOT one of the three habits that catch hallucination? | Ground it in a real source | Give it an exit to say no | Check the checkable facts | Ask it to rate its confidence | **D** |
| 18 | 'Summarise this email and tell me what to do' breaks which rule? | Always use a role line | Never mention email | Use a formal tone only | One verb, one deliverable | **D** |
| 19 | Which product and feature pair is correct? | Gems: Microsoft Copilot | Projects: Claude | Custom GPTs: Gemini | Notebooks: ChatGPT | **B** |
| 20 | In the lab, which documents may you upload to your assistant? | Your real HR files | Any internal contract | Public or made-up policies | Colleagues' emails | **C** |
