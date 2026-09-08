// Behavior checks on generated HTML with mocked browser APIs. No visual QA claim.
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict'),path=require('path'),cp=require('child_process');
const root=path.resolve(__dirname,'..');
const out=process.env.PROBATUM_OUT||path.join(root,'dist');
const fixtures=JSON.parse(cp.execFileSync('python3',[path.join(__dirname,'dom-fixtures.py')],{maxBuffer:8*1024*1024}));
class El {
 constructor(node={tag:'div',attrs:{},children:[]},parent=null){
  this.tag=node.tag;this.attrs={...node.attrs};this.parent=parent;this.children=node.children.map(n=>new El(n,this));this.text=node.text||'';this.events={};this.hidden='hidden'in this.attrs;this.style={setProperty(k,v){this[k]=v}};this.dataset={};
  for(const[k,v]of Object.entries(this.attrs))if(k.startsWith('data-'))this.dataset[k.slice(5).replace(/-([a-z])/g,(_,x)=>x.toUpperCase())]=v;
  this.classList={contains:c=>(this.attrs.class||'').split(' ').includes(c),toggle:(c,on)=>{const set=new Set((this.attrs.class||'').split(' '));on?set.add(c):set.delete(c);this.attrs.class=[...set].join(' ')},add:(...c)=>c.forEach(x=>this.classList.toggle(x,true)),remove:(...c)=>c.forEach(x=>this.classList.toggle(x,false))};
  if(this.tag==='video'){this.paused=true;this.currentTime=0;this.duration=10;this.load=()=>this.loads=(this.loads||0)+1;this.play=()=>{this.paused=false;return Promise.resolve()};this.pause=()=>{this.paused=true}};
 }
 matches(selector){
  return selector.split(',').some(s=>{s=s.trim();if(s.startsWith('.'))return this.classList.contains(s.slice(1));if(s.startsWith('[')){const m=s.match(/^\[([^=\]]+)(?:="([^"]*)")?\]$/);return m&&(m[2]===undefined?m[1]in this.attrs:this.attrs[m[1]]===m[2]);}return this.tag===s;});
 }
 querySelectorAll(s){return this.children.flatMap(c=>[...(c.matches(s)?[c]:[]),...c.querySelectorAll(s)]);}
 querySelector(s){return this.querySelectorAll(s)[0]||null;}
 closest(s){return this.matches(s)?this:this.parent?.closest(s)||null;}
 setAttribute(k,v){this.attrs[k]=String(v)}getAttribute(k){return this.attrs[k]}
 get textContent(){return this.text+this.children.map(c=>c.textContent).join('')}set textContent(v){this.text=v;this.children=[]}
 set innerHTML(v){this.text=v;this.children=[]}
 addEventListener(k,f){(this.events[k]??=[]).push(f)}
 emit(k,e={}){return Promise.all((this.events[k]||[]).map(f=>f({target:this,...e})));}
 dispatchEvent(e){this.emit(e.type,e)}
 replaceChildren(...children){this.children=children;children.forEach(c=>c.parent=this)}append(child){child.parent=this;this.children.push(child)}
 focus(){this.focused=true}select(){this.selected=true}
 getBoundingClientRect(){return{left:0,top:0,width:1200,height:700}}
}
function setup(page,opts={}){
 const doc=new El(fixtures[page]),timers=new Map(),frames=new Map(),observers=new Map(),media=new Map();let tid=0,rid=0;
 doc.body=doc.querySelector('body');doc.documentElement=doc.querySelector('html');doc.documentElement.scrollHeight=3500;doc.createElement=tag=>new El({tag,attrs:{},children:[]});doc.hidden=false;
 const pref={matches:!!opts.reduced,addEventListener(k,f){this.change=f}},conn={saveData:!!opts.saveData,addEventListener(k,f){this.change=f}};
 const ctx={document:doc,navigator:{connection:conn,clipboard:{writeText:async text=>{ctx.copied=text}}},console,CustomEvent:class{constructor(type,options){this.type=type;this.detail=options.detail}},matchMedia:q=>q.includes('prefers-reduced')?pref:{matches:q.includes('max-width')?!!opts.mobile:false},setTimeout:f=>{timers.set(++tid,f);return tid},clearTimeout:i=>timers.delete(i),requestAnimationFrame:f=>{frames.set(++rid,f);return rid},cancelAnimationFrame:i=>frames.delete(i),IntersectionObserver:class{constructor(f){this.f=f}observe(el){observers.set(el,this.f)}},innerHeight:800,scrollY:0,addEventListener:()=>{}};
 ctx.window=ctx;vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(out,'assets/studio.js'),'utf8'),ctx);
 return{doc,ctx,pref,conn,timers,frames,visible(el,value){assert(observers.has(el),'Scene is observed');observers.get(el)([{isIntersecting:value,intersectionRatio:value?1:0}]);},tick(){const next=timers.entries().next().value;assert(next,'A finite step is scheduled');timers.delete(next[0]);next[1]()},flush(){let limit=20;while(frames.size&&limit--){const current=[...frames.values()];frames.clear();current.forEach(f=>f())}assert.equal(frames.size,0,'No perpetual rAF loop while idle')}};
}
const q=(x,s)=>x.doc.querySelector(s);
const micro=async()=>{await Promise.resolve();await Promise.resolve()};
(async()=>{
 // The website assembles only in view, stops once, and leaves the final real link usable.
 let x=setup('strony-www.html'),scene=q(x,'[data-sequence]'),stage=q(x,'.build-stage'),surface=q(x,'.architecture-canvas'),video=q(x,'video'),play=q(x,'[data-sequence-play]');
 assert.equal(scene.dataset.step,'0');assert(!video.src);x.visible(surface,true);assert(!video.src,'Film waits for the final composition');
 x.visible(stage,true);x.tick();assert.equal(scene.dataset.step,'1');x.visible(stage,false);assert.equal(x.timers.size,0,'No background sequencing offscreen');
 x.visible(stage,true);x.tick();assert.equal(scene.dataset.step,'2');x.tick();assert.equal(scene.dataset.step,'3');await micro();
 assert.equal(x.timers.size,0,'Sequence does not loop');assert(!video.paused);assert(video.src.endsWith('architecture-desktop.mp4'));
 assert(video.classList.contains('is-playing'));assert.equal(q(x,'.architecture-link').getAttribute('href'),'/horyzont.html');
 x.visible(surface,false);assert(video.paused);x.visible(surface,true);await micro();assert(!video.paused);
 x.doc.hidden=true;await x.doc.emit('visibilitychange');assert(video.paused);x.doc.hidden=false;await x.doc.emit('visibilitychange');await micro();assert(!video.paused);
 await q(x,'[data-film-toggle]').emit('click');assert(video.paused);x.visible(surface,false);x.visible(surface,true);assert(video.paused,'Explicit video pause survives visibility changes');
 await play.emit('click');assert.equal(scene.dataset.step,'0');await play.emit('click');assert.equal(x.timers.size,0);x.visible(stage,false);x.visible(stage,true);assert.equal(x.timers.size,0,'Explicit sequence pause survives visibility');
 await scene.querySelector('[data-sequence-step="2"]').emit('click');assert.equal(scene.dataset.step,'2');assert.equal(x.timers.size,0);x.flush();

 // Automatic loading respects motion and data preferences; explicit playback still works.
 for(const option of [{reduced:true},{saveData:true}]){
  x=setup('horyzont.html',option);surface=q(x,'.concept-home');video=q(x,'video');x.visible(surface,true);assert(!video.src);
  await q(x,'[data-film-toggle]').emit('click');await micro();assert(!video.paused);assert(video.src);
  video.paused=true;await video.emit('ended');x.visible(surface,false);x.visible(surface,true);assert(video.paused,'No automatic film loop');
  await q(x,'[data-film-toggle]').emit('click');await micro();assert.equal(video.currentTime,0);assert(!video.paused);
 }
 x=setup('horyzont.html',{mobile:true});x.visible(q(x,'.concept-home'),true);await micro();assert(q(x,'video').src.endsWith('architecture-mobile.mp4'));
 x.pref.matches=true;x.pref.change();assert(q(x,'video').paused,'Changed preference pauses media');
 x=setup('horyzont.html');video=q(x,'video');video.play=()=>Promise.reject(new Error('Autoplay blocked'));x.visible(q(x,'.concept-home'),true);await micro();assert(!q(x,'[data-film-toggle]').hidden);assert(!video.classList.contains('is-playing'));
 await video.emit('error');assert(q(x,'[data-film-toggle]').disabled,'Failure retains still image');
 // A rejected old play request cannot cancel a later successful manual retry.
 x=setup('horyzont.html');surface=q(x,'.concept-home');video=q(x,'video');let rejectOld;
 video.play=()=>new Promise((_,r)=>rejectOld=r);x.visible(surface,true);x.visible(surface,false);video.play=()=>{video.paused=false;return Promise.resolve()};x.visible(surface,true);await micro();rejectOld(new Error('Old request'));await micro();assert(!video.paused);

 x=setup('marketing.html');scene=q(x,'[data-sequence]');assert(q(x,'.campaign-wide').inert);assert(q(x,'.campaign-phone').inert);
 await scene.querySelector('[data-sequence-step="1"]').emit('click');assert(!q(x,'.campaign-wide').inert);assert(q(x,'.campaign-phone').inert);
 await scene.querySelector('[data-sequence-step="2"]').emit('click');assert(!q(x,'.campaign-phone').inert);

 // Intent survives the journey from interactive offer to contact.
 x=setup('oferta.html');const contactTree=new El(fixtures['kontakt.html']);
 for(const button of x.doc.querySelectorAll('[data-offer-option]')){
  await button.emit('click');const href=q(x,'[data-offer-contact]').href,topic=new URL(href,'https://example.test').searchParams.get('temat');
  assert(contactTree.querySelectorAll('input').some(i=>i.attrs.name==='usluga'&&i.attrs.value===topic),'Every offer has a selectable contact intent');
  assert(q(x,'[data-offer-more]').href);assert(q(x,'[data-offer-announcement]').textContent.length>20);
 }
 x.flush();
 // Real user-triggered clipboard action with a usable permission-denied fallback.
 x=setup('akademia.html');await q(x,'[data-prompt-option="research"]').emit('click');await q(x,'[data-prompt-copy]').emit('click');assert(x.ctx.copied.includes('research'));assert(x.ctx.copied.includes('Nie wymyślaj'));
 x.ctx.navigator.clipboard.writeText=async()=>{throw new Error('Denied')};await q(x,'[data-prompt-copy]').emit('click');assert(!q(x,'[data-prompt-export]').hidden);assert(q(x,'[data-prompt-export]').selected);x.flush();
 // No external iframe requests until an explicit click. Closing releases the frame.
 x=setup('realizacje.html');assert.equal(x.doc.querySelectorAll('iframe').length,0);
 for(const preview of x.doc.querySelectorAll('[data-live-site]')){
  const open=preview.querySelector('[data-open-live]');await open.emit('click');const iframe=preview.querySelector('iframe');assert.equal(iframe.src,preview.dataset.siteUrl);assert(iframe.title);assert.equal(open.getAttribute('aria-expanded'),'true');
  await iframe.emit('load');assert(preview.querySelector('[data-frame-status]').textContent.includes('Jeśli'),'Load is not presented as verified cross-origin rendering');
  await open.emit('click');assert.equal(preview.querySelectorAll('iframe').length,0);assert(preview.querySelector('.live-site-frame').hidden);
 }
 // Evaluate all pages: a missing optional widget must not break the shared script.
 for(const page of Object.keys(fixtures)){x=setup(page);x.flush()}
 console.log('PASS: '+Object.keys(fixtures).length+'-page script initialization; finite sequencing, manual controls, visibility, video/data preferences, mobile media source, failure and stale-request handling; offer→contact intents; clipboard/fallback; opt-in external previews. Mocked DOM only, no browser rendering.');
})().catch(error=>{console.error(error);process.exitCode=1});
