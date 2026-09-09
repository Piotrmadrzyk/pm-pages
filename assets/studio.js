/* Finite demonstrations. Real links. No background work when a scene is hidden. */
(() => {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const quiet = () => reduce.matches || !!connection?.saveData;
  const all = (selector, root = document) => [...root.querySelectorAll(selector)];
  const onPreference = callback => {
    reduce.addEventListener?.('change', callback);
    connection?.addEventListener?.('change', callback);
  };
  const observe = (element, callback, threshold = .2) => {
    if (!('IntersectionObserver' in window)) { callback(true); return; }
    new IntersectionObserver(entries => entries.forEach(entry => callback(entry.isIntersecting && entry.intersectionRatio >= threshold)), {threshold: [0, threshold]}).observe(element);
  };

  all('[data-sequence]').forEach(root => {
    const count = Number(root.dataset.count);
    const duration = Number(root.dataset.duration) || 2200;
    const buttons = all('[data-sequence-step]', root);
    const play = root.querySelector('[data-sequence-play]');
    if (!play || buttons.length !== count) return;
    let step = quiet() ? count - 1 : 0;
    let timer = 0, visible = false, started = false, running = false, manualPause = false;
    const update = () => {
      root.dataset.step = String(step);
      buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === step)));
      const wide = root.querySelector('.campaign-wide'), phone = root.querySelector('.campaign-phone');
      if (wide) wide.inert = step < 1;
      if (phone) phone.inert = step < 2;
      play.textContent = running ? 'Wstrzymaj pokaz Ⅱ' : step === count - 1 || !started ? 'Odtwórz przemianę ▶' : 'Wznów pokaz ▶';
      root.dispatchEvent(new CustomEvent('studio:stage', {detail: {step, final: step === count - 1}}));
    };
    const halt = () => { clearTimeout(timer); timer = 0; running = false; update(); };
    const schedule = () => {
      clearTimeout(timer);
      if (!visible || document.hidden || manualPause) { halt(); return; }
      running = true; update();
      timer = setTimeout(() => {
        if (step < count - 1) { step++; update(); }
        if (step === count - 1) halt(); else schedule();
      }, duration);
    };
    const resume = () => {
      if (!visible || document.hidden || manualPause || quiet()) return;
      if (!started) { started = true; schedule(); }
      else if (step < count - 1) schedule();
    };
    root.classList.add('sequence-ready', 'sequence-initial');
    root.querySelector('.sequence-controls').hidden = false;
    play.hidden = false; update();
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('sequence-initial')));
    buttons.forEach((button, i) => button.addEventListener('click', () => {
      manualPause = true; started = true; step = i; halt();
    }));
    play.addEventListener('click', () => {
      if (running) { manualPause = true; halt(); return; }
      manualPause = false; started = true;
      if (step === count - 1) step = 0;
      visible = true; schedule();
    });
    root.addEventListener('focusin', event => {
      if (running && event.target !== play) { manualPause = true; halt(); }
    });
    observe(root.querySelector('.build-stage, .campaign-canvas') || root, active => {
      visible = active;
      if (active) resume(); else halt();
    }, .55);
    document.addEventListener('visibilitychange', () => document.hidden ? halt() : resume());
    onPreference(() => {
      if (quiet()) { manualPause = true; step = count - 1; halt(); }
    });
  });

  all('[data-studio-film]').forEach(video => {
    const surface = video.closest('.architecture-canvas, .campaign-poster, .concept-home, .home-work-art');
    const button = surface?.querySelector('[data-film-toggle]');
    if (!surface || !button) return;
    const sequence = surface.closest('[data-sequence]');
    let visible = false, loaded = false, started = false, userPaused = false, ended = false, request = 0;
    let explicit = false;
    const finalStage = () => !sequence || Number(sequence.dataset.step) === Number(sequence.dataset.count) - 1;
    const label = () => {
      button.textContent = ended ? 'Odtwórz film ponownie ↻' : !video.paused ? 'Wstrzymaj film Ⅱ' : started ? 'Wznów film ▶' : 'Ożyw obraz ▶';
    };
    const pause = () => { request++; video.pause(); label(); };
    const start = (manual = false) => {
      if (document.hidden || !visible || !finalStage()) return;
      if (!manual && (userPaused || ended || (quiet() && !explicit))) return;
      if (!loaded) {
        video.src = matchMedia('(max-width: 700px)').matches ? video.dataset.small : video.dataset.desktop;
        video.muted = true; video.load(); loaded = true;
      }
      if (manual && ended) { video.currentTime = 0; ended = false; }
      started = true;
      const id = ++request;
      Promise.resolve(video.play()).then(() => {
        if (id !== request) return;
        if (!visible || document.hidden || userPaused || !finalStage()) { pause(); return; }
        video.classList.add('is-playing'); label();
      }).catch(() => { if (id === request) { userPaused = true; label(); } });
    };
    button.hidden = false; label();
    button.addEventListener('click', () => {
      if (!video.paused) { userPaused = true; pause(); }
      else { userPaused = false; explicit = true; visible = true; start(true); }
    });
    video.addEventListener('ended', () => { ended = true; label(); });
    video.addEventListener('error', () => {
      pause(); video.classList.remove('is-playing');
      button.textContent = 'Film niedostępny. Dostępne jest zdjęcie.'; button.disabled = true;
    });
    observe(surface, active => { visible = active; if (active) start(); else pause(); });
    sequence?.addEventListener('studio:stage', () => finalStage() ? start() : pause());
    document.addEventListener('visibilitychange', () => document.hidden ? pause() : start());
    onPreference(() => { if (quiet()) { explicit = false; userPaused = true; pause(); } });
  });

  const offers = [
    {kind:'STRATEGIA / DESIGN / WDROŻENIE', title:'Pokaż klientom,<br><em>co oferujesz.</em>', description:'Uporządkujemy ofertę, napiszemy treści i zaprojektujemy stronę, na której klient łatwo znajdzie usługę i kontakt.', result:'Efekt prac: treści, projekt i działająca strona w uzgodnionym zakresie.', topic:'Strona internetowa', href:'/strony-www.html', image:'architecture'},
    {kind:'RESEARCH / STRATEGIA / TOŻSAMOŚĆ', title:'Dobry pomysł.<br><em>Własny charakter.</em>', description:'Sprawdzimy rynek i konkurencję. Ustalimy, do kogo kierujesz ofertę, czym się wyróżnisz i jak zaprezentujesz nową firmę.', result:'Efekt prac: strategia, identyfikacja i plan wejścia na rynek w ustalonym zakresie.', topic:'Nowa marka', href:'/o-donie.html#od-zera', image:'interior'},
    {kind:'AUDYT / NOWY KIERUNEK / ODNOWA', title:'Twoja historia.<br><em>Nowa siła.</em>', description:'Przejrzymy ofertę, stronę i dotychczasowe materiały. Ustalimy, co zachować, a co zmienić, żeby lepiej przedstawiały Twoją firmę.', result:'Efekt prac: kierunek odnowy, komunikacja i nowy wizerunek w uzgodnionym zakresie.', topic:'Odnowa marki', href:'/o-donie.html#przemiana', image:'architecture'},
    {kind:'PRZEKAZ / KREACJA / KAMPANIA', title:'Dobra oferta.<br><em>Dobry rozgłos.</em>', description:'Przygotujemy reklamy i stronę, na którą trafią zainteresowani. Ustalimy budżet, odbiorców i sposób oceny kampanii.', result:'Efekt prac: plan kampanii, materiały i konfiguracja uzgodnionych działań. Emisja rozliczana oddzielnie.', topic:'Marketing', href:'/marketing.html', image:'interior'},
    {kind:'PROCES / INTEGRACJE / KONTROLA', title:'Mniej rutyny.<br><em>Więcej Twojego czasu.</em>', description:'Wybierzemy zadanie do automatyzacji, połączymy potrzebne programy i ustalimy, które działania wymagają Twojej zgody.', result:'Efekt prac: uzgodniony proces, integracje, scenariusze kontroli i instrukcja obsługi.', topic:'Automatyzacja', href:'/automatyzacja.html', image:'architecture'}
  ];
  all('[data-offer]').forEach(root => {
    const buttons = all('[data-offer-option]', root), panel = root.querySelector('.offer-result');
    const image = panel.querySelector('img');
    buttons.forEach((button, i) => button.addEventListener('click', () => {
      const offer = offers[i];
      buttons.forEach((b, j) => b.setAttribute('aria-pressed', String(i === j)));
      root.querySelector('[data-offer-kind]').textContent = offer.kind;
      root.querySelector('[data-offer-title]').innerHTML = offer.title;
      root.querySelector('[data-offer-description]').textContent = offer.description;
      root.querySelector('[data-offer-result]').textContent = offer.result;
      root.querySelector('[data-offer-contact]').href = '/kontakt.html?temat=' + encodeURIComponent(offer.topic);
      root.querySelector('[data-offer-more]').href = offer.href;
      image.srcset = `/assets/studio/${offer.image}-small.webp 960w, /assets/studio/${offer.image}.webp 1672w`;
      image.src = `/assets/studio/${offer.image}.webp`;
      image.alt = offer.image === 'interior' ? 'Koncepcyjne wnętrze marki Horyzont' : 'Koncepcyjna architektura marki Horyzont';
      panel.classList.remove('is-changing');
      requestAnimationFrame(() => panel.classList.add('is-changing'));
      panel.querySelector('[data-offer-announcement]').textContent = offer.topic + '. ' + offer.result;
      if (matchMedia('(max-width: 950px)').matches) panel.scrollIntoView?.({behavior:quiet() ? 'auto' : 'smooth',block:'start'});
    }));
  });

  const prompts = {
    mail: ['„Napisz odpowiedź na e-mail.”', 'Napisz za mnie odpowiedź na wiadomość, którą dostałem — taką, żebym wysłał ją bez poprawek.', 'Zanim napiszesz, zadaj mi po kolei — jedno pytanie naraz — tylko trzy: co ta osoba napisała (wkleję albo streszczę byle jak), kim jest dla mnie i co ma zrobić po przeczytaniu. Jeśli coś już powiedziałem, nie pytaj drugi raz. Używaj tylko tego, co podam — cen, terminów ani obietnic nie wymyślaj, dopytaj.', 'Do 100 słów, w moim tonie (zapytaj: Pan/Pani czy na Ty), z jednym następnym krokiem na końcu. Pokaż i zapytaj, co zmienić — to pierwsza wersja, nie ostatnia.'],
    social: ['„Napisz coś na social media.”', 'Zaproponuj pięć tematów na posty, które odpowiadają na prawdziwe pytania moich klientów — nie na to, co chciałbym o sobie napisać.', 'Najpierw zapytaj — jedno pytanie naraz — czym się zajmuję, o co klienci pytają najczęściej (mogę wkleić ich wiadomości) i gdzie publikuję. Buduj wyłącznie na tym. Nie dopisuj osiągnięć, liczb ani opinii klientów.', 'Do każdego tematu: pierwsze zdanie posta, jedna myśl i co czytelnik ma zrobić. Zaznacz, co muszę sprawdzić przed publikacją. Na koniec zapytaj, który temat rozwinąć w gotowy post.'],
    explain: ['„Wytłumacz mi to.”', 'Wytłumacz mi rzecz, której nie rozumiem, tak, żebym umiał powtórzyć ją własnymi słowami.', 'Zadaj mi dwa pytania, jedno naraz: co to jest (mogę wkleić zdanie, zrobić zdjęcie pisma albo opisać byle jak), a potem czym się zajmuję, żeby dobrać przykład z mojego świata. Nie streszczaj planu — po prostu zacznij od pytania. Jeśli czegoś nie jesteś pewien, powiedz to — nie zgaduj.', 'Cztery kroki: jedno zdanie, o co chodzi; porównanie z mojej codzienności; jaki problem to rozwiązuje; co z tego wynika dla mnie. Bez fachowych słów. Na koniec zapytaj, która część była najmniej jasna, i wytłumacz ją inaczej.']
  };
  all('[data-prompt-lab]').forEach(root => {
    const buttons = all('[data-prompt-option]', root);
    const status = root.querySelector('[data-prompt-status]');
    const exported = root.querySelector('[data-prompt-export]');
    const copy = root.querySelector('[data-prompt-copy]');
    let selected = 'mail', operation = 0;
    buttons.forEach(button => button.addEventListener('click', () => {
      selected = button.dataset.promptOption; operation++;
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      ['before', 'goal', 'context', 'format'].forEach((key, i) => root.querySelector('[data-prompt-' + key + ']').textContent = prompts[selected][i]);
      exported.hidden = true;
      status.textContent = 'Przykład: ' + button.textContent.replace('', '').trim() + '. Możesz skopiować całe polecenie.';
      const sheet = root.querySelector('.prompt-sheet');
      sheet.classList.remove('is-changing'); requestAnimationFrame(() => sheet.classList.add('is-changing'));
    }));
    copy.addEventListener('click', async () => {
      const id = ++operation, value = prompts[selected].slice(1).join('\n\n');
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(value);
        if (id === operation) { status.textContent = 'Polecenie skopiowane. Wklej je do wybranego asystenta AI.'; exported.hidden = true; }
      } catch {
        if (id !== operation) return;
        exported.value = value; exported.hidden = false; exported.focus(); exported.select();
        status.textContent = 'Skopiuj zaznaczone polecenie ręcznie. Automatyczne kopiowanie jest niedostępne.';
      }
    });
  });

  all('[data-live-site]').forEach(root => {
    const button = root.querySelector('[data-open-live]');
    const frame = root.querySelector('.live-site-frame');
    const slot = root.querySelector('[data-frame-slot]');
    const status = root.querySelector('[data-frame-status]');
    let open = false, timer = 0;
    button.addEventListener('click', () => {
      open = !open; clearTimeout(timer);
      frame.hidden = !open; button.setAttribute('aria-expanded', String(open));
      button.textContent = open ? 'Zamknij podgląd' : 'Otwórz podgląd';
      slot.replaceChildren();
      if (!open) return;
      const iframe = document.createElement('iframe');
      iframe.title = 'Działająca strona: ' + root.dataset.siteTitle;
      iframe.referrerPolicy = 'no-referrer';
      // These public project URLs are fixed in generated markup, never user input.
      iframe.src = root.dataset.siteUrl;
      status.textContent = 'Wczytywanie zewnętrznego serwisu. Możesz też otworzyć go w nowej karcie.';
      const fallback = () => {
        if (open) status.textContent = 'Jeśli strona nie jest widoczna poniżej, wybierz „Otwórz w nowej karcie”. Zewnętrzny serwis może ograniczać osadzanie.';
      };
      iframe.addEventListener('load', () => { clearTimeout(timer); fallback(); });
      iframe.addEventListener('error', () => { clearTimeout(timer); fallback(); });
      slot.append(iframe); timer = setTimeout(fallback, 8000);
    });
  });

  all('.build-stage').forEach(stage => {
    const canvas = stage.querySelector('.architecture-canvas');
    let tick = 0, x = 0, y = 0;
    const reset = () => { cancelAnimationFrame(tick); tick = 0; canvas.style.setProperty('--scene-rx', '0deg'); canvas.style.setProperty('--scene-ry', '0deg'); };
    stage.addEventListener('pointermove', event => {
      if (quiet() || !matchMedia('(hover: hover) and (pointer: fine)').matches || stage.closest('[data-sequence]').dataset.step !== '3') return;
      const rect = stage.getBoundingClientRect();
      x = (event.clientX - rect.left) / rect.width - .5; y = (event.clientY - rect.top) / rect.height - .5;
      if (!tick) tick = requestAnimationFrame(() => {
        canvas.style.setProperty('--scene-rx', (x * 2.8).toFixed(2) + 'deg');
        canvas.style.setProperty('--scene-ry', (-y * 2).toFixed(2) + 'deg'); tick = 0;
      });
    }, {passive:true});
    stage.addEventListener('pointerleave', reset);
    onPreference(reset);
  });

  all('[data-editorial-motion]').forEach(scene => {
    let played = false;
    observe(scene, visible => {
      if (visible && !played && !quiet()) {
        played = true;
        scene.classList.add('is-active');
      } else if (!visible) scene.classList.remove('is-active');
    }, .4);
    onPreference(() => { if (quiet()) scene.classList.remove('is-active'); });
  });

  const homeHeader = document.body.classList.contains('home') ? document.querySelector('.site-header') : null;
  const progress = document.querySelector('[data-studio-progress]');
  if (progress) {
    let tick = 0;
    const update = () => {
      if (homeHeader) homeHeader.classList.toggle('past-opening', scrollY > 80);
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.transform = 'scaleX(' + (max > 0 ? Math.max(0, Math.min(1, scrollY / max)) : 0) + ')'; tick = 0;
    };
    addEventListener('scroll', () => { if (!tick) tick = requestAnimationFrame(update); }, {passive:true});
    addEventListener('resize', update, {passive:true}); update();
  }
})();
