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

  /* ---------- formularz „Zamów online” (demo) ---------- */
  var orderForm = document.getElementById('order-form');
  var orderStatus = document.getElementById('order-status');
  if (orderForm && orderStatus) {
    orderForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!orderForm.checkValidity()) {
        orderForm.reportValidity();
        return;
      }
      var data = new FormData(orderForm);
      var day = data.get('day');
      var time = data.get('time');
      orderStatus.textContent =
        'To formularz demonstracyjny — zamówienie nie trafiło do prawdziwej piekarni. ' +
        'W gotowej wersji strony taki formularz wysyłałby SMS z potwierdzeniem odbioru ' +
        (day && time ? 'na ' + day.toLowerCase() + ', godz. ' + time + '.' : '.');
      orderStatus.classList.add('ok');
      orderForm.reset();
    });
  }
})();
