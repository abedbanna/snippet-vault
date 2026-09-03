"""Compare visible text of live/<page> vs src/<page>; report sentences missing after conversion.
Usage: python3 tools/check_convert.py <relative path, e.g. git.html>"""
import re,sys,os,html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def text(p):
    s=open(p,encoding='utf-8',errors='replace').read()
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S|re.I)
    s=re.sub(r'<!--.*?-->','',s,flags=re.S)
    s=re.sub(r'<[^>]+>','\n',s); s=H.unescape(s)
    return [re.sub(r'\s+',' ',x).strip() for x in s.split('\n') if len(x.strip())>=25]
def scripts(p):
    s=open(p,encoding='utf-8',errors='replace').read()
    return re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>',s,flags=re.S|re.I)
rel=sys.argv[1]; a=os.path.join(ROOT,'live',rel); b=os.path.join(ROOT,'src',rel)
ta=text(a); tb=set(text(b)); joined=' '.join(text(b))
missing=[x for x in ta if x not in tb and x not in joined]
print(f'{rel}: original lines {len(ta)}, missing {len(missing)}')
for m in missing[:40]: print('  MISSING:',m[:140])
# quiz/data sanity: count of question-like strings
qa=len(re.findall(r'\?',open(a,encoding='utf-8',errors='replace').read())); qb=len(re.findall(r'\?',open(b,encoding='utf-8',errors='replace').read()))
print(f'question marks: live {qa} -> src {qb}')
ia=len(re.findall(r'<img',open(a,encoding='utf-8',errors='replace').read(),re.I)); ib=len(re.findall(r'<img',open(b,encoding='utf-8',errors='replace').read(),re.I))
print(f'images: live {ia} -> src {ib}')
sys.exit(1 if len(missing)>max(3,len(ta)*0.02) else 0)
