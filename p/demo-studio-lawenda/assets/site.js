/* Studio Lawenda — skrypty strony */
(function () {
  'use strict';

  /* ---------- rok w stopce ---------- */
  document.querySelectorAll('.js-year').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- nagłówek: cień po odjechaniu od góry ---------- */
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
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
        burger.setAttribute('aria-label', 'Otwórz menu');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('open')) {
        header.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
      }
    });
  }

  /* ---------- pojawianie się sekcji ---------- */
  var reveals = document.querySelectorAll('.reveal');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- informacja o plikach cookie ---------- */
  var cookieBar = document.getElementById('cookie-bar');
  if (cookieBar) {
    var COOKIE_KEY = 'lawenda-cookies-v1';
    var seen = false;
    try { seen = localStorage.getItem(COOKIE_KEY) === 'ok'; } catch (e) { seen = false; }
    if (!seen) {
      cookieBar.classList.add('show');
      var accept = document.getElementById('cookie-ok');
      if (accept) {
        accept.addEventListener('click', function () {
          cookieBar.classList.remove('show');
          try { localStorage.setItem(COOKIE_KEY, 'ok'); } catch (e) {}
        });
      }
    }
  }

  /* ---------- widget czatu ---------- */
  var chatPanel = document.getElementById('chat-panel');
  var chatFab = document.getElementById('chat-fab');

  if (chatPanel && chatFab) {
    var CHAT_URL = 'https://pmresearch.app.n8n.cloud/webhook/studio-lawenda-asystent';
    var chatLog = document.getElementById('chat-log');
    var chatForm = document.getElementById('chat-form');
    var chatInput = document.getElementById('chat-input');
    var chatSend = document.getElementById('chat-send');
    var chatChips = document.getElementById('chat-chips');
    var chatClose = document.getElementById('chat-close');
    var busy = false;
    var greeted = false;

    /* nazwa podstrony — trafia do logu rozmow, zeby bylo wiadomo skad pytanie */
    var strona = (location.pathname.replace(/\/$/, '').split('/').pop() || 'index')
      .replace('demo-studio-lawenda-', '')
      .replace('demo-studio-lawenda', 'index');

    /* identyfikator rozmowy — trzyma watek w obrebie jednej karty przegladarki */
    var sessionId;
    try {
      sessionId = sessionStorage.getItem('lawenda-chat');
      if (!sessionId) {
        sessionId = 'w' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
        sessionStorage.setItem('lawenda-chat', sessionId);
      }
    } catch (e) {
      sessionId = 'w' + Date.now().toString(36);
    }

    var scrollDown = function () { chatLog.scrollTop = chatLog.scrollHeight; };

    var addMsg = function (text, kind) {
      var el = document.createElement('div');
      el.className = 'msg ' + kind;
      el.textContent = text;
      chatLog.appendChild(el);
      scrollDown();
      return el;
    };

    var showTyping = function () {
      var el = document.createElement('div');
      el.className = 'msg bot typing';
      el.innerHTML = '<i></i><i></i><i></i>';
      el.setAttribute('aria-label', 'Asystentka pisze');
      chatLog.appendChild(el);
      scrollDown();
      return el;
    };

    var ask = function (text) {
      if (busy || !text) return;
      busy = true;
      chatSend.disabled = true;
      if (chatChips) chatChips.style.display = 'none';
      addMsg(text, 'me');
      chatInput.value = '';
      var dots = showTyping();

      fetch(CHAT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, sessionId: sessionId, page: strona })
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          dots.remove();
          addMsg(res && res.reply ? res.reply : 'Przepraszam, nie udało się odpowiedzieć. Zadzwoń proszę: 17 853 62 14.', 'bot');
        })
        .catch(function () {
          dots.remove();
          addMsg('Brak połączenia z asystentką. Zadzwoń proszę: 17 853 62 14.', 'err');
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
        addMsg('Dzień dobry! Odpowiem na pytania o zabiegi, ceny i przygotowanie do wizyty, a jeśli chcesz — pomogę dobrać termin.', 'bot');
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

    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      ask(chatInput.value.trim());
    });

    if (chatChips) {
      chatChips.querySelectorAll('button').forEach(function (b) {
        b.addEventListener('click', function () { ask(b.textContent.trim()); });
      });
    }

    /* odnosniki "zapytaj asystentki" rozsiane po stronie */
    document.querySelectorAll('[data-chat-open]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        openChat();
        var q = el.getAttribute('data-chat-ask');
        if (q) ask(q);
      });
    });
  }

  /* ---------- formularz rezerwacji ---------- */
  var form = document.getElementById('lead-form');
  if (!form) return;
  var status = document.getElementById('form-status');

  /* przeniesienie parametrów kampanii z adresu do ukrytych pól */
  var params = new URLSearchParams(location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (key) {
    var input = form.querySelector('input[name="' + key + '"]');
    if (input && params.get(key)) input.value = params.get(key);
  });

  var setStatus = function (text, kind) {
    if (!status) return;
    status.textContent = text;
    status.className = 'form-status' + (kind ? ' ' + kind : '');
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    /* pułapka na boty — wypełnione pole oznacza automat */
    var trap = form.querySelector('input[name="firma"]');
    if (trap && trap.value) return;

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var button = form.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
    setStatus('Wysyłam zgłoszenie…');

    var data = {};
    new FormData(form).forEach(function (value, key) { data[key] = value; });
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
          setStatus(res.wiadomosc || 'Dziękujemy — odezwiemy się z propozycją terminu.', 'ok');
        } else {
          if (button) button.disabled = false;
          setStatus(res.wiadomosc || 'Nie udało się wysłać. Sprawdź dane i spróbuj ponownie.', 'err');
        }
      })
      .catch(function () {
        if (button) button.disabled = false;
        setStatus('Błąd połączenia. Zadzwoń do nas: 17 853 62 14.', 'err');
      });
  });
})();
