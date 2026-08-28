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

/* ── powiększanie zdjęć z przewijaniem ──────────────────────
   Wcześniej trzeba było zamknąć jedno zdjęcie, żeby otworzyć następne.
   Teraz działają strzałki, klawiatura i przesunięcie palcem, a licznik
   pokazuje, ile zdjęć jest w tej galerii.                              */
(function () {
  var przyciski = [].slice.call(document.querySelectorAll('.powieksz'));
  if (!przyciski.length) return;

  var lupa = document.createElement('div');
  lupa.className = 'lupa';
  lupa.setAttribute('role', 'dialog');
  lupa.setAttribute('aria-modal', 'true');
  lupa.innerHTML =
    '<button class="lupa-zamknij" type="button" aria-label="Zamknij">✕</button>' +
    '<button class="lupa-strzalka wstecz" type="button" aria-label="Poprzednie zdjęcie">‹</button>' +
    '<button class="lupa-strzalka dalej" type="button" aria-label="Następne zdjęcie">›</button>' +
    '<div class="lupa-scena"><img alt=""></div>' +
    '<p class="lupa-podpis"></p>' +
    '<p class="lupa-licznik"></p>';
  document.body.appendChild(lupa);

  var obraz = lupa.querySelector('img');
  var podpis = lupa.querySelector('.lupa-podpis');
  var licznik = lupa.querySelector('.lupa-licznik');
  var zamknij = lupa.querySelector('.lupa-zamknij');
  var wstecz = lupa.querySelector('.wstecz');
  var dalej = lupa.querySelector('.dalej');
  var teraz = 0;

  function pokaz(i) {
    teraz = (i + przyciski.length) % przyciski.length;   /* zapętla się */
    var p = przyciski[teraz];
    obraz.style.opacity = 0;
    var nowy = new Image();
    nowy.onload = function () { obraz.src = nowy.src; obraz.style.opacity = 1; };
    nowy.src = p.dataset.pelne;
    var mini = p.querySelector('img');
    obraz.alt = mini ? mini.alt : '';
    podpis.textContent = p.dataset.podpis || '';
    licznik.textContent = (teraz + 1) + ' / ' + przyciski.length;
    /* przy jednym zdjeciu strzalki nie maja sensu */
    var wiele = przyciski.length > 1;
    wstecz.hidden = !wiele;
    dalej.hidden = !wiele;
    licznik.hidden = !wiele;
  }

  function otworz(i) {
    pokaz(i);
    lupa.classList.add('otwarta');
    document.body.style.overflow = 'hidden';
    zamknij.focus();
  }
  function zamknijLupe() {
    lupa.classList.remove('otwarta');
    obraz.removeAttribute('src');
    document.body.style.overflow = '';
    if (przyciski[teraz]) przyciski[teraz].focus();
  }

  przyciski.forEach(function (p, i) {
    p.addEventListener('click', function () { otworz(i); });
  });
  zamknij.addEventListener('click', zamknijLupe);
  wstecz.addEventListener('click', function (e) { e.stopPropagation(); pokaz(teraz - 1); });
  dalej.addEventListener('click', function (e) { e.stopPropagation(); pokaz(teraz + 1); });
  lupa.addEventListener('click', function (e) { if (e.target === lupa) zamknijLupe(); });

  document.addEventListener('keydown', function (e) {
    if (!lupa.classList.contains('otwarta')) return;
    if (e.key === 'Escape') zamknijLupe();
    if (e.key === 'ArrowLeft') pokaz(teraz - 1);
    if (e.key === 'ArrowRight') pokaz(teraz + 1);
  });

  /* przesuniecie palcem na telefonie */
  var startX = null;
  lupa.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, {passive: true});
  lupa.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var roznica = e.changedTouches[0].clientX - startX;
    if (Math.abs(roznica) > 45) pokaz(teraz + (roznica < 0 ? 1 : -1));
    startX = null;
  }, {passive: true});
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


/* ── wysuwany panel z dolnego doku ──────────────────────────
   Na telefonie kciuk siega dolu ekranu, nie gory strony.       */
(function () {
  var otworzGo = document.getElementById('dok-menu');
  var panel = document.getElementById('panel');
  var zaslona = document.getElementById('zaslona');
  if (!otworzGo || !panel || !zaslona) return;
  var zamknijGo = document.getElementById('panel-zamknij');

  function otworz() {
    panel.classList.add('widac');
    zaslona.classList.add('widac');
    otworzGo.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    if (zamknijGo) zamknijGo.focus();
  }
  function zamknij() {
    panel.classList.remove('widac');
    zaslona.classList.remove('widac');
    otworzGo.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    otworzGo.focus();
  }
  otworzGo.addEventListener('click', function () {
    panel.classList.contains('widac') ? zamknij() : otworz();
  });
  if (zamknijGo) zamknijGo.addEventListener('click', zamknij);
  zaslona.addEventListener('click', zamknij);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel.classList.contains('widac')) zamknij();
  });
})();

/* ── zapytanie o termin i cene ───────────────────────────── */
(function () {
  var form = document.getElementById('form-wycena');
  if (!form) return;
  var ADRES = 'https://pmresearch.app.n8n.cloud/webhook/newage-kontakt';
  var status = document.getElementById('k-status');
  var przycisk = document.getElementById('k-wyslij');

  function pokaz(tekst, klasa) {
    status.textContent = tekst;
    status.className = 'status ' + (klasa || '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.strona.value) return;

    var imie = form.imie.value.trim();
    var telefon = form.telefon.value.trim();
    if (!imie || !telefon) { pokaz('Podaj imię i telefon — inaczej nie oddzwonię.', 'blad'); return; }
    if (!form.zgoda.checked) { pokaz('Potrzebuję zgody na przetwarzanie danych.', 'blad'); return; }

    przycisk.disabled = true;
    pokaz('Wysyłam…');

    fetch(ADRES, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        form_key: 'newage-kontakt',
        imie: imie,
        telefon: telefon,
        usluga: form.usluga.value,
        dlugosc: form.dlugosc.value,
        grubosc: form.grubosc.value,
        termin: form.termin.value,
        tresc: form.tresc.value.trim(),
        consent: true,
        strona: 'new age Lewandowska'
      })
    })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json().catch(function () { return {}; }); })
      .then(function () { form.reset(); pokaz('Dziękuję — odezwę się najszybciej, jak będę mogła.', 'ok'); })
      .catch(function () { pokaz('Nie udało się wysłać. Zadzwoń proszę: 506 116 008.', 'blad'); })
      .then(function () { przycisk.disabled = false; });
  });
})();

/* ── otwarte czy zamknięte ──────────────────────────────────
   Ktoś, kto wchodzi na stronę o 19:00, chce wiedzieć od razu,
   czy ma sens dzwonić teraz, czy dopiero jutro rano.          */
(function () {
  var pole = document.getElementById('stan');
  if (!pole) return;

  /* 0 = niedziela … 6 = sobota; null = nieczynne */
  var GODZINY = { 0: null, 1: null, 2: [10, 18], 3: [10, 18], 4: [10, 18],
                  5: [10, 18], 6: [8, 13] };
  var NAZWY = ['niedzielę', 'poniedziałek', 'wtorek', 'środę', 'czwartek',
               'piątek', 'sobotę'];

  var teraz = new Date();
  var dzis = GODZINY[teraz.getDay()];
  var minuty = teraz.getHours() * 60 + teraz.getMinutes();

  if (dzis && minuty >= dzis[0] * 60 && minuty < dzis[1] * 60) {
    var doKonca = dzis[1] * 60 - minuty;
    pole.textContent = doKonca <= 60
      ? 'Otwarte — zamykam za ' + doKonca + ' min'
      : 'Otwarte do ' + dzis[1] + ':00';
    pole.className = 'stan otwarte';
  } else {
    /* znajdz najblizszy dzien roboczy */
    for (var i = 1; i <= 7; i++) {
      var d = (teraz.getDay() + i) % 7;
      if (GODZINY[d]) {
        var kiedy = (i === 1) ? 'jutro' : 'w ' + NAZWY[d];
        pole.textContent = 'Zamknięte · otwieram ' + kiedy + ' o ' +
          String(GODZINY[d][0]).padStart(2, '0') + ':00';
        break;
      }
    }
    pole.className = 'stan zamkniete';
  }
  pole.hidden = false;
})();
