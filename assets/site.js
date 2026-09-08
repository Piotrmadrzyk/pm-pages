/* Probatum | progressive enhancement; no external runtime dependencies. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const menuButton = $('.menu-button');
  const menu = $('#mobile-menu');
  function closeMenu(restore = false) {
    if (!menu || !menuButton) return;
    menu.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Otwórz menu');
    document.body.classList.remove('menu-open');
    if (restore) menuButton.focus();
  }
  menuButton?.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menu.hidden = !open;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
    document.body.classList.toggle('menu-open', open);
    if (open) $('a', menu)?.focus();
  });
  $$('a', menu || document.createElement('div')).forEach(a => a.addEventListener('click', () => closeMenu()));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu && !menu.hidden) closeMenu(true);
    if (e.key === 'Tab' && menu && !menu.hidden) {
      const links = $$('a', menu);
      if (!e.shiftKey && document.activeElement === links.at(-1)) { e.preventDefault(); menuButton.focus(); }
      if (e.shiftKey && document.activeElement === menuButton) { e.preventDefault(); links.at(-1)?.focus(); }
    }
  });
  window.matchMedia('(min-width: 951px)').addEventListener('change', e => { if (e.matches) closeMenu(); });

  if ('IntersectionObserver' in window && !reduced.matches) {
    document.documentElement.classList.add('reveal-ready');
    const reveal = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); reveal.unobserve(e.target); }
    }), { threshold: .07 });
    $$('[data-reveal]').forEach(el => reveal.observe(el));
    // Content remains available even if an observer is delayed in a background tab.
    setTimeout(() => document.documentElement.classList.remove('reveal-ready'), 12000);
  }

  const scenarios = {
    poczta: { input: '„Dzień dobry, chcę zapytać o ofertę dla mojej firmy…”', source: 'Nowa wiadomość e-mail', action: 'Rozpoznaje temat, porządkuje informacje i przygotowuje szkic odpowiedzi.', result: 'Gotową propozycję odpowiedzi.', detail: 'Czytasz, poprawiasz i decydujesz, co wysłać.' },
    klient: { input: 'Nowy klient zaakceptował zakres współpracy. Co trzeba przygotować?', source: 'Dane nowego klienta', action: 'Zapisuje dane klienta i tworzy uporządkowaną listę zadań na rozpoczęcie współpracy.', result: 'Jasny plan rozpoczęcia projektu.', detail: 'Widzisz, co trzeba zrobić, zamiast kompletować ustalenia w kilku miejscach.' },
    raport: { input: 'Co wydarzyło się w firmie w ostatnim tygodniu?', source: 'Dane z podłączonych procesów', action: 'Zbiera informacje o zapytaniach, zadaniach i statusach w jedno podsumowanie.', result: 'Podsumowanie na Twoim telefonie.', detail: 'Dostajesz raport w Telegramie. Szybciej widzisz, co wymaga Twojej uwagi.' }
  };
  $$('[data-agent-demo]').forEach(demo => {
    let timers = [];
    const clear = () => { timers.forEach(clearTimeout); timers = []; delete demo.dataset.stage; const b = $('[data-play-agent]', demo); if(b) b.disabled = false; };
    const choose = (key, focus = false) => {
      clear(); const data = scenarios[key]; if(!data) return;
      $$('[data-agent]', demo).forEach(t => {
        const selected = t.dataset.agent === key;
        t.setAttribute('aria-selected', String(selected)); t.tabIndex = selected ? 0 : -1;
        if (selected && focus) t.focus();
      });
      $('#agent-panel', demo).setAttribute('aria-labelledby', `tab-${key}`);
      Object.entries(data).forEach(([k,v]) => { const el = $(`[data-agent-${k}]`, demo); if(el) el.textContent = v; });
    };
    $$('[data-agent]', demo).forEach((b,i,buttons) => {
      b.addEventListener('click', () => choose(b.dataset.agent));
      b.addEventListener('keydown', e => {
        let n = i;
        if(e.key==='ArrowRight') n=(i+1)%buttons.length;
        else if(e.key==='ArrowLeft') n=(i-1+buttons.length)%buttons.length;
        else if(e.key==='Home') n=0;
        else if(e.key==='End') n=buttons.length-1;
        else return;
        e.preventDefault(); choose(buttons[n].dataset.agent, true);
      });
    });
    $('[data-play-agent]',demo)?.addEventListener('click', () => {
      clear(); const b=$('[data-play-agent]',demo); b.disabled=true;
      const key=$('[aria-selected=true]',demo)?.dataset.agent || 'poczta';
      const live=$('[data-agent-live]',demo);
      if(reduced.matches) {demo.dataset.stage='3';live.textContent=scenarios[key].result+' '+scenarios[key].detail;b.disabled=false;return;}
      demo.dataset.stage='1';live.textContent='Krok 1. '+scenarios[key].source;
      timers.push(setTimeout(()=>{demo.dataset.stage='2';live.textContent='Krok 2. '+scenarios[key].action;},1200));
      timers.push(setTimeout(()=>{demo.dataset.stage='3';live.textContent='Krok 3. '+scenarios[key].result;},2800));
      timers.push(setTimeout(()=>{clear();},4800));
    });
  });

  $$('[data-project-filter]').forEach(b => b.addEventListener('click', () => {
    const category=b.dataset.projectFilter;
    $$('[data-project-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    let count=0;$$('.project[data-category]').forEach(p=>{p.hidden=category!=='all' && p.dataset.category!==category;if(!p.hidden)count++;});
    const demos=$('[data-demo-collection]');if(demos)demos.hidden=category==='live';
    const status=$('[data-filter-status]');if(status)status.textContent=`Widoczne projekty: ${count}`;
  }));
  $$('[data-site-switch]').forEach(b=>b.addEventListener('click',()=>{
    const img=$('[data-switched-image]');if(!img)return;
    img.src=b.dataset.siteSwitch;img.alt=b.dataset.alt||'';
    $$('[data-site-switch]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    const title=$('[data-switch-name]');if(title)title.textContent=b.textContent;
  }));

  // A real, transparent email handoff. No fake submission or background lead capture.
  const topic = new URLSearchParams(location.search).get('temat');
  if (topic) $$('input[name="usluga"]').forEach(i=>{if(i.value===topic)i.checked=true;});
  $$('form[data-mail-brief]').forEach(form=>{
    const panels=$$('[data-quote-panel]',form);
    let step=0;
    const showStep=()=>{
      panels.forEach((p,i)=>p.hidden=i!==step);
      const label=$('[data-step-label]',form);if(label)label.textContent=`Krok ${step+1} z ${panels.length}`;
      const bar=$('[data-quote-progress]',form);if(bar)bar.style.width=`${(step+1)/panels.length*100}%`;
    };
    if(panels.length){form.classList.add('wizard-ready');showStep();}
    $$('[data-next-step]',form).forEach(b=>b.addEventListener('click',()=>{
      const invalid=$(':invalid',panels[step]);if(invalid){invalid.reportValidity();return;}
      step=Math.min(step+1,panels.length-1);showStep();$('h2',panels[step])?.focus();
    }));
    $$('[data-prev-step]',form).forEach(b=>b.addEventListener('click',()=>{step=Math.max(0,step-1);showStep();$('h2',panels[step])?.focus();}));
    form.addEventListener('submit',e=>{
      e.preventDefault();
      if(!form.checkValidity()){
        const invalid=$(':invalid',form);
        if(panels.length && invalid){const idx=panels.findIndex(p=>p.contains(invalid));if(idx>=0){step=idx;showStep();}}
        invalid?.reportValidity();return;
      }
      const f=new FormData(form);
      const newsletter=form.dataset.mailBrief==='newsletter';
      const subject=newsletter?'Probatum | materiały o stronach i AI':`Probatum | ${f.get('usluga')||'porozmawiajmy o projekcie'}`;
      const fields=[['Imię','imie'],['E-mail','email'],['Telefon','telefon'],['Firma','firma'],['Obecna strona','www_klienta'],['Usługa','usluga'],['Budżet orientacyjny','budzet'],['Termin','termin'],['Opis','wiadomosc']];
      const message=newsletter?`Proszę o informacje o nowych materiałach Probatum.\nMój e-mail: ${f.get('email')||''}`:fields.filter(([,k])=>f.get(k)).map(([label,k])=>`${label}: ${f.get(k)}`).join('\n\n');
      const status=$('[data-form-result]',form.parentElement);
      if(!status)return;
      status.hidden=false;
      const link=$('[data-mail-link]',status);if(link)link.href=`mailto:kontakt@probatum.pl?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
      const text=$('[data-brief-text]',status);if(text)text.value=message;
      status.scrollIntoView({behavior:reduced.matches?'auto':'smooth',block:'center'});
      status.focus();
    });
  });
  $$('[data-copy-brief]').forEach(b=>b.addEventListener('click',async()=>{
    const text=$('[data-brief-text]',b.closest('[data-form-result]'));if(!text)return;
    try{await navigator.clipboard.writeText(text.value);b.textContent='Skopiowano';}
    catch{ text.focus();text.select();b.textContent='Tekst zaznaczony. Skopiuj go.';}
  }));

  const progress=$('[data-reading-progress]');
  if(progress){const update=()=>{const body=$('.article-body');if(!body)return;const top=body.getBoundingClientRect().top+scrollY;const range=body.offsetHeight-innerHeight*.55;const pct=Math.min(100,Math.max(0,(scrollY-top+innerHeight*.3)/Math.max(1,range)*100));progress.style.width=pct+'%';};addEventListener('scroll',update,{passive:true});addEventListener('resize',update,{passive:true});update();}
})();
