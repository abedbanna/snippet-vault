"""Generate favicon set, web manifest icons and default OG image from images/logo.png."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'src'); OUT=os.path.join(SRC,'assets'); os.makedirs(OUT,exist_ok=True)
site=json.load(open(os.path.join(ROOT,'site.json')))
logo=Image.open(os.path.join(SRC,'images','logo.png')).convert('RGBA')
alpha=logo.split()[3]
bbox=alpha.getbbox()            # tight bbox of the whole logo
# The square "AT" mark is the left ~28% of the logo's bbox
x0,y0,x1,y1=bbox
mark_box=(x0, y0, x0+int((x1-x0)*0.30), y1)
mark_alpha=alpha.crop(mark_box); mb=mark_alpha.getbbox(); mark_alpha=mark_alpha.crop(mb)
def hex2rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
DARK=hex2rgb(site['brand']['dark']); PRI=hex2rgb(site['brand']['primary'])
def gradient(w,h):
    im=Image.new('RGB',(w,h)); d=ImageDraw.Draw(im)
    for x in range(w):
        t=x/max(w-1,1); c=tuple(int(DARK[i]*(1-t)+PRI[i]*t) for i in range(3)); d.line([(x,0),(x,h)],fill=c)
    return im
def icon(size, radius_frac=0.22, pad_frac=0.16):
    im=gradient(size,size).convert('RGBA')
    mask=Image.new('L',(size,size),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,size-1,size-1],radius=int(size*radius_frac),fill=255)
    im.putalpha(mask)
    inner=int(size*(1-2*pad_frac)); m=mark_alpha.copy(); m.thumbnail((inner,inner),Image.LANCZOS)
    white=Image.new('RGBA',m.size,(255,255,255,255)); white.putalpha(m)
    im.alpha_composite(white,((size-m.width)//2,(size-m.height)//2)); return im
for s in (16,32,48,180,192,512):
    name={180:'apple-touch-icon.png',192:'icon-192.png',512:'icon-512.png'}.get(s,f'favicon-{s}.png')
    icon(s).save(os.path.join(OUT,name))
icon(64).save(os.path.join(SRC,'favicon.ico'),format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64)])
# maskable icon (safe zone) for manifest
icon(512,radius_frac=0.0,pad_frac=0.26).save(os.path.join(OUT,'icon-512-maskable.png'))
# SVG-free logo mark PNG for the portal bar (white on transparent, 64px high)
m=mark_alpha.copy(); m.thumbnail((256,256),Image.LANCZOS); w=Image.new('RGBA',m.size,(255,255,255,255)); w.putalpha(m); w.save(os.path.join(OUT,'mark-white.png'))
# Default Open Graph image 1200x630
og=gradient(1200,630).convert('RGBA')
full=logo.crop(bbox); fa=full.split()[3]; full_w=Image.new('RGBA',full.size,(255,255,255,255)); full_w.putalpha(fa)
full_w.thumbnail((720,260),Image.LANCZOS); og.alpha_composite(full_w,(80,120))
d=ImageDraw.Draw(og)
try: f1=ImageFont.load_default(size=40); f2=ImageFont.load_default(size=28)
except TypeError: f1=f2=ImageFont.load_default()
import textwrap
y=410
for line in textwrap.wrap(site['tagline'],46)[:2]:
    d.text((84,y),line,font=f1,fill=(255,255,255,235)); y+=52
d.text((84,y+18),site['url'].replace('https://',''),font=f2,fill=(232,234,246,200))
og.convert('RGB').save(os.path.join(OUT,'og-default.png'),optimize=True)
manifest={"name":site['name'],"short_name":site['short_name'],"start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":site['brand']['dark'],
 "icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png"},{"src":"/assets/icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}
json.dump(manifest,open(os.path.join(SRC,'site.webmanifest'),'w'),indent=2)
print("icons written:", sorted(os.listdir(OUT)))
