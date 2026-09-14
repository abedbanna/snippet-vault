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

# Module 3 reflection

## The non-goal I cut to keep M1 tiny

Editing a snippet. It sounds small, but it needs a route, a form state and tests on both
sides, and nothing in M1 depends on it. It is parked under Non-goals and can be promoted
later.

## Where the AI's draft over-scoped, and what I trimmed

The first draft was 139 lines: a "success looks like" paragraph, the exact shape of the
storage file, CORS rules and an "open questions" section. Good thinking, but not a
two-page contract. I asked for the spec to stay under 90 lines with one-line acceptance
criteria, and it came back at 88. I also reversed one of its decisions: delete is back in
the MVP as story S4, because version 1 already had it.

# Module 4 reflection

## My history after M1

```
Add create + list endpoints for snippets (M1)
Add module 3 reflection
Add SPEC: stories, data model, milestones
Add project brief
Add module 2 reflection
Scaffold monorepo (web + api)
Add project context file
Add module 1 reflection
First vibe: snippet vault v1
```

M1 was built on `feature/m1-create-list` and merged into `main` after the diff review.

## One thing the diff review caught that running the app would have hidden

`create` in `snippets.service.ts` stores whatever the request body contains. The tests
pass and the server runs, but a POST with an empty body would happily save a snippet with
every field undefined. The spec parks validation in M5, so nothing changes today, but it
is now written down instead of hidden behind a green test run. I also asked the assistant
why `findAll` reverses a copy instead of `create` using `unshift`: the store stays
append-only so the JSON file version can swap in later. Now I can explain every line.

# Module 5 reflection

## Where I took the wheel, and why

After the search milestone landed, the search box just said "Search". The spec says code
content is not searched, and nothing on the page told the user that. Adding a placeholder,
"title or language", is a five-second edit, so I made it by hand instead of spending a
prompt on it, ran the seven web tests again, and committed it separately from the
assistant's work: "Hint that search matches title or language (hand edit)".

## Acceptance criteria I verified by hand

- S3: typing narrows the list live; matching is case-insensitive ("deb" and "Deb"); it
  matches language too ("css"); clearing restores the full list; nonsense shows
  "No snippets match."
- S1 and S2: saving prepends the snippet and clears the form; the list survives a page
  reload because it comes from the API.
- S4: delete removes the item from the list and from the API.

## One debugging moment worth keeping

The first M2 run had a failing component test. The assistant read the error, named the
root cause (leftover DOM between tests because Testing Library's auto-cleanup needs vitest
globals, which this project does not enable), added an explicit cleanup call, and reran.
Root cause first, then the smallest fix.
