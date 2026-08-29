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

/* ── każde zdjęcie treściowe ma się dać powiększyć ──────────
   Człowiek odruchowo klika w zdjęcie i oczekuje, że się powiększy.
   Galerie to miały, ale zdjęcie główne, portret w „o mnie", kadry
   przy usługach i pas z tłem — już nie. Zamiast dopisywać przycisk
   w każdym szablonie z osobna, opakowujemy je tutaj: dzięki temu
   każde nowe zdjęcie dostanie to zachowanie samo z siebie.        */
(function () {
  var WYBOR = '.hero-foto img, .dwie img, .usluga-duza .u-foto > img, .pas img';
  document.querySelectorAll(WYBOR).forEach(function (obraz) {
    if (obraz.closest('.powieksz')) return;             /* już klikalne */

    var przycisk = document.createElement('button');
    przycisk.type = 'button';
    przycisk.className = 'powieksz powieksz-luzny';
    przycisk.dataset.pelne = obraz.currentSrc || obraz.src;
    przycisk.dataset.podpis = obraz.alt || '';
    przycisk.setAttribute('aria-label', 'Powiększ: ' + (obraz.alt || 'zdjęcie'));

    var lupa = document.createElement('span');
    lupa.className = 'kafel-lupa';
    lupa.setAttribute('aria-hidden', 'true');
    lupa.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="1.6"><circle cx="11" cy="11" r="7"/>' +
      '<path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg>';

    obraz.parentNode.insertBefore(przycisk, obraz);
    przycisk.appendChild(obraz);
    przycisk.appendChild(lupa);
  });
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

/* ── gwiazdki oceny ─────────────────────────────────────────
   Wcześniej gwiazdki tylko się zaznaczały. Teraz podświetlają się
   też przy najechaniu i pod każdą jest słowny opis oceny — inaczej
   nie wiadomo, czy kliknięcie w ogóle zadziałało.               */
(function () {
  var grupa = document.querySelector('.ocena-gwiazdki');
  if (!grupa) return;

  var OPISY = ['', 'Źle', 'Słabo', 'Może być', 'Dobrze', 'Świetnie'];
  var etykiety = [].slice.call(grupa.querySelectorAll('label'));
  var opis = document.createElement('p');
  opis.className = 'ocena-opis';
  grupa.parentNode.insertBefore(opis, grupa.nextSibling);

  function wybrana() {
    var w = grupa.querySelector('input:checked');
    return w ? parseInt(w.value, 10) : 0;
  }
  function maluj(ile, podglad) {
    etykiety.forEach(function (l, i) {
      l.classList.toggle('wybrana', !podglad && i < ile);
      l.classList.toggle('podswietlona', podglad && i < ile);
    });
    opis.textContent = ile ? OPISY[ile] : '';
  }

  grupa.addEventListener('change', function () { maluj(wybrana(), false); });

  etykiety.forEach(function (l, i) {
    l.addEventListener('mouseenter', function () { maluj(i + 1, true); });
    l.addEventListener('focus', function () { maluj(i + 1, true); });
  });
  grupa.addEventListener('mouseleave', function () { maluj(wybrana(), false); });

  maluj(wybrana(), false);
})();

/* ── wysyłka formularzy ────────────────────────────────────
   Formularze celuja w n8n. Dopoki workflow nie jest zalozony,
   wysylka konczy sie bledem — a pusty blad wyglada jak zepsuta
   strona i klientka po prostu odchodzi.

   Dlatego jest zapasowa droga: jesli n8n nie odpowie, otwiera sie
   program pocztowy z gotowa, wypelniona wiadomoscia. Nic nie ginie,
   a osoba widzi, ze cos sie stalo. Po zalozeniu workflow zapasowa
   droga po prostu przestanie sie uruchamiac.                      */
(function () {
  var MAIL = 'kontakt@probatum.pl';
  var TEL = '507 330 730';

  function obsluz(idFormularza, adres, klucz, zbierz, temat, gotowe) {
    var form = document.getElementById(idFormularza);
    if (!form) return;
    var status = form.querySelector('.status');
    var przycisk = form.querySelector('button[type=submit]');

    function pokaz(tekst, klasa) {
      if (!status) return;
      status.textContent = tekst;
      status.className = 'status ' + (klasa || '');
    }

    function przezPoczte(dane) {
      var tresc = Object.keys(dane)
        .filter(function (k) { return dane[k] !== '' && dane[k] !== null; })
        .map(function (k) { return k + ': ' + dane[k]; })
        .join('\n');
      var adresMail = 'mailto:' + MAIL +
        '?subject=' + encodeURIComponent(temat) +
        '&body=' + encodeURIComponent(tresc);
      window.location.href = adresMail;
      pokaz('Otwieram program pocztowy — wystarczy wysłać gotową wiadomość. ' +
            'Jeśli się nie otworzył, zadzwoń: ' + TEL + '.', 'ok');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.strona && form.strona.value) return;      /* pułapka na roboty */

      var dane = zbierz(form, pokaz);
      if (!dane) return;

      przycisk.disabled = true;
      pokaz('Wysyłam…');

      var czasomierz = setTimeout(function () { throw 0; }, 9000);
      fetch(adres, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.assign({ form_key: klucz }, dane))
      })
        .then(function (r) {
          clearTimeout(czasomierz);
          if (!r.ok) throw new Error(r.status);
          return r.json().catch(function () { return {}; });
        })
        .then(function () { form.reset(); pokaz(gotowe, 'ok'); })
        .catch(function () { clearTimeout(czasomierz); przezPoczte(dane); })
        .then(function () { przycisk.disabled = false; });
    });
  }

  /* opinia */
  obsluz('form-opinia',
    'https://pmresearch.app.n8n.cloud/webhook/newage-opinia', 'newage-opinia',
    function (f, pokaz) {
      var imie = f.imie.value.trim(), tresc = f.tresc.value.trim();
      if (!imie || !tresc) { pokaz('Podaj imię i treść opinii.', 'blad'); return null; }
      if (!f.zgoda.checked) { pokaz('Potrzebuję zgody na przetwarzanie danych.', 'blad'); return null; }
      var o = f.querySelector('input[name=ocena]:checked');
      return { imie: imie, email: f.email.value.trim(),
               ocena: o ? Number(o.value) : null, tresc: tresc, consent: true };
    },
    'Opinia dla new age Lewandowska',
    'Dziękuję — opinia do mnie dotarła.');

  /* zapytanie o termin i cenę */
  obsluz('form-wycena',
    'https://pmresearch.app.n8n.cloud/webhook/newage-kontakt', 'newage-kontakt',
    function (f, pokaz) {
      var imie = f.imie.value.trim(), tel = f.telefon.value.trim();
      if (!imie || !tel) { pokaz('Podaj imię i telefon — inaczej nie oddzwonię.', 'blad'); return null; }
      if (!f.zgoda.checked) { pokaz('Potrzebuję zgody na przetwarzanie danych.', 'blad'); return null; }
      return { imie: imie, telefon: tel, usluga: f.usluga.value,
               dlugosc: f.dlugosc.value, grubosc: f.grubosc.value,
               termin: f.termin.value, tresc: f.tresc.value.trim(), consent: true };
    },
    'Zapytanie o termin i cenę — new age Lewandowska',
    'Dziękuję — odezwę się najszybciej, jak będę mogła.');
})();
