"""Generate the portal's own pages into src/ using the shared design system (assets/theme.css):
home (index.html), courses, search, about, contact, privacy, terms, 404, certificate, exam, quantum-courses, vibe-coding-courses."""
import os, sys, json, html as H
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import portal_lib as P
SRC=os.path.join(P.ROOT,'src'); S=P.SITE; A=S['author']; esc=lambda s:H.escape(str(s),quote=True)
# Self-hosted fonts + Font Awesome (no third-party origins on the render path).
FONTS='<link rel="preload" href="/assets/fonts/inter-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n    <link rel="preload" href="/assets/fonts/inter-600-latin.woff2" as="font" type="font/woff2" crossorigin>\n    <link rel="stylesheet" href="/assets/fonts.css">'
FA='<link rel="stylesheet" href="/assets/fa/all.min.css">'
GA=f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={S['ga4_id']}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{S['ga4_id']}');</script>"""
ACCENT=':root{--primary:#6366f1;--primary-hover:#818cf8;--glow:rgba(99,102,241,.14)}'
SITE_NAV=[('/courses.html','Courses'),('/roadmaps/','Roadmaps'),('/exam.html','Exams'),('/about.html','About'),('/contact.html','Contact')]
MODS={c['id']:len(P.course_modules(SRC,c)) for c in P.COURSES}
live=[c for c in P.COURSES if c.get('status')!='coming-soon']
N_COURSES=len([c for c in live if c['type']=='course']); N_TUT=len([c for c in live if c['type']=='tutorial'])
N_PAGES=sum(1 for dp,dn,fn in os.walk(SRC) for f in fn if f.endswith('.html'))

def navbar(logo_icon,logo_text,links,extra=''):
    li=''.join(f'<a href="{esc(h)}">{esc(t)}</a>' for h,t in links)
    return f"""<nav class="navbar"><div class="nav-inner">
  <a class="nav-logo" href="/"><i class="fas {logo_icon}"></i> {esc(logo_text)}</a>
  <div class="nav-links">{li}{extra}</div>
  <div style="display:flex;gap:8px;align-items:center"><button class="theme-toggle" aria-label="Toggle light/dark theme"><i class="fas fa-sun"></i></button><button class="hamburger" aria-label="Menu"><i class="fas fa-bars"></i></button></div>
</div></nav>
<div class="mobile-menu">{li}</div>"""
def hero(h1,sub,extra=''):
    return f'<section class="hero"><div class="hero-content"><h1>{h1}</h1><p class="hero-sub">{sub}</p>{extra}</div></section>'
def page(fn,title,desc,body,accent=ACCENT,extra_head='',extra_js='',noindex=False,lang='en'):
    doc=f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
{GA}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}">
    {'<meta name="robots" content="noindex,follow">' if noindex else ''}
    {FONTS}
    {FA}
    <link rel="stylesheet" href="/assets/theme.css">
    <style>{accent}{extra_head}</style>
</head>
<body>
{body}
<footer class="footer"><div class="footer-bottom">© <span class="ab-year">2026</span> {esc(S['name'])} · <a href="{A['profile']}">{esc(A['name'])}</a></div></footer>
<button class="scroll-top" aria-label="Back to top"><i class="fas fa-arrow-up"></i></button>
<script src="/assets/theme.js"></script>
{extra_js}
</body>
</html>
"""
    open(os.path.join(SRC,fn),'w',encoding='utf-8').write(doc); print(' wrote',fn)

def lang_tags(c): return ''.join(f'<span class="tag">{"عربي" if l=="ar" else "English"}</span>' for l in c.get('languages',['en']))
def course_card(c,no=None):
    soon=c.get('status')=='coming-soon'; n=MODS.get(c['id'],0)
    kind={'course':'Course','tutorial':'Tutorial','practice':'Practice','roadmaps':'Roadmaps'}[c['type']]
    top=f'<span class="mod-no">{no:02d}</span>' if no else f'<span class="mod-no">{kind}</span>'
    count=f'<span class="tag">{n} modules</span>' if n and c['type']=='course' else (f'<span class="tag">{n} problems</span>' if n and c['id']=='torchcode' else '')
    status=f'<span class="mod-tag tag-soon">Coming {esc(c.get("eta","soon"))}</span>' if soon else '<span class="mod-tag tag-ready">Available</span>'
    return f"""<a class="module-card{' locked' if soon else ''} course-item" href="{c['path']}" data-cat="{esc(c['category'])}" data-level="{esc(c['level'])}" data-type="{c['type']}" data-lang="{' '.join(c.get('languages',['en']))}" data-title="{esc(c['title'].lower())}">
  <div class="mod-top"><div class="mod-icon" style="background:{c['color']}22;color:{c['color']}"><i class="fas {c['icon']}"></i></div>{top}</div>
  <div class="mod-title">{esc(c['title'])}</div>
  <div class="mod-desc">{esc(c['description'])}</div>
  <div>{status}<span class="mod-tag">{esc(c['level'])}</span>{count}</div>
  <div class="mt-1">{lang_tags(c)}</div>
  <div data-ab-course-progress="{c['id']}" data-ab-total="{n}" hidden class="mt-2" style="font-size:.78rem;color:var(--success)"></div>
</a>"""

# ================= HOME =================
courses=[c for c in P.COURSES if c['type']=='course']; tutorials=[c for c in P.COURSES if c['type']=='tutorial']
practice=[c for c in P.COURSES if c['type'] in('practice','roadmaps')]; bilingual=[c for c in live if 'ar' in c.get('languages',[])]
cats=sorted({c['category'] for c in live})
home_nav=[('#courses','Courses'),('#tutorials','Tutorials'),('#bilingual','عربي'),('/roadmaps/','Roadmaps'),('/exam.html','Exams'),('/about.html','About')]
page('index.html','Al-banna Tutorials | Free Courses in AI, Deep Learning, DevOps, Robotics & Quantum',S['description'],
navbar('fa-graduation-cap','Home',home_nav)+hero(f'Learn AI, Deep Learning &amp; DevOps<br>the university way — free',esc(S['tagline'])+f'. Structured courses with worked examples and hands-on labs, by {esc(A["name"])}.',
f"""<div class="mt-3"><a class="btn btn-primary" href="/courses.html"><i class="fas fa-book-open"></i> Browse all courses</a> <a class="btn btn-outline" href="/roadmaps/"><i class="fas fa-map-signs"></i> Pick a roadmap</a></div>
<div class="stats"><div class="stat-card"><div class="stat-num">{N_COURSES}</div><div class="stat-label">Structured courses</div></div><div class="stat-card"><div class="stat-num">{N_TUT}+</div><div class="stat-label">In-depth tutorials</div></div><div class="stat-card"><div class="stat-num">18</div><div class="stat-label">Learning roadmaps</div></div><div class="stat-card"><div class="stat-num">{N_PAGES}+</div><div class="stat-label">Lessons &amp; labs</div></div></div>""")+f"""
<div class="container wide">
 <div class="section fade-up" id="courses">
  <h2 class="section-title"><i class="fas fa-layer-group"></i> Structured Courses</h2>
  <p class="section-sub">Numbered modules, worked examples and a practical lab in each. Mark modules complete to track your progress and earn a certificate.</p>
  <div class="modules">{''.join(course_card(c,i+1) for i,c in enumerate(courses))}</div>
 </div>
 <div class="section fade-up" id="bilingual">
  <h2 class="section-title"><i class="fas fa-language"></i> Available in English and Arabic · متاح بالعربية</h2>
  <p class="section-sub">Full Arabic (RTL) versions with the same figures, equations and labs. Switch language from the bar at the top of any page.</p>
  <div class="modules">{''.join(course_card(c) for c in bilingual)}</div>
 </div>
 <div class="section fade-up" id="tutorials">
  <h2 class="section-title"><i class="fas fa-book"></i> Tutorials &amp; Guides</h2>
  <p class="section-sub">Focused deep-dives on one topic each: LLM agents, MCP, transformers, LangChain, Django, Git and more.</p>
  <div class="modules">{''.join(course_card(c) for c in tutorials)}</div>
 </div>
 <div class="section fade-up" id="practice">
  <h2 class="section-title"><i class="fas fa-dumbbell"></i> Practice &amp; Roadmaps</h2>
  <p class="section-sub">Coding problems, timed exams and step-by-step learning paths.</p>
  <div class="modules">{''.join(course_card(c) for c in practice)}</div>
 </div>
 <div id="quantum"></div><div id="vibe-coding"></div>
 <div class="section fade-up" id="topics">
  <h2 class="section-title"><i class="fas fa-tags"></i> Topics We Cover</h2>
  <div>{''.join(f'<a class="cat-badge" href="/courses.html?topic={esc(c)}">{esc(c)}</a>' for c in cats)}</div>
  <div class="mt-2">{''.join(f'<span class="tag">{esc(t)}</span>' for t in sorted({t for c in live for t in c.get("tags",[]) if t not in("عربي","New")}))}</div>
 </div>
 <div class="section fade-up" id="about">
  <h2 class="section-title"><i class="fas fa-user-graduate"></i> About the author</h2>
  <div class="grid" style="grid-template-columns:auto 1fr;align-items:center;gap:24px">
   <img src="/assets/icon-192.png" alt="" width="84" height="84" style="border-radius:16px">
   <div><p><strong>{esc(A['name'])}</strong> — {esc(A['title'])}. PhD in Computer Science (Loughborough University, UK), researcher in deep learning and speech technology, and Vice Chair of the IEEE CS/CIS Jordan Chapter. Several courses here are the online companion to modules taught at the University of Petra.</p>
   <a class="btn btn-outline btn-sm" href="/about.html">About the portal</a> <a class="btn btn-outline btn-sm" href="{A['profile']}">Academic profile</a> <a class="btn btn-outline btn-sm" href="/contact.html">Contact</a></div>
  </div>
 </div>
</div>""")

# ================= COURSES =================
levels=['Beginner','Intermediate','Advanced']
fbtn=lambda group,vals: ''.join(f'<button type="button" class="btn btn-outline btn-sm" data-f="{group}" data-v="{esc(v)}">{esc(v)}</button>' for v in vals)
page('courses.html',f'All Courses & Tutorials | {S["name"]}',f'Browse every free course and tutorial on {S["name"]}: AI and LLM agents, Deep Learning, DevOps, ROS2 robotics, Python, Java, Scrum, Quantum Physics and Vibe Coding. Filter by topic, level and language.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Courses &amp; Tutorials',f'{N_COURSES} structured courses, {N_TUT}+ in-depth tutorials and 18 learning roadmaps. All free, in English and Arabic.')+f"""
<div class="container wide">
 <div class="section fade-up" id="catalogue">
  <div class="filters" style="display:flex;flex-direction:column;gap:10px;margin-bottom:24px">
   <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center"><span class="text-muted" style="font-size:.85rem;margin-right:4px">Topic:</span><button type="button" class="btn btn-primary btn-sm" data-f="cat" data-v="">All</button>{fbtn('cat',cats)}</div>
   <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center"><span class="text-muted" style="font-size:.85rem;margin-right:4px">Level:</span><button type="button" class="btn btn-primary btn-sm" data-f="level" data-v="">All</button>{fbtn('level',levels)}</div>
   <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center"><span class="text-muted" style="font-size:.85rem;margin-right:4px">Type:</span><button type="button" class="btn btn-primary btn-sm" data-f="type" data-v="">All</button>{fbtn('type',['course','tutorial','practice','roadmaps'])}
    <span class="text-muted" style="font-size:.85rem;margin:0 4px 0 16px">Language:</span><button type="button" class="btn btn-primary btn-sm" data-f="lang" data-v="">All</button><button type="button" class="btn btn-outline btn-sm" data-f="lang" data-v="ar">عربي</button>
    <input type="search" class="form-input" style="max-width:240px;margin-left:auto" id="cf" placeholder="Filter by name…" aria-label="Filter by name"></div>
  </div>
  <div class="modules" id="grid">{''.join(course_card(c) for c in P.COURSES)}</div>
  <p class="text-muted mt-3" id="none" hidden>No courses match those filters.</p>
 </div>
</div>""",extra_js="""<script>
(function(){var f={cat:'',level:'',type:'',lang:'',q:''};var items=document.querySelectorAll('.course-item');
function apply(){var n=0;items.forEach(function(el){var ok=(!f.cat||el.dataset.cat===f.cat)&&(!f.level||el.dataset.level===f.level)&&(!f.type||el.dataset.type===f.type)&&(!f.lang||el.dataset.lang.indexOf(f.lang)>=0)&&(!f.q||el.dataset.title.indexOf(f.q)>=0);el.hidden=!ok;if(ok)n++;});document.getElementById('none').hidden=n>0;}
document.querySelectorAll('.filters [data-f]').forEach(function(b){b.addEventListener('click',function(){f[b.dataset.f]=b.dataset.v;document.querySelectorAll('.filters [data-f="'+b.dataset.f+'"]').forEach(function(x){x.classList.remove('btn-primary');x.classList.add('btn-outline')});b.classList.add('btn-primary');b.classList.remove('btn-outline');apply();});});
document.getElementById('cf').addEventListener('input',function(){f.q=this.value.toLowerCase();apply();});
var m=location.search.match(/[?&]topic=([^&]*)/);if(m){var v=decodeURIComponent(m[1].replace(/\\+/g,' '));var b=document.querySelector('.filters [data-f="cat"][data-v="'+v+'"]');if(b)b.click();}
})();</script>""")

# ================= CATEGORY PAGES =================
def category_page(fn,title,desc,h1,sub,ids,extra_cards,accent,icon):
    entries=[c for c in P.COURSES if c['id'] in ids]
    page(fn,title,desc,navbar(icon,h1,[('/','Home'),('/courses.html','All courses')]+[(c['path'],c['title']) for c in entries if c.get('status')!='coming-soon']+[(c['ar_path'],'بالعربية') for c in entries if c.get('ar_path')])+
    hero(h1,sub)+f"""<div class="container wide"><div class="section fade-up"><h2 class="section-title"><i class="fas {icon}"></i> Courses in this category</h2>
    <div class="modules">{''.join(course_card(c) for c in entries)}{extra_cards}</div>
    <div class="page-nav"><a class="nav-btn prev" href="/">← Back to Home</a><a class="nav-btn next" href="{entries[0]['path']}">Start the course →</a></div></div></div>""",accent=accent)
category_page('quantum-courses.html','Quantum Courses | Al-banna Tutorials','Free quantum physics and quantum computing courses in English and Arabic: photons, wave-particle duality, the double-slit experiment, qubits and quantum gates.','Quantum Courses','The physics of the very small — from the first quantum ideas to the machines that will compute with them. Free, beginner-friendly, and available in English and Arabic.',['quantum','quantum-computing'],'',':root{--primary:#22d3ee;--primary-hover:#67e8f9;--glow:rgba(34,211,238,.14)}','fa-atom')
category_page('vibe-coding-courses.html','Vibe Coding Courses | Al-banna Tutorials','Build real software with AI coding assistants like Claude Code, then ship it to a professional DevOps standard: version control, tests, CI/CD, containers and monitoring.','Vibe Coding','Build real software with AI coding assistants like Claude Code — then ship it to a professional DevOps standard: version control, tests, CI/CD, containers and monitoring. Tool-agnostic principles, from idea to production.',['vibe-coding'],
 """<div class="module-card locked"><div class="mod-top"><div class="mod-icon"><i class="fas fa-robot"></i></div><span class="mod-no">Next</span></div><div class="mod-title">Building &amp; Shipping AI Agents</div><div class="mod-desc">The natural next step: go beyond vibe-coding a web app to building autonomous agents and tools — still with the same DevOps rigor. In preparation.</div><div><span class="mod-tag tag-soon">Coming 2027</span></div></div>""",
 ':root{--primary:#ec4899;--primary-hover:#f472b6;--glow:rgba(236,72,153,.14)}','fa-wand-magic-sparkles')

# ================= EXAMS =================
exams=[('pced-exam.html','Practice Exam','160 questions · practice mode with instant feedback'),('pced-test1.html','Test 1','40 questions'),('pced-test2.html','Test 2','40 questions'),('pced-exam3.html','Exam 3','40 questions'),('pced-exam4.html','Exam 4','40 questions · fixed set covering all syllabus topics')]
page('exam.html',f'Certification Practice Exams | {S["name"]}','Practice for the PCED Python data-analyst certification with 234 real exam-style questions: practice mode with instant feedback or timed exam mode.',
navbar('fa-clipboard-check','Exams',[('/','Home'),('/courses.html','Courses'),('/pced/','PCED Course')])+hero('Certification Exams','Practice for professional certifications with real exam-style questions. Choose Practice Mode to learn at your own pace, or Exam Mode to simulate the real test.',
'<div class="stats"><div class="stat-card"><div class="stat-num">1</div><div class="stat-label">Certification</div></div><div class="stat-card"><div class="stat-num">234</div><div class="stat-label">Questions</div></div><div class="stat-card"><div class="stat-num">2</div><div class="stat-label">Modes</div></div></div>')+f"""
<div class="container"><div class="section fade-up" id="available">
 <h2 class="section-title"><i class="fas fa-file-circle-check"></i> Python Data Analytics Certification (PCED)</h2>
 <p class="section-sub">Data Analyst Essentials with Python — entry-level Python for data analytics. Covers data acquisition, pre-processing, Python fundamentals, statistical analysis, data modeling, and visualization. Each exam offers Practice Mode (instant feedback) and Exam Mode (timed, scored).</p>
 <div class="modules">{''.join(f'<a class="module-card" href="/{h}"><div class="mod-top"><div class="mod-icon"><i class="fas fa-pen-to-square"></i></div><span class="mod-no">{i+1:02d}</span></div><div class="mod-title">{t}</div><div class="mod-desc">{d}</div><div><span class="mod-tag tag-ready">Entry-level</span></div></a>' for i,(h,t,d) in enumerate(exams))}</div>
 <div class="page-nav"><a class="nav-btn prev" href="/pced/">← Study the PCED course first</a><a class="nav-btn next" href="/pced-exam.html">Start the practice exam →</a></div>
</div></div>""",accent=':root{--primary:#22c55e;--primary-hover:#4ade80;--glow:rgba(34,197,94,.14)}')

# ================= ABOUT =================
page('about.html',f'About {S["name"]} | Free AI, Deep Learning, DevOps & Quantum Courses',S['description'],
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero(f'About {esc(S["name"])}',esc(S['tagline'])+'. Free for everyone, built by a university educator, and used by students at the University of Petra and learners worldwide.',
f'<div class="stats"><div class="stat-card"><div class="stat-num">{N_COURSES}</div><div class="stat-label">Structured courses</div></div><div class="stat-card"><div class="stat-num">{N_TUT}+</div><div class="stat-label">In-depth tutorials</div></div><div class="stat-card"><div class="stat-num">{N_PAGES}+</div><div class="stat-label">Lessons &amp; labs</div></div><div class="stat-card"><div class="stat-num">2</div><div class="stat-label">Languages: EN &amp; AR</div></div></div>')+f"""
<div class="container">
 <div class="section fade-up" id="mission"><h2 class="section-title"><i class="fas fa-bullseye"></i> Our mission</h2>
  <p>{esc(S['name'])} exists to make rigorous, university-level technical education freely available to anyone with a browser. Every course is written the way a good lecture is taught: concepts first, then worked examples, then a practical lab you can run yourself.</p>
  <p>The portal covers Artificial Intelligence and LLM agents, Deep Learning, DevOps, robotics with ROS2, Python data analysis, Java, Scrum, Quantum Physics and AI-assisted software development. Several courses are available in both English and Arabic to serve learners across the Arab world.</p></div>
 <div class="section fade-up" id="how"><h2 class="section-title"><i class="fas fa-graduation-cap"></i> How the courses work</h2>
  <ul><li><strong>Free and open.</strong> No account, no paywall. Content is published under the terms on our <a href="/terms.html">Terms</a> page.</li>
  <li><strong>Structured paths.</strong> Each course is a numbered sequence of modules with objectives, examples and a hands-on lab. Use the <a href="/roadmaps/">learning roadmaps</a> to choose a path.</li>
  <li><strong>Track your progress.</strong> Mark modules complete as you go; progress is stored privately in your browser. Finish a course to generate a completion certificate.</li>
  <li><strong>Interactive where it matters.</strong> Simulators, quizzes, practice exams and coding exercises (for example the <a href="/torchcode/">TorchCode</a> PyTorch problem set and the <a href="/deep_learning/rnn_simulator.html">RNN simulator</a>).</li></ul></div>
 <div class="section fade-up" id="university"><h2 class="section-title"><i class="fas fa-university"></i> Used in university teaching</h2>
  <p>Several courses here are the online companion to modules taught in the Department of Data Science and Artificial Intelligence at the University of Petra, Jordan, including Deep Learning, Data Analysis with Python, Programming Language 1, DevOps Lab and Robotics with ROS2.</p></div>
 <div class="section fade-up" id="author"><h2 class="section-title"><i class="fas fa-user-graduate"></i> The author</h2>
  <div class="grid" style="grid-template-columns:auto 1fr;align-items:start;gap:24px"><img src="/assets/icon-192.png" alt="" width="84" height="84" style="border-radius:16px">
  <div><p><strong>{esc(A['name'])}</strong> — {esc(A['title'])}. PhD in Computer Science (Loughborough University, UK). Researcher in deep learning and speech technology, entrepreneur, and Vice Chair of the IEEE CS/CIS Jordan Chapter. Founder and author of {esc(S['name'])}.</p>
  <a class="btn btn-primary btn-sm" href="{A['profile']}"><i class="fas fa-user"></i> Academic profile</a> <a class="btn btn-outline btn-sm" href="/contact.html"><i class="fas fa-envelope"></i> Contact</a>
  <p class="mt-2" style="font-size:.9rem"><a href="{A['scholar']}" target="_blank" rel="noopener">Google Scholar</a> · <a href="{A['orcid']}" target="_blank" rel="noopener">ORCID</a> · <a href="{A['github']}" target="_blank" rel="noopener">GitHub</a> · <a href="{A['huggingface']}" target="_blank" rel="noopener">Hugging Face</a></p></div></div></div>
 <div class="section fade-up" id="contribute"><h2 class="section-title"><i class="fas fa-hand-holding-heart"></i> Contribute</h2><p>Found an error or want to suggest a topic? <a href="/contact.html">Get in touch</a>. Corrections and topic requests from learners shape what gets written next.</p></div>
</div>""")

# ================= CONTACT =================
page('contact.html',f'Contact | {S["name"]}',f'Contact {S["name"]}: questions about courses, corrections, topic requests, or academic and speaking enquiries for {A["name"]}.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Contact','Questions about a course, spotted a mistake, or want to request a topic? We read every message.')+f"""
<div class="container">
 <div class="section fade-up" id="email"><h2 class="section-title"><i class="fas fa-envelope"></i> Email</h2>
  <p>The fastest way to reach us is email:</p><p style="font-size:1.2rem"><a href="mailto:{A['email']}?subject=Al-banna%20Tutorials">{A['email']}</a></p>
  <p class="text-muted" style="font-size:.9rem">Please mention the page URL when reporting an error so we can fix it quickly.</p>
  <div class="info-box"><h3><i class="fas fa-lightbulb"></i> What to write about</h3><ul><li>Corrections and broken links</li><li>Topic or course requests</li><li>Using the material in your own classroom (it is free; attribution appreciated)</li><li>Academic collaboration, talks and workshops</li></ul></div></div>
 <div class="section fade-up" id="elsewhere"><h2 class="section-title"><i class="fas fa-share-nodes"></i> Elsewhere</h2>
  <ul><li><i class="fab fa-github"></i> <a href="{A['github']}" target="_blank" rel="noopener">GitHub</a></li><li><i class="fas fa-graduation-cap"></i> <a href="{A['scholar']}" target="_blank" rel="noopener">Google Scholar</a></li><li><i class="fas fa-id-badge"></i> <a href="{A['orcid']}" target="_blank" rel="noopener">ORCID</a></li><li><i class="fas fa-face-smile"></i> <a href="{A['huggingface']}" target="_blank" rel="noopener">Hugging Face</a></li><!-- TODO: add LinkedIn / YouTube / X links here and in site.json --></ul>
  <p class="text-muted" style="font-size:.9rem"><i class="fas fa-location-dot"></i> University of Petra, Amman, Jordan</p></div>
</div>""")

# ================= PRIVACY / TERMS =================
page('privacy.html',f'Privacy Policy | {S["name"]}',f'How {S["name"]} handles your data: analytics, cookies, local progress storage and third-party services.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Privacy Policy','Last updated: 2 September 2026')+f"""
<div class="container"><div class="section fade-up">
 <h3>Summary</h3><p>{esc(S['name'])} is a free, static educational website. We do not require accounts, we do not sell data, and we collect only the anonymous usage statistics needed to understand which content helps learners.</p>
 <h3>What we collect</h3><ul>
  <li><strong>Analytics.</strong> We use Google Analytics 4 (measurement ID {S['ga4_id']}) to count page views, approximate location (country/city), device type and referring sites. IP addresses are truncated by Google and we do not receive them. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics opt-out add-on</a> or by blocking the <code>googletagmanager.com</code> domain.</li>
  <li><strong>Server logs.</strong> Our web server keeps standard access logs (IP address, requested URL, user agent, time) for security and capacity planning. Logs are rotated and deleted automatically.</li>
  <li><strong>Feedback.</strong> If you click “Was this page helpful?”, only the answer and the page URL are sent to analytics. No free-text is collected.</li></ul>
 <h3>What stays on your device</h3><p>Course progress, theme preferences and the completion certificate name are stored in your browser's <em>localStorage</em>. This data never leaves your device and is not visible to us. Clearing your browser data removes it.</p>
 <h3>Cookies</h3><p>The only cookies set are those used by Google Analytics (<code>_ga</code>, <code>_ga_*</code>) to distinguish visitors. We do not use advertising cookies.</p>
 <h3>Third-party content</h3><p>Pages load fonts, icons and libraries from Google Fonts, cdnjs (Cloudflare) and jsDelivr, and some tutorials embed videos or diagrams from YouTube or GitHub. These providers may receive your IP address when their resources load and apply their own privacy policies.</p>
 <h3>Email</h3><p>If you contact us by email we keep the correspondence only as long as needed to answer you.</p>
 <h3>Your rights</h3><p>You may request information about, or deletion of, any personal data we hold by emailing <a href="mailto:{A['email']}">{A['email']}</a>.</p>
 <h3>Changes</h3><p>We will post any changes to this policy on this page and update the date above.</p>
</div></div>""")
page('terms.html',f'Terms of Use | {S["name"]}',f'Terms of use and content licence for {S["name"]} courses and tutorials.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Terms of Use','Last updated: 2 September 2026')+f"""
<div class="container"><div class="section fade-up">
 <h3>Using this site</h3><p>{esc(S['name'])} provides free educational content. By using the site you agree to these terms. The material is provided for learning purposes and is offered “as is”: while we work hard to keep everything accurate and up to date, we make no warranty that the content is error-free or suitable for any particular purpose.</p>
 <h3>Content licence</h3><p>Unless a page states otherwise, the text, figures and original code on this site are © {esc(A['name'])} and licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)</a>. You may copy, adapt and share the material for non-commercial purposes, including classroom teaching, provided you credit “{esc(S['name'])} — albanna-tutorials.com” and share adaptations under the same licence. For commercial use, please <a href="/contact.html">contact us</a>.</p>
 <p>Code snippets that reproduce third-party libraries, datasets or documentation remain under their original licences. Trademarks and logos of third parties (PyTorch, ROS, Docker, Kubernetes and others) belong to their respective owners.</p>
 <h3>Certificates</h3><p>Completion certificates are generated in your browser as a personal record of self-study. They are not accredited qualifications and do not represent an assessment by any university.</p>
 <h3>External links</h3><p>We link to external sites for reference. We are not responsible for their content or availability.</p>
 <h3>Acceptable use</h3><p>Do not attempt to disrupt the site, scrape it at a rate that degrades service for others, or misrepresent our content as your own.</p>
 <h3>Contact</h3><p>Questions about these terms: <a href="mailto:{A['email']}">{A['email']}</a>.</p>
</div></div>""")

# ================= 404 =================
page('404.html',f'Page not found | {S["name"]}','The page you requested could not be found.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Page not found','The page you were looking for has moved or never existed.')+"""
<div class="container"><div class="section fade-up"><h3>Try one of these</h3>
 <ul><li><a href="/">Homepage</a></li><li><a href="/courses.html">All courses and tutorials</a></li><li><a href="/roadmaps/">Learning roadmaps</a></li><li><a href="/search.html">Search the site</a></li></ul>
 <form action="/search.html" method="get" style="display:flex;gap:8px;margin-top:16px"><input class="form-input" type="search" name="q" placeholder="Search courses and tutorials…" aria-label="Search"><button class="btn btn-primary" type="submit"><i class="fas fa-search"></i></button></form>
 <div class="info-box mt-3"><h3><i class="fas fa-link-slash"></i> Report a broken link</h3><p>If you followed a link from this site to get here, please <a href="/contact.html">let us know</a> which page it was on and we will fix it.</p></div></div></div>""",noindex=True)

# ================= SEARCH =================
page('search.html',f'Search | {S["name"]}',f'Search all courses, modules and tutorials on {S["name"]}.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Search','Search every course, module and tutorial on the site.')+"""
<div class="container"><div class="section fade-up">
 <form style="display:flex;gap:8px;margin-bottom:16px" action="/search.html" method="get" role="search"><input class="form-input" style="font-size:1.05rem;padding:12px 16px" type="search" name="q" id="q" placeholder="e.g. LSTM, docker compose, double slit, ReAct…" aria-label="Search" autofocus><button class="btn btn-primary" type="submit"><i class="fas fa-search"></i></button></form>
 <p class="text-muted" id="status">Type a query to search.</p>
 <div id="results"></div>
</div></div>""",extra_head=".result{background:var(--surface2);border:1px solid var(--border2);border-radius:10px;padding:16px 20px;margin-bottom:12px}.result h3{margin:4px 0;font-size:1.05rem}.result p{font-size:.9rem;margin:0 0 4px}.result mark{background:rgba(250,204,21,.35);color:var(--text);padding:0 2px;border-radius:2px}.result small{color:var(--text2);font-size:.75rem}",
extra_js="""<script src="https://cdnjs.cloudflare.com/ajax/libs/fuse.js/7.0.0/fuse.min.js"></script>
<script>
(function(){var q=document.getElementById('q'),st=document.getElementById('status'),out=document.getElementById('results'),fuse=null;
function esc(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});}
function hl(s,terms){s=esc(s);terms.forEach(function(t){if(t.length<2)return;s=s.replace(new RegExp('('+t.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','ig'),'<mark>$1</mark>');});return s;}
function run(){var v=(q.value||'').trim();if(!v){st.textContent='Type a query to search.';out.innerHTML='';return;}
 if(!fuse){st.textContent='Loading index…';return;}
 var r=fuse.search(v,{limit:40});var terms=v.split(/\\s+/);st.textContent=r.length?r.length+' result'+(r.length>1?'s':'')+' for “'+v+'”':'No results for “'+v+'”. Try a broader term.';
 out.innerHTML=r.map(function(x){var d=x.item;var ctx=d.c?'<span class="tag">'+esc(d.c)+'</span>':'';var lang=d.l==='ar'?'<span class="tag">عربي</span>':'';
  return '<div class="result"><div>'+ctx+lang+'</div><h3><a href="'+d.u+'">'+hl(d.t,terms)+'</a></h3><p>'+hl(d.d,terms)+'</p><small>'+esc(d.u)+'</small></div>';}).join('');
 if(window.gtag)gtag('event','search',{search_term:v});}
fetch('/search-index.json').then(function(r){return r.json()}).then(function(j){fuse=new Fuse(j,{keys:[{name:'t',weight:.5},{name:'tags',weight:.2},{name:'d',weight:.2},{name:'x',weight:.1},{name:'c',weight:.1}],threshold:.38,ignoreLocation:true,minMatchCharLength:2});run();});
var m=location.search.match(/[?&]q=([^&]*)/);if(m)q.value=decodeURIComponent(m[1].replace(/\\+/g,' '));
var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(run,150);});document.querySelector('form[role=search]').addEventListener('submit',function(e){e.preventDefault();run();history.replaceState(null,'','/search.html?q='+encodeURIComponent(q.value));});
})();</script>""")

# ================= CERTIFICATE =================
courses_js=json.dumps({c['id']:{"title":c['title'],"path":c['path'],"n":MODS[c['id']]} for c in P.COURSES if c['type'] in('course','practice') and MODS[c['id']]>0},ensure_ascii=False)
page('certificate.html',f'Certificate of Completion | {S["name"]}','Generate your certificate of completion for a course on Al-banna Tutorials.',
navbar('fa-graduation-cap',S['name'],SITE_NAV)+hero('Certificate of Completion','Complete every module of a course (use the “Mark complete” button on each module) to unlock its certificate. It is generated in your browser; nothing is sent to a server.')+f"""
<div class="container" id="ui"><div class="section fade-up">
  <div class="grid" style="grid-template-columns:2fr 2fr 1fr;align-items:end;gap:12px">
   <div><label for="course" class="text-muted" style="font-size:.85rem">Course</label><select class="form-select" id="course"></select></div>
   <div><label for="name" class="text-muted" style="font-size:.85rem">Your full name</label><input class="form-input" id="name" placeholder="As it should appear on the certificate"></div>
   <button class="btn btn-primary" id="gen">Generate</button>
  </div>
  <p class="mt-2" id="msg" style="font-size:.9rem"></p>
</div></div>
<div id="cert" hidden>
 <div class="cert-page"><div class="cert-border">
   <img src="/assets/icon-192.png" alt="" width="64" height="64">
   <div class="cert-site">{esc(S['name'])}</div><div class="cert-title">Certificate of Completion</div>
   <div class="cert-sub">This certifies that</div><div class="cert-name" id="c-name"></div>
   <div class="cert-sub">has completed all <span id="c-n"></span> modules of the free online course</div><div class="cert-course" id="c-course"></div>
   <div class="cert-foot"><div><div class="cert-line"></div>{esc(A['name'])}<br><small>{esc(A['title'])}</small></div><div><div class="cert-line"></div><span id="c-date"></span><br><small>Date of completion</small></div></div>
   <div class="cert-id">Self-study record generated on albanna-tutorials.com · ID <span id="c-id"></span> · Not an accredited qualification</div>
 </div></div>
 <div class="text-center no-print" style="margin:20px 0"><button class="btn btn-primary" onclick="window.print()"><i class="fas fa-print"></i> Print / Save as PDF</button> <button class="btn btn-outline" onclick="document.getElementById('cert').hidden=true;document.getElementById('ui').hidden=false">Back</button></div>
</div>""",extra_head="""
.cert-page{background:#fff;max-width:1000px;margin:24px auto;padding:28px;box-shadow:0 4px 30px rgba(0,0,0,.3)}
.cert-border{border:10px double #283593;padding:44px 56px;text-align:center;color:#1a237e;background:linear-gradient(#fff,#f5f6fc)}
.cert-site{letter-spacing:4px;text-transform:uppercase;font-size:13px;color:#3949ab;margin-top:10px}
.cert-title{font-size:38px;font-weight:800;margin:14px 0 22px}.cert-sub{color:#555}
.cert-name{font-size:34px;font-weight:600;margin:10px 0;border-bottom:2px solid #3949ab;display:inline-block;padding:0 30px 4px}
.cert-course{font-size:24px;font-weight:600;margin:10px 0 34px}
.cert-foot{display:flex;justify-content:space-around;gap:40px;margin-top:20px;font-size:14px}.cert-line{border-top:1px solid #333;width:220px;margin:0 auto 6px}
.cert-id{margin-top:26px;font-size:11px;color:#888}
@media print{body{background:#fff}.no-print,.hero,.navbar,.footer{display:none!important}.cert-page{box-shadow:none;margin:0;max-width:none}@page{size:landscape;margin:10mm}}
@media(max-width:768px){#ui .grid{grid-template-columns:1fr}}""",extra_js=f"""<script>
(function(){{var C={courses_js};var sel=document.getElementById('course'),nm=document.getElementById('name'),msg=document.getElementById('msg');
Object.keys(C).forEach(function(k){{var o=document.createElement('option');o.value=k;o.textContent=C[k].title;sel.appendChild(o);}});
var m=location.search.match(/[?&]course=([^&]*)/);if(m&&C[decodeURIComponent(m[1])])sel.value=decodeURIComponent(m[1]);
try{{nm.value=localStorage.getItem('ab-cert-name')||'';}}catch(e){{}}
function status(){{var c=C[sel.value];var done=window.ABProgress?window.ABProgress.count(sel.value):0;var ok=done>=c.n&&c.n>0;msg.innerHTML=ok?'<span style="color:var(--success)">All '+c.n+' modules completed. You can generate your certificate.</span>':'<span style="color:var(--warning)">'+done+' of '+c.n+' modules completed. <a href="'+c.path+'">Continue the course</a> to unlock the certificate.</span>';return ok;}}
sel.addEventListener('change',status);window.addEventListener('load',status);
document.getElementById('gen').addEventListener('click',function(){{if(!status())return;var n=nm.value.trim();if(!n){{nm.focus();return;}}try{{localStorage.setItem('ab-cert-name',n);}}catch(e){{}}
 var c=C[sel.value];document.getElementById('c-name').textContent=n;document.getElementById('c-course').textContent=c.title;document.getElementById('c-n').textContent=c.n;
 document.getElementById('c-date').textContent=new Date().toLocaleDateString('en-GB',{{day:'numeric',month:'long',year:'numeric'}});
 var h=0,s=sel.value+'|'+n;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;document.getElementById('c-id').textContent=sel.value.toUpperCase()+'-'+h.toString(16).toUpperCase();
 document.getElementById('ui').hidden=true;document.getElementById('cert').hidden=false;if(window.gtag)gtag('event','certificate_generated',{{course_id:sel.value}});}});
}})();</script>""",noindex=True)
print('pages generated')
