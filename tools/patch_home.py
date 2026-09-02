"""One-off, idempotent content fixes to src/index.html (portal home)."""
import os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import portal_lib as P
p=os.path.join(P.ROOT,'src','index.html'); s=open(p,encoding='utf-8').read(); o=s
S=P.SITE; A=S['author']
# 1. Title + description
s=s.replace('<title>Al-banna Tutorials | Advanced AI Learning Platform</title>','<title>Al-banna Tutorials | Free Courses in AI, Deep Learning, DevOps, Robotics & Quantum</title>')
if 'name="description"' not in s:
    s=s.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">','<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <meta name="description" content="%s">'%S['description'].replace('"','&quot;'),1)
# 2. Bootstrap alpha -> stable
s=s.replace('bootstrap@5.3.0-alpha1','bootstrap@5.3.3')
# 3. Brand link goes home, nav gets Courses + About
s=s.replace('<a class="navbar-brand" href="#">','<a class="navbar-brand" href="/">')
s=s.replace('<a class="nav-link active" href="#">Home</a>','<a class="nav-link active" href="/">Home</a>')
if 'href="courses.html">Courses' not in s:
    s=s.replace('<a class="nav-link" href="#tutorials">Tutorials</a>','<a class="nav-link" href="#tutorials">Tutorials</a>\n                    </li>\n                    <li class="nav-item">\n                        <a class="nav-link" href="courses.html">Courses</a>',1)
if 'href="about.html">About' not in s:
    s=s.replace('<a class="nav-link" href="profile.html">Albanna</a>','<a class="nav-link" href="about.html">About</a>',1)
# 4. Wrong link: Quantum Computing card pointed at vibe-coding-courses.html
s=re.sub(r'(Quantum Computing.{0,1500}?)href="vibe-coding-courses\.html"',r'\1href="quantum-courses.html"',s,count=1,flags=re.S)
# 5. Coming soon -> dated
s=s.replace('Coming Soon','Coming 2026 Q4').replace('Coming soon','Coming 2026 Q4').replace('coming soon','coming 2026 Q4')
# 6. Replace the old footer with a professional one (portal footer strip is injected separately; this is the home's own)
new_footer=f'''<footer>
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <h5>About Al-banna Tutorials</h5>
                    <p>{S['tagline']}. Written by <a href="{A['profile']}">{A['name']}</a>, {A['title']}, and used in university teaching and by self-learners worldwide.</p>
                    <a href="about.html" class="btn btn-sm btn-outline-light mt-1">About the portal</a>
                </div>
                <div class="col-md-4 mb-4">
                    <h5>Quick Links</h5>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="courses.html">All Courses &amp; Tutorials</a></li>
                        <li><a href="roadmaps/">Learning Roadmaps</a></li>
                        <li><a href="search.html">Search</a></li>
                        <li><a href="about.html">About</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-4">
                    <h5>Connect</h5>
                    <div class="social-icons">
                        <a href="{A['github']}" class="text-white" target="_blank" rel="noopener" title="GitHub"><i class="fab fa-github"></i></a>
                        <a href="{A['scholar']}" class="text-white" target="_blank" rel="noopener" title="Google Scholar"><i class="fas fa-graduation-cap"></i></a>
                        <a href="{A['orcid']}" class="text-white" target="_blank" rel="noopener" title="ORCID"><i class="fab fa-orcid"></i></a>
                        <a href="{A['huggingface']}" class="text-white" target="_blank" rel="noopener" title="Hugging Face"><i class="fas fa-face-smile"></i></a>
                        <a href="mailto:{A['email']}" class="text-white" title="Email"><i class="fas fa-envelope"></i></a>
                        <!-- TODO: LinkedIn / YouTube / X links (set in site.json and add here) -->
                    </div>
                    <p class="mt-3 mb-0 small"><i class="fas fa-envelope me-1"></i> <a href="mailto:{A['email']}">{A['email']}</a></p>
                </div>
            </div>
            <div class="text-center mt-4 pt-3 border-top border-secondary">
                <p class="text-muted mb-0">&copy; <span class="ab-year">2026</span> Al-banna Tutorials. All Rights Reserved. &nbsp;·&nbsp; <a href="privacy.html">Privacy</a> &nbsp;·&nbsp; <a href="terms.html">Terms</a> &nbsp;·&nbsp; <a href="sitemap.xml">Sitemap</a></p>
            </div>
        </div>
    </footer>'''
s=re.sub(r'<footer>.*?</footer>',lambda m:new_footer,s,count=1,flags=re.S)
open(p,'w',encoding='utf-8').write(s)
print('home patched; changed:',s!=o)
