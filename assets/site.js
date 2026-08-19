// PM Przewaga Metoda - site.js (Dona)

document.addEventListener('DOMContentLoaded', function(){

  // Mobile nav toggle
  var burger = document.querySelector('.navburger');
  var mobileNav = document.querySelector('.navmobile');
  if(burger && mobileNav){
    burger.setAttribute('aria-expanded', 'false');
    burger.addEventListener('click', function(){
      var open = mobileNav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mobileNav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        mobileNav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Hero video: skip autoplay/preload on mobile or when the visitor prefers reduced motion
  // (partial mitigation for oversized hero video — see audit P0-7; full re-encode still pending)
  document.querySelectorAll('.hero-bg video').forEach(function(video){
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var isSmallScreen = window.matchMedia && window.matchMedia('(max-width: 760px)').matches;
    if(reduceMotion || isSmallScreen){
      video.removeAttribute('autoplay');
      video.setAttribute('preload', 'none');
      video.pause();
    } else {
      video.setAttribute('preload', 'auto');
      var playPromise = video.play();
      if(playPromise && playPromise.catch){ playPromise.catch(function(){}); }
    }
  });

  // Scroll reveal
  var revealEls = document.querySelectorAll('.reveal, .reveal-stagger');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, {threshold:0.15});
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    revealEls.forEach(function(el){ el.classList.add('in'); });
  }

  // Starfield generator (used on pages with .stars container)
  document.querySelectorAll('.stars').forEach(function(starsEl){
    var html = '';
    for(var i=0;i<90;i++){
      var top = Math.random()*100, left = Math.random()*100, size = Math.random()*1.6+0.6, op = Math.random()*0.6+0.2;
      html += '<span style="position:absolute;top:'+top+'%;left:'+left+'%;width:'+size+'px;height:'+size+'px;opacity:'+op+';background:#fff;border-radius:50%;"></span>';
    }
    starsEl.innerHTML = html;
  });

  // Orbit tick marks (used on pages with .ticks container inside .portal-wrap)
  document.querySelectorAll('.ticks').forEach(function(ticksEl){
    var html = '';
    for(var i=0;i<24;i++){
      var deg = i * 15;
      html += '<div class="tick" style="position:absolute;top:50%;left:50%;width:1px;height:270px;margin-top:-270px;margin-left:-0.5px;transform-origin:50% 270px;transform:rotate('+deg+'deg);"><i style="position:absolute;top:0;left:0;width:1px;height:7px;background:rgba(255,255,255,.16);display:block;"></i></div>';
    }
    ticksEl.innerHTML = html;
  });

  // Animated counters
  document.querySelectorAll('[data-count]').forEach(function(el){
    var target = parseInt(el.getAttribute('data-count'), 10);
    if(isNaN(target)) return;
    var started = false;
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting && !started){
          started = true;
          var cur = 0;
          var step = Math.max(1, Math.round(target/40));
          var iv = setInterval(function(){
            cur += step;
            if(cur >= target){ cur = target; clearInterval(iv); }
            el.textContent = cur;
          }, 25);
        }
      });
    }, {threshold:0.4});
    obs.observe(el);
  });

  // ===== Form handling (real backend: PM Agent OS — Lead Capture, n8n) =====
  var LEAD_ENDPOINT = 'https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture';

  function qsParam(name){
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
  }

  document.querySelectorAll('form[data-lead-form]').forEach(function(form){
    var formKey = form.getAttribute('data-form-key');
    var okBox = document.querySelector(form.getAttribute('data-success-target'));
    var errBox = document.querySelector(form.getAttribute('data-error-target'));
    var submitBtn = form.querySelector('button[type="submit"]');
    var submitBtnDefaultText = submitBtn ? submitBtn.textContent : '';
    var isSubmitting = false;

    function showError(msg){
      if(!errBox) return;
      errBox.textContent = msg;
      errBox.classList.add('show');
    }
    function hideError(){
      if(errBox) errBox.classList.remove('show');
    }

    // Chip error state clears as soon as a chip is picked (see chip handler below)
    var uslugaInput = form.querySelector('#usluga-value');
    var chiprow = form.querySelector('.chiprow');

    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(isSubmitting) return;

      // Honeypot — real visitors never fill this hidden field
      var honeypot = form.querySelector('input[name="strona_www"]');
      if(honeypot && honeypot.value){ return; }

      // Required chip-select validation (P0-6)
      if(uslugaInput && uslugaInput.hasAttribute('required') && !uslugaInput.value){
        if(chiprow) chiprow.classList.add('chip-error');
        showError('Wybierz jedną z opcji powyżej, żeby przejść dalej.');
        return;
      }

      var consentBox = form.querySelector('input[name="consent"]');
      if(consentBox && !consentBox.checked){
        showError('Zaznacz zgodę na przetwarzanie danych, żeby wysłać formularz.');
        return;
      }

      hideError();

      var fd = new FormData(form);
      var tresc = fd.get('wiadomosc') || fd.get('opis') || '';
      if(fd.get('usluga')){
        var extra = ['Usługa: ' + fd.get('usluga')];
        if(fd.get('firma')) extra.push('Firma: ' + fd.get('firma'));
        if(fd.get('branza')) extra.push('Branża: ' + fd.get('branza'));
        if(fd.get('budzet')) extra.push('Budżet: ' + fd.get('budzet'));
        tresc = extra.join(' | ') + ' | ' + tresc;
      }
      if(fd.get('temat')) tresc = 'Temat: ' + fd.get('temat') + ' | ' + tresc;

      var payload = {
        form_key: formKey,
        imie: fd.get('imie') || '',
        email: fd.get('email') || '',
        telefon: fd.get('telefon') || '',
        tresc: tresc,
        consent: !!(consentBox && consentBox.checked),
        zrodlo: 'przewagametoda.pl',
        utm_source: qsParam('utm_source'),
        utm_medium: qsParam('utm_medium'),
        utm_campaign: qsParam('utm_campaign'),
        utm_content: qsParam('utm_content'),
        utm_term: qsParam('utm_term'),
        page_url: window.location.href
      };

      isSubmitting = true;
      if(submitBtn){ submitBtn.disabled = true; submitBtn.textContent = 'Wysyłanie...'; }

      fetch(LEAD_ENDPOINT, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      }).then(function(res){
        return res.json().catch(function(){ return {}; }).then(function(data){
          return {ok: res.ok, data: data};
        });
      }).then(function(result){
        isSubmitting = false;
        if(submitBtn){ submitBtn.disabled = false; submitBtn.textContent = submitBtnDefaultText; }
        var status = result.data && result.data.status;
        if(result.ok && (status === 'OK' || status === 'DUPLIKAT')){
          if(okBox){
            form.style.display = 'none';
            okBox.classList.add('show');
          }
        } else {
          showError((result.data && result.data.wiadomosc) || 'Coś poszło nie tak. Spróbuj ponownie albo napisz bezpośrednio na e-mail.');
        }
      }).catch(function(){
        isSubmitting = false;
        if(submitBtn){ submitBtn.disabled = false; submitBtn.textContent = submitBtnDefaultText; }
        showError('Nie udało się wysłać — sprawdź połączenie z internetem i spróbuj ponownie, albo napisz bezpośrednio na e-mail.');
      });
    });
  });

  // Chip-select groups (single select within a group)
  document.querySelectorAll('.chiprow').forEach(function(row){
    var hiddenInput = document.querySelector(row.getAttribute('data-target'));
    row.querySelectorAll('.chip').forEach(function(chip){
      chip.addEventListener('click', function(){
        row.querySelectorAll('.chip').forEach(function(c){ c.classList.remove('on'); });
        chip.classList.add('on');
        row.classList.remove('chip-error');
        if(hiddenInput) hiddenInput.value = chip.getAttribute('data-value') || chip.textContent.trim();
      });
    });
  });

  // ===== Site FAQ assistant widget (canned FAQ answers — not a live AI connection) =====
  var chatBtn = document.getElementById('dona-chat-btn');
  var chatPanel = document.getElementById('dona-chat-panel');
  var chatBody = document.getElementById('dona-chat-body');
  var chatInput = document.getElementById('dona-chat-input');
  var chatSend = document.getElementById('dona-chat-send');
  var chatSuggest = document.getElementById('dona-chat-suggest');

  var FAQ = [
    { keys: ['cena','koszt','ile kosztuje','wycena','budzet'], a: 'Wycena zależy od zakresu — strona wielostronicowa, kampania lejkowa czy prowadzenie social mediów mają różne widełki. Najszybciej dostaniesz konkretną liczbę przez formularz wyceny — wypełnienie zajmuje 2 minuty.', link: {label:'Otwórz formularz wyceny →', href:'wycena.html'} },
    { keys: ['strona','strony','www','witryna'], a: 'Buduję wielostronicowe witryny dopasowane do konkretnej branży — nie szablony z katalogu. Zobacz 5 pełnych realizacji w zakładce Realizacje, każda to gotowa, żywa strona.', link: {label:'Zobacz realizacje →', href:'realizacje.html'} },
    { keys: ['kampania','kampanie','lejek','marketing','reklama'], a: 'Kampanie lejkowe to ścieżka klienta zaprojektowana od pierwszego kontaktu po decyzję zakupową — z jasnym celem na każdym etapie, nie pojedyncze posty bez planu.', link: {label:'Zobacz ofertę →', href:'oferta.html#kampanie'} },
    { keys: ['social', 'media', 'instagram', 'facebook'], a: 'Prowadzę profile na bieżąco — dostarczasz materiał, resztą (treść, harmonogram, publikacja) zajmuje się system.', link: {label:'Zobacz ofertę →', href:'oferta.html#social'} },
    { keys: ['dona','agent','agenci','ai','jak dziala'], a: 'Dona to rdzeń systemu — zarządza 87 zautomatyzowanymi elementami w 8 obszarach (budowa stron, kampanie, social media i więcej). Każda praca przechodzi przeze mnie ręcznie, zanim trafi do sieci.', link: {label:'Poznaj Donę →', href:'o-donie.html'} },
    { keys: ['kontakt','telefon','mail','email','napisac'], a: 'Najprościej przez formularz kontaktowy — odpiszę osobiście. Adres e-mail też tam znajdziesz.', link: {label:'Przejdź do kontaktu →', href:'kontakt.html'} },
    { keys: ['ile trwa','czas','termin','szybko'], a: 'Pierwsza wersja strony zwykle powstaje w kilka dni, nie tygodni — każdy etap zatwierdzam ręcznie po drodze, więc tempo zależy też od Twoich odpowiedzi.' }
  ];

  function addMsg(text, cls, linkObj){
    var div = document.createElement('div');
    div.className = 'msg ' + cls;
    div.textContent = text;
    if(linkObj){
      var br = document.createElement('br');
      var a = document.createElement('a');
      a.href = linkObj.href;
      a.textContent = linkObj.label;
      a.style.color = cls === 'bot' ? '#5ad1ff' : '#00131c';
      a.style.fontWeight = '600';
      div.appendChild(br);
      div.appendChild(a);
    }
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function botReply(userText){
    var lower = userText.toLowerCase();
    var match = FAQ.find(function(f){ return f.keys.some(function(k){ return lower.indexOf(k) !== -1; }); });
    setTimeout(function(){
      if(match){
        addMsg(match.a, 'bot', match.link);
      } else {
        addMsg('Nie mam gotowej odpowiedzi na to pytanie, ale Piotr odpisze osobiście — najszybciej przez formularz kontaktowy albo wyceny.', 'bot', {label:'Przejdź do kontaktu →', href:'kontakt.html'});
      }
    }, 500);
  }

  if(chatBtn && chatPanel){
    chatBtn.addEventListener('click', function(){
      chatPanel.classList.toggle('open');
    });
    if(chatSend && chatInput){
      function sendMsg(){
        var val = chatInput.value.trim();
        if(!val) return;
        addMsg(val, 'user');
        chatInput.value = '';
        botReply(val);
      }
      chatSend.addEventListener('click', sendMsg);
      chatInput.addEventListener('keydown', function(e){ if(e.key === 'Enter') sendMsg(); });
    }
    if(chatSuggest){
      chatSuggest.querySelectorAll('button').forEach(function(b){
        b.addEventListener('click', function(){
          addMsg(b.textContent, 'user');
          botReply(b.textContent);
        });
      });
    }
  }

});
