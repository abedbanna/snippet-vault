---
title: "Quiz Bank, Session 2: Prompting for Operators"
subtitle: "AI Administrator · Day 1 · Session 2 · Prompting for Operators"
kind: "Instructor quiz bank with answer key"
---

Fifteen multiple-choice questions in the style of the final exam (40 MCQs, 60 minutes). One correct option each. Questions 1 to 5 are the module's own knowledge check and appear on the slides; 6 to 15 are additional. The **Outcome** tag names the curriculum "Key Outcomes" bullet each question assesses.

## Questions

**1.** Which of the five prompt parts is most often missing from a prompt that gives a different shape of answer every time?
A. Role
B. Context
C. Output format
D. Task

**2.** What is few-shot prompting?
A. Asking the same question several times
B. Including worked examples of input and expected output inside the prompt
C. Using fewer than ten words
D. Splitting a task across several models

**3.** The best fix for a classifier that mislabels two of ten test emails is to...
A. Add "please be more accurate" to the prompt
B. Add a constraint or an example that covers the failing cases, then re-run all ten
C. Switch to a longer prompt
D. Remove the two awkward emails from the test set

**4.** A department assistant built from a Project with uploaded documents is best described as...
A. A full autonomous agent
B. A model plus instructions plus memory, with no tools
C. An automation
D. A search engine

**5.** Which single instruction most reduces the damage from hallucination?
A. Answer in under 50 words
B. Use a friendly tone
C. If the answer is not in the source, say so instead of guessing
D. Always give three options

**6.** What are the five parts of a working prompt, as taught in this session?
A. Greeting, question, examples, thanks, signature
B. Role, context, task, constraints, output format
C. Model, tools, memory, instructions, output
D. Input, process, output, feedback, review

**7.** Why does a prompt that goes inside an automation need a stricter standard than a prompt in a chat?
A. Automations charge more per word
B. It will run hundreds of times without anyone watching, so it must produce the same shape of answer for every input
C. Automations cannot read English
D. Chat prompts are not allowed to use roles

**8.** "Category must be one of: billing, technical, sales, other." This line is an example of...
A. A role
B. Stating allowed values so the output can be consumed by a spreadsheet or workflow
C. A few-shot example
D. A hallucination

**9.** What is the purpose of keeping the ten-row test set after the prompt works?
A. To prove to management that the work was done
B. To re-run it whenever the prompt or the model changes, so a drop in quality is noticed immediately
C. It has no further use
D. To train the model

**10.** Which statement about uploading documents to an assistant is correct?
A. All products use uploads for training, so never upload anything
B. Consumer tiers may use uploads for training and business tiers usually do not; check the data terms and your organisation's rules first
C. Uploads are always private because they are encrypted
D. Only PDF files are ever safe to upload

**11.** A model produces a confident, fluent answer that cites a policy section that does not exist. The most likely cause is...
A. The model is broken
B. No source was provided, or the source was not searched, so the model produced a plausible fact instead of a real one
C. The prompt was too long
D. The user typed too fast

**12.** Which of the following is NOT one of the three habits that catch hallucination?
A. Ground it: give the model the source and require a quote
B. Give it an exit: allow it to say "not found"
C. Check the checkable: verify names, dates, numbers and clauses
D. Ask the model to rate its own confidence from 1 to 10

**13.** A prompt says "Summarise this email and tell me what to do." Which prompt-writing principle does it break?
A. One verb, one deliverable
B. Use a friendly tone
C. Never use the word "email"
D. Always include examples

**14.** Which product feature pairs correctly with its vendor?
A. Gems: Microsoft Copilot
B. Projects with project knowledge: Claude
C. Custom GPTs: Google Gemini
D. Copilot Notebooks: ChatGPT

**15.** How is the department assistant built today different from the agent built on Day 4 (Module 8)?
A. The Day 4 agent uses a bigger model
B. The department assistant has no tools, so it can only answer; the Day 4 agent adds tools, so it can look things up and take actions
C. The department assistant has no instructions
D. There is no difference

## Answer key

| # | Answer | Why | Outcome |
|---|---|---|---|
| 1 | C | Without an explicit output format the model chooses its own shape each run, which breaks anything downstream. | Automation and agents (agent instructions) |
| 2 | B | Examples inside the prompt show the model the pattern to copy, which is more reliable than describing it. | Automation and agents (agent instructions) |
| 3 | B | Prompts improve through specific constraints and examples, tested against the whole set so nothing that worked breaks. | Responsible operation (output evaluation) |
| 4 | B | Three of the four agent parts are present; without tools it can answer but not act. | Automation and agents |
| 5 | C | An explicit way to say "not found" turns an invented answer into a flag a person can act on. | Responsible operation |
| 6 | B | Role, context, task, constraints, output format. Most weak prompts are missing two of them. | Automation and agents (agent instructions) |
| 7 | B | Repeatability is the standard: the same prompt must return the same shape of answer for every input, unattended. | Workflow patterns |
| 8 | B | Allowed values make the answer machine-readable and stop the model inventing a new category. | Connecting tools and information (data fields) |
| 9 | B | Models and prompts change; the test set becomes the evaluation set used again in Module 12. | Responsible operation (output evaluation, monitoring) |
| 10 | B | Data goes where the model goes; the tier and the organisation's rules decide what may be uploaded. | Responsible operation (privacy, PII) |
| 11 | B | Hallucination is the model producing the most plausible next words when it lacks the fact. | Responsible operation |
| 12 | D | Self-rated confidence is not one of the three habits and is itself often over-confident. | Responsible operation |
| 13 | A | It is two tasks; split into two prompts or two labelled output sections. | Automation and agents (agent instructions) |
| 14 | B | Gems are Gemini; custom GPTs and Projects are ChatGPT; Copilot agents and Notebooks are Microsoft. | Connecting tools and information |
| 15 | B | Adding tools turns an answering assistant into an acting agent, which is why controls come before tools in this course. | Automation and agents |

## Notes for the instructor

- Questions 3, 9 and 12 test the operations habits (test set, re-run everything, three habits) that participants most often skip under time pressure.
- For a five-minute in-session check, use questions 1 to 5 (on the slides). For a homework quiz, use 6 to 15.
- The online module scores the first five questions in the browser: albanna-tutorials.com/ai-administrator/02_prompting_for_operators.html
