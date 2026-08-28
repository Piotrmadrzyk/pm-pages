/* ═══════════════════════════════════════════════════════════════
   new age Lewandowska — wspólne zachowania wszystkich podstron
   ═══════════════════════════════════════════════════════════════ */

/* ── menu na telefonie ──────────────────────────────────────── */
(function () {
  var przycisk = document.getElementById('hamburger');
  var menu = document.getElementById('menu-mobilne');
  if (!przycisk || !menu) return;
  przycisk.addEventListener('click', function () {
    var otwarte = menu.classList.toggle('otwarte');
    przycisk.setAttribute('aria-expanded', otwarte ? 'true' : 'false');
    przycisk.setAttribute('aria-label', otwarte ? 'Zamknij menu' : 'Otwórz menu');
  });
})();

/* ── odsłanianie sekcji przy przewijaniu ───────────────────── */
(function () {
  var cele = document.querySelectorAll('.wejscie, .kosmyk');
  if (!cele.length) return;
  if (!('IntersectionObserver' in window)) {
    cele.forEach(function (e) { e.classList.add('widoczny'); });
    return;
  }
  var obs = new IntersectionObserver(function (wpisy) {
    wpisy.forEach(function (w) {
      if (w.isIntersecting) { w.target.classList.add('widoczny'); obs.unobserve(w.target); }
    });
  }, { threshold: .12, rootMargin: '0px 0px -8% 0px' });
  cele.forEach(function (e) { obs.observe(e); });
})();

/* ── powiększanie zdjęć ─────────────────────────────────────
   Dyplomy trzeba dać się przeczytać, a miniatura tego nie da.  */
(function () {
  var przyciski = document.querySelectorAll('.powieksz');
  if (!przyciski.length) return;

  var lupa = document.createElement('div');
  lupa.className = 'lupa';
  lupa.setAttribute('role', 'dialog');
  lupa.setAttribute('aria-modal', 'true');
  lupa.innerHTML =
    '<button class="lupa-zamknij" type="button" aria-label="Zamknij">✕</button>' +
    '<img alt=""><p class="lupa-podpis"></p>';
  document.body.appendChild(lupa);

  var obraz = lupa.querySelector('img');
  var podpis = lupa.querySelector('.lupa-podpis');
  var zamknij = lupa.querySelector('.lupa-zamknij');
  var ostatni = null;

  function otworz(przycisk) {
    ostatni = przycisk;
    obraz.src = przycisk.dataset.pelne;
    obraz.alt = przycisk.querySelector('img') ? przycisk.querySelector('img').alt : '';
    podpis.textContent = przycisk.dataset.podpis || '';
    lupa.classList.add('otwarta');
    document.body.style.overflow = 'hidden';
    zamknij.focus();
  }
  function zamknijLupe() {
    lupa.classList.remove('otwarta');
    obraz.removeAttribute('src');
    document.body.style.overflow = '';
    if (ostatni) ostatni.focus();
  }

  przyciski.forEach(function (p) {
    p.addEventListener('click', function () { otworz(p); });
  });
  zamknij.addEventListener('click', zamknijLupe);
  lupa.addEventListener('click', function (e) { if (e.target === lupa) zamknijLupe(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lupa.classList.contains('otwarta')) zamknijLupe();
  });
})();

/* ── gwiazdki oceny ─────────────────────────────────────────── */
(function () {
  var grupa = document.querySelector('.ocena-gwiazdki');
  if (!grupa) return;
  function odswiez() {
    var wybrana = grupa.querySelector('input:checked');
    var ile = wybrana ? parseInt(wybrana.value, 10) : 0;
    grupa.querySelectorAll('label').forEach(function (l, i) {
      l.classList.toggle('wybrana', i < ile);
    });
  }
  grupa.addEventListener('change', odswiez);
  odswiez();
})();

/* ── wysyłka opinii ─────────────────────────────────────────
   Opinia idzie do n8n. Workflow trzeba jeszcze założyć — do tego
   czasu formularz zgłasza błąd zamiast udawać, że wysłał.        */
(function () {
  var form = document.getElementById('form-opinia');
  if (!form) return;
  var ADRES = 'https://pmresearch.app.n8n.cloud/webhook/newage-opinia';
  var status = document.getElementById('op-status');
  var przycisk = document.getElementById('op-wyslij');

  function pokaz(tekst, klasa) {
    status.textContent = tekst;
    status.className = 'status ' + (klasa || '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.strona.value) return;                     /* pułapka na roboty */

    var imie = form.imie.value.trim();
    var tresc = form.tresc.value.trim();
    if (!imie || !tresc) { pokaz('Podaj imię i treść opinii.', 'blad'); return; }
    if (!form.zgoda.checked) { pokaz('Potrzebuję zgody na przetwarzanie danych.', 'blad'); return; }

    var ocena = form.querySelector('input[name=ocena]:checked');
    przycisk.disabled = true;
    pokaz('Wysyłam…');

    fetch(ADRES, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        form_key: 'newage-opinia',
        imie: imie,
        email: form.email.value.trim(),
        ocena: ocena ? Number(ocena.value) : null,
        tresc: tresc,
        consent: true,
        strona: 'new age Lewandowska'
      })
    })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json().catch(function () { return {}; }); })
      .then(function () { form.reset(); pokaz('Dziękuję — opinia do mnie dotarła.', 'ok'); })
      .catch(function () { pokaz('Nie udało się wysłać. Zadzwoń proszę: 506 116 008.', 'blad'); })
      .then(function () { przycisk.disabled = false; });
  });
})();
