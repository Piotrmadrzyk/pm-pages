/* Dom i Wnętrze Warszawa — skrypty strony */
(function () {
  'use strict';

  document.querySelectorAll('.js-year').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- nagłówek ---------- */
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- menu mobilne ---------- */
  var burger = document.getElementById('burger');
  if (burger && header) {
    burger.addEventListener('click', function () {
      var open = header.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
    });
    header.querySelectorAll('.mobile-menu a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- pojawianie się sekcji ---------- */
  var reveals = document.querySelectorAll('.reveal');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- suwak PRZED / PO ---------- */
  /* Natywny input[type=range] rozciagniety na zdjeciu dziala na dotyku fatalnie:
     iOS nie reaguje na tapniecie w tor, a przeciaganie w pionie potrafi zablokowac
     przewijanie strony. Sterujemy wiec wskaznikiem (Pointer Events), a input
     zostaje jako sciezka klawiaturowa i awaryjna, gdy JS nie wystartuje. */
  var hasPointer = 'PointerEvent' in window && 'setPointerCapture' in Element.prototype;
  if (hasPointer) document.documentElement.classList.add('ba-js');

  document.querySelectorAll('[data-ba]').forEach(function (fig) {
    var range = fig.querySelector('.ba-range');
    var stage = fig.querySelector('.after');
    if (!range || !stage) return;

    var apply = function () { fig.style.setProperty('--pos', range.value + '%'); };
    apply();
    range.addEventListener('input', apply); /* strzalki na klawiaturze */

    /* podpowiedz na wejsciu w kadr — pokazujemy, ze to suwak */
    var tick = null;
    var stopTeaser = function () { if (tick) { clearInterval(tick); tick = null; } };
    if (!reduce && 'IntersectionObserver' in window) {
      var teaser = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          teaser.unobserve(e.target);
          var v = 50, dir = -1, steps = 0;
          tick = setInterval(function () {
            v += dir * 2;
            if (v <= 34) dir = 1;
            if (v >= 50 && steps > 0) { stopTeaser(); v = 50; }
            if (v <= 34) steps++;
            range.value = v;
            apply();
          }, 22);
        });
      }, { threshold: 0.5 });
      teaser.observe(fig);
    }

    if (!hasPointer) return; /* zostaje natywny suwak */

    var setFromX = function (clientX) {
      var r = stage.getBoundingClientRect();
      if (!r.width) return;
      var pct = (clientX - r.left) / r.width * 100;
      range.value = pct < 0 ? 0 : (pct > 100 ? 100 : pct);
      apply();
    };

    var id = null, startX = 0, moved = false;

    fig.addEventListener('pointerdown', function (e) {
      var r = stage.getBoundingClientRect();
      /* podpis pod zdjeciem nie przesuwa suwaka */
      if (e.clientY < r.top || e.clientY > r.bottom) return;
      stopTeaser();
      id = e.pointerId;
      startX = e.clientX;
      moved = false;
      if (e.pointerType !== 'touch') {
        /* mysz i rysik: skok od razu, przeciaganie poza kadr tez ma dzialac */
        moved = true;
        try { fig.setPointerCapture(id); } catch (err) {}
        setFromX(e.clientX);
      }
    });

    fig.addEventListener('pointermove', function (e) {
      if (id === null || e.pointerId !== id) return;
      /* na dotyku czekamy na wyrazny ruch w poziomie — pion zostawiamy przewijaniu */
      if (!moved) {
        if (Math.abs(e.clientX - startX) < 6) return;
        moved = true;
        try { fig.setPointerCapture(id); } catch (err) {}
      }
      e.preventDefault();
      setFromX(e.clientX);
    });

    fig.addEventListener('pointerup', function (e) {
      if (id === null || e.pointerId !== id) return;
      if (!moved) setFromX(e.clientX); /* zwykle tapniecie w kadr */
      try { fig.releasePointerCapture(id); } catch (err) {}
      id = null;
    });

    fig.addEventListener('pointercancel', function (e) {
      if (id === null || e.pointerId !== id) return; /* przejal przewijanie strony */
      id = null;
    });
  });

  /* ---------- cookies ---------- */
  var cookieBar = document.getElementById('cookie-bar');
  if (cookieBar) {
    var KEY = 'diw-cookies-v1', seen = false;
    try { seen = localStorage.getItem(KEY) === 'ok'; } catch (e) {}
    if (!seen) {
      cookieBar.classList.add('show');
      var ok = document.getElementById('cookie-ok');
      if (ok) ok.addEventListener('click', function () {
        cookieBar.classList.remove('show');
        try { localStorage.setItem(KEY, 'ok'); } catch (e) {}
      });
    }
  }

  /* ---------- czat ---------- */
  var chatPanel = document.getElementById('chat-panel');
  var chatFab = document.getElementById('chat-fab');

  if (chatPanel && chatFab) {
    var CHAT_URL = 'https://pmresearch.app.n8n.cloud/webhook/dom-i-wnetrze-asystent';
    var chatLog = document.getElementById('chat-log');
    var chatForm = document.getElementById('chat-form');
    var chatInput = document.getElementById('chat-input');
    var chatSend = document.getElementById('chat-send');
    var chatChips = document.getElementById('chat-chips');
    var chatClose = document.getElementById('chat-close');
    var busy = false, greeted = false;

    var strona = (location.pathname.replace(/\/$/, '').split('/').pop() || 'index')
      .replace('demo-dom-i-wnetrze-', '')
      .replace('demo-dom-i-wnetrze', 'index');

    var sessionId;
    try {
      sessionId = sessionStorage.getItem('diw-chat');
      if (!sessionId) {
        sessionId = 'w' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
        sessionStorage.setItem('diw-chat', sessionId);
      }
    } catch (e) { sessionId = 'w' + Date.now().toString(36); }

    var addMsg = function (text, kind) {
      var el = document.createElement('div');
      el.className = 'msg ' + kind;
      el.textContent = text;
      chatLog.appendChild(el);
      chatLog.scrollTop = chatLog.scrollHeight;
      return el;
    };

    var ask = function (text) {
      if (busy || !text) return;
      busy = true;
      chatSend.disabled = true;
      if (chatChips) chatChips.style.display = 'none';
      addMsg(text, 'me');
      chatInput.value = '';
      var dots = document.createElement('div');
      dots.className = 'msg bot typing';
      dots.innerHTML = '<i></i><i></i><i></i>';
      dots.setAttribute('aria-label', 'Asystent pisze');
      chatLog.appendChild(dots);
      chatLog.scrollTop = chatLog.scrollHeight;

      fetch(CHAT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, sessionId: sessionId, page: strona })
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          dots.remove();
          addMsg(res && res.reply ? res.reply : 'Przepraszam, nie udało się odpowiedzieć. Zadzwoń proszę: 22 490 52 18.', 'bot');
        })
        .catch(function () {
          dots.remove();
          addMsg('Brak połączenia z asystentem. Zadzwoń proszę: 22 490 52 18.', 'err');
        })
        .finally(function () {
          busy = false;
          chatSend.disabled = false;
          chatInput.focus();
        });
    };

    var openChat = function () {
      chatPanel.classList.add('open');
      chatFab.style.display = 'none';
      chatFab.setAttribute('aria-expanded', 'true');
      if (!greeted) {
        greeted = true;
        addMsg('Dzień dobry! Odpowiem na pytania o zakres prac, ceny i terminy, a jeśli chcesz — umówię bezpłatny obmiar u Ciebie.', 'bot');
      }
      chatInput.focus();
    };
    var closeChat = function () {
      chatPanel.classList.remove('open');
      chatFab.style.display = '';
      chatFab.setAttribute('aria-expanded', 'false');
      chatFab.focus();
    };

    chatFab.addEventListener('click', openChat);
    chatClose.addEventListener('click', closeChat);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && chatPanel.classList.contains('open')) closeChat();
    });
    chatForm.addEventListener('submit', function (e) { e.preventDefault(); ask(chatInput.value.trim()); });
    if (chatChips) chatChips.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () { ask(b.textContent.trim()); });
    });
    document.querySelectorAll('[data-chat-open]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        openChat();
        var q = el.getAttribute('data-chat-ask');
        if (q) ask(q);
      });
    });
  }

  /* ---------- formularz ---------- */
  var form = document.getElementById('lead-form');
  if (!form) return;
  var status = document.getElementById('form-status');

  var params = new URLSearchParams(location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
    var i = form.querySelector('input[name="' + k + '"]');
    if (i && params.get(k)) i.value = params.get(k);
  });

  var setStatus = function (t, kind) {
    if (!status) return;
    status.textContent = t;
    status.className = 'form-status' + (kind ? ' ' + kind : '');
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var trap = form.querySelector('input[name="firma"]');
    if (trap && trap.value) return;
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var button = form.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
    setStatus('Wysyłam zgłoszenie…');

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data.consent = form.querySelector('input[name="consent"]').checked;
    data.page_url = location.href;
    delete data.firma;

    fetch('https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.status === 'OK' || res.status === 'DUPLIKAT') {
          form.querySelectorAll('input,textarea,select,button').forEach(function (el) { el.disabled = true; });
          setStatus(res.wiadomosc || 'Dziękujemy — odezwiemy się i umówimy obmiar.', 'ok');
        } else {
          if (button) button.disabled = false;
          setStatus(res.wiadomosc || 'Nie udało się wysłać. Sprawdź dane i spróbuj ponownie.', 'err');
        }
      })
      .catch(function () {
        if (button) button.disabled = false;
        setStatus('Błąd połączenia. Zadzwoń do nas: 22 490 52 18.', 'err');
      });
  });
})();
