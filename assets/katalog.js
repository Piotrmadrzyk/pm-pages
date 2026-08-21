
// Katalog funkcji — wspolny mechanizm dla wszystkich demo.
// Strona ustawia window.KATALOG = { id, webhook, demo, pozycje } PRZED
// wczytaniem tego pliku. Zmiana mechanizmu = zmiana tutaj, raz dla wszystkich.
(function () {
  'use strict';

  var CFG = window.KATALOG || {};
  var DEMO_ID = CFG.id || 'katalog';

  var deck = document.querySelector('.deck');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var total = slides.length;
  var idx = 0;

  var SECTION_LABELS = {
    title: 'Start', intro: 'Start', divider: 'Przejście',
    feature: 'Co już działa', addition: 'Co można dodać', summary: 'Podsumowanie'
  };

  var progressFill = document.getElementById('progress-fill');
  var hudSection = document.getElementById('hud-section');
  var hudFrac = document.getElementById('hud-frac');
  var btnPrev = document.getElementById('btn-prev');
  var btnNext = document.getElementById('btn-next');

  var STORE_KEY = 'katalog_' + DEMO_ID + '_wybory_v1';
  function loadStore() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); } catch (e) { return {}; }
  }
  function saveStore(s) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(s)); } catch (e) { /* tryb prywatny */ }
  }
  var store = loadStore();

  function slideIdOf(el) { return el.id.replace(/^slide-/, ''); }

  function applyPickerState(slideEl) {
    var sid = slideIdOf(slideEl);
    var choice = store[sid];
    var yes = slideEl.querySelector('.pick-yes');
    var maybe = slideEl.querySelector('.pick-maybe');
    if (yes) yes.classList.toggle('is-active', choice === 'wybieram');
    if (maybe) maybe.classList.toggle('is-active', choice === 'zainteresowany');
  }

  slides.forEach(function (s) { applyPickerState(s); });

  var mobileScrollMode = window.matchMedia('(max-width: 900px)');

  // Zywy podglad zamiast zrzutu ekranu: ramka dostaje adres dopiero wtedy,
  // gdy slajd staje sie widoczny. Dzieki temu strona nie wczytuje na starcie
  // czterdziestu podstron naraz.
  // Podglad ma pokazywac strone tak, jak wyglada dla goscia, ktory juz na niej
  // jest: bez banera ciasteczek i z trescia widoczna. Animacje wejscia sa
  // sterowane przewijaniem, a w nieruchomej ramce nigdy by sie nie odpalily —
  // wiec odslaniamy je recznie. Demo sa na tym samym serwerze, wiec wolno.
  function oswojPodglad(f) {
    var d;
    try { d = f.contentDocument; } catch (e) { return; }
    if (!d || !d.body) return;
    if (!d.getElementById('katalog-podglad')) {
      var st = d.createElement('style');
      st.id = 'katalog-podglad';
      st.textContent =
        'html{scroll-behavior:auto !important;}' +
        '.reveal{opacity:1 !important;transform:none !important;}' +
        '#cookie-bar,.cookie-bar{display:none !important;}' +
        '#chat-panel,#chat-btn{display:none !important;}' +
        '::-webkit-scrollbar{width:0;height:0}';
      (d.head || d.documentElement).appendChild(st);
    }
    var nazwa = f.dataset.kotwica;
    if (!nazwa) return;
    var cel = d.getElementById(nazwa);
    if (!cel) return;
    // Ustawiamy pozycje wprost, nie przez scrollIntoView — czesc demo ma
    // wlaczone plynne przewijanie, przez ktore skok nie zdazyl dojsc do konca.
    var y = cel.getBoundingClientRect().top + (d.documentElement.scrollTop || d.body.scrollTop || 0);
    d.documentElement.scrollTop = y;
    d.body.scrollTop = y;
  }

  function obudzPodglad(slideEl) {
    var f = slideEl.querySelector('iframe[data-src]');
    if (!f) return;
    var adres = f.getAttribute('data-src');
    var h = adres.indexOf('#');
    if (h > -1) f.dataset.kotwica = adres.slice(h + 1);
    f.addEventListener('load', function () {
      // Zdjecia dociagaja sie po wczytaniu i przesuwaja uklad, wiec pozycje
      // ustawiamy kilka razy, az przestanie sie ruszac.
      [0, 250, 700, 1400].forEach(function (ms) {
        setTimeout(function () { oswojPodglad(f); }, ms);
      });
    });
    f.src = adres;
    f.removeAttribute('data-src');
  }

  function render() {
    slides.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
    var current = slides[idx];
    obudzPodglad(current);
    if (slides[idx + 1]) obudzPodglad(slides[idx + 1]);   // nastepny gotowy zawczasu
    // Na telefonie slajdy stoją jedne pod drugimi w normalnym przepływie strony
    // (patrz CSS) — przełączenie klasy .is-active samo nic nie przewija, trzeba
    // to zrobić ręcznie.
    if (mobileScrollMode.matches) {
      // 'auto' (nie 'smooth') celowo: przy płynnym przewijaniu przez wiele
      // slajdów z obrazkami "loading=lazy" po drodze ich ładowanie w locie
      // przesuwało układ strony i przewijało w złe miejsce.
      current.scrollIntoView({ behavior: 'auto', block: 'start' });
    }
    var section = current.getAttribute('data-section');
    hudSection.textContent = SECTION_LABELS[section] || '';
    hudFrac.textContent = (idx + 1) + ' / ' + total;
    progressFill.style.width = (idx / (total - 1) * 100) + '%';
    btnPrev.disabled = idx === 0;
    btnNext.disabled = idx === total - 1;
    if (section === 'summary') renderSummary();
    try { history.replaceState(null, '', '#' + slideIdOf(current)); } catch (e) {}
    var heading = current.querySelector('h1, h2');
    if (heading) {
      heading.setAttribute('tabindex', '-1');
      heading.focus({ preventScroll: true });
    }
  }

  function goTo(i) {
    idx = Math.max(0, Math.min(total - 1, i));
    render();
  }
  function next() { if (idx < total - 1) { idx++; render(); } }
  function prev() { if (idx > 0) { idx--; render(); } }

  btnNext.addEventListener('click', next);
  btnPrev.addEventListener('click', prev);

  document.addEventListener('keydown', function (e) {
    if (tocOpen()) {
      if (e.key === 'Escape') closeToc();
      return;
    }
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
    else if (e.key === 'm' || e.key === 'M') { openToc(); }
    else if (e.key === 'Home') { goTo(0); }
    else if (e.key === 'End') { goTo(total - 1); }
  });

  // swipe (dotyk)
  var touchX = null;
  deck.addEventListener('touchstart', function (e) { touchX = e.changedTouches[0].clientX; }, { passive: true });
  deck.addEventListener('touchend', function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 60) { dx < 0 ? next() : prev(); }
    touchX = null;
  }, { passive: true });

  // przyciski „start” / skoki wewnętrzne
  document.getElementById('btn-go-start')?.addEventListener('click', function () { next(); });

  // ---------- picker (Wybieram / Wstępnie zainteresowany) ----------
  document.querySelectorAll('.picker').forEach(function (picker) {
    picker.addEventListener('click', function (e) {
      var btn = e.target.closest('.pick');
      if (!btn) return;
      var sid = picker.getAttribute('data-slide-id');
      var choice = btn.getAttribute('data-choice');
      var was = store[sid];
      if (was === choice) { delete store[sid]; } else { store[sid] = choice; }
      saveStore(store);
      applyPickerState(picker.closest('.slide'));
      scheduleNotify();
    });
  });

  // ---------- reset ----------
  function resetAll() {
    if (!window.confirm('Wyczyścić wszystkie zaznaczenia „Wybieram” / „Wstępnie zainteresowany”? Przyda się przed nowym spotkaniem z kolejnym klientem.')) return;
    store = {};
    saveStore(store);
    slides.forEach(applyPickerState);
    renderSummary();
  }
  document.getElementById('btn-reset-top')?.addEventListener('click', resetAll);
  document.getElementById('btn-reset-bottom')?.addEventListener('click', resetAll);

  // ---------- powiadomienie e-mail o wyborach ----------
  // Gdy ktoś przegląda ten materiał samodzielnie (bez Ciebie obok), jego wybory
  // trafiają e-mailem — z opóźnieniem po ostatniej zmianie i przy zamknięciu karty,
  // żeby nie wysyłać osobnego maila po każdym pojedynczym kliknięciu.
  var NOTIFY_ENDPOINT = CFG.webhook || 'https://pmresearch.app.n8n.cloud/webhook/probatum-katalog-wybory';
  var NOTIFY_IDLE_MS = 20000;
  var notifySessionId = (function () {
    try {
      var k = 'katalog_' + DEMO_ID + '_sesja_v1';
      var v = sessionStorage.getItem(k);
      if (!v) { v = 'sid-' + Date.now() + '-' + Math.random().toString(36).slice(2, 9); sessionStorage.setItem(k, v); }
      return v;
    } catch (e) { return 'sid-' + Date.now(); }
  })();
  var CHOOSABLE = CFG.pozycje || window.__ZP_CHOOSABLE__ || [];
  var lastNotifySignature = '';
  var notifyTimer = null;

  function currentSelections() {
    var yes = [], maybe = [];
    CHOOSABLE.forEach(function (row) {
      if (store[row[0]] === 'wybieram') yes.push(row[1]);
      else if (store[row[0]] === 'zainteresowany') maybe.push(row[1]);
    });
    return { yes: yes, maybe: maybe };
  }

  function sendNotify(useBeacon) {
    var sel = currentSelections();
    if (!sel.yes.length && !sel.maybe.length) return;
    var signature = sel.yes.join('|') + '::' + sel.maybe.join('|');
    if (signature === lastNotifySignature) return;
    var payload = {
      sessionId: notifySessionId,
      wybieram: sel.yes,
      zainteresowany: sel.maybe,
      demo: CFG.demo || DEMO_ID,
      strona: location.pathname.split('/').pop() || 'katalog.html'
    };
    lastNotifySignature = signature;
    try {
      if (useBeacon && navigator.sendBeacon) {
        navigator.sendBeacon(NOTIFY_ENDPOINT, new Blob([JSON.stringify(payload)], { type: 'application/json' }));
      } else {
        fetch(NOTIFY_ENDPOINT, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload), keepalive: true
        }).catch(function () {});
      }
    } catch (e) { /* brak połączenia — spróbujemy przy kolejnej zmianie */ }
  }

  function scheduleNotify() {
    clearTimeout(notifyTimer);
    notifyTimer = setTimeout(function () { sendNotify(false); }, NOTIFY_IDLE_MS);
  }

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') { clearTimeout(notifyTimer); sendNotify(true); }
  });
  window.addEventListener('pagehide', function () { clearTimeout(notifyTimer); sendNotify(true); });

  // ---------- prosba o wycene ----------
  // Idzie tym samym kanalem co formularze na stronie (pm-lead-capture),
  // zeby zgloszenie trafilo tam, gdzie wszystkie pozostale. Zaznaczenia
  // wchodza do tresci, wiec od razu widac, o co klient prosi.
  var LEAD_ENDPOINT = 'https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture';

  (function () {
    var form = document.getElementById('wycena-form');
    if (!form) return;
    var status = document.getElementById('wycena-status');
    var btn = document.getElementById('wycena-wyslij');

    function pokaz(txt, klasa) {
      if (!status) return;
      status.textContent = txt;
      status.className = 'wycena-status' + (klasa ? ' ' + klasa : '');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var imie = (d.get('imie') || '').trim();
      var tel = (d.get('telefon') || '').trim();
      var mail = (d.get('email') || '').trim();

      if (!imie) { pokaz('Podaj imię — inaczej nie wiem, jak się zwracać.', 'zle'); return; }
      if (!tel) { pokaz('Podaj telefon albo napisz w nim „tylko mail".', 'zle'); return; }
      if (mail.indexOf('@') < 1) { pokaz('Sprawdź adres e-mail — wygląda na niepełny.', 'zle'); return; }
      if (!d.get('consent')) { pokaz('Potrzebna jest zgoda na kontakt.', 'zle'); return; }
      if ((d.get('strona_www') || '') !== '') { return; }   // robot spamujacy

      var sel = currentSelections();
      if (!sel.yes.length && !sel.maybe.length) {
        pokaz('Najpierw zaznacz choć jedną funkcję — inaczej nie ma czego wyceniać.', 'zle');
        return;
      }

      var tresc = 'Katalog funkcji: ' + (CFG.demo || DEMO_ID) + '\n\n';
      if (sel.yes.length) tresc += 'WYBIERAM:\n- ' + sel.yes.join('\n- ') + '\n\n';
      if (sel.maybe.length) tresc += 'WSTĘPNIE ZAINTERESOWANY:\n- ' + sel.maybe.join('\n- ');

      if (btn) { btn.disabled = true; btn.textContent = 'Wysyłam...'; }
      pokaz('');

      fetch(LEAD_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          form_key: 'katalog-' + DEMO_ID,
          imie: imie, email: mail, telefon: tel,
          tresc: tresc,
          consent: true,
          zrodlo: 'probatum.pl',
          demo: CFG.demo || DEMO_ID,
          wybieram: sel.yes,
          zainteresowany: sel.maybe
        })
      }).then(function () {
        form.style.display = 'none';
        var blok = document.getElementById('wycena-blok');
        if (blok) {
          blok.innerHTML = '<h3>Mamy to.</h3><p class="wycena-lede">Odezwiemy się z widełkami dla zaznaczonych funkcji, zwykle w 1–2 dni robocze. Listę możesz sobie skopiować przyciskiem wyżej.</p>';
        }
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = 'Poproś o wycenę'; }
        pokaz('Nie udało się wysłać — sprawdź połączenie i spróbuj jeszcze raz.', 'zle');
      });
    });
  })();

  // ---------- podsumowanie ----------
  function renderSummary() {
    var sumYes = document.getElementById('sum-yes');
    var sumMaybe = document.getElementById('sum-maybe');
    if (!sumYes || !sumMaybe) return;
    var yesItems = [], maybeItems = [];
    CHOOSABLE.forEach(function (row) {
      var id = row[0], title = row[1];
      if (store[id] === 'wybieram') yesItems.push(title);
      else if (store[id] === 'zainteresowany') maybeItems.push(title);
    });
    function fill(ul, items) {
      ul.innerHTML = '';
      if (!items.length) {
        var li = document.createElement('li');
        li.className = 'summary-empty';
        li.textContent = 'Nic jeszcze niezaznaczone.';
        ul.appendChild(li);
        return;
      }
      items.forEach(function (t) {
        var li = document.createElement('li');
        li.textContent = t;
        ul.appendChild(li);
      });
    }
    fill(sumYes, yesItems);
    fill(sumMaybe, maybeItems);
  }

  document.getElementById('btn-copy')?.addEventListener('click', function () {
    var yes = [], maybe = [];
    CHOOSABLE.forEach(function (row) {
      if (store[row[0]] === 'wybieram') yes.push('- ' + row[1]);
      else if (store[row[0]] === 'zainteresowany') maybe.push('- ' + row[1]);
    });
    var text = 'ZIELONA PERGOLA — PODSUMOWANIE SPOTKANIA\n\n' +
      'WYBIERAM:\n' + (yes.length ? yes.join('\n') : '(brak)') + '\n\n' +
      'WSTĘPNIE ZAINTERESOWANY:\n' + (maybe.length ? maybe.join('\n') : '(brak)');
    var hint = document.getElementById('copy-hint');
    function ok() { if (hint) { hint.textContent = 'Skopiowano do schowka ✓'; setTimeout(function () { hint.textContent = ''; }, 3500); } }
    function fail() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); ok(); } catch (e) { if (hint) hint.textContent = 'Nie udało się skopiować — zaznacz i skopiuj ręcznie.'; }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(ok).catch(fail);
    } else { fail(); }
  });

  // ---------- spis treści ----------
  var tocOverlay = document.getElementById('toc-overlay');
  function tocOpen() { return tocOverlay.classList.contains('is-open'); }
  function openToc() { tocOverlay.classList.add('is-open'); }
  function closeToc() { tocOverlay.classList.remove('is-open'); }
  document.getElementById('toc-btn-open')?.addEventListener('click', openToc);
  document.getElementById('toc-close')?.addEventListener('click', closeToc);
  tocOverlay.addEventListener('click', function (e) { if (e.target === tocOverlay) closeToc(); });
  document.getElementById('toc-list')?.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-jump]');
    if (!btn) return;
    var targetId = 'slide-' + btn.getAttribute('data-jump');
    var i = slides.findIndex(function (s) { return s.id === targetId; });
    if (i >= 0) { goTo(i); closeToc(); }
  });

  // ---------- start position via hash ----------
  var startHash = location.hash.replace('#', '');
  if (startHash) {
    var found = slides.findIndex(function (s) { return s.id === 'slide-' + startHash; });
    if (found >= 0) idx = found;
  }
  render();
})();
