#!/usr/bin/env python3
# Składa statyczne pliki HTML z jednego szablonu — wspólna nawigacja,
# stopka i widget FAQ na każdej podstronie.
import io, os, sys
import wpisy

# build/ lezy w katalogu repozytorium, wiec gotowe strony ida poziom wyzej.
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts')

# Odnosniki do regulaminu i polityki prywatnosci w stopce. Domyslnie WYLACZONE:
# dokumenty czekaja na akceptacje prawna i maja jeszcze luke przy operatorze
# platnosci. Wlacz dopiero, gdy beda gotowe:  DOKUMENTY=1 python3 build.py
DOKUMENTY = os.environ.get('DOKUMENTY', '0') == '1'
BLOK_DOKUMENTOW = ('        <h5 style="margin-top:1.2rem">Dokumenty</h5>\n'
                   '        <a href="regulamin.html">Regulamin</a>\n'
                   '        <a href="polityka-prywatnosci.html">Polityka prywatno\u015bci</a>\n')

# ── JEDNO MIEJSCE NA DANE KONTAKTOWE ──────────────────────────────────────
# Zmieniasz tutaj i uruchamiasz build.py — podmienia sie na wszystkich
# podstronach naraz. W szablonach uzywaj znacznikow {{EMAIL}}, {{TEL}},
# {{TEL_LINK}} zamiast wpisywac dane na sztywno.
KONTAKT = {
    'EMAIL':    'kontakt@probatum.pl',
    'TEL':      '+48 573 569 141',
    'TEL_LINK': '+48573569141',      # bez spacji — do href="tel:"

    # ── DANE DO REGULAMINU I POLITYKI PRYWATNOSCI ────────────────────────
    # UWAGA, Piotr, 28.08: Probatum to MARKA, nie firma. Kurs sprzedaje
    # inkubator przedsiebiorczosci — to on jest strona umowy z klientem,
    # on wystawia fakture i on jest administratorem danych. W regulaminie
    # musza wiec stac dane INKUBATORA, a Probatum wystepuje jako nazwa,
    # pod ktora prowadzony jest projekt.
    #
    # Wpisanie tu wlasnych danych Piotra byloby bledem merytorycznym:
    # klient zawiera umowe z podmiotem, ktory nie istnieje jako firma.
    #
    # Uzupelnij ponizsze pola danymi inkubatora (sa jawne w KRS) i uruchom
    # build.py — podmienia sie w obu dokumentach naraz. Dopoki sa puste,
    # build.py wypisuje ostrzezenie i wstawia widoczny znacznik
    # [DO UZUPELNIENIA], zeby nie dalo sie tego przeoczyc na zywej stronie.
    # Piotr, 28.08: inkubatorem jest TWOJ STARTUP (twojstartup.pl). Przez nich
    # idzie sprzedaz i oni wystawiaja faktury.
    # Dane potwierdzone 28.08 w dokumencie na serwerze samej fundacji
    # (twojstartup.pl/ObowiazekInformacyjnyRODOFundacja23-05-2018.pdf) oraz
    # zgodne z trzema niezaleznymi rejestrami KRS. To nie sa dane przepisane
    # z pamieci.
    #
    # UWAGA, zanim to trafi na produkcje: samo posiadanie danych NIE wystarczy.
    # Regulamin, w ktorym Fundacja wystepuje jako Sprzedawca, jest zobowiazaniem
    # zaciagnietym w jej imieniu, a §5 ust. 11 ich Regulaminu (od 1.06.2026)
    # mowi wprost, ze przystapienie do Programu Wsparcia NIE jest
    # pelnomocnictwem do reprezentacji Fundacji. Dokument wymaga ich akceptacji
    # — patrz notatka na Dysku 00_USTALENIA_BIZNESOWE_AKADEMIA.
    'SPRZEDAWCA_NAZWA': 'Fundacja Rozwoju Przedsiębiorczości „Twój StartUp”',
    'SPRZEDAWCA_ADRES': 'ul. Żurawia 6/12 lok. 766, 00-503 Warszawa',
    'SPRZEDAWCA_NIP':   '5213641211',
    'SPRZEDAWCA_KRS':   '0000442857',
    'MARKA':            'Probatum',
    # Przy modelu inkubatorowym najprostsza jest „Platnosc manualna” w Zanfii:
    # przelew na rachunek fundacji, potwierdzany recznie. Wtedy nie ma zadnego
    # zewnetrznego operatora i to pole opisuje wlasnie taki przelew.
    'OPERATOR_PLATNOSCI': '',
    'DATA_REGULAMINU':  '28 sierpnia 2026 r.',
}

# Pola, bez ktorych dokumenty prawne sa niekompletne.
WYMAGANE_DO_DOKUMENTOW = ('SPRZEDAWCA_NAZWA', 'SPRZEDAWCA_ADRES', 'SPRZEDAWCA_NIP',
                          'SPRZEDAWCA_KRS', 'OPERATOR_PLATNOSCI')

def dane(html):
    """Podmienia znaczniki kontaktowe w gotowym HTML-u.

    Puste pole firmowe zostawia widoczny slad zamiast pustki — inaczej zdanie
    „Sprzedawca:  , NIP ” wyszloby na produkcje i nikt by tego nie zauwazyl."""
    # Odnosniki do dokumentow prawnych — tylko gdy DOKUMENTY=1.
    html = html.replace('<!--DOKUMENTY-->', BLOK_DOKUMENTOW if DOKUMENTY else '')
    for k, v in KONTAKT.items():
        if not v and k in WYMAGANE_DO_DOKUMENTOW:
            v = '[DO UZUPEŁNIENIA: %s]' % k.replace('SPRZEDAWCA_', '').lower()
        html = html.replace('{{%s}}' % k, v).replace('[[%s]]' % k, v)
    return html


def ostrzez_o_danych():
    braki = [k for k in WYMAGANE_DO_DOKUMENTOW if not KONTAKT[k]]
    if braki:
        print('UWAGA: regulamin i polityka prywatnosci maja luki — uzupelnij w build.py: %s'
              % ', '.join(braki))
    return braki


NAV_GLOWNA = [
    ('oferta.html',       'Oferta'),
    ('realizacje.html',   'Realizacje'),
    ('o-donie.html',      'Jak pracuję'),
]

NAV_WIECEJ = [
    ('automatyzacja.html','Agenci AI'),
    ('akademia.html',     'Akademia AI'),
    ('warsztat.html',     'Warsztat'),
    ('blog.html',         'Blog'),
]

NAV_MOBILE = [('index.html', 'Start')] + NAV_GLOWNA + NAV_WIECEJ + [
    ('kontakt.html', 'Kontakt'),
]

PAGES = [
    dict(file='index.html', active='index.html',
         title='Probatum — nowe życie Twojej marki',
         desc='Nowoczesne strony internetowe, kampanie i komunikacja, które pokazują, jak naprawdę rozwinęła się Twoja firma.'),
    dict(file='o-donie.html', active='o-donie.html',
         title='Jak pracuję — od starej strony do nowego wizerunku | Probatum',
         desc='Poznaj spokojny i przejrzysty proces: diagnoza, kierunek, projekt, wdrożenie i ręczne zatwierdzenie przed publikacją.'),
    dict(file='oferta.html', active='oferta.html',
         title='Oferta — strony, kampanie i social media | Probatum',
         desc='Trzy usługi prowadzone tym samym sposobem: wielostronicowe witryny pod branżę, kampanie lejkowe z celem na każdym etapie i stałe prowadzenie profili społecznościowych.'),
    dict(file='realizacje.html', active='realizacje.html',
         title='Realizacje — strony dla różnych branż | Probatum',
         desc='Zobacz działające strony przygotowane dla różnych branż i otwórz każdą realizację w pełnym widoku.'),
    dict(file='automatyzacja.html', active='automatyzacja.html',
         title='Agenci do automatyzacji — co powstaje | Probatum',
         desc='Wdrożenia agentów automatyzujących powtarzalną pracę w firmie. Jeszcze nie w sprzedaży — trwa lista pierwszeństwa.'),
    dict(file='akademia.html', active='akademia.html',
         title='Akademia AI — kurs po polsku, dla ludzi bez technicznego zaplecza | Probatum',
         desc='Praktyczna nauka AI po polsku, przygotowana dla osób, które chcą usprawnić codzienną pracę bez technicznego zaplecza.'),
    dict(file='wycena.html', active='',
         title='Bezpłatna wycena projektu | Probatum',
         desc='Dwie minuty wypełniania, konkretne widełki w odpowiedzi. Zapytanie trafia bezpośrednio do mnie — odpisuję osobiście w 1–2 dni robocze.'),
    dict(file='warsztat.html', active='warsztat.html',
         title='Warsztat — automatyzacje, które zbudujesz sam | Probatum',
         desc='Instrukcje krok po kroku: jak własnymi rękami zbudować małe automatyzacje w swojej firmie. Za darmo, z prawdziwymi zrzutami ekranu.'),
    dict(file='blog.html', active='blog.html',
         title='Blog — nowości i ciekawostki o agentach | Probatum',
         desc='Co nowego w automatyzacji, co się sprawdza w praktyce i czego lepiej nie robić. Krótko i bez marketingowej waty.'),
    dict(file='kontakt.html', active='kontakt.html',
         title='Kontakt | Probatum',
         desc='Napisz przez formularz albo e-mail. Każda wiadomość trafia bezpośrednio do mnie — odpisuję osobiście, bez automatycznych szablonów.'),
    # Dokumenty — poza nawigacja glowna, linkowane ze stopki. Musza byc
    # dostepne przed zakupem i mozliwe do zapisania; stad zwykle podstrony,
    # a nie modal czy plik do pobrania.
    dict(file='regulamin.html', active='',
         title='Regulamin Akademii AI | Probatum',
         desc='Zasady sprzedaży i korzystania z kursu: co obejmuje każdy pakiet, jak dochodzi do zakupu, prawo odstąpienia, reklamacje i licencja.'),
    dict(file='polityka-prywatnosci.html', active='',
         title='Polityka prywatności | Probatum',
         desc='Jakie dane zbieram, po co, jak długo je trzymam i komu przekazuję. Kurs nie zbiera analityki i nikogo nie śledzi.'),
]

def odcisk(sciezka):
    """Skrot z zawartosci pliku — zmienia sie tylko wtedy, gdy plik faktycznie
    sie zmienil. Doklejany do adresu CSS/JS, zeby przegladarka nie serwowala
    starej wersji z pamieci podrecznej."""
    import hashlib
    with open(sciezka, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


def nav_links(active):
    out = []
    for href, label in NAV_GLOWNA:
        cls = ' class="active"' if href == active else ''
        out.append('    <a href="%s"%s>%s</a>' % (href, cls, label))
    wiecej_active = ' class="active"' if active in [x[0] for x in NAV_WIECEJ] else ''
    extra = []
    for href, label in NAV_WIECEJ:
        cls = ' class="active"' if href == active else ''
        extra.append('        <a href="%s"%s>%s</a>' % (href, cls, label))
    out.append('    <details class="navmore"%s><summary>Więcej</summary><div>\n%s\n      </div></details>'
               % (wiecej_active, '\n'.join(extra)))
    return '\n'.join(out)

def nav_mobile():
    out = []
    for href, label in NAV_MOBILE:
        out.append('  <a href="%s">%s</a>' % (href, label))
    out.append('  <a href="wycena.html">Poproś o wycenę</a>')
    return '\n'.join(out)

TPL = '''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#fcfdf9">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Probatum">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">

<script>document.documentElement.className += ' js';</script>

<link rel="stylesheet" href="assets/site.css?v={ODCISK_CSS}">
</head>
<body class="site">
<a class="skip-link" href="#main">Przejdź do treści</a>

<nav class="nav">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Probatum — strona główna">Probatum<i>.</i></a>
    <div class="navlinks">
{navlinks}
    </div>
    <a href="kontakt.html" class="navcta">Porozmawiajmy</a>
    <button type="button" class="burger" aria-label="Otwórz menu" aria-expanded="false" aria-controls="navmobile">Menu</button>
  </div>
</nav>
<div class="navmobile" id="navmobile" aria-label="Menu mobilne">
{navmobile}
</div>

<main id="main">
{body}
</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="index.html">Probatum<i>.</i></a>
        <p>Nowe strony i nowy wizerunek dla firm, które wyrosły ze swojej obecnej obecności w sieci.</p>
      </div>
      <div>
        <h5>Nawigacja</h5>
        <a href="o-donie.html">Jak pracuję</a>
        <a href="oferta.html">Oferta</a>
        <a href="realizacje.html">Realizacje</a>
        <a href="automatyzacja.html">Agenci AI</a>
        <a href="akademia.html">Akademia</a>
      </div>
      <div>
        <h5>Rozpocznij</h5>
        <a href="wycena.html">Poproś o wycenę</a>
        <a href="kontakt.html">Kontakt</a>
<!--DOKUMENTY-->      </div>
      <div>
        <h5>Kontakt</h5>
        <a href="mailto:[[EMAIL]]">[[EMAIL]]</a>
        <a href="tel:[[TEL_LINK]]">[[TEL]]</a>
        <p class="small" style="margin:0">Odpisuję osobiście, zwykle w 1–2 dni robocze.</p>
      </div>
    </div>
    <div class="foot-bottom">
      <span>Probatum © <span data-year>2026</span></span>
      <span>Strategia · projekt · wdrożenie</span>
    </div>
  </div>
</footer>

<button id="chat-btn" aria-label="Otwórz odpowiedzi na pytania" aria-controls="chat-panel" aria-expanded="false">Masz pytanie?</button>
<div id="chat-panel" role="dialog" aria-modal="false" aria-label="Najczęstsze pytania" aria-hidden="true">
  <div class="chat-head">
    <i class="led"></i>
    <div><b>W czym mogę pomóc?</b><span>Najczęstsze pytania przed rozmową</span></div>
    <button class="chat-x" id="chat-x" aria-label="Zamknij">×</button>
  </div>
  <div class="chat-body" id="chat-body">
    <div class="msg bot">Cześć. Tu znajdziesz krótkie odpowiedzi o ofercie i współpracy. Przy indywidualnym pytaniu napisz przez formularz — odpowiem osobiście.</div>
  </div>
  <div class="chat-sug" id="chat-sug">
    <button type="button">Ile to kosztuje?</button>
    <button type="button">Jak wygląda współpraca?</button>
    <button type="button">Czym są agenci AI?</button>
  </div>
  <div class="chat-in">
    <input type="text" id="chat-input" placeholder="Napisz pytanie...">
    <button type="button" id="chat-send">Wyślij</button>
  </div>
</div>

<script src="assets/site.js?v={ODCISK_JS}"></script>
<script src="assets/spring.js?v={ODCISK_SPRING}"></script>
</body>
</html>
'''

ODCISK_CSS = odcisk(os.path.join(OUT, 'assets', 'site.css'))
ODCISK_JS  = odcisk(os.path.join(OUT, 'assets', 'site.js'))
SPRING_JS_PATH = os.path.join(OUT, 'assets', 'spring.js')
ODCISK_SPRING = odcisk(SPRING_JS_PATH) if os.path.exists(SPRING_JS_PATH) else 'dev'
print('odcisk CSS: %s   odcisk JS: %s   odcisk filmu: %s' %
      (ODCISK_CSS, ODCISK_JS, ODCISK_SPRING))

built = 0
for p in PAGES:
    part = os.path.join(PARTS, p['file'])
    if not os.path.exists(part):
        print('POMINIĘTO (brak części): ' + p['file']); continue
    body = io.open(part, encoding='utf-8').read()
    html = TPL.format(title=p['title'], desc=p['desc'], body=body,
                      navlinks=nav_links(p['active']), navmobile=nav_mobile(),
                      ODCISK_CSS=ODCISK_CSS, ODCISK_JS=ODCISK_JS,
                      ODCISK_SPRING=ODCISK_SPRING)
    if p['file'] == 'index.html':
        preloads = ('<link rel="preload" as="image" href="assets/spring/dormant.webp" '
                    'media="(min-width:701px)" fetchpriority="high">\n'
                    '<link rel="preload" as="image" href="assets/spring/dormant-mobile.webp" '
                    'media="(max-width:700px)" fetchpriority="high">\n')
        html = html.replace('</head>', preloads + '</head>')
    io.open(os.path.join(OUT, p['file']), 'w', encoding='utf-8').write(dane(html))
    print('zbudowano: %s (%d znaków)' % (p['file'], len(html)))
    built += 1

STOPKA_WARSZTAT = (
    '<h3>Utkn\u0105\u0142e\u015b w po\u0142owie?</h3>'
    '<p>Ta instrukcja jest za darmo i zawsze b\u0119dzie. Ale je\u015bli co\u015b nie chce zadzia\u0142a\u0107 '
    'albo nie masz na to wieczor\u00f3w \u2014 mog\u0119 wdro\u017cy\u0107 to z Tob\u0105 albo za Ciebie.</p>'
    '<a href="../kontakt.html" class="btn">Napisz, co chcesz zautomatyzowa\u0107 \u2192</a>'
)

STOPKA_BLOG = (
    '<h3>Chcesz to u siebie?</h3>'
    '<p>W <a href="../warsztat.html">Warsztacie</a> pokazuj\u0119 krok po kroku, jak zbudowa\u0107 '
    'takie rzeczy samodzielnie. A je\u015bli wolisz mie\u0107 to z g\u0142owy \u2014 odezwij si\u0119.</p>'
    '<a href="../kontakt.html" class="btn">Porozmawiajmy \u2192</a>'
)


# ---------------------------------------------------------------
#  Wpisy: Blog i Warsztat
# ---------------------------------------------------------------
import re


def blok_listy(skad, naglowek, opis, prefiks=''):
    """Zachęta do zapisania się — inna tresc na blogu i w warsztacie,
       bo ludzie trafiaja tam z roznymi oczekiwaniami."""
    return (
        '<div class="news reveal">'
        '<div class="news-w">'
        '<div>'
        '<h3>%s</h3>'
        '<p>%s</p>'
        '</div>'
        '<div>'
        '<form class="news-form" data-news-form data-skad="%s" data-news-ok="#news-ok-%s">'
        '<input class="input" type="email" placeholder="twoj@adres.pl" required '
        'autocomplete="email" aria-label="Twój adres e-mail">'
        '<button type="submit" class="btn btn-primary" data-js-submit disabled>Zapisz mnie</button>'
        '<label class="news-mini" style="width:100%%;display:flex;gap:8px;align-items:flex-start">'
        '<input type="checkbox" required style="margin-top:3px;flex:none">'
        '<span>Zgadzam się na otrzymywanie wiadomości. '
        'Wypisujesz się jednym kliknięciem, adresu nie przekazuję nikomu.</span>'
        '</label>'
        '</form>'
        '<div class="news-ok" id="news-ok-%s">'
        'Zapisane. Pierwsza wiadomość przyjdzie, gdy będzie o czym pisać — nie wcześniej.'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    ) % (naglowek, opis, skad, skad, skad)


def do_podkatalogu(html):
    """Strony wpisow leza o poziom glebiej, wiec sciezki musza sie cofnac."""
    html = html.replace('href="assets/', 'href="../assets/')
    html = html.replace('src="assets/',  'src="../assets/')
    html = html.replace('url(assets/',   'url(../assets/')
    # linki nawigacji do stron w korzeniu
    html = re.sub(r'href="([a-z0-9-]+\.html)"', r'href="../\1"', html)
    # ...ale nie te, ktore juz sie cofnely
    html = html.replace('href="../../', 'href="../')
    return html


def karta_wpisu(w, katalog):
    meta = []
    if w.get('data'):
        meta.append('<time datetime="%s">%s</time>' % (w['data'], wpisy.data_po_polsku(w['data'])))
    for klucz, etykieta in (('czas', ''), ('poziom', ''), ('narzedzia', '')):
        if w.get(klucz):
            meta.append('<span>%s</span>' % w[klucz])
    return (
        '<a class="wpis-karta" href="%s/%s.html">'
        '<div class="wpis-meta">%s</div>'
        '<h3>%s</h3>'
        '<p>%s</p>'
        '<span class="arrow">Czytaj \u2192</span>'
        '</a>'
    ) % (katalog, w['plik'], ' \u00b7 '.join(meta), w['tytul'], w.get('opis', ''))


SEKCJE_LIST = {
    'blog': dict(
        naglowek='Blog',
        tytul='Co si\u0119 dzieje w automatyzacji',
        wstep='Nowo\u015bci, ciekawostki i rzeczy, kt\u00f3re sprawdzi\u0142em w praktyce: '
              'zar\u00f3wno te, kt\u00f3re zadzia\u0142a\u0142y, jak i te, kt\u00f3re nie.',
        pusto='Pierwsze wpisy pojawi\u0105 si\u0119 w najbli\u017cszych dniach.',
        news_h='Nie przegap tego, co dzia\u0142a',
        news_p='Dwa razy w tygodniu wysy\u0142am to, co sam sprawdzi\u0142em w praktyce, '
               'razem z tym, co nie zadzia\u0142a\u0142o. Bez ofert, bez waty, bez codziennego spamu.'),
    'warsztat': dict(
        naglowek='Warsztat',
        tytul='Automatyzacje, kt\u00f3re zbudujesz sam',
        wstep='Instrukcje krok po kroku, za darmo. Je\u015bli utkniesz, pomog\u0119 wdro\u017cy\u0107. '
              'A je\u015bli nie masz na to czasu, zrobi\u0119 to za Ciebie.',
        pusto='Pierwsze instrukcje pojawi\u0105 si\u0119 w najbli\u017cszych dniach.',
        news_h='Ka\u017cda nowa instrukcja prosto do Ciebie',
        news_p='Nowe automatyzacje krok po kroku, zanim trafi\u0105 gdziekolwiek indziej. '
               'Dostajesz te\u017c fragmenty podr\u0119cznika, nad kt\u00f3rym w\u0142a\u015bnie pracuj\u0119.'),
}

for katalog, opis in SEKCJE_LIST.items():
    lista = wpisy.wczytaj_katalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wpisy', katalog))

    karty = ''.join(karta_wpisu(w, katalog) for w in lista) if lista else \
            '<p class="small">%s</p>' % opis['pusto']

    body = (
        '<section class="phead %s">'
        '<div class="wrap">'
        '<span class="eyebrow">%s</span>'
        '<h1 class="display">%s</h1>'
        '<p class="lead">%s</p>'
        '</div></section>'
        '<section class="sec"><div class="wrap">'
        '<div class="wpis-lista">%s</div>'
        '%s'
        '</div></section>'
    ) % ('blue' if katalog == 'blog' else 'pink', opis['naglowek'], opis['tytul'], opis['wstep'], karty,
         blok_listy(katalog, opis['news_h'], opis['news_p']))

    strona = [x for x in PAGES if x['file'] == katalog + '.html'][0]
    html = TPL.format(title=strona['title'], desc=strona['desc'], body=body,
                      navlinks=nav_links(strona['active']), navmobile=nav_mobile(),
                      ODCISK_CSS=ODCISK_CSS, ODCISK_JS=ODCISK_JS,
                      ODCISK_SPRING=ODCISK_SPRING)
    io.open(os.path.join(OUT, katalog + '.html'), 'w', encoding='utf-8').write(dane(html))
    print('zbudowano: %s.html (%d wpis\u00f3w)' % (katalog, len(lista)))

    # pojedyncze wpisy
    kat_out = os.path.join(OUT, katalog)
    if not os.path.isdir(kat_out):
        os.makedirs(kat_out)
    for w in lista:
        meta = []
        if w.get('data'):
            meta.append('<time datetime="%s">%s</time>' % (w['data'], wpisy.data_po_polsku(w['data'])))
        for k in ('czas', 'poziom', 'narzedzia'):
            if w.get(k):
                meta.append('<span>%s</span>' % w[k])

        body = (
            '<article class="wpis">'
            '<div class="wrap">'
            '<a class="wpis-wroc" href="%s.html">\u2190 %s</a>'
            '<div class="wpis-meta">%s</div>'
            '<h1 class="display">%s</h1>'
            '<p class="lead">%s</p>'
            '<div class="wpis-tresc">%s</div>'
            '<div class="wpis-stopka">%s</div>'
            '</div></article>'
        ) % (katalog, SEKCJE_LIST[katalog]['naglowek'], ' \u00b7 '.join(meta),
             w['tytul'], w.get('opis', ''), wpisy.na_html(w['tresc']),
             STOPKA_WARSZTAT if katalog == 'warsztat' else STOPKA_BLOG)

        html = TPL.format(title=w['tytul'] + ' | Probatum',
                          desc=w.get('opis', '')[:180],
                          body=body,
                          navlinks=nav_links(katalog + '.html'), navmobile=nav_mobile(),
                          ODCISK_CSS=ODCISK_CSS, ODCISK_JS=ODCISK_JS,
                          ODCISK_SPRING=ODCISK_SPRING)
        io.open(os.path.join(kat_out, w['plik'] + '.html'), 'w', encoding='utf-8').write(dane(do_podkatalogu(html)))
        print('   \u2514 %s/%s.html' % (katalog, w['plik']))

print('--- gotowe: %d stron' % built)
ostrzez_o_danych()
