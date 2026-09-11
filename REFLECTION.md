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
