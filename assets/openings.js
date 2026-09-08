/* One finite opening; no loops, hidden-tab work or dependency downloads. */
(() => {
 const reduce=matchMedia('(prefers-reduced-motion: reduce)'),connection=navigator.connection;
 const quiet=()=>reduce.matches||!!connection?.saveData;
 document.querySelectorAll('[data-opening-motion]').forEach(scene=>{
  const button=scene.querySelector('[data-opening-toggle]');
  let visible=false,started=false,ended=false,userPaused=false;
  const animations=()=>scene.getAnimations?.({subtree:true})||[];
  const update=()=>{
   const paused=userPaused||!visible||document.hidden;
   scene.classList.toggle('motion-paused',paused);
   animations().forEach(a=>{if(a.playState==='finished')return;if(paused)a.pause();else if(a.playState==='paused')a.play();});
   if(button){button.textContent=ended?'Powtórz ruch':paused?'Wznów ruch':'Wstrzymaj ruch';button.setAttribute('aria-label',ended?'Powtórz animację otwarcia':paused?'Wznów animację otwarcia':'Wstrzymaj animację otwarcia');}
  };
  const start=()=>{
   started=true;ended=false;scene.classList.remove('motion-complete');scene.classList.add('motion-ready');
   requestAnimationFrame(()=>requestAnimationFrame(()=>{scene.classList.add('motion-running');update();}));
  };
  scene.addEventListener('animationend',event=>{
   if(['opening-travel','resonance-flight','social-flight','photo-enter-2','insight-focus','encounter-arrival'].includes(event.animationName)){
    ended=true;scene.classList.add('motion-complete');if(button){button.textContent='Powtórz ruch';button.setAttribute('aria-label','Powtórz animację otwarcia');}
   }
  });
  if(button){button.hidden=false;button.textContent='Odtwórz ruch';button.addEventListener('click',()=>{
   if(!started||ended){scene.classList.remove('motion-running','motion-ready');userPaused=false;start();}
   else{userPaused=!userPaused;update();}
  });}
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>entries.forEach(e=>{
   visible=e.isIntersecting&&e.intersectionRatio>=.15;
   if(visible&&!started&&!quiet())start();else if(started&&!ended)update();
  }),{threshold:[0,.15]}).observe(scene);
  else{visible=true;if(!quiet())start();}
  document.addEventListener('visibilitychange',()=>{if(started&&!ended)update();});
  const stop=()=>{if(quiet()){ended=true;scene.classList.remove('motion-running','motion-ready','motion-paused');scene.classList.add('motion-complete');animations().forEach(a=>a.cancel());if(button)button.textContent='Odtwórz ruch';}};
  reduce.addEventListener?.('change',stop);connection?.addEventListener?.('change',stop);
 });
})();
