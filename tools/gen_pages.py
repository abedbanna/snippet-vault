"""Generate the portal's own pages into src/: about, contact, privacy, terms, 404, courses, search, certificate."""
import os, sys, json, html as H
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import portal_lib as P
SRC=os.path.join(P.ROOT,'src'); S=P.SITE; A=S['author']
BOOT_CSS='<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">'
BOOT_JS='<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>'
FA='<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">'
FONTS='<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">'
GA=f"""<script async src="https://www.googletagmanager.com/gtag/js?id={S['ga4_id']}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{S['ga4_id']}');</script>"""
CSS=f"""<style>
:root{{--primary-color:{S['brand']['primary']};--accent-color:{S['brand']['accent']};--dark-color:{S['brand']['dark']};--light-color:{S['brand']['light']}}}
body{{font-family:'Roboto',sans-serif;color:#333;background:#f8f9fa;line-height:1.7}}
h1,h2,h3,h4,h5{{font-family:'Poppins',sans-serif;font-weight:600}}
.hero{{background:linear-gradient(135deg,var(--dark-color),var(--primary-color));color:#fff;padding:56px 0 44px}}
.hero h1{{font-weight:700}} .hero p{{opacity:.9;max-width:760px}}
.card-x{{background:#fff;border-radius:12px;padding:28px 32px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.06)}}
.card-x h2{{font-size:1.3rem;color:var(--primary-color);padding-bottom:10px;border-bottom:3px solid var(--light-color);margin-bottom:18px}}
.btn-primary{{background:var(--primary-color);border-color:var(--primary-color)}} .btn-primary:hover{{background:var(--accent-color);border-color:var(--accent-color)}}
a{{color:var(--primary-color)}}
.course-card{{background:#fff;border:0;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,.06);transition:transform .2s,box-shadow .2s;height:100%;overflow:hidden}}
.course-card:hover{{transform:translateY(-4px);box-shadow:0 10px 24px rgba(0,0,0,.1)}}
.course-card .top{{height:6px}} .course-card .icon{{width:46px;height:46px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px}}
.tag{{display:inline-block;background:var(--light-color);color:var(--accent-color);font-size:.72rem;font-weight:600;padding:3px 9px;border-radius:12px;margin:2px}}
.filters .btn{{border-radius:20px;font-size:.85rem}} .filters .btn.active{{background:var(--primary-color);color:#fff;border-color:var(--primary-color)}}
.result{{background:#fff;border-radius:10px;padding:16px 20px;margin-bottom:12px;box-shadow:0 1px 6px rgba(0,0,0,.05)}} .result mark{{background:#fff3b0;padding:0 2px}}
.stat{{font-size:2rem;font-weight:700;color:var(--primary-color);font-family:'Poppins',sans-serif}}
</style>"""
def page(fn,title,desc,body,extra_head='',extra_js='',noindex=False,lang='en'):
    doc=f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
{GA}
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{H.escape(title)}</title>
    <meta name="description" content="{H.escape(desc,quote=True)}">
    {'<meta name="robots" content="noindex,follow">' if noindex else ''}
    {BOOT_CSS}
    {FA}
    {FONTS}
    {CSS}
    {extra_head}
</head>
<body>
{body}
{BOOT_JS}
{extra_js}
</body>
</html>
"""
    open(os.path.join(SRC,fn),'w',encoding='utf-8').write(doc); print(' wrote',fn)

def hero(h1,p,extra=''): return f'<section class="hero"><div class="container"><h1>{h1}</h1><p class="lead mb-0">{p}</p>{extra}</div></section>'
live=[c for c in P.COURSES if c.get('status')!='coming-soon']
n_courses=len([c for c in live if c['type']=='course']); n_tut=len([c for c in live if c['type']=='tutorial'])
n_pages=sum(1 for dp,dn,fn in os.walk(SRC) for f in fn if f.endswith('.html'))

# ---------- About ----------
page('about.html',f'About {S["name"]} | Free AI, Deep Learning, DevOps & Quantum Courses',S['description'],
hero(f'About {S["name"]}',S['tagline']+'. Free for everyone, built by a university educator, and used by students at the University of Petra and learners worldwide.')+f"""
<div class="container py-5">
 <div class="row g-4 mb-4 text-center">
  <div class="col-6 col-md-3"><div class="card-x mb-0"><div class="stat">{n_courses}</div>Structured courses</div></div>
  <div class="col-6 col-md-3"><div class="card-x mb-0"><div class="stat">{n_tut}+</div>In-depth tutorials</div></div>
  <div class="col-6 col-md-3"><div class="card-x mb-0"><div class="stat">{n_pages}+</div>Lessons &amp; labs</div></div>
  <div class="col-6 col-md-3"><div class="card-x mb-0"><div class="stat">2</div>Languages: English &amp; Arabic</div></div>
 </div>
 <div class="row g-4">
  <div class="col-lg-8">
   <div class="card-x"><h2><i class="fas fa-bullseye me-2"></i>Our mission</h2>
    <p>{S['name']} exists to make rigorous, university-level technical education freely available to anyone with a browser. Every course is written the way a good lecture is taught: concepts first, then worked examples, then a practical lab you can run yourself.</p>
    <p>The portal covers Artificial Intelligence and LLM agents, Deep Learning, DevOps, robotics with ROS2, Python data analysis, Java, Scrum, Quantum Physics and AI-assisted software development. Several courses are available in both English and Arabic to serve learners across the Arab world.</p></div>
   <div class="card-x"><h2><i class="fas fa-graduation-cap me-2"></i>How the courses work</h2>
    <ul class="mb-0">
     <li><strong>Free and open.</strong> No account, no paywall. Content is published under the terms on our <a href="/terms.html">Terms</a> page.</li>
     <li><strong>Structured paths.</strong> Each course is a numbered sequence of modules with objectives, examples and a hands-on lab. Use the <a href="/roadmaps/">learning roadmaps</a> to choose a path.</li>
     <li><strong>Track your progress.</strong> Mark modules complete as you go; progress is stored privately in your browser. Finish a course to generate a completion certificate.</li>
     <li><strong>Interactive where it matters.</strong> Simulators, quizzes, practice exams and coding exercises (for example the <a href="/torchcode/">TorchCode</a> PyTorch problem set and the <a href="/deep_learning/rnn_simulator.html">RNN simulator</a>).</li>
    </ul></div>
   <div class="card-x"><h2><i class="fas fa-university me-2"></i>Used in university teaching</h2>
    <p class="mb-0">Several courses here are the online companion to modules taught in the Department of Data Science and Artificial Intelligence at the University of Petra, Jordan, including Deep Learning, Data Analysis with Python, Programming Language 1, DevOps Lab and Robotics with ROS2.</p></div>
  </div>
  <div class="col-lg-4">
   <div class="card-x text-center"><img src="/assets/icon-192.png" alt="" width="72" height="72" class="rounded-3 mb-3">
    <h2 style="border:0;margin-bottom:6px">{H.escape(A['name'])}</h2><p class="text-muted">{H.escape(A['title'])}</p>
    <p class="small">PhD in Computer Science (Loughborough University, UK). Researcher in deep learning and speech technology, entrepreneur, and Vice Chair of the IEEE CS/CIS Jordan Chapter. Founder and author of {S['name']}.</p>
    <a class="btn btn-primary btn-sm" href="{A['profile']}"><i class="fas fa-user me-1"></i> Academic profile</a>
    <a class="btn btn-outline-primary btn-sm ms-1" href="/contact.html"><i class="fas fa-envelope me-1"></i> Contact</a>
    <div class="mt-3 small"><a href="{A['scholar']}" target="_blank" rel="noopener">Google Scholar</a> · <a href="{A['orcid']}" target="_blank" rel="noopener">ORCID</a> · <a href="{A['github']}" target="_blank" rel="noopener">GitHub</a></div>
   </div>
   <div class="card-x"><h2><i class="fas fa-hand-holding-heart me-2"></i>Contribute</h2><p class="small mb-0">Found an error or want to suggest a topic? <a href="/contact.html">Get in touch</a>. Corrections and topic requests from learners shape what gets written next.</p></div>
  </div>
 </div>
</div>""")

# ---------- Contact ----------
page('contact.html',f'Contact | {S["name"]}',f'Contact {S["name"]}: questions about courses, corrections, topic requests, or academic and speaking enquiries for {A["name"]}.',
hero('Contact','Questions about a course, spotted a mistake, or want to request a topic? We read every message.')+f"""
<div class="container py-5"><div class="row g-4">
 <div class="col-lg-7"><div class="card-x">
  <h2><i class="fas fa-envelope me-2"></i>Email</h2>
  <p>The fastest way to reach us is email:</p>
  <p class="fs-5"><a href="mailto:{A['email']}?subject=Al-banna%20Tutorials">{A['email']}</a></p>
  <p class="text-muted small">Please mention the page URL when reporting an error so we can fix it quickly.</p>
  <h2 class="mt-4"><i class="fas fa-lightbulb me-2"></i>What to write about</h2>
  <ul class="mb-0"><li>Corrections and broken links</li><li>Topic or course requests</li><li>Using the material in your own classroom (it is free; attribution appreciated)</li><li>Academic collaboration, talks and workshops</li></ul>
 </div></div>
 <div class="col-lg-5"><div class="card-x">
  <h2><i class="fas fa-share-nodes me-2"></i>Elsewhere</h2>
  <ul class="list-unstyled mb-0">
   <li class="mb-2"><i class="fab fa-github me-2 text-secondary"></i><a href="{A['github']}" target="_blank" rel="noopener">GitHub</a></li>
   <li class="mb-2"><i class="fas fa-graduation-cap me-2 text-secondary"></i><a href="{A['scholar']}" target="_blank" rel="noopener">Google Scholar</a></li>
   <li class="mb-2"><i class="fas fa-id-badge me-2 text-secondary"></i><a href="{A['orcid']}" target="_blank" rel="noopener">ORCID</a></li>
   <li class="mb-2"><i class="fas fa-face-smile me-2 text-secondary"></i><a href="{A['huggingface']}" target="_blank" rel="noopener">Hugging Face</a></li>
   <!-- TODO: add LinkedIn / YouTube / X links here and in site.json -->
  </ul>
  <hr><p class="small text-muted mb-0"><i class="fas fa-location-dot me-1"></i> University of Petra, Amman, Jordan</p>
 </div></div>
</div></div>""")

# ---------- Privacy ----------
page('privacy.html',f'Privacy Policy | {S["name"]}',f'How {S["name"]} handles your data: analytics, cookies, local progress storage and third-party services.',
hero('Privacy Policy','Last updated: 2 September 2026')+f"""
<div class="container py-5"><div class="card-x">
 <h2>Summary</h2>
 <p>{S['name']} is a free, static educational website. We do not require accounts, we do not sell data, and we collect only the anonymous usage statistics needed to understand which content helps learners.</p>
 <h2>What we collect</h2>
 <ul>
  <li><strong>Analytics.</strong> We use Google Analytics 4 (measurement ID {S['ga4_id']}) to count page views, approximate location (country/city), device type and referring sites. IP addresses are truncated by Google and we do not receive them. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics opt-out add-on</a> or by blocking the <code>googletagmanager.com</code> domain.</li>
  <li><strong>Server logs.</strong> Our web server keeps standard access logs (IP address, requested URL, user agent, time) for security and capacity planning. Logs are rotated and deleted automatically.</li>
  <li><strong>Feedback.</strong> If you click “Was this page helpful?”, only the answer and the page URL are sent to analytics. No free-text is collected.</li>
 </ul>
 <h2>What stays on your device</h2>
 <p>Course progress, theme preferences and the completion certificate name are stored in your browser's <em>localStorage</em>. This data never leaves your device and is not visible to us. Clearing your browser data removes it.</p>
 <h2>Cookies</h2>
 <p>The only cookies set are those used by Google Analytics (<code>_ga</code>, <code>_ga_*</code>) to distinguish visitors. We do not use advertising cookies.</p>
 <h2>Third-party content</h2>
 <p>Pages load fonts, icons and libraries from Google Fonts, cdnjs (Cloudflare) and jsDelivr, and some tutorials embed videos or diagrams from YouTube or GitHub. These providers may receive your IP address when their resources load and apply their own privacy policies.</p>
 <h2>Email</h2>
 <p>If you contact us by email we keep the correspondence only as long as needed to answer you.</p>
 <h2>Your rights</h2>
 <p>You may request information about, or deletion of, any personal data we hold by emailing <a href="mailto:{A['email']}">{A['email']}</a>.</p>
 <h2>Changes</h2>
 <p>We will post any changes to this policy on this page and update the date above.</p>
</div></div>""")

# ---------- Terms ----------
page('terms.html',f'Terms of Use | {S["name"]}',f'Terms of use and content licence for {S["name"]} courses and tutorials.',
hero('Terms of Use','Last updated: 2 September 2026')+f"""
<div class="container py-5"><div class="card-x">
 <h2>Using this site</h2>
 <p>{S['name']} provides free educational content. By using the site you agree to these terms. The material is provided for learning purposes and is offered “as is”: while we work hard to keep everything accurate and up to date, we make no warranty that the content is error-free or suitable for any particular purpose.</p>
 <h2>Content licence</h2>
 <p>Unless a page states otherwise, the text, figures and original code on this site are © {A['name']} and licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)</a>. You may copy, adapt and share the material for non-commercial purposes, including classroom teaching, provided you credit “{S['name']} — albanna-tutorials.com” and share adaptations under the same licence. For commercial use, please <a href="/contact.html">contact us</a>.</p>
 <p>Code snippets that reproduce third-party libraries, datasets or documentation remain under their original licences. Trademarks and logos of third parties (PyTorch, ROS, Docker, Kubernetes and others) belong to their respective owners.</p>
 <h2>Certificates</h2>
 <p>Completion certificates are generated in your browser as a personal record of self-study. They are not accredited qualifications and do not represent an assessment by any university.</p>
 <h2>External links</h2>
 <p>We link to external sites for reference. We are not responsible for their content or availability.</p>
 <h2>Acceptable use</h2>
 <p>Do not attempt to disrupt the site, scrape it at a rate that degrades service for others, or misrepresent our content as your own.</p>
 <h2>Contact</h2>
 <p>Questions about these terms: <a href="mailto:{A['email']}">{A['email']}</a>.</p>
</div></div>""")

# ---------- 404 ----------
page('404.html',f'Page not found | {S["name"]}','The page you requested could not be found.',
hero('Page not found','The page you were looking for has moved or never existed.')+f"""
<div class="container py-5"><div class="row g-4">
 <div class="col-lg-7"><div class="card-x">
  <h2>Try one of these</h2>
  <ul><li><a href="/">Homepage</a></li><li><a href="/courses.html">All courses and tutorials</a></li><li><a href="/roadmaps/">Learning roadmaps</a></li><li><a href="/search.html">Search the site</a></li></ul>
  <form action="/search.html" method="get" class="d-flex gap-2 mt-3"><input class="form-control" type="search" name="q" placeholder="Search courses and tutorials…" aria-label="Search"><button class="btn btn-primary" type="submit"><i class="fas fa-search"></i></button></form>
 </div></div>
 <div class="col-lg-5"><div class="card-x"><h2>Report a broken link</h2><p class="mb-0">If you followed a link from this site to get here, please <a href="/contact.html">let us know</a> which page it was on and we will fix it.</p></div></div>
</div></div>""",noindex=True)

# ---------- Courses catalogue ----------
cats=sorted({c['category'] for c in P.COURSES}); levels=['Beginner','Intermediate','Advanced']
def card(c):
    langs=' '.join(f'<span class="tag">{"عربي" if l=="ar" else "English"}</span>' for l in c.get('languages',['en']))
    kind={'course':'Course','tutorial':'Tutorial','practice':'Practice','roadmaps':'Roadmaps'}[c['type']]
    soon=c.get('status')=='coming-soon'
    badge=f'<span class="badge bg-warning text-dark">Coming {H.escape(c.get("eta","soon"))}</span>' if soon else f'<span class="badge" style="background:{c["color"]}">{kind}</span>'
    return f"""<div class="col-md-6 col-lg-4 course-item" data-cat="{H.escape(c['category'])}" data-level="{H.escape(c['level'])}" data-type="{c['type']}" data-lang="{' '.join(c.get('languages',['en']))}" data-title="{H.escape(c['title'].lower())}">
 <a class="text-decoration-none text-dark d-block h-100" href="{c['path']}"><div class="course-card">
  <div class="top" style="background:{c['color']}"></div>
  <div class="p-4">
   <div class="d-flex justify-content-between align-items-start mb-3"><div class="icon" style="background:{c['color']}"><i class="fas {c['icon']}"></i></div>{badge}</div>
   <h5 class="mb-2">{H.escape(c['title'])}</h5>
   <p class="small text-muted mb-3">{H.escape(c['description'])}</p>
   <div class="mb-2"><span class="tag">{H.escape(c['level'])}</span>{langs}</div>
   <div data-ab-course-progress="{c['id']}" data-ab-total="__N_{c['id']}__" hidden class="mt-2 small text-success"></div>
  </div>
 </div></a>
</div>"""
cards='\n'.join(card(c) for c in P.COURSES)
fbtn=lambda group,vals: ''.join(f'<button type="button" class="btn btn-outline-secondary btn-sm" data-f="{group}" data-v="{H.escape(v)}">{H.escape(v)}</button>' for v in vals)
page('courses.html',f'All Courses & Tutorials | {S["name"]}',f'Browse every free course and tutorial on {S["name"]}: AI and LLM agents, Deep Learning, DevOps, ROS2 robotics, Python, Java, Scrum, Quantum Physics and Vibe Coding. Filter by topic, level and language.',
hero('Courses &amp; Tutorials',f'{n_courses} structured courses, {n_tut}+ in-depth tutorials and 18 learning roadmaps. All free, in English and Arabic.')+f"""
<div class="container py-4">
 <div class="filters mb-4">
  <div class="d-flex flex-wrap gap-2 align-items-center mb-2"><span class="text-muted small me-1">Topic:</span><button type="button" class="btn btn-outline-secondary btn-sm active" data-f="cat" data-v="">All</button>{fbtn('cat',cats)}</div>
  <div class="d-flex flex-wrap gap-2 align-items-center mb-2"><span class="text-muted small me-1">Level:</span><button type="button" class="btn btn-outline-secondary btn-sm active" data-f="level" data-v="">All</button>{fbtn('level',levels)}</div>
  <div class="d-flex flex-wrap gap-2 align-items-center"><span class="text-muted small me-1">Type:</span><button type="button" class="btn btn-outline-secondary btn-sm active" data-f="type" data-v="">All</button>{fbtn('type',['course','tutorial','practice','roadmaps'])}
   <span class="text-muted small ms-3 me-1">Language:</span><button type="button" class="btn btn-outline-secondary btn-sm active" data-f="lang" data-v="">All</button><button type="button" class="btn btn-outline-secondary btn-sm" data-f="lang" data-v="ar">عربي</button>
   <input type="search" class="form-control form-control-sm ms-auto" style="max-width:240px" id="cf" placeholder="Filter by name…" aria-label="Filter by name"></div>
 </div>
 <div class="row g-4" id="grid">{cards}</div>
 <p class="text-muted mt-4" id="none" hidden>No courses match those filters.</p>
</div>""",extra_js="""<script>
(function(){var f={cat:'',level:'',type:'',lang:'',q:''};var items=document.querySelectorAll('.course-item');
function apply(){var n=0;items.forEach(function(el){var ok=(!f.cat||el.dataset.cat===f.cat)&&(!f.level||el.dataset.level===f.level)&&(!f.type||el.dataset.type===f.type)&&(!f.lang||el.dataset.lang.indexOf(f.lang)>=0)&&(!f.q||el.dataset.title.indexOf(f.q)>=0);el.hidden=!ok;if(ok)n++;});document.getElementById('none').hidden=n>0;}
document.querySelectorAll('.filters [data-f]').forEach(function(b){b.addEventListener('click',function(){f[b.dataset.f]=b.dataset.v;document.querySelectorAll('.filters [data-f="'+b.dataset.f+'"]').forEach(function(x){x.classList.remove('active')});b.classList.add('active');apply();});});
document.getElementById('cf').addEventListener('input',function(){f.q=this.value.toLowerCase();apply();});
var m=location.search.match(/[?&]topic=([^&]*)/);if(m){var v=decodeURIComponent(m[1]);var b=document.querySelector('.filters [data-f="cat"][data-v="'+v+'"]');if(b)b.click();}
fetch('/assets/module-counts.json').then(function(r){return r.json()}).then(function(c){document.querySelectorAll('[data-ab-course-progress]').forEach(function(el){var id=el.getAttribute('data-ab-course-progress');el.setAttribute('data-ab-total',c[id]||0);});if(window.ABProgress){var ev=document.createEvent('Event');ev.initEvent('ab-counts',true,true);document.dispatchEvent(ev);}}).catch(function(){});
})();</script>""")
# The module counts placeholder is resolved at build time by build.py? Simpler: replace now with a fixed count from the src tree.
p=os.path.join(SRC,'courses.html'); d=open(p,encoding='utf-8').read()
for c in P.COURSES: d=d.replace(f'__N_{c["id"]}__',str(len(P.course_modules(SRC,c))))
open(p,'w',encoding='utf-8').write(d)

# ---------- Search ----------
page('search.html',f'Search | {S["name"]}',f'Search all courses, modules and tutorials on {S["name"]}.',
hero('Search','Search every course, module and tutorial on the site.')+"""
<div class="container py-4">
 <form class="d-flex gap-2 mb-4" action="/search.html" method="get" role="search"><input class="form-control form-control-lg" type="search" name="q" id="q" placeholder="e.g. LSTM, docker compose, double slit, ReAct…" aria-label="Search" autofocus><button class="btn btn-primary btn-lg" type="submit"><i class="fas fa-search"></i></button></form>
 <p class="text-muted" id="status">Type a query to search.</p>
 <div id="results"></div>
</div>""",extra_js="""<script src="https://cdnjs.cloudflare.com/ajax/libs/fuse.js/7.0.0/fuse.min.js"></script>
<script>
(function(){var q=document.getElementById('q'),st=document.getElementById('status'),out=document.getElementById('results'),fuse=null,data=[];
function esc(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});}
function hl(s,terms){s=esc(s);terms.forEach(function(t){if(t.length<2)return;s=s.replace(new RegExp('('+t.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','ig'),'<mark>$1</mark>');});return s;}
function run(){var v=(q.value||'').trim();if(!v){st.textContent='Type a query to search.';out.innerHTML='';return;}
 if(!fuse){st.textContent='Loading index…';return;}
 var r=fuse.search(v,{limit:40});var terms=v.split(/\\s+/);st.textContent=r.length?r.length+' result'+(r.length>1?'s':'')+' for “'+v+'”':'No results for “'+v+'”. Try a broader term.';
 out.innerHTML=r.map(function(x){var d=x.item;var ctx=d.c?'<span class="badge bg-light text-secondary border me-2">'+esc(d.c)+'</span>':'';var lang=d.l==='ar'?'<span class="badge bg-light text-secondary border">عربي</span>':'';
  return '<div class="result"><div class="mb-1">'+ctx+lang+'</div><h5 class="mb-1"><a href="'+d.u+'">'+hl(d.t,terms)+'</a></h5><p class="small text-muted mb-1">'+hl(d.d,terms)+'</p><small class="text-secondary">'+esc(d.u)+'</small></div>';}).join('');
 if(window.gtag)gtag('event','search',{search_term:v});}
fetch('/search-index.json').then(function(r){return r.json()}).then(function(j){data=j;fuse=new Fuse(data,{keys:[{name:'t',weight:.5},{name:'tags',weight:.2},{name:'d',weight:.2},{name:'x',weight:.1},{name:'c',weight:.1}],threshold:.38,ignoreLocation:true,minMatchCharLength:2});run();});
var m=location.search.match(/[?&]q=([^&]*)/);if(m)q.value=decodeURIComponent(m[1].replace(/\\+/g,' '));
var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(run,150);});document.querySelector('form').addEventListener('submit',function(e){e.preventDefault();run();history.replaceState(null,'','/search.html?q='+encodeURIComponent(q.value));});
})();</script>""")

# ---------- Certificate ----------
courses_js=json.dumps({c['id']:{"title":c['title'],"path":c['path'],"n":len(P.course_modules(SRC,c))} for c in P.COURSES if c['type'] in('course','practice')},ensure_ascii=False)
page('certificate.html',f'Certificate of Completion | {S["name"]}','Generate your certificate of completion for a course on Al-banna Tutorials.',
f"""<div class="container py-4" id="ui">
 <h1 class="h3">Certificate of Completion</h1>
 <p class="text-muted">Complete every module of a course (use the “Mark complete” button on each module) to unlock its certificate. The certificate is generated in your browser; nothing is sent to a server.</p>
 <div class="card-x">
  <div class="row g-3 align-items-end">
   <div class="col-md-5"><label class="form-label" for="course">Course</label><select class="form-select" id="course"></select></div>
   <div class="col-md-5"><label class="form-label" for="name">Your full name</label><input class="form-control" id="name" placeholder="As it should appear on the certificate"></div>
   <div class="col-md-2 d-grid"><button class="btn btn-primary" id="gen">Generate</button></div>
  </div>
  <p class="small mt-3 mb-0" id="msg"></p>
 </div>
</div>
<div id="cert" hidden>
 <div class="cert-page">
  <div class="cert-border">
   <img src="/assets/icon-192.png" alt="" width="64" height="64">
   <div class="cert-site">{H.escape(S['name'])}</div>
   <div class="cert-title">Certificate of Completion</div>
   <div class="cert-sub">This certifies that</div>
   <div class="cert-name" id="c-name"></div>
   <div class="cert-sub">has completed all <span id="c-n"></span> modules of the free online course</div>
   <div class="cert-course" id="c-course"></div>
   <div class="cert-foot"><div><div class="cert-line"></div>{H.escape(A['name'])}<br><small>{H.escape(A['title'])}</small></div><div><div class="cert-line"></div><span id="c-date"></span><br><small>Date of completion</small></div></div>
   <div class="cert-id">Self-study record generated on albanna-tutorials.com · ID <span id="c-id"></span> · Not an accredited qualification</div>
  </div>
 </div>
 <div class="text-center my-3 no-print"><button class="btn btn-primary" onclick="window.print()"><i class="fas fa-print me-1"></i> Print / Save as PDF</button> <button class="btn btn-outline-secondary" onclick="document.getElementById('cert').hidden=true;document.getElementById('ui').hidden=false">Back</button></div>
</div>""",extra_head="""<style>
.cert-page{background:#fff;max-width:1000px;margin:24px auto;padding:28px;box-shadow:0 4px 30px rgba(0,0,0,.12)}
.cert-border{border:10px double #283593;padding:44px 56px;text-align:center;font-family:'Poppins',sans-serif;color:#1a237e;background:linear-gradient(#fff,#f5f6fc)}
.cert-site{letter-spacing:4px;text-transform:uppercase;font-size:13px;color:#3949ab;margin-top:10px}
.cert-title{font-size:38px;font-weight:700;margin:14px 0 22px}
.cert-sub{color:#555;font-family:'Roboto',sans-serif}
.cert-name{font-size:34px;font-weight:600;margin:10px 0;border-bottom:2px solid #3949ab;display:inline-block;padding:0 30px 4px}
.cert-course{font-size:24px;font-weight:600;margin:10px 0 34px}
.cert-foot{display:flex;justify-content:space-around;gap:40px;margin-top:20px;font-size:14px}
.cert-line{border-top:1px solid #333;width:220px;margin:0 auto 6px}
.cert-id{margin-top:26px;font-size:11px;color:#888;font-family:'Roboto',sans-serif}
@media print{body{background:#fff}.no-print,.hero{display:none!important}.cert-page{box-shadow:none;margin:0;max-width:none}@page{size:landscape;margin:10mm}}
</style>""",extra_js=f"""<script>
(function(){{var C={courses_js};var sel=document.getElementById('course'),nm=document.getElementById('name'),msg=document.getElementById('msg');
Object.keys(C).forEach(function(k){{var o=document.createElement('option');o.value=k;o.textContent=C[k].title;sel.appendChild(o);}});
var m=location.search.match(/[?&]course=([^&]*)/);if(m&&C[decodeURIComponent(m[1])])sel.value=decodeURIComponent(m[1]);
try{{nm.value=localStorage.getItem('ab-cert-name')||'';}}catch(e){{}}
function status(){{var c=C[sel.value];var done=window.ABProgress?window.ABProgress.count(sel.value):0;var ok=done>=c.n&&c.n>0;msg.innerHTML=ok?'<span class="text-success">All '+c.n+' modules completed. You can generate your certificate.</span>':'<span class="text-warning">'+done+' of '+c.n+' modules completed. <a href="'+c.path+'">Continue the course</a> to unlock the certificate.</span>';return ok;}}
sel.addEventListener('change',status);window.addEventListener('load',status);
document.getElementById('gen').addEventListener('click',function(){{if(!status())return;var n=nm.value.trim();if(!n){{nm.focus();return;}}try{{localStorage.setItem('ab-cert-name',n);}}catch(e){{}}
 var c=C[sel.value];document.getElementById('c-name').textContent=n;document.getElementById('c-course').textContent=c.title;document.getElementById('c-n').textContent=c.n;
 document.getElementById('c-date').textContent=new Date().toLocaleDateString('en-GB',{{day:'numeric',month:'long',year:'numeric'}});
 var h=0,s=sel.value+'|'+n;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;document.getElementById('c-id').textContent=sel.value.toUpperCase()+'-'+h.toString(16).toUpperCase();
 document.getElementById('ui').hidden=true;document.getElementById('cert').hidden=false;if(window.gtag)gtag('event','certificate_generated',{{course_id:sel.value}});}});
}})();</script>""",noindex=True)
print('pages generated')
