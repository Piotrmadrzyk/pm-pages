/* Piekarnia Kłos — skrypty strony */
(function () {
  'use strict';

  /* ---------- menu mobilne ---------- */
  var toggle = document.getElementById('nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- niezawodne przewijanie do sekcji ----------
     Własne fonty (EB Garamond / Merriweather) doczytują się już PO
     pierwszym renderze i zmieniają wysokość tekstu — natywne przewinięcie
     do #kotwicy (czy to przy wejściu z linkiem w adresie, czy po kliknięciu
     w menu) trafiało wtedy w miejsce sprzed przeliczenia układu i wyglądało,
     jakby „nic się nie otworzyło”. Przewijamy dopiero, gdy fonty są gotowe. */
  function scrollToTarget(id) {
    var target = document.getElementById(id);
    if (!target) return;
    var go = function () { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(go).catch(go);
    } else {
      go();
    }
  }
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    var id = a.getAttribute('href').slice(1);
    if (!id || !document.getElementById(id)) return;
    a.addEventListener('click', function (e) {
      e.preventDefault();
      history.pushState(null, '', '#' + id);
      scrollToTarget(id);
    });
  });
  if (location.hash.length > 1) {
    window.addEventListener('load', function () { scrollToTarget(location.hash.slice(1)); });
  }

  /* ---------- animacje przy przewijaniu ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add('in'); });
    }
  }

  /* ---------- lista produktów: liczniki + podsumowanie ---------- */
  var picker = document.getElementById('order-picker');
  var summary = document.getElementById('order-summary');
  var orderField = document.querySelector('input[name="order"]');
  var submitBtn = document.getElementById('order-submit');

  function refreshSummary() {
    var items = [];
    var total = 0;
    picker.querySelectorAll('.pick-item').forEach(function (row) {
      var qty = parseInt(row.querySelector('.qty-val').textContent, 10) || 0;
      row.classList.toggle('picked', qty > 0);
      if (qty > 0) {
        var price = parseFloat(row.dataset.price);
        total += price * qty;
        items.push(row.dataset.name + ' × ' + qty);
      }
    });
    if (items.length) {
      summary.textContent = 'Zamówienie: ' + items.join(', ') + '. Razem: ' + total + ' zł (płatność przy odbiorze).';
      summary.classList.remove('empty');
      orderField.value = items.join(', ');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Zamawiam — odbiór osobisty';
    } else {
      summary.textContent = 'Nie wybrałeś jeszcze żadnego produktu.';
      summary.classList.add('empty');
      orderField.value = '';
      submitBtn.disabled = true;
      submitBtn.textContent = 'Wybierz produkt, żeby zamówić';
    }
  }

  if (picker) {
    picker.addEventListener('click', function (e) {
      var btn = e.target.closest('.qty-btn');
      if (!btn) return;
      var row = btn.closest('.pick-item');
      var valEl = row.querySelector('.qty-val');
      var qty = parseInt(valEl.textContent, 10) || 0;
      if (btn.classList.contains('plus')) qty += 1;
      else qty = Math.max(0, qty - 1);
      valEl.textContent = qty;
      refreshSummary();
    });
    refreshSummary();
  }

  /* ---------- formularz „Zamów online” (demo) ---------- */
  var orderForm = document.getElementById('order-form');
  var orderStatus = document.getElementById('order-status');
  if (orderForm && orderStatus) {
    orderForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!orderForm.checkValidity() || !orderField.value) {
        orderForm.reportValidity();
        return;
      }
      var data = new FormData(orderForm);
      var day = data.get('day');
      var time = data.get('time');
      orderStatus.textContent =
        'To formularz demonstracyjny — zamówienie („' + orderField.value + '”) nie trafiło do prawdziwej piekarni. ' +
        'W gotowej wersji strony taki formularz wysyłałby SMS z potwierdzeniem odbioru ' +
        (day && time ? 'na ' + day.toLowerCase() + ', godz. ' + time + '.' : '.');
      orderStatus.classList.add('ok');
      orderForm.reset();
      picker.querySelectorAll('.qty-val').forEach(function (el) { el.textContent = '0'; });
      refreshSummary();
    });
  }
})();
