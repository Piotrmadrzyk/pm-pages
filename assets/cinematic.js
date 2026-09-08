(() => {
  'use strict';
  const q = (s, root = document) => root.querySelector(s);
  const qa = (s, root = document) => [...root.querySelectorAll(s)];
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  const clamp = (n, min = 0, max = 1) => Math.min(max, Math.max(min, n));
  const mediaSource = v => matchMedia('(max-width:700px)').matches ? v.dataset.small : v.dataset.desktop;
  const watch = (element, callback, options = {}) => {
    if (!('IntersectionObserver' in window)) { callback(true); return; }
    const observer = new IntersectionObserver(entries => entries.forEach(entry => callback(entry.isIntersecting)), options);
    observer.observe(element);
  };

  qa('[data-live-projects]').forEach(section => {
    qa('[data-postcard-stage]', section).forEach(stage => watch(stage, visible => {
      if (visible) stage.classList.add('is-visible');
    }, {threshold: .2}));
    qa('[data-history-toggle]', section).forEach(button => {
      const card = button.closest('[data-case]');
      const photograph = q('[data-history-photo]', card);
      button.addEventListener('click', () => {
        const active = button.getAttribute('aria-pressed') !== 'true';
        button.setAttribute('aria-pressed', String(active));
        photograph.classList.toggle('is-colour', active);
        q('.history-original', photograph).setAttribute('aria-hidden', String(active));
        q('.history-colour', photograph).setAttribute('aria-hidden', String(!active));
        q('[data-history-mode]', card).textContent = active ? 'KOLORYZACJA AI' : 'ORYGINAŁ';
        button.innerHTML = `${active ? 'Zobacz oryginał' : 'Ożyw kolor'} <span aria-hidden="true"></span>`;
      });
    });
    qa('[data-postcard-flip]', section).forEach(button => {
      const card = button.closest('[data-case]');
      button.addEventListener('click', () => {
        const flipped = button.getAttribute('aria-pressed') !== 'true';
        q('[data-postcard-turn]', card).classList.toggle('is-flipped', flipped);
        q('[data-postcard-front]', card).setAttribute('aria-hidden', String(flipped));
        q('[data-postcard-back]', card).setAttribute('aria-hidden', String(!flipped));
        button.setAttribute('aria-pressed', String(flipped));
        button.innerHTML = `${flipped ? 'Pokaż awers' : 'Odwróć pocztówkę'} <span aria-hidden="true">↻</span>`;
        q('[data-postcard-side]', card).textContent = flipped ? 'Rewers · Druga strona tej samej pocztówki' : 'Awers · Barbakan i Brama Floriańska';
      });
    });
  });

  const spring = q('[data-spring-opening]');
  if (spring) {
    const video = q('[data-spring-video]', spring);
    const button = q('[data-spring-toggle]', spring);
    button.hidden = false;
    let inView = true, started = false, interrupted = false;
    const label = () => {
      button.innerHTML = `${video.paused ? (started && !video.ended ? 'Wznów przemianę' : 'Odtwórz przemianę') : 'Wstrzymaj ruch'} <span aria-hidden="true">${video.paused ? '▶' : 'Ⅱ'}</span>`;
      button.setAttribute('aria-pressed', String(!video.paused));
    };
    const play = () => {
      if (!video.src) {
        video.poster = matchMedia('(max-width:700px)').matches ? '/assets/spring/dormant-mobile.webp' : '/assets/spring/dormant.webp';
        spring.classList.add('video-visible');
        video.src = mediaSource(video);
      }
      if (video.ended) video.currentTime = 0;
      started = true;
      const promise = video.play();
      if (promise) promise.catch(() => { spring.classList.remove('video-visible'); label(); });
    };
    video.addEventListener('playing', () => { spring.classList.add('video-visible'); label(); });
    video.addEventListener('pause', label);
    video.addEventListener('ended', () => { spring.classList.remove('video-visible'); label(); });
    video.addEventListener('error', () => { spring.classList.remove('video-visible'); button.hidden = true; });
    button.addEventListener('click', () => { interrupted = false; video.paused ? play() : video.pause(); });
    watch(spring, visible => {
      inView = visible;
      if (!visible) { interrupted = !video.paused; video.pause(); }
      else if (!motion.matches && !saveData && (!started || interrupted) && !document.hidden) { interrupted = false; play(); }
    }, {threshold: .1});
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) { interrupted = !video.paused; video.pause(); }
      else if (interrupted && inView && !motion.matches) { interrupted = false; play(); }
    });
    motion.addEventListener('change', () => { if (motion.matches) { video.pause(); spring.classList.remove('video-visible'); } });
  }

  const scene = q('[data-restoration]');
  if (!scene) return;
  const video = q('[data-restoration-video]', scene);
  const player = q('[data-restoration-mode]', scene);
  const steps = qa('[data-restoration-step]', scene);
  const chapters = qa('[data-restoration-chapter]', scene);
  const header = q('.site-header');
  const phases = [0, .27, .52, .78];
  let ready = false, visible = false, started = false, resume = false, intended = false, failed = false;
  let currentStage = -1, playRequest = 0;
  const alignScene = () => scene.style.setProperty('--header', `${Math.ceil(header ? header.getBoundingClientRect().height : 90)}px`);
  const setStage = progress => {
    const index = progress < .25 ? 0 : progress < .5 ? 1 : progress < .75 ? 2 : 3;
    if (index === currentStage) return;
    currentStage = index;
    scene.dataset.stage = String(index);
    chapters.forEach((chapter, i) => { chapter.hidden = i !== index; });
    steps.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
  };
  const label = () => {
    const active = intended && !video.ended;
    const text = active ? (ready ? 'Wstrzymaj przemianę' : 'Przygotowuję przemianę…') : video.ended ? 'Odtwórz ponownie' : video.currentTime > 0 ? 'Wznów przemianę' : 'Odtwórz przemianę';
    player.innerHTML = `${text} <span aria-hidden="true">${active ? 'Ⅱ' : '▶'}</span>`;
    player.setAttribute('aria-pressed', String(active));
  };
  const showFilm = () => {
    scene.classList.remove('restoration-static');
    scene.classList.add('restoration-enhanced', 'has-film');
  };
  const play = () => {
    if (failed) return;
    const request = ++playRequest;
    intended = true; started = true; resume = false;
    if (!video.src) {
      video.poster = '/assets/approach/before.webp';
      video.preload = 'auto';
      video.src = mediaSource(video);
      video.load();
    }
    if (video.ended) { video.currentTime = 0; setStage(0); }
    if (ready) showFilm();
    const promise = video.play();
    label();
    if (promise) promise.catch(() => {
      if (request !== playRequest) return;
      if (intended) { intended = false; resume = false; }
      label();
    });
  };
  const pause = () => { playRequest++; intended = false; video.pause(); label(); };
  const interrupt = () => { resume = intended && !video.ended; pause(); };
  const autoPlay = () => {
    if (visible && !document.hidden && !motion.matches && !saveData && (!started || resume)) play();
  };
  video.addEventListener('loadeddata', () => {
    ready = true;
    if (intended && visible && !document.hidden) showFilm();
    label();
  });
  video.addEventListener('playing', () => {
    if (!intended || !visible || document.hidden) { video.pause(); return; }
    ready = true; showFilm(); label();
  });
  video.addEventListener('pause', label);
  video.addEventListener('timeupdate', () => {
    if (ready && video.duration) setStage(clamp(video.currentTime / video.duration));
  });
  video.addEventListener('ended', () => {
    intended = false; resume = false; setStage(1); label();
  });
  video.addEventListener('error', () => {
    failed = true; resume = false; pause();
    scene.classList.remove('restoration-enhanced', 'has-film');
    scene.classList.add('restoration-static');
    player.hidden = true;
  });
  player.addEventListener('click', () => {
    resume = false;
    intended ? pause() : play();
  });
  steps.forEach((button, index) => button.addEventListener('click', () => {
    if (!ready || failed) return;
    resume = false; pause(); showFilm();
    video.currentTime = phases[index] * Math.max(0, video.duration - .045);
    setStage(phases[index]); label();
  }));
  watch(scene, inView => {
    visible = inView;
    if (visible) autoPlay();
    else if (intended) interrupt();
  }, {threshold: .2});
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { if (intended) interrupt(); }
    else autoPlay();
  });
  motion.addEventListener('change', () => {
    if (motion.matches) {
      resume = false; pause();
      scene.classList.remove('restoration-enhanced', 'has-film');
      scene.classList.add('restoration-static');
    } else autoPlay();
  });
  player.hidden = false;
  label(); alignScene();
  window.addEventListener('resize', alignScene, {passive: true});
})();
