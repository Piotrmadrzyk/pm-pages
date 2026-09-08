#!/usr/bin/env python3
"""Validate navigation, assets, labels and generated document structure."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import re, sys

import os
ROOT=Path(os.environ.get('PROBATUM_OUT') or (Path(__file__).parent/'dist'))
errors=[]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.refs=[];self.h1=0;self.main=0;self.title=False;self.description=False
        self.controls=[];self.labels=[];self.label_depth=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='title':self.title=True
        if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
        if tag=='label':
            self.label_depth+=1
            if a.get('for'):self.labels.append(a['for'])
        if tag in ('input','textarea','select') and a.get('type') not in ('hidden','submit'):
            self.controls.append((a,self.label_depth>0))
        for k in ('href','src','poster','data-src','data-mobile','data-site-switch','data-desktop','data-small'):
            if a.get(k):self.refs.append(a[k])
        if tag=='img' and 'alt' not in a:errors.append('Image missing alt')
        if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):errors.append('External tab link missing noopener')
    def handle_endtag(self,tag):
        if tag=='label':self.label_depth=max(0,self.label_depth-1)

pages={}
for path in ROOT.rglob('*.html'):
    p=Page();p.feed(path.read_text());pages[path.resolve()]=p
    name=str(path.relative_to(ROOT))
    if p.h1!=1 or p.main!=1:errors.append(f'{name}: h1={p.h1}, main={p.main}')
    if not p.title or not p.description:errors.append(f'{name}: metadata missing')
    for i,n in Counter(p.ids).items():
        if n>1:errors.append(f'{name}: duplicate id {i}')
    for a,wrapped in p.controls:
        if not wrapped and not a.get('aria-label') and a.get('id') not in p.labels:errors.append(f'{name}: unlabeled input {a.get("name")}')

for path,p in pages.items():
    for ref in p.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else path.parent/u.path if u.path else path
        if target.is_dir():target/='index.html'
        target=target.resolve()
        if not target.exists():errors.append(f'{path.name}: missing {ref}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{path.name}: missing anchor {ref}')

for css in (ROOT/'assets').glob('*.css'):
    for ref in re.findall(r'url\([\'"]?([^\)\'"\s]+)',css.read_text()):
        if ref.startswith(('http','data:')):continue
        target=ROOT/ref.lstrip('/') if ref.startswith('/') else css.parent/ref
        if not target.exists():errors.append(f'{css.name}: missing {ref}')

if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} pages, local links, fragments, assets, unique IDs, headings and input labels.')
