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
