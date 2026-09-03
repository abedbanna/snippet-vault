# Page conversion brief — Al-banna Tutorials design system

Goal: re-skin the assigned page(s) so they look exactly like the Deep Learning course pages, WITHOUT changing any content.

Read first (do not modify): `src/deep_learning/06_backpropagation.html` (structure reference) and `src/assets/theme.css` (every class you may use). Originals are in `live/<same path>`; write your result to `src/<same path>` (overwrite).

## Head
Keep: the Google tag snippet, charset, viewport, `<title>`, meta description (add one ≤155 chars if missing), `<html lang="..">` and `dir="rtl"` on Arabic pages.
Use exactly these resources (nothing else — no Bootstrap, no Tailwind, no old CSS files):
```
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">   (Arabic pages: add &family=Tajawal:wght@400;500;700)
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link rel="stylesheet" href="/assets/theme.css">
<style>:root{--primary:#HEX;--primary-hover:#HEX;--glow:rgba(R,G,B,.14)} /* + only page-specific CSS */</style>
```
Keep MathJax/KaTeX/Prism/Chart.js includes if the page uses them. Do NOT add favicon, canonical, OG, JSON-LD, or any site-wide bar/footer — the build injects those.

## Body skeleton
```
<nav class="navbar"><div class="nav-inner">
  <a class="nav-logo" href="#"><i class="fas fa-ICON"></i> Short Title</a>
  <div class="nav-links"><a href="#sec1">Section</a> … (max ~7; keep any English/عربي toggle link here too)</div>
  <div style="display:flex;gap:8px;align-items:center"><button class="theme-toggle" aria-label="Toggle theme"><i class="fas fa-sun"></i></button><button class="hamburger" aria-label="Menu"><i class="fas fa-bars"></i></button></div>
</div></nav>
<div class="mobile-menu"> same links </div>
<section class="hero"><div class="hero-content"><h1>Page title</h1><p class="hero-sub">subtitle</p><span class="diff-badge">Level</span> <span class="cat-badge"><i class="fas fa-clock"></i> ~N min</span></div></section>
<div class="container">
  <div class="section fade-up" id="sec1"><h2 class="section-title"><i class="fas fa-ICON"></i> Heading</h2> … </div>
  …
  <div class="page-nav"><a class="nav-btn prev" href="/">← Home</a><a class="nav-btn next" href="/courses.html">All courses →</a></div>
</div>
<footer class="footer"><div class="footer-bottom">© Al-banna Tutorials · Dr. Abedal-Kareem Al-Banna</div></footer>
<button class="scroll-top" aria-label="Back to top"><i class="fas fa-arrow-up"></i></button>
<script src="/assets/theme.js"></script>   ← last thing in <body>, no defer
```
Mapping: callouts/notes/tips → `.info-box` (`.warning`, `.success`, `.danger`); code → `<div class="code-block"><button class="copy-btn">Copy</button>CODE</div>` or `<pre><code>`; tables → `<div class="table-wrap"><table class="dark-table">`; numbered procedures → `.step` / `.step-num` / `.step-body`; buttons → `.btn.btn-primary` / `.btn.btn-outline`; sub-headings → `.subsection h3`; cards/grids → `.grid` + `.card`; collapsible answers → `<details class="solution"><summary>…</summary><div>…</div></details>`; badges → `.tag`. Drop all framework utility classes; write small page-specific CSS for anything with no equivalent. Keep in-page `id`s that anchors point to.

## Content rules (strict)
Every heading, paragraph, list item, code line, image (same src), link href, table cell, question, answer, explanation, iframe and figure must survive verbatim — no summarising, rewording, reordering or trimming. Keep functional JavaScript (quizzes, timers, scoring, tabs, progress, copy) working: adapt selectors/classes to the new markup, remove only old nav/theme/framework code.

## Verify before you finish (mandatory)
1. `python3 tools/check_convert.py <relative path>` — must report missing ≈ 0 (only old nav/footer boilerplate may be missing). Fix until it passes.
2. Syntax-check inline scripts (extract to a temp file and `node --check`).
3. Serve and screenshot: `cd ~/albanna-portal/src && python3 -m http.server PORT --bind 127.0.0.1 &` then
   `perl -e 'alarm 40; exec @ARGV' "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --no-first-run --user-data-dir=/tmp/prof_PORT_$RANDOM --virtual-time-budget=4000 --window-size=1366,1400 --screenshot=/tmp/shot_PORT.png http://127.0.0.1:PORT/<path>`
   View the PNG (Read tool), fix layout problems (unreadable text, light-on-light, overflow, broken quiz UI), re-shoot. Kill your server when done.
Report: files written, check_convert results, screenshot verdict, anything you could not preserve.
