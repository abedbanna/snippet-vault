"""Build: src/ -> dist/ with portal chrome injected, sitemap, robots, search index."""
import os, re, shutil, sys, json, time, datetime, html as H
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import portal_lib as P
ROOT=P.ROOT; SRC=os.path.join(ROOT,'src'); DIST=os.path.join(ROOT,'dist')
NOINDEX={'/404.html','/certificate.html'}

def all_html():
    for dp,dn,fn in os.walk(SRC):
        dn[:]=[d for d in dn if d not in P.SKIP_DIRS and not d.startswith('.')]
        for f in fn:
            if f.endswith('.html'): yield os.path.relpath(os.path.join(dp,f),SRC)

def main():
    if os.path.isdir(DIST): shutil.rmtree(DIST)
    shutil.copytree(SRC,DIST,ignore=shutil.ignore_patterns('.DS_Store','.idea','*.zip'))
    pages=sorted(all_html()); urls={P.rel_url(r) for r in pages}
    def exists(u): return u in urls or (u.endswith('/') and u+'index.html' in {('/'+r.replace(os.sep,'/')) for r in pages})
    mods={c['id']:P.course_modules(SRC,c) for c in P.COURSES}
    index=[]; done=skipped=0; sitemap=[]
    for rel in pages:
        url=P.rel_url(rel); sp=os.path.join(SRC,rel); dp=os.path.join(DIST,rel)
        doc=open(sp,encoding='utf-8',errors='replace').read()
        course,role=P.course_for(url); modules=mods.get(course['id'],[]) if course else []
        out,ok=P.inject(doc,url,modules,exists)
        if not ok: skipped+=1; print('  ! no <body>, left untouched:',rel); continue
        open(dp,'w',encoding='utf-8').write(out); done+=1
        title=P.get_title(doc); desc,_=P.get_description(doc); lang=P.lang_of(doc)
        if url in NOINDEX or rel.split(os.sep)[-1].startswith('_'): continue
        lm=datetime.datetime.fromtimestamp(os.path.getmtime(sp)).strftime('%Y-%m-%d')
        pri='1.0' if role=='home' else '0.9' if role=='course-index' else '0.8' if role=='tutorial' else '0.6'
        alt=P.alt_lang_url(url,exists); sitemap.append((url,lm,pri,alt,lang))
        mb=re.search(r'<body[^>]*>',doc,re.I); body=doc[mb.end():] if mb else doc
        text=P.strip_tags(body)[:400]
        index.append({"t":title,"d":desc,"u":url,"c":course['title'] if course else '',"cid":course['id'] if course else '',"tags":(course or {}).get('tags',[]),"l":lang[:2],"x":text,"r":role})
    # sitemap.xml
    xs=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for url,lm,pri,alt,lang in sitemap:
        xs.append(f'  <url><loc>{P.BASE}{H.escape(url)}</loc><lastmod>{lm}</lastmod><priority>{pri}</priority>')
        if alt:
            en,ar=(url,alt) if not lang.startswith('ar') else (alt,url)
            xs.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{P.BASE}{H.escape(en)}"/><xhtml:link rel="alternate" hreflang="ar" href="{P.BASE}{H.escape(ar)}"/>')
        xs.append('  </url>')
    xs.append('</urlset>')
    open(os.path.join(DIST,'sitemap.xml'),'w',encoding='utf-8').write('\n'.join(xs))
    open(os.path.join(DIST,'robots.txt'),'w').write(f"User-agent: *\nAllow: /\nDisallow: /404.html\nDisallow: /certificate.html\nDisallow: /search.html?\n\nSitemap: {P.BASE}/sitemap.xml\n")
    json.dump(index,open(os.path.join(DIST,'search-index.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    json.dump({c['id']:len(m) for c,m in ((c,mods[c['id']]) for c in P.COURSES)},open(os.path.join(DIST,'assets','module-counts.json'),'w'))
    print(f'built {done} pages ({skipped} skipped) -> dist/ ; sitemap {len(sitemap)} urls ; search index {len(index)} docs')
if __name__=='__main__': main()
