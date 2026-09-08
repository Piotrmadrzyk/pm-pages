"""Read actual built HTML for event tests. This deliberately does not render CSS."""
from html.parser import HTMLParser
from pathlib import Path
import json

class Tree(HTMLParser):
    void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__()
        self.root={'tag':'document','attrs':{},'children':[],'text':''}
        self.stack=[self.root]
    def handle_starttag(self, tag, attrs):
        node={'tag':tag,'attrs':{k:v or '' for k,v in attrs},'children':[],'text':''}
        self.stack[-1]['children'].append(node)
        if tag not in self.void:self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i]['tag']==tag:
                self.stack=self.stack[:i]
                break
    def handle_data(self, data):self.stack[-1]['text']+=data

pages={}
import os
root=Path(os.environ.get('PROBATUM_OUT') or (Path(__file__).resolve().parents[1]/'dist'))
for p in root.rglob('*.html'):
    tree=Tree();tree.feed(p.read_text());pages[str(p.relative_to(root))]=tree.root
print(json.dumps(pages,ensure_ascii=False))
