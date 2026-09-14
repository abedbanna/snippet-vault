# Module 1 reflection

## The prompt I used

Build a single-file index.html "snippet vault": a page where I can save code snippets,
each with a title and a language tag, kept in the browser with localStorage. Show saved
snippets in a list with a search box at the top that filters by title. Plain HTML, CSS
and JavaScript in one file, no build step.

## Failure modes I hit or nearly hit

- **No undo (#2).** I pasted the second version over index.html without reading it.
  If it had broken the list, the working version was gone. Fixed by: version control (Git).
- **Works once (#1).** Nothing checks that saving and searching still work after a change.
  Fixed by: automated tests and CI (Modules 6 and 9).
- **Hallucinated code (#3).** I did not read the 500 lines the assistant wrote.
  Fixed by: reviewing every diff like a pull request (Module 4).

## What would make this app trustworthy enough to ship?

A test that proves save and search work, run automatically on every commit, before
anyone can merge a change.

# Module 2 reflection

## My context file (CLAUDE.md)

Stack: React in web/, NestJS in api/, one repo with two apps. Conventions: TypeScript
everywhere, small focused commits, every feature needs a test. Don'ts: no features I did
not ask for, no hard-coded secrets, no skipped error handling.

## My prompt

Goal: scaffold the snippet vault as a monorepo. Constraints: React front end in web/,
NestJS API in api/, TypeScript. Acceptance: each app starts with one documented command;
no features yet. Out of scope: snippets, search, styling; leave the module 1 files
untouched. First show me the folder plan. Do not write code until I say "go".

## One thing the assistant assumed, and how I steered it

It proposed a root package.json with npm workspaces and root-level `npm run dev:web` /
`npm run dev:api` scripts. I did not ask for that, so before saying "go" I corrected the
plan: two independent apps, no root package.json, no workspaces, and a README with one
start command per app. It also added a GET /health route on its own; I kept it, because
"the app starts" is easier to check with one route than with none.

## How the structured prompt beat "make me a snippet app"

I got exactly two folders, two start commands and no features, instead of a random
framework with choices I never made.
