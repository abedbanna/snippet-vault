# albanna-tutorials.com — portal workspace

Source of truth for https://albanna-tutorials.com. `src/` is the site exactly as authored; `tools/build.py`
produces `dist/`, which is what gets deployed. Never edit `dist/` by hand.

```
site.json            site name, URL, author, social links, brand colours   (edit to change footer/about details)
courses.json         catalogue: every course/tutorial with description, level, tags, language, module rules
src/                 the pages (courses, tutorials, images) + portal pages + assets/
  assets/portal.css  global bar / breadcrumbs / footer / progress styling
  assets/portal.js   menu, progress tracking (localStorage), feedback events, fixed-navbar offset
tools/build.py       src -> dist: injects head meta (canonical, OG, JSON-LD, favicon, hreflang), portal bar,
                     breadcrumbs, footer; writes sitemap.xml, robots.txt, search-index.json, module-counts.json
tools/portal_lib.py  the injection logic (idempotent via <!-- ab:head/bar/footer --> markers)
tools/gen_pages.py   regenerates about/contact/privacy/terms/404/courses/search/certificate into src/
tools/gen_icons.py   favicon set, manifest, og-default.png from src/images/logo.png
tools/patch_home.py  one-off homepage fixes (already applied; idempotent)
templates/           module-template.html — skeleton for new course modules
deploy/              zz-albanna-portal.conf (Apache: www->apex, gzip, caching, security headers, 404) + deploy.sh
live/                (git-ignored) HTTP mirror of production taken 2026-09-02 — reference only
```

## Everyday workflow
1. Add or edit pages under `src/` (new module: copy `templates/module-template.html`, match the course's own CSS).
2. New course or tutorial: add an entry to `courses.json` (title, path, description, level, tags, languages).
3. `python3 tools/gen_pages.py && python3 tools/build.py`
4. Preview: `cd dist && python3 -m http.server 8765` → http://127.0.0.1:8765/
5. Commit. Deploy with `deploy/deploy.sh --dry-run`, then `deploy/deploy.sh` (backs up the server docroot first).

## Progress / certificates
Progress lives in the learner's browser (`localStorage["ab-progress"]`). A course's module list is every
top-level `*.html` in its folder except `index.html` (override with `modules_dir` / `modules_exclude` in courses.json).
Certificates unlock when all modules are marked complete: `/certificate.html?course=<id>`.
