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

# Module 6 reflection

## Which test caught the deliberate bug

After validation was green, I reintroduced the failure mode on purpose: I made `create`
accept an empty title again. Two tests went red immediately, "POST /snippets returns 400
and saves nothing when title is ''" and the whitespace-only variant. That is the proof the
test is real: it fails for the right reason. Reverting the one-line change turned them
green again.

## Did any AI-written test turn out to assert nothing?

No test was empty, but I checked each one for a real assertion, because a test that only
does `.expect(201)` without checking the body would pass even if the API returned the
wrong snippet. The create test also asserts the returned id matches a UUID v4 pattern and
the body matches the input, and the list test asserts the exact newest-first order, not
just the length. The six validation tests were red before the guard existed, which is the
strongest evidence they test something.

## The TDD moment

Writing the blank-field tests first, watching six go red, then implementing the smallest
guard until they went green, was test-driven development with the assistant: the failing
tests were a target it could not wander away from.

# Module 7 reflection

## The gate, and the first thing it refused

`npm run gate` in `api/` runs lint, the Prettier check, the unit tests and the e2e tests,
and a pre-commit hook runs it before every commit. To prove it bites I swapped the quotes
in the controller and tried to commit: the hook stopped at the format check and refused
the commit. `npm run format` put the quotes back and there was nothing left to commit. The
gate also caught the assistant itself: in the validation step it wrapped one line that
Prettier wanted on a single line, the gate went red, and it had to fix its own formatting.

## Where a secret or unvalidated input was hiding

There was no secret, but there was an open door: the API had no CORS policy and a
hard-coded port. Both now come from `api/.env` (gitignored) through `config.ts`; the
committed `api/.env.example` documents the shape, and `CORS_ORIGIN='*'` is rejected at
startup. On input, `POST /snippets` accepted a title of any length. Three tests went red
first, then `requireText` gained a limit: 200 for title, 40 for language, 20000 for code.

## The dependency scan

`npm audit` reported nine vulnerabilities. Five were in `undici`, pulled in only by
`@nestjs/mau`, a deploy CLI the project never uses, so the fix was `npm uninstall`. The
remaining four are in `multer`, which Nest's Express adapter depends on for file uploads.
This API accepts no uploads, `npm audit fix` cannot change it without a breaking Nest
upgrade, so it is recorded here as an accepted risk to re-check after the next Nest release.

# Module 8 reflection

## What my machine used to provide, and the container now provides

Until this module the vault ran because this laptop had Node 24, npm, the Vite dev server
with its `/snippets` proxy, and a shell with `PORT` and `CORS_ORIGIN` exported. All of that
is now inside the images: `api/Dockerfile` ships Node 22 with the compiled `dist/` and the
production `node_modules` only, running as the `node` user; `web/Dockerfile` builds the Vite
bundle and hands it to nginx, whose `nginx.conf` proxies `/snippets` to the `api` service.
`docker compose up --build` starts both, and `docker compose exec api node --version` answers
22 while the host says 24: the runtime is the container's business now, not the machine's.

## What the first build taught me

The API image failed to build the first time: `node:22-alpine` ships npm 10, which rejects
this project's lock file (a transitive dev dependency declares a TypeScript 5 peer while the
project is on 6). The assistant read the error, found the cause in `package-lock.json`, pinned
npm 11 inside the build stage, and the build passed. Containers make "works on my machine"
visible: the image had a different npm than my laptop, and the difference surfaced at once.

## No secrets in the images

Both `.dockerignore` files exclude `node_modules`, `dist`, `.git` and `.env`. Configuration
reaches the API at run time through `env_file: api/.env` in `docker-compose.yml`; `ls -a` inside
the running container shows `dist`, `node_modules` and `package.json` and no `.env` at all.

# Module 9 reflection

## What CI caught that I might have merged locally

The pipeline runs the module 7 gate on GitHub's clean runner for every push to `main` and
every pull request, then builds both Docker images. To prove it, I opened a pull request with
a "simplification" in the snippets service that dropped the copy-and-reverse in `list()`. The
local pre-commit hook refused it, but a hook lives in one clone: I committed with
`--no-verify`, exactly as a teammate without the hook would. CI went red on the newest-first
test, and branch protection refused `gh pr merge`: "the base branch policy prohibits the
merge". Restoring the line turned the checks green and the merge went through. The gate on my
laptop is a convenience; the gate in CI is the one nobody can skip.

## One thing worth knowing

`node:22` and GitHub's Node 22 both ship npm 10, which rejects this repo's lock file, so the
`api` job installs npm 11 before `npm ci`, mirroring the Dockerfile. CI ran on a machine that
is not mine, and it passed: "works on my machine" is now "works on the runner".
