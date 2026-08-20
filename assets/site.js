/* ============================================================
   PM PRZEWAGA METODĄ — site.js
   ============================================================ */

/* ------------------------------------------------------------
   >>> LINKI DO MEDIÓW SPOŁECZNOŚCIOWYCH — JEDYNE MIEJSCE DO EDYCJI <<<
   Wklej pełny adres profilu między apostrofy. Puste = kafelek
   pokazuje się jako "wkrótce" i nie da się w niego kliknąć.
   Po uzupełnieniu linki pojawią się automatycznie na wszystkich
   podstronach — w sekcji "Obserwuj" i w stopce.
------------------------------------------------------------ */
var SOCIAL = {
  facebook:  '',
  instagram: '',
  linkedin:  '',
  youtube:   '',
  tiktok:    ''
};

(function () {
  'use strict';

  var ICONS = {
    facebook:'<path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>',
    instagram:'<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.2"/>',
    linkedin:'<path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-4 0v7h-4v-7a6 6 0 016-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    youtube:'<path d="M22.5 7.2a2.8 2.8 0 00-2-2C18.7 4.7 12 4.7 12 4.7s-6.7 0-8.5.5a2.8 2.8 0 00-2 2A29 29 0 001 12a29 29 0 00.5 4.8 2.8 2.8 0 002 2c1.8.5 8.5.5 8.5.5s6.7 0 8.5-.5a2.8 2.8 0 002-2A29 29 0 0023 12a29 29 0 00-.5-4.8z"/><path d="M9.8 15.3l5.5-3.3-5.5-3.2z" fill="#07080b" stroke="none"/>',
    tiktok:'<path d="M16 3a5 5 0 005 5v3a8 8 0 01-5-1.8V15a6 6 0 11-6-6c.3 0 .7 0 1 .1V12a3 3 0 102 2.8V3z"/>'
  };
  var NAMES = {facebook:'Facebook',instagram:'Instagram',linkedin:'LinkedIn',youtube:'YouTube',tiktok:'TikTok'};

  function svg(key){
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" ' +
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[key] + '</svg>';
  }

  document.addEventListener('DOMContentLoaded', function () {

    /* ---------- rok w stopce ---------- */
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });

    /* ---------- nawigacja mobilna ---------- */
    var burger = document.querySelector('.burger');
    var navmob = document.querySelector('.navmobile');
    if (burger && navmob) {
      burger.addEventListener('click', function () {
        var open = navmob.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      navmob.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          navmob.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
        });
      });
    }

    /* ---------- media społecznościowe ---------- */
    var order = ['facebook', 'instagram', 'linkedin', 'youtube', 'tiktok'];

    document.querySelectorAll('[data-social-grid]').forEach(function (grid) {
      grid.innerHTML = order.map(function (k) {
        var url = (SOCIAL[k] || '').trim();
        var open = url ? '<a class="sbtn" href="' + url + '" target="_blank" rel="noopener">'
                       : '<span class="sbtn soon">';
        var close = url ? '</a>' : '</span>';
        var sub = url ? 'Obserwuj' : 'Wkrótce';
        return open + svg(k) + '<span style="display:block"><b>' + NAMES[k] + '</b>' +
               '<span>' + sub + '</span></span>' + close;
      }).join('');
    });

    document.querySelectorAll('[data-social-foot]').forEach(function (box) {
      var live = order.filter(function (k) { return (SOCIAL[k] || '').trim(); });
      if (!live.length) {
        box.innerHTML = '<p class="small" style="margin:0">Profile ruszają w najbliższych dniach.</p>';
        return;
      }
      box.innerHTML = live.map(function (k) {
        return '<a href="' + SOCIAL[k] + '" target="_blank" rel="noopener" aria-label="' +
               NAMES[k] + '">' + svg(k) + '</a>';
      }).join('');
    });

    /* ---------- co jest w kadrze: jeden wspólny mechanizm ----------
       Świadomie bez IntersectionObserver. Obserwator bywa dławiony
       (nieaktywna karta, słabszy telefon, osadzenie w ramce) i potrafi
       odpalić z kilkusekundowym opóźnieniem albo wcale — a wtedy klient
       widzi pustą sekcję albo pusty podgląd realizacji. Zwykłe sprawdzanie
       pozycji przy przewijaniu jest mniej eleganckie, ale nie ma prawa
       zawieść. Bez JS nic i tak nie jest ukryte (klasa .js w <head>). */
    var watchers = [];

    function watch(el, fn, margin, minBottom) {
      watchers.push({
        el: el, fn: fn,
        m: margin || 0,
        b: (minBottom === undefined ? -Infinity : minBottom)
      });
    }

    function sweep() {
      if (!watchers.length) return;
      var vh = window.innerHeight || document.documentElement.clientHeight;
      for (var i = watchers.length - 1; i >= 0; i--) {
        var wch = watchers[i];
        var r = wch.el.getBoundingClientRect();
        /* Warunek jest jednostronny: wystarczy, że element wszedł w kadr
           od dołu. Gdyby wymagał też, żeby nie wyjechał górą, sekcja
           przeskoczona przy szybkim przewijaniu zostałaby niewidoczna. */
        if (r.top < vh + wch.m && r.bottom > wch.b) {
          wch.fn(wch.el);
          watchers.splice(i, 1);
        }
      }
    }

    /* Throttling czasowy, nie przez requestAnimationFrame z flagą.
       Gdyby rAF został wstrzymany (karta w tle, ramka uznana za niewidoczną),
       flaga zostałaby na true na zawsze i przewijanie nie odsłoniłoby już nic. */
    var lastSweep = 0, sweepTimer = null, sweepPoll = null;

    function onSweepScroll() {
      if (!watchers.length) return;
      var now = Date.now();
      if (now - lastSweep > 120) {
        lastSweep = now;
        sweep();
      } else {
        clearTimeout(sweepTimer);
        sweepTimer = setTimeout(function () { lastSweep = Date.now(); sweep(); }, 120);
      }
    }

    window.addEventListener('scroll', onSweepScroll, { passive: true });
    window.addEventListener('resize', onSweepScroll, { passive: true });
    window.addEventListener('load', sweep);
    document.addEventListener('visibilitychange', sweep);

    /* Ostatnia siatka bezpieczeństwa: dopóki cokolwiek czeka na odsłonięcie,
       sprawdzamy to cyklicznie. Zatrzymuje się samo, gdy lista pustoszeje. */
    sweepPoll = setInterval(function () {
      if (!watchers.length) { clearInterval(sweepPoll); return; }
      sweep();
    }, 1000);

    /* ---------- odsłanianie sekcji ---------- */
    document.querySelectorAll('.reveal, .stagger').forEach(function (el) {
      watch(el, function (e) { e.classList.add('in'); }, -30);
    });

    /* ---------- liczniki ----------
       W HTML stoi od razu prawdziwa liczba, więc nawet gdyby animacja
       nie ruszyła, klient widzi poprawną wartość, a nie zero. */
    document.querySelectorAll('[data-count]').forEach(function (el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      if (isNaN(target)) return;
      watch(el, function (e) {
        /* Liczymy czasem, nie tyknięciami — przeglądarka potrafi zdławić
           setInterval i licznik zatrzymałby się na przypadkowej liczbie. */
        var DUR = 900, t0 = null;
        function frame(t) {
          if (t0 === null) t0 = t;
          var p = Math.min(1, (t - t0) / DUR);
          e.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(frame);
          else e.textContent = target;
        }
        requestAnimationFrame(frame);
        setTimeout(function () { e.textContent = target; }, DUR + 500);
      }, -60);
    });

    /* ---------- żywe podglądy realizacji ----------
       Każda ramka osadza PRAWDZIWĄ stronę, nie zrzut ekranu.
       Iframe montuje się dopiero, gdy karta wjeżdża w kadr —
       poza kadrem nie kosztuje ani jednego bajtu transferu. */
    /* Renderujemy w sztywnym oknie pulpitu 1440x900 — inaczej sekcje
       o wysokości 100vh rozciągnęłyby się na całą, przeskalowaną ramkę
       i strona wyglądałaby zupełnie inaczej niż w rzeczywistości. */
    var VIEW_W = 1440, VIEW_H = 900;

    /* Ramka może udawać inny ekran — telefon renderuje się w 390x844,
       dzięki czemu widać prawdziwy układ mobilny, a nie ściśnięty pulpit. */
    function viewOf(stage) {
      return {
        w: parseInt(stage.getAttribute('data-vw'), 10) || VIEW_W,
        h: parseInt(stage.getAttribute('data-vh'), 10) || VIEW_H
      };
    }

    /* Przeglądarka potrafi nie namalować przeskalowanej, osadzonej strony,
       mimo że treść jest poprawnie wczytana — klient widzi wtedy ciemny
       prostokąt zamiast realizacji. Wymuszamy przemalowanie mikrozmianą
       skali. UWAGA: każdy krok musi różnić się od poprzedniego, bo
       ustawienie tej samej wartości nie jest dla przeglądarki żadną zmianą
       i nic nie przemalowuje. Różnice rzędu 0,02% są niewidoczne. */
    function nudge(stage) {
      var frame = stage.querySelector('iframe');
      if (!frame) return;
      var v = viewOf(stage);
      var base = stage.clientWidth / v.w;
      [80, 400, 1000, 2200, 4000].forEach(function (ms, i) {
        setTimeout(function () {
          if (!frame.isConnected) return;
          var eps = (i % 2 === 0) ? 0.0006 : 0.0002;
          frame.style.transform = 'scale(' + (base + eps) + ') translateZ(0)';
        }, ms);
      });
    }

    function fitFrame(stage) {
      var frame = stage.querySelector('iframe');
      if (!frame) return;
      var v = viewOf(stage);
      frame.style.width = v.w + 'px';
      frame.style.height = v.h + 'px';
      /* translateZ(0) wymusza własną warstwę graficzną. Bez tego
         przeglądarka potrafi w ogóle nie namalować przeskalowanej,
         osadzonej strony i klient widzi czarny prostokąt. */
      frame.style.transform = 'scale(' + (stage.clientWidth / v.w) + ') translateZ(0)';
    }

    var stages = document.querySelectorAll('[data-live]');
    if (stages.length) {
      var mount = function (stage) {
        if (stage.dataset.mounted) return;
        stage.dataset.mounted = '1';
        var f = document.createElement('iframe');
        f.setAttribute('loading', 'lazy');
        f.setAttribute('tabindex', '-1');
        f.setAttribute('aria-hidden', 'true');
        f.setAttribute('scrolling', 'no');
        f.setAttribute('sandbox', 'allow-scripts allow-same-origin');
        f.setAttribute('title', stage.getAttribute('data-title') || 'Podgląd realizacji');
        f.src = stage.getAttribute('data-live');
        f.addEventListener('load', function () {
          var skel = stage.querySelector('.skel');
          if (!skel) return;
          /* Podkład zostaje jako siatka bezpieczeństwa — gasimy tylko
             animację ładowania i podpisujemy go adresem strony. */
          stage.classList.add('loaded');
          skel.remove();
          /* Przeglądarka bywa leniwa przy malowaniu przeskalowanej,
             osadzonej strony — potrafi zostawić czarny prostokąt mimo
             poprawnie wczytanej treści. Zachowanie jest niedeterministyczne,
             więc zamiast szukać winnej reguły CSS trącamy ramkę kilka razy
             mikrozmianą skali, co wymusza przemalowanie. Niewidoczne dla oka. */
          nudge(stage);
        });
        stage.insertBefore(f, stage.firstChild);
        fitFrame(stage);
      };

      stages.forEach(function (s) { watch(s, mount, 300, -2200); });
      sweep();

      var rt;
      window.addEventListener('resize', function () {
        clearTimeout(rt);
        rt = setTimeout(function () {
          sweep();
          stages.forEach(fitFrame);
        }, 150);
      }, { passive: true });
    }

    /* ---------- wybór jednej opcji (chipy) ---------- */
    document.querySelectorAll('.chiprow').forEach(function (row) {
      var hidden = document.querySelector(row.getAttribute('data-target'));
      row.querySelectorAll('.chip').forEach(function (chip) {
        chip.addEventListener('click', function () {
          row.querySelectorAll('.chip').forEach(function (c) { c.classList.remove('on'); });
          chip.classList.add('on');
          row.classList.remove('chip-error');
          if (hidden) hidden.value = chip.getAttribute('data-value') || chip.textContent.trim();
        });
      });
    });

    /* ---------- formularze (backend: n8n — PM Agent OS Lead Capture) ---------- */
    var LEAD_ENDPOINT = 'https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture';

    function qsParam(name) {
      var m = new RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
      return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
    }

    document.querySelectorAll('form[data-lead-form]').forEach(function (form) {
      var formKey = form.getAttribute('data-form-key');
      var okBox = document.querySelector(form.getAttribute('data-success-target'));
      var errBox = document.querySelector(form.getAttribute('data-error-target'));
      var btn = form.querySelector('button[type="submit"]');
      var btnText = btn ? btn.textContent : '';
      var sending = false;

      function showError(msg) {
        if (!errBox) return;
        errBox.textContent = msg;
        errBox.classList.add('show');
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (sending) return;

        var honeypot = form.querySelector('input[name="strona_www"]');
        if (honeypot && honeypot.value) return;

        var uslugaInput = form.querySelector('#usluga-value');
        var chiprow = form.querySelector('.chiprow');
        if (uslugaInput && uslugaInput.hasAttribute('required') && !uslugaInput.value) {
          if (chiprow) chiprow.classList.add('chip-error');
          showError('Wybierz jedną z opcji powyżej, żeby przejść dalej.');
          return;
        }

        var consentBox = form.querySelector('input[name="consent"]');
        if (consentBox && !consentBox.checked) {
          showError('Zaznacz zgodę na przetwarzanie danych, żeby wysłać formularz.');
          return;
        }
        if (errBox) errBox.classList.remove('show');

        var fd = new FormData(form);
        var tresc = fd.get('wiadomosc') || fd.get('opis') || '';
        if (fd.get('usluga')) {
          var extra = ['Usługa: ' + fd.get('usluga')];
          if (fd.get('firma')) extra.push('Firma: ' + fd.get('firma'));
          if (fd.get('branza')) extra.push('Branża: ' + fd.get('branza'));
          if (fd.get('budzet')) extra.push('Budżet: ' + fd.get('budzet'));
          tresc = extra.join(' | ') + ' | ' + tresc;
        }
        if (fd.get('temat')) tresc = 'Temat: ' + fd.get('temat') + ' | ' + tresc;

        var payload = {
          form_key: formKey,
          imie: fd.get('imie') || '',
          email: fd.get('email') || '',
          telefon: fd.get('telefon') || '',
          tresc: tresc,
          consent: !!(consentBox && consentBox.checked),
          zrodlo: 'probatum.pl',
          utm_source: qsParam('utm_source'),
          utm_medium: qsParam('utm_medium'),
          utm_campaign: qsParam('utm_campaign'),
          utm_content: qsParam('utm_content'),
          utm_term: qsParam('utm_term'),
          page_url: window.location.href
        };

        sending = true;
        if (btn) { btn.disabled = true; btn.textContent = 'Wysyłanie...'; }

        fetch(LEAD_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
          .then(function (r) { return r.json().catch(function () { return {}; }); })
          .then(function () {
            form.style.display = 'none';
            if (okBox) {
              okBox.classList.add('show');
              okBox.scrollIntoView({ block: 'center', behavior: 'smooth' });
            }
          })
          .catch(function () {
            sending = false;
            if (btn) { btn.disabled = false; btn.textContent = btnText; }
            showError('Nie udało się wysłać — sprawdź połączenie i spróbuj ponownie, albo napisz bezpośrednio na e-mail.');
          });
      });
    });

    /* ---------- asystent FAQ (gotowe odpowiedzi, nie żywe AI) ---------- */
    var chatBtn = document.getElementById('chat-btn');
    var chatPanel = document.getElementById('chat-panel');
    var chatBody = document.getElementById('chat-body');
    var chatInput = document.getElementById('chat-input');
    var chatSend = document.getElementById('chat-send');
    var chatSug = document.getElementById('chat-sug');
    var chatX = document.getElementById('chat-x');

    var FAQ = [
      { k: ['cena', 'koszt', 'ile kosztuje', 'wycena', 'budzet', 'budżet'],
        a: 'Wycena zależy od zakresu — strona wielostronicowa, kampania lejkowa i prowadzenie social mediów mają różne widełki. Najszybciej dostaniesz konkretną liczbę przez formularz wyceny: 2 minuty wypełniania.',
        l: { t: 'Otwórz formularz wyceny →', h: 'wycena.html' } },
      { k: ['strona', 'strony', 'www', 'witryna'],
        a: 'Buduję wielostronicowe witryny pisane pod konkretną branżę — nie szablony z katalogu. W Realizacjach osadzam pięć prawdziwych, żywych stron: możesz je otworzyć i sprawdzić.',
        l: { t: 'Zobacz realizacje →', h: 'realizacje.html' } },
      { k: ['kampania', 'kampanie', 'lejek', 'marketing', 'reklama'],
        a: 'Kampania lejkowa to zaprojektowana ścieżka klienta od pierwszego kontaktu po decyzję — z osobnym celem i osobną treścią na każdym etapie, nie jedna reklama powtarzana w kółko.',
        l: { t: 'Zobacz ofertę →', h: 'oferta.html#kampanie' } },
      { k: ['social', 'media', 'instagram', 'facebook', 'profil'],
        a: 'Prowadzę profile na bieżąco — Ty dostarczasz materiał z firmy, ja odpowiadam za harmonogram, treść i publikację. Plan zatwierdzasz przed publikacją.',
        l: { t: 'Zobacz ofertę →', h: 'oferta.html#social' } },
      { k: ['agent', 'agenty', 'automatyzacja', 'automatyzacje'],
        a: 'Wdrożenia agentów automatyzujących pracę w firmie klienta to kolejna rzecz, którą przygotowuję. Nie sprzedaję tego jeszcze — zbieram listę pierwszeństwa, żeby dać znać, gdy ruszy.',
        l: { t: 'Zobacz, co powstaje →', h: 'automatyzacja.html' } },
      { k: ['dona', 'ai', 'jak dziala', 'jak działa', 'system'],
        a: 'Dona to rdzeń systemu — zarządza 87 zautomatyzowanymi elementami w 8 obszarach. Zasada jest jedna: nic nie trafia do sieci bez mojego ręcznego zatwierdzenia.',
        l: { t: 'Poznaj metodę →', h: 'o-donie.html' } },
      { k: ['kontakt', 'telefon', 'mail', 'email', 'napisac', 'napisać'],
        a: 'Najprościej przez formularz — każda wiadomość trafia bezpośrednio do mnie i odpisuję osobiście, zwykle w 1–2 dni robocze.',
        l: { t: 'Przejdź do kontaktu →', h: 'kontakt.html' } },
      { k: ['ile trwa', 'czas', 'termin', 'szybko', 'kiedy'],
        a: 'Pierwsza wersja strony powstaje zwykle w 5–7 dni roboczych, całość w 10–14. Tempo zależy też od tego, jak szybko wracasz z akceptacją.' }
    ];

    function addMsg(text, cls, link) {
      var d = document.createElement('div');
      d.className = 'msg ' + cls;
      d.textContent = text;
      if (link) {
        var a = document.createElement('a');
        a.href = link.h;
        a.textContent = link.t;
        d.appendChild(document.createElement('br'));
        d.appendChild(a);
      }
      chatBody.appendChild(d);
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    function reply(text) {
      var low = text.toLowerCase();
      var hit = FAQ.find(function (f) {
        return f.k.some(function (key) { return low.indexOf(key) !== -1; });
      });
      setTimeout(function () {
        if (hit) addMsg(hit.a, 'bot', hit.l);
        else addMsg('Na to nie mam gotowej odpowiedzi, ale odpiszę osobiście — najszybciej przez formularz.', 'bot', { t: 'Przejdź do kontaktu →', h: 'kontakt.html' });
      }, 420);
    }

    if (chatBtn && chatPanel) {
      chatBtn.addEventListener('click', function () {
        chatPanel.classList.add('open');
        chatBtn.style.display = 'none';
        if (chatInput) chatInput.focus();
      });
      function closeChat() {
        chatPanel.classList.remove('open');
        chatBtn.style.display = '';
      }
      if (chatX) chatX.addEventListener('click', closeChat);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && chatPanel.classList.contains('open')) closeChat();
      });
      function send() {
        var v = chatInput.value.trim();
        if (!v) return;
        addMsg(v, 'user');
        chatInput.value = '';
        reply(v);
      }
      if (chatSend && chatInput) {
        chatSend.addEventListener('click', send);
        chatInput.addEventListener('keydown', function (e) { if (e.key === 'Enter') send(); });
      }
      if (chatSug) {
        chatSug.querySelectorAll('button').forEach(function (b) {
          b.addEventListener('click', function () {
            addMsg(b.textContent, 'user');
            reply(b.textContent);
          });
        });
      }
    }

  });
})();
