#!/usr/bin/env python3
"""Rewrite every src/**/*.html <head> to load fonts + Font Awesome from this origin
instead of Google Fonts / cdnjs. Idempotent — safe to run repeatedly.
See tools/gen_pages.py FONTS/FA for the canonical block new pages get."""
import glob, re, sys

LOCAL_FONTS = ('    <link rel="preload" href="/assets/fonts/inter-400-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
               '    <link rel="preload" href="/assets/fonts/inter-600-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
               '    <link rel="stylesheet" href="/assets/fonts.css">')
LOCAL_FA = '<link rel="stylesheet" href="/assets/fa/all.min.css">'

def rewrite(doc):
    orig = doc
    # 1. Font Awesome cdnjs -> local (any version/path)
    doc = re.sub(r'<link[^>]*cdnjs\.cloudflare\.com/ajax/libs/font-awesome[^>]*>', LOCAL_FA, doc)
    # 2. drop preconnect / dns-prefetch to google font origins
    doc = re.sub(r'[ \t]*<link[^>]*rel="(?:preconnect|dns-prefetch)"[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>\n?', '', doc)
    # 3. any <link ...fonts.googleapis.com...> (stylesheet or preload-swap) -> collapse to local block once
    gf = re.compile(r'[ \t]*<link[^>]*fonts\.googleapis\.com[^>]*>\n?')
    if gf.search(doc):
        first = [True]
        def repl(m):
            if first[0]:
                first[0] = False
                return LOCAL_FONTS + '\n'
            return ''
        doc = gf.sub(repl, doc)
    # 4. strip <noscript> fallbacks that referenced google fonts
    doc = re.sub(r'[ \t]*<noscript><link[^>]*fonts\.googleapis\.com[^>]*></noscript>\n?', '', doc)
    return doc, doc != orig

def main():
    changed = skipped = 0
    for f in glob.glob('src/**/*.html', recursive=True):
        s = open(f, encoding='utf-8').read()
        new, ch = rewrite(s)
        if ch:
            open(f, 'w', encoding='utf-8').write(new); changed += 1
        else:
            skipped += 1
    print(f'{changed} rewritten, {skipped} unchanged')

if __name__ == '__main__':
    main()
