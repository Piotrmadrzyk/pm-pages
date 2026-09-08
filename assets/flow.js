/* Animated public diagrams. No API calls, workflow executions or customer data. */
(() => {
  'use strict';
  const data = window.PROBATUM_FLOWS;
  if (!data) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const narrow = matchMedia('(max-width: 700px)');
  const STARTS = [0, 1600, 5100, 9500];
  const END = 14000;
  const phaseAt = time => STARTS.reduce((phase, start, i) => time >= start ? i : phase, 0);
  const seekTime = phase => phase === 3 ? END : Math.min(STARTS[phase] + 2200, STARTS[phase + 1] - 1);
  const clamp = x => Math.max(0, Math.min(1, x));
  document.querySelectorAll('[data-flow-scene]').forEach(scene => {
    const one = s => scene.querySelector(s);
    const all = s => [...scene.querySelectorAll(s)];
    const pause = one('[data-flow-pause]');
    const replay = one('[data-flow-replay]');
    const live = one('[data-flow-live]');
    let key = scene.dataset.flowScene;
    let elapsed = reduce.matches || navigator.connection?.saveData ? END : 0;
    let stopped = elapsed === END;
    let visible = !('IntersectionObserver' in window);
    let raf = 0, previous = 0, phase = -1, map = null, paths = [];
    let selected = null, decision = '';

    function mapPaths() {
      const panel = one(`[data-flow-panel="${key}"]`);
      map = panel.querySelector(narrow.matches ? '.flow-map-mobile' : '.flow-map-desktop');
      paths = [...map.querySelectorAll('.flow-edge')].map((edge, i) => {
        const line = edge.querySelector('.flow-wire');
        return { edge, line, length: line.getTotalLength(), trace: edge.querySelector('.flow-trace'),
          dot: edge.querySelector('.flow-packet'), halo: edge.querySelector('.flow-packet-halo'),
          stage: Number(edge.dataset.edgeStage), decision: edge.dataset.decision, index: i };
      });
    }
    function caption(title, description, index) {
      one('[data-flow-title]').textContent = title;
      one('[data-flow-description]').textContent = description;
      one('[data-flow-index]').textContent = index;
    }
    function updatePhase(next, force = false) {
      if (next === phase && !force) return;
      phase = next;
      scene.dataset.phase = String(phase);
      one('[data-flow-approval]').hidden = key !== 'poczta' || phase !== 3;
      const value = data[key].phases[phase];
      if (!selected) caption(value[1], value[2], `0${phase + 1} / 04`);
      all('[data-node-stage]').forEach(node => {
        const stage = Number(node.dataset.nodeStage);
        const permitted = !node.dataset.decision || node.dataset.decision === decision;
        node.classList.toggle('is-lit', stage <= phase && permitted);
        node.classList.toggle('is-current', stage === phase && permitted);
      });
      all('[data-flow-step]').forEach((button, i) => {
        button.setAttribute('aria-pressed', String(i === phase));
        button.classList.toggle('is-complete', i < phase);
        button.querySelector('[data-step-label]').textContent = data[key].phases[i][0];
      });
    }
    function paint() {
      updatePhase(phaseAt(elapsed));
      for (const path of paths) {
        const permitted = !path.decision || path.decision === decision;
        const progress = permitted ? clamp((elapsed - STARTS[path.stage]) / 1550) : 0;
        path.trace.style.strokeDashoffset = String(100 - progress * 100);
        path.edge.classList.toggle('is-lit', progress > 0);
        const active = !stopped && progress > .08 && !reduce.matches;
        const distance = ((elapsed / 2100 + path.index * .173) % 1) * Math.max(.01, progress);
        if (active) {
          const p = path.line.getPointAtLength(distance * path.length);
          for (const dot of [path.dot,path.halo]) {
            dot.setAttribute('cx',p.x); dot.setAttribute('cy',p.y);
          }
        }
        path.dot.style.opacity = active ? '1' : '0';
        path.halo.style.opacity = active ? '.18' : '0';
      }
      const sectionStart = STARTS[phase];
      const sectionEnd = STARTS[phase + 1] || END;
      one(`[data-flow-step="${phase}"]`).style.setProperty('--progress', `${clamp((elapsed-sectionStart)/(sectionEnd-sectionStart))*100}%`);
      // One opening camera move, then a steady overview. Mobile keeps every label in view.
      const ease = 1 - Math.pow(1-clamp(elapsed/2800),3);
      const camera = map?.querySelector('.flow-camera');
      if(camera) camera.style.transform = !narrow.matches && scene.dataset.hero === 'true' && !reduce.matches
        ? `translate(${(1-ease)*185}px,${(1-ease)*-17}px) scale(${1+(1-ease)*.25})` : '';
    }
    function controls() {
      const isPaused = stopped || reduce.matches;
      scene.classList.toggle('flow-paused', isPaused || !visible || document.hidden);
      pause.setAttribute('aria-pressed', String(isPaused));
      pause.disabled = reduce.matches;
      replay.disabled = reduce.matches;
      pause.innerHTML = reduce.matches ? 'Ruch ograniczony' : elapsed >= END ? 'Odtwórz <span aria-hidden="true">▶</span>' : stopped ? 'Wznów <span aria-hidden="true">▶</span>' : 'Wstrzymaj <span aria-hidden="true">Ⅱ</span>';
    }
    function frame(now) {
      raf = 0;
      if(stopped || reduce.matches || !visible || document.hidden) {previous = 0;return;}
      if(!previous) previous = now;
      const delta = Math.min(now-previous,100);
      if(delta >= 31 || elapsed === 0) {
        elapsed = Math.min(END, elapsed + delta);
        previous = now;
        paint();
      }
      if(elapsed >= END) {stopped = true; controls(); paint();return;}
      raf = requestAnimationFrame(frame);
    }
    function sync() {
      if(raf) cancelAnimationFrame(raf);
      raf = 0; previous = 0; controls(); paint();
      if(!stopped && !reduce.matches && visible && !document.hidden) raf = requestAnimationFrame(frame);
    }
    function restart() {
      selected = null; decision = '';
      all('[data-flow-decision]').forEach(button=>button.setAttribute('aria-pressed','false'));
      all('[data-node]').forEach(node => node.classList.remove('is-selected'));
      elapsed = reduce.matches ? END : 0;
      stopped = reduce.matches;
      phase = -1;
      sync();
    }
    function choose(next, focus = false) {
      if(!data[next]) return;
      key = next; scene.dataset.flowScene = key;
      all('[data-flow-tab]').forEach(tab => {
        const chosen = tab.dataset.flowTab === key;
        tab.setAttribute('aria-selected', String(chosen)); tab.tabIndex = chosen ? 0 : -1;
        if(chosen && focus) tab.focus();
      });
      all('[data-flow-panel]').forEach(panel => panel.hidden = panel.dataset.flowPanel !== key);
      mapPaths(); restart();
      live.textContent = `Wybrany proces: ${one('[aria-selected="true"]').textContent.trim()}. ${data[key].phases[0][1]}`;
    }
    all('[data-flow-tab]').forEach((tab,i,tabs) => {
      tab.addEventListener('click',()=>choose(tab.dataset.flowTab));
      tab.addEventListener('keydown',e=>{
        const next = e.key==='ArrowRight' ? (i+1)%tabs.length : e.key==='ArrowLeft' ? (i-1+tabs.length)%tabs.length : e.key==='Home' ? 0 : e.key==='End' ? tabs.length-1 : null;
        if(next!==null) {e.preventDefault();choose(tabs[next].dataset.flowTab,true);}
      });
    });
    pause.addEventListener('click',()=>{
      if(elapsed >= END) restart();
      else {stopped = !stopped; sync();}
    });
    replay.addEventListener('click',restart);
    all('[data-flow-decision]').forEach(button=>button.addEventListener('click',()=>{
      decision = button.dataset.flowDecision;
      selected = decision;
      all('[data-flow-decision]').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));
      const title = decision==='send' ? 'Zgoda uruchamia wysyłkę.' : 'Brak zgody. Wysyłka zatrzymana.';
      const description = decision==='send' ? 'W tym przykładzie zatwierdzona odpowiedź przechodzi do wysyłki. To pokaz. Wiadomość nie jest wysyłana.' : 'Odrzucenie zatrzymuje odpowiedź. Możesz poprawić szkic i ponownie go ocenić.';
      caption(title,description,'TWOJA DECYZJA');
      elapsed = reduce.matches ? END : STARTS[3]+50;
      stopped = reduce.matches;
      updatePhase(3,true); sync();live.textContent=title+' '+description;
    }));
    all('[data-flow-step]').forEach(button=>button.addEventListener('click',()=>{
      selected = null;
      all('[data-node]').forEach(node=>node.classList.remove('is-selected'));
      const index = Number(button.dataset.flowStep);
      elapsed = seekTime(index);
      stopped = true; updatePhase(index,true); sync();
      live.textContent = `${data[key].phases[index][1]} ${data[key].phases[index][2]}`;
    }));
    all('[data-node]').forEach(node=>{
      function inspect() {
        selected = node.dataset.node;
        const value = data[key].nodes[selected];
        elapsed = seekTime(value.stage);
        stopped = true;
        all('[data-node]').forEach(other=>other.classList.toggle('is-selected',other.dataset.node===selected));
        caption(value.title,value.detail,'WYBRANY ETAP');
        sync(); live.textContent = `${value.title}. ${value.detail}`;
      }
      node.addEventListener('click',inspect);
      node.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' ') {event.preventDefault();inspect();}});
    });
    if('IntersectionObserver' in window) new IntersectionObserver(entries=>{
      visible = entries[0].isIntersecting; sync();
    },{threshold:.08}).observe(scene);
    document.addEventListener('visibilitychange',sync);
    narrow.addEventListener('change',()=>{mapPaths();sync();});
    reduce.addEventListener('change',()=>{
      if(reduce.matches) {elapsed = END; stopped = true;selected = null;phase = -1;}
      sync();
    });
    mapPaths(); scene.classList.add('flow-ready'); sync();
  });
})();
