"""Shared helpers: site/course config, page classification, HTML injection (idempotent)."""
import json, os, re, html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE=json.load(open(os.path.join(ROOT,'site.json'),encoding='utf-8'))
COURSES=json.load(open(os.path.join(ROOT,'courses.json'),encoding='utf-8'))
BY_PATH={c['path']:c for c in COURSES}
BASE=SITE['url']
MARK=('<!-- ab:%s -->','<!-- /ab:%s -->')
SKIP_DIRS={'cm_images','images','assets','_reference'}
NO_PROGRESS_TYPES={'roadmaps'}

def rel_url(rel):
    """filesystem rel path -> site URL path ('/' for index.html, '/x/' for x/index.html)."""
    u='/'+rel.replace(os.sep,'/')
    if u.endswith('/index.html'): u=u[:-len('index.html')]
    return u

def course_for(url):
    """Return (course, role) for a URL path. role in: home, course-index, module, tutorial, page."""
    if url=='/': return None,'home'
    for c in COURSES:
        p=c['path']
        if p.endswith('/') and url.startswith(p):
            if url==p: return c,'course-index'
            if c.get('ar_path') and url==c['ar_path']: return c,'course-index'
            return c,'module'
        if url==p or url==c.get('ar_path'): return c,'tutorial'
    return None,'page'

def course_modules(src_dir,c):
    """List of module URL paths for a course directory (top-level html except index)."""
    if not c['path'].endswith('/') or c.get('type') in NO_PROGRESS_TYPES: return []
    sub=c.get('modules_dir',''); d=os.path.join(src_dir,c['path'].strip('/'),sub)
    if not os.path.isdir(d): return []
    ex=set(c.get('modules_exclude',[]))
    files=sorted(f for f in os.listdir(d) if f.endswith('.html') and f!='index.html' and not f.startswith('_') and f not in ex)
    return [c['path']+sub+f for f in files]

def strip_tags(s):
    s=re.sub(r'<(script|style|nav|header|footer)[^>]*>.*?</\1>','',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>',' ',s); s=H.unescape(s); return re.sub(r'\s+',' ',s).strip()

def get_title(doc):
    m=re.search(r'<title[^>]*>(.*?)</title>',doc,re.S|re.I)
    return re.sub(r'\s+',' ',H.unescape(m.group(1))).strip() if m else SITE['name']

def get_description(doc):
    m=re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',doc,re.I) or re.search(r'<meta\s+content=["\']([^"\']*)["\']\s+name=["\']description["\']',doc,re.I)
    if m and m.group(1).strip(): return H.unescape(m.group(1).strip()),True
    body=doc.split('<body',1)[1] if '<body' in doc else doc
    for p in re.findall(r'<p[^>]*>(.*?)</p>',body,re.S|re.I):
        t=strip_tags(p)
        if len(t)>=60:
            if len(t)>155: t=t[:152].rsplit(' ',1)[0]+'…'
            return t,False
    return SITE['description'],False

def remove_block(doc,name):
    a,b=MARK[0]%name,MARK[1]%name
    return re.sub(re.escape(a)+r'.*?'+re.escape(b)+r'\n?','',doc,flags=re.S)

def wrap(name,inner): return f'{MARK[0]%name}\n{inner}\n{MARK[1]%name}\n'

def esc(s): return H.escape(s,quote=True)

def lang_of(doc):
    m=re.search(r'<html[^>]*\blang=["\']([a-zA-Z-]+)',doc); return (m.group(1).lower() if m else 'en')

SVG={
 'github':'<svg viewBox="0 0 24 24"><path d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.9 10.9.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.4-3.9-1.4-.5-1.3-1.3-1.7-1.3-1.7-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.4 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.2 2.8.1 3.1.8.8 1.2 1.9 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.2c0 .3.2.7.8.6 4.6-1.5 7.9-5.8 7.9-10.9C23.5 5.7 18.3.5 12 .5z"/></svg>',
 'linkedin':'<svg viewBox="0 0 24 24"><path d="M20.4 20.5h-3.5v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9v5.7H9.4V9h3.4v1.6h.1c.5-.9 1.6-1.9 3.4-1.9 3.6 0 4.3 2.4 4.3 5.5v6.3zM5.3 7.4a2 2 0 1 1 0-4.1 2 2 0 0 1 0 4.1zM7.1 20.5H3.6V9h3.5v11.5zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.5c0 1 .8 1.8 1.8 1.8h20.4c1 0 1.8-.8 1.8-1.8V1.7c0-.9-.8-1.7-1.8-1.7z"/></svg>',
 'youtube':'<svg viewBox="0 0 24 24"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>',
 'x':'<svg viewBox="0 0 24 24"><path d="M18.2 2h3.4l-7.4 8.5L23 22h-6.8l-5.3-7-6.1 7H1.4l7.9-9.1L1 2h7l4.8 6.4L18.2 2zm-1.2 18h1.9L7.1 3.9H5.1L17 20z"/></svg>',
 'scholar':'<svg viewBox="0 0 24 24"><path d="M12 2 1 9l11 7 9-5.7V17h2V9L12 2zm0 16.2L5 13.7V17c0 2.2 3.1 4 7 4s7-1.8 7-4v-3.3l-7 4.5z"/></svg>',
 'orcid':'<svg viewBox="0 0 24 24"><path d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24zM7.4 17.6H5.9V7.4h1.5v10.2zM6.6 6.2a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm3.1 1.2h3.9c3.7 0 5.4 2.7 5.4 5.1 0 2.6-2 5.1-5.4 5.1H9.7V7.4zm1.5 1.4v7.4h2.3c3.3 0 4-2.5 4-3.7 0-2-1.3-3.7-4.1-3.7h-2.2z"/></svg>',
 'huggingface':'<svg viewBox="0 0 24 24"><path d="M12 2a9 9 0 0 0-8.8 11h-.3a1.8 1.8 0 0 0-1.3 3.1 1.8 1.8 0 0 0 .8 3.3c.7 1.5 3.2 2.6 5.3 2.6.9 0 1.8-.2 2.5-.7a9 9 0 0 0 3.6 0c.7.5 1.6.7 2.5.7 2.1 0 4.6-1.1 5.3-2.6a1.8 1.8 0 0 0 .8-3.3 1.8 1.8 0 0 0-1.3-3.1h-.3A9 9 0 0 0 12 2zm-3.3 6.4a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2zm6.6 0a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2zM8.6 12.3c.3 0 .5.2.8.5.7.6 1.6 1 2.6 1s1.9-.4 2.6-1c.3-.3.5-.5.8-.5.4 0 .6.4.4.9-.6 1.5-2.2 2.4-3.8 2.4s-3.2-.9-3.8-2.4c-.2-.5 0-.9.4-.9z"/></svg>',
 'mail':'<svg viewBox="0 0 24 24"><path d="M2 4h20a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm10 7.6L20 6H4l8 5.6zM3 8v10h18V8l-9 6.3L3 8z"/></svg>',
 'search':'<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M15.5 14h-.8l-.3-.3A6.5 6.5 0 1 0 9.5 16a6.5 6.5 0 0 0 4.2-1.6l.3.3v.8l5 5 1.5-1.5-5-5zm-6 0a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9z"/></svg>',
}
LABELS={'en':dict(courses='Courses',roadmaps='Roadmaps',about='About',contact='Contact',search='Search…',home='Home',tutorials='Tutorials',privacy='Privacy',terms='Terms',sitemap='Sitemap',helpful='Was this page helpful?',yes='Yes',no='No',menu='Menu',by='by',explore='Explore',lang='عربي',rights='All rights reserved.',profile='Academic profile'),
        'ar':dict(courses='الدورات',roadmaps='خرائط التعلم',about='عن الموقع',contact='اتصل بنا',search='ابحث…',home='الرئيسية',tutorials='الدروس',privacy='الخصوصية',terms='الشروط',sitemap='خريطة الموقع',helpful='هل كانت هذه الصفحة مفيدة؟',yes='نعم',no='لا',menu='القائمة',by='بواسطة',explore='استكشف',lang='English',rights='جميع الحقوق محفوظة.',profile='الملف الأكاديمي')}

def social_links():
    a=SITE['author']; out=[]
    for key,label in (('github','GitHub'),('linkedin','LinkedIn'),('youtube','YouTube'),('x','X'),('scholar','Google Scholar'),('orcid','ORCID'),('huggingface','Hugging Face')):
        url=a.get(key,'')
        if url: out.append(f'<a href="{esc(url)}" target="_blank" rel="noopener me" title="{label}" aria-label="{label}">{SVG[key]}</a>')
        else: out.append(f'<!-- TODO: add {label} URL in site.json (author.{key}) -->')
    if a.get('email'): out.append(f'<a href="mailto:{esc(a["email"])}" title="Email" aria-label="Email">{SVG["mail"]}</a>')
    return '\n'.join(out)

def alt_lang_url(url,exists):
    """URL of the other-language twin if it exists, else None."""
    c,_=course_for(url)
    if c and c.get('ar_path'):
        if c['path'].endswith('/'):
            if url.startswith(c['ar_path']): cand=c['path']+url[len(c['ar_path']):]
            else: cand=c['ar_path']+url[len(c['path']):]
        else: cand=c['ar_path'] if url==c['path'] else c['path']
        if exists(cand): return cand
    return None

def bar_html(url,lang,course,role,alt):
    L=LABELS['ar' if lang.startswith('ar') else 'en']
    home_label=SITE['name']
    links=[('/courses.html',L['courses']),('/roadmaps/',L['roadmaps']),('/about.html',L['about']),('/contact.html',L['contact'])]
    li=''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in links)
    altl=f'<a class="ab-lang" href="{esc(alt)}" hreflang="{"en" if lang.startswith("ar") else "ar"}">{L["lang"]}</a>' if alt else ''
    return f'''<div class="ab-bar" role="navigation" aria-label="{esc(SITE['name'])}">
 <div class="ab-in">
  <a class="ab-brand" href="/" title="{esc(SITE['name'])} — {L['home']}"><img src="/assets/mark-white.png" alt="" width="26" height="26"><span>{esc(home_label)}</span></a>
  <button class="ab-toggle" type="button" aria-expanded="false" aria-label="{L['menu']}">☰ {L['menu']}</button>
  <ul class="ab-links">{li}</ul>
  <span class="ab-spacer"></span>
  <span class="ab-slot"></span>
  {altl}
  <form class="ab-search" action="/search.html" method="get" role="search"><input type="search" name="q" placeholder="{L['search']}" aria-label="{L['search']}"><button type="submit" aria-label="{L['search']}">{SVG['search']}</button></form>
 </div>
</div>'''

def crumbs_html(url,lang,title,course,role):
    if role=='home': return ''
    L=LABELS['ar' if lang.startswith('ar') else 'en']
    items=[('/',L['home'])]
    if course and role=='module':
        items.append(('/courses.html',L['courses']))
        cpath=course['ar_path'] if (course.get('ar_path') and url.startswith(course['ar_path'])) else course['path']
        items.append((cpath,course['title']))
    elif course and role in('course-index','tutorial'):
        items.append(('/courses.html',L['courses']))
    elif role=='page' and url not in('/courses.html',):
        pass
    lis=''.join(f'<li><a href="{esc(h)}">{esc(t)}</a></li>' for h,t in items)
    short=title.split(' | ')[0].split(' - ')[0].split(' — ')[0].strip() or title
    lis+=f'<li><span aria-current="page">{esc(short)}</span></li>'
    return f'<nav class="ab-crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

def footer_html(url,lang,role):
    L=LABELS['ar' if lang.startswith('ar') else 'en']; a=SITE['author']
    fb='' if role in('home','page') else f'<div class="ab-feedback"><span>{L["helpful"]}</span><button type="button" data-v="yes">👍 {L["yes"]}</button><button type="button" data-v="no">👎 {L["no"]}</button></div>'
    return f'''<footer class="ab-footer">
 <div class="ab-in">
  <div class="ab-row">
   <div class="ab-col" style="flex:1.4">
    <a class="ab-brand" href="/"><img src="/assets/mark-white.png" alt="" width="26" height="26"><span>{esc(SITE['name'])}</span></a>
    <p>{esc(SITE['tagline'])}. {L['by']} <a href="{a['profile']}">{esc(a['name'])}</a>, {esc(a['title'])}.</p>
    <div class="ab-social">{social_links()}</div>
   </div>
   <div class="ab-col"><h6>{L['explore']}</h6><ul><li><a href="/courses.html">{L['courses']}</a></li><li><a href="/roadmaps/">{L['roadmaps']}</a></li><li><a href="/search.html">{L['search'].rstrip('…')}</a></li><li><a href="/exam.html">Exams</a></li></ul></div>
   <div class="ab-col"><h6>{L['about']}</h6><ul><li><a href="/about.html">{L['about']}</a></li><li><a href="{a['profile']}">{L['profile']}</a></li><li><a href="/contact.html">{L['contact']}</a></li><li><a href="/privacy.html">{L['privacy']}</a></li><li><a href="/terms.html">{L['terms']}</a></li></ul></div>
   <div class="ab-col">{fb}</div>
  </div>
  <div class="ab-copy"><span>© <span class="ab-year">2026</span> {esc(SITE['name'])}. {L['rights']}</span><span><a href="/sitemap.xml">{L['sitemap']}</a> · <a href="/privacy.html">{L['privacy']}</a> · <a href="/terms.html">{L['terms']}</a></span></div>
 </div>
</footer>'''

def jsonld(url,lang,title,desc,course,role,modules,img):
    org={"@type":"Organization","name":SITE['name'],"url":BASE+"/","logo":BASE+"/assets/icon-512.png",
         "founder":{"@type":"Person","name":SITE['author']['name'],"url":BASE+SITE['author']['profile']}}
    person={"@type":"Person","name":SITE['author']['name'],"url":BASE+SITE['author']['profile'],"jobTitle":SITE['author']['title'],
            "sameAs":[v for k,v in SITE['author'].items() if k in('orcid','scholar','github','huggingface','linkedin','youtube') and v]}
    graph=[]
    if role=='home':
        graph+= [dict(org,**{"@id":BASE+"/#org"}),{"@type":"WebSite","url":BASE+"/","name":SITE['name'],"publisher":{"@id":BASE+"/#org"},
                 "potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":BASE+"/search.html?q={search_term_string}"},"query-input":"required name=search_term_string"}},person]
    else:
        crumbs=[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"}]
        if course and role=='module':
            crumbs.append({"@type":"ListItem","position":2,"name":"Courses","item":BASE+"/courses.html"})
            crumbs.append({"@type":"ListItem","position":3,"name":course['title'],"item":BASE+course['path']})
            crumbs.append({"@type":"ListItem","position":4,"name":title})
        elif course:
            crumbs.append({"@type":"ListItem","position":2,"name":"Courses","item":BASE+"/courses.html"})
            crumbs.append({"@type":"ListItem","position":3,"name":title})
        else: crumbs.append({"@type":"ListItem","position":2,"name":title})
        graph.append({"@type":"BreadcrumbList","itemListElement":crumbs})
        if course and role=='course-index' and course.get('type') in('course','practice'):
            graph.append({"@type":"Course","name":course['title'],"description":course['description'],"url":BASE+url,"inLanguage":course.get('languages',['en']),
                "provider":org,"educationalLevel":course.get('level'),"isAccessibleForFree":True,"image":BASE+img,"author":person,
                "hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","courseWorkload":f"PT{max(len(modules),1)}H"},
                "offers":{"@type":"Offer","price":"0","priceCurrency":"USD","category":"Free"}})
        elif role in('module','tutorial'):
            graph.append({"@type":"TechArticle","headline":title,"description":desc,"url":BASE+url,"inLanguage":lang,"image":BASE+img,"author":person,"publisher":org,
                          **({"isPartOf":{"@type":"Course","name":course['title'],"url":BASE+course['path']}} if course and role=='module' else {})})
    return json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)

def head_html(url,lang,title,desc,has_desc,course,role,modules,alt,has_hreflang):
    img='/assets/og-default.png'
    og_type='website' if role in('home','page','course-index') else 'article'
    locale='ar_JO' if lang.startswith('ar') else 'en_US'
    parts=[]
    if not has_desc: parts.append(f'<meta name="description" content="{esc(desc)}">')
    parts+= [f'<link rel="canonical" href="{esc(BASE+url)}">',
        '<link rel="icon" href="/favicon.ico" sizes="any">','<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">',
        '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">',  # no rel="manifest": the site is a plain website, not an installable app
        f'<meta name="theme-color" content="{SITE["brand"]["dark"]}">',
        f'<meta name="author" content="{esc(SITE["author"]["name"])}">',
        f'<meta property="og:site_name" content="{esc(SITE["name"])}">',f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:title" content="{esc(title)}">',f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{esc(BASE+url)}">',f'<meta property="og:image" content="{BASE+img}">','<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{locale}">','<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',f'<meta name="twitter:description" content="{esc(desc)}">',f'<meta name="twitter:image" content="{BASE+img}">']
    if alt and not has_hreflang:
        en,ar=(url,alt) if not lang.startswith('ar') else (alt,url)
        parts+= [f'<link rel="alternate" hreflang="en" href="{BASE+en}">',f'<link rel="alternate" hreflang="ar" href="{BASE+ar}">',f'<link rel="alternate" hreflang="x-default" href="{BASE+en}">']
    parts+= ['<link rel="stylesheet" href="/assets/portal.css">','<script defer src="/assets/portal.js"></script>',
             f'<script type="application/ld+json">{jsonld(url,lang,title,desc,course,role,modules,img)}</script>']
    cfg={"page":{"path":url,"role":role}}
    if course and modules: cfg["course"]={"id":course['id'],"title":course['title'],"path":course['path'],"modules":modules}
    parts.append(f'<script id="ab-config" type="application/json">{json.dumps(cfg,ensure_ascii=False)}</script>')
    return '\n'.join(parts)

def inject(doc,url,modules,exists):
    """Return the document with portal head/bar/footer injected (idempotent)."""
    for n in('head','bar','footer'): doc=remove_block(doc,n)
    lang=lang_of(doc); title=get_title(doc); desc,has_desc=get_description(doc)
    course,role=course_for(url); alt=alt_lang_url(url,exists)
    has_hreflang='hreflang=' in doc
    head=wrap('head',head_html(url,lang,title,desc,has_desc,course,role,modules,alt,has_hreflang))
    m=re.search(r'</head\s*>',doc,re.I)
    if m: doc=doc[:m.start()]+head+doc[m.start():]
    else:
        m2=re.search(r'<body[^>]*>',doc,re.I)
        if not m2: return doc,False
        doc=doc[:m2.start()]+'<head>'+head+'</head>'+doc[m2.start():]
    bar=wrap('bar',bar_html(url,lang,course,role,alt)+crumbs_html(url,lang,title,course,role))
    m=re.search(r'<body[^>]*>',doc,re.I)
    if not m: return doc,False
    doc=doc[:m.end()]+'\n'+bar+doc[m.end():]
    foot=wrap('footer',footer_html(url,lang,role))
    m=re.search(r'</body\s*>',doc,re.I)
    if m: doc=doc[:m.start()]+foot+doc[m.start():]
    else:
        m=re.search(r'</html\s*>',doc,re.I)
        doc=(doc[:m.start()]+foot+doc[m.start():]) if m else doc+foot
    return doc,True
