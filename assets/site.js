/* Probatum — wspólne zachowanie serwisu. Bez bibliotek zewnętrznych. */
(function () {
  'use strict';

  var LEAD_ENDPOINT = 'https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture';
  var lastFocus = null;

  function one(selector, root) {
    return (root || document).querySelector(selector);
  }

  function all(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function setVisible(element, visible) {
    if (element) element.classList.toggle('show', visible);
  }

  function qsParam(name) {
    return new URLSearchParams(window.location.search).get(name) || '';
  }

  function siteHref(file) {
    var script = one('script[src*="assets/site.js"]');
    try {
      return new URL('../' + file, script ? script.src : window.location.href).pathname;
    } catch (error) {
      return '/' + file;
    }
  }

  function request(payload) {
    var controller = new AbortController();
    var timer = window.setTimeout(function () { controller.abort(); }, 15000);
    return fetch(LEAD_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal
    }).then(function (response) {
      window.clearTimeout(timer);
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.text().then(function (text) {
        if (!text) return {};
        try { return JSON.parse(text); } catch (error) { return {}; }
      });
    }).catch(function (error) {
      window.clearTimeout(timer);
      throw error;
    });
  }

  function firstInvalid(form) {
    return one(':invalid', form);
  }

  function showFormError(box, message) {
    if (!box) return;
    box.textContent = message;
    box.classList.add('show');
    box.setAttribute('role', 'alert');
  }

  function initNavigation() {
    var button = one('.burger');
    var menu = one('.navmobile');
    if (!button || !menu) return;

    function closeMenu(restoreFocus) {
      menu.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      button.setAttribute('aria-label', 'Otwórz menu');
      if (restoreFocus) button.focus();
    }

    button.addEventListener('click', function () {
      var open = !menu.classList.contains('open');
      menu.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
      button.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
      if (open) one('a', menu).focus();
    });

    all('a', menu).forEach(function (link) {
      link.addEventListener('click', function () { closeMenu(false); });
    });

    document.addEventListener('click', function (event) {
      if (menu.classList.contains('open') && !menu.contains(event.target) && !button.contains(event.target)) {
        closeMenu(false);
      }
      all('.navmore[open]').forEach(function (details) {
        if (!details.contains(event.target)) details.removeAttribute('open');
      });
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.classList.contains('open')) closeMenu(true);
    });
  }

  function initQuoteChoices() {
    all('.chiprow').forEach(function (row) {
      var hidden = one(row.getAttribute('data-target'));
      all('.chip', row).forEach(function (chip) {
        chip.setAttribute('aria-pressed', 'false');
        chip.addEventListener('click', function () {
          all('.chip', row).forEach(function (item) {
            item.classList.remove('on');
            item.setAttribute('aria-pressed', 'false');
          });
          chip.classList.add('on');
          chip.setAttribute('aria-pressed', 'true');
          row.classList.remove('chip-error');
          if (hidden) hidden.value = chip.getAttribute('data-value') || chip.textContent.trim();
        });
      });
    });
  }

  function initContactTopics() {
    var box = one('[data-tematy]');
    if (!box) return;
    var service = one('#k-usluga');
    var companyFields = one('[data-pola-firmy]');
    var company = one('#k-firma');
    var phone = one('#k-telefon');

    function choose(chip, shouldScroll) {
      all('.temat-chip', box).forEach(function (item) {
        item.setAttribute('aria-pressed', String(item === chip));
      });
      if (service) service.value = chip.getAttribute('data-temat') || '';
      var isAcademy = service && service.value === 'Kod dostępu do Akademii AI';
      var isOther = service && service.value === 'Coś innego';
      if (companyFields) companyFields.classList.add('widoczne');
      if (company) company.required = !isAcademy && !isOther;
      if (phone) phone.required = !isAcademy;
      box.classList.remove('chip-error');
      if (shouldScroll) chip.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }

    box.addEventListener('click', function (event) {
      var chip = event.target.closest('.temat-chip');
      if (chip && box.contains(chip)) choose(chip, false);
    });

    var anchor = (window.location.hash || '').slice(1);
    if (/^[a-z0-9-]+$/.test(anchor)) {
      var matching = one('[data-kotwica="' + anchor + '"]', box);
      if (matching) window.setTimeout(function () { choose(matching, true); }, 120);
    }
  }

  function initLeadForms() {
    all('form[data-lead-form]').forEach(function (form) {
      var formKey = form.getAttribute('data-form-key') || '';
      var success = one(form.getAttribute('data-success-target'));
      var errorBox = one(form.getAttribute('data-error-target'));
      var button = one('button[type="submit"]', form);
      var idleText = button ? button.textContent : '';
      var sending = false;

      form.addEventListener('submit', function (event) {
        event.preventDefault();
        if (sending) return;
        var trap = one('input[name="strona_www"]', form);
        if (trap && trap.value) return;

        var service = one('input[name="usluga"]', form);
        if (service && service.required && !service.value) {
          var choices = one('.chiprow, [data-tematy]', form);
          if (choices) choices.classList.add('chip-error');
          showFormError(errorBox, 'Wybierz, czego dotyczy wiadomość.');
          if (choices) choices.scrollIntoView({ block: 'center', behavior: 'smooth' });
          return;
        }

        if (!form.checkValidity()) {
          var invalid = firstInvalid(form);
          if (invalid) invalid.reportValidity();
          showFormError(errorBox, 'Uzupełnij zaznaczone pola i spróbuj ponownie.');
          return;
        }

        var data = new FormData(form);
        var message = data.get('wiadomosc') || data.get('opis') || '';
        var details = [];
        if (data.get('usluga')) details.push('Usługa: ' + data.get('usluga'));
        if (data.get('firma')) details.push('Firma/NIP: ' + data.get('firma'));
        if (data.get('www_klienta')) details.push('Obecna strona: ' + data.get('www_klienta'));
        if (data.get('social_klienta')) details.push('Social: ' + data.get('social_klienta'));
        if (data.get('branza')) details.push('Branża: ' + data.get('branza'));
        if (data.get('budzet')) details.push('Budżet: ' + data.get('budzet'));
        if (details.length) message = details.join(' | ') + (message ? ' | ' + message : '');

        var payload = {
          form_key: formKey,
          imie: data.get('imie') || '',
          email: data.get('email') || '',
          telefon: data.get('telefon') || '',
          tresc: message,
          usluga: data.get('usluga') || '',
          firma: data.get('firma') || '',
          www_klienta: data.get('www_klienta') || '',
          social_klienta: data.get('social_klienta') || '',
          consent: !!data.get('consent'),
          zrodlo: 'probatum.pl',
          utm_source: qsParam('utm_source'),
          utm_medium: qsParam('utm_medium'),
          utm_campaign: qsParam('utm_campaign'),
          utm_content: qsParam('utm_content'),
          utm_term: qsParam('utm_term'),
          page_url: window.location.href
        };

        sending = true;
        if (errorBox) errorBox.classList.remove('show');
        if (button) {
          button.disabled = true;
          button.textContent = 'Wysyłanie…';
        }

        request(payload).then(function () {
          form.hidden = true;
          setVisible(success, true);
          if (success) success.scrollIntoView({ block: 'center', behavior: 'smooth' });
        }).catch(function () {
          sending = false;
          if (button) {
            button.disabled = false;
            button.textContent = idleText;
          }
          showFormError(errorBox, 'Nie udało się wysłać wiadomości. Spróbuj ponownie albo napisz na kontakt@probatum.pl.');
        });
      });
    });
  }

  function initNewsletters() {
    all('[data-news-form]').forEach(function (form) {
      var button = one('button[type="submit"]', form);
      var idleText = button ? button.textContent : '';
      form.addEventListener('submit', function (event) {
        event.preventDefault();
        var email = one('input[type="email"]', form);
        var consent = one('input[type="checkbox"]', form);
        var success = one(form.getAttribute('data-news-ok'));
        var oldError = one('.news-error', form);
        if (oldError) oldError.remove();

        if (!form.checkValidity()) {
          var invalid = firstInvalid(form);
          if (invalid) invalid.reportValidity();
          return;
        }

        if (button) {
          button.disabled = true;
          button.textContent = 'Zapisuję…';
        }
        request({
          form_key: 'lista',
          imie: '',
          email: email ? email.value.trim() : '',
          telefon: '',
          tresc: 'Zapis na listę · ' + (form.getAttribute('data-skad') || document.title),
          consent: !!(consent && consent.checked),
          zrodlo: 'probatum.pl',
          page_url: window.location.href
        }).then(function () {
          form.hidden = true;
          setVisible(success, true);
        }).catch(function () {
          if (button) {
            button.disabled = false;
            button.textContent = idleText;
          }
          var message = document.createElement('p');
          message.className = 'news-error';
          message.setAttribute('role', 'alert');
          message.textContent = 'Nie udało się zapisać. Spróbuj ponownie albo napisz na kontakt@probatum.pl.';
          form.appendChild(message);
        });
      });
    });
  }

  function initChat() {
    var openButton = one('#chat-btn');
    var panel = one('#chat-panel');
    var closeButton = one('#chat-x');
    var body = one('#chat-body');
    var input = one('#chat-input');
    var sendButton = one('#chat-send');
    var suggestions = one('#chat-sug');
    if (!openButton || !panel || !body || !input) return;

    var answers = [
      { keys: ['cena', 'koszt', 'ile kosztuje', 'wycena', 'budżet', 'budzet'], text: 'Cena zależy od zakresu. Opisz firmę i cel, a przygotuję konkretne widełki.', link: ['Poproś o wycenę →', 'wycena.html'] },
      { keys: ['współpraca', 'wspolpraca', 'jak prac', 'proces'], text: 'Zaczynam od diagnozy. Potem ustalamy kierunek, przygotowuję projekt, wdrażam i pokazuję całość do zatwierdzenia.', link: ['Zobacz, jak pracuję →', 'o-donie.html'] },
      { keys: ['strona', 'www', 'witryna', 'realizac'], text: 'Projektuję strony dopasowane do branży i etapu firmy. Istniejące przykłady możesz otworzyć i sprawdzić w pełnym widoku.', link: ['Zobacz realizacje →', 'realizacje.html'] },
      { keys: ['kampania', 'reklama', 'marketing'], text: 'Kampania zaczyna się od celu i drogi klienta. Kreacja, strona i pomiar muszą pracować razem.', link: ['Zobacz ofertę →', 'oferta.html#kampanie'] },
      { keys: ['agent', 'automatyzacja', 'ai'], text: 'Agenci AI mogą przejąć część powtarzalnych zadań, ale zakres zawsze dobieram do realnego procesu firmy.', link: ['Poznaj agentów AI →', 'automatyzacja.html'] },
      { keys: ['termin', 'ile trwa', 'kiedy'], text: 'Termin zależy od zakresu i materiałów. Po krótkim briefie podam realny harmonogram zamiast obiecywać datę w ciemno.' },
      { keys: ['kontakt', 'telefon', 'mail', 'email'], text: 'Możesz użyć formularza albo napisać bezpośrednio. Każdą wiadomość czytam osobiście.', link: ['Przejdź do kontaktu →', 'kontakt.html'] }
    ];

    function addMessage(text, className, link) {
      var message = document.createElement('div');
      message.className = 'msg ' + className;
      message.textContent = text;
      if (link) {
        var anchor = document.createElement('a');
        anchor.href = siteHref(link[1]);
        anchor.textContent = link[0];
        message.appendChild(document.createElement('br'));
        message.appendChild(anchor);
      }
      body.appendChild(message);
      body.scrollTop = body.scrollHeight;
    }

    function respond(question) {
      var lower = question.toLowerCase();
      var hit = answers.find(function (item) {
        return item.keys.some(function (key) { return lower.indexOf(key) !== -1; });
      });
      window.setTimeout(function () {
        if (hit) addMessage(hit.text, 'bot', hit.link);
        else addMessage('Na to nie mam gotowej odpowiedzi. Napisz przez formularz, a odpowiem osobiście.', 'bot', ['Napisz wiadomość →', 'kontakt.html']);
      }, 220);
    }

    function openChat() {
      lastFocus = document.activeElement;
      panel.classList.add('open');
      panel.setAttribute('aria-hidden', 'false');
      openButton.setAttribute('aria-expanded', 'true');
      openButton.hidden = true;
      input.focus();
    }

    function closeChat() {
      panel.classList.remove('open');
      panel.setAttribute('aria-hidden', 'true');
      openButton.setAttribute('aria-expanded', 'false');
      openButton.hidden = false;
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function send() {
      var value = input.value.trim();
      if (!value) return;
      addMessage(value, 'user');
      input.value = '';
      respond(value);
    }

    openButton.addEventListener('click', openChat);
    if (closeButton) closeButton.addEventListener('click', closeChat);
    if (sendButton) sendButton.addEventListener('click', send);
    input.addEventListener('keydown', function (event) { if (event.key === 'Enter') send(); });
    if (suggestions) all('button', suggestions).forEach(function (button) {
      button.addEventListener('click', function () {
        addMessage(button.textContent, 'user');
        respond(button.textContent);
      });
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && panel.classList.contains('open')) closeChat();
    });
  }

  function initHomeState() {
    var hero = one('.spring-hero');
    if (!hero) return;
    function update() {
      document.body.classList.toggle('past-hero', hero.getBoundingClientRect().bottom < 140);
    }
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  document.addEventListener('DOMContentLoaded', function () {
    all('[data-js-submit]').forEach(function (button) { button.disabled = false; });
    all('[data-year]').forEach(function (year) { year.textContent = new Date().getFullYear(); });
    initNavigation();
    initQuoteChoices();
    initContactTopics();
    initLeadForms();
    initNewsletters();
    initChat();
    initHomeState();
  });
})();
