#!/usr/bin/env python3
# Składa statyczne pliki HTML z jednego szablonu — wspólna nawigacja,
# stopka i widget FAQ na każdej podstronie.
import io, os, sys
import wpisy

# build/ lezy w katalogu repozytorium, wiec gotowe strony ida poziom wyzej.
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts')

# ── JEDNO MIEJSCE NA DANE KONTAKTOWE ──────────────────────────────────────
# Zmieniasz tutaj i uruchamiasz build.py — podmienia sie na wszystkich
# podstronach naraz. W szablonach uzywaj znacznikow {{EMAIL}}, {{TEL}},
# {{TEL_LINK}} zamiast wpisywac dane na sztywno.
KONTAKT = {
    'EMAIL':    'kontakt@probatum.pl',
    'TEL':      '+48 573 569 141',
    'TEL_LINK': '+48573569141',      # bez spacji — do href="tel:"
}

def dane(html):
    """Podmienia znaczniki kontaktowe w gotowym HTML-u."""
    for k, v in KONTAKT.items():
        html = html.replace('{{%s}}' % k, v).replace('[[%s]]' % k, v)
    return html


NAV = [
    ('index.html',        'Start'),
    ('o-donie.html',      'Metoda'),
    ('oferta.html',       'Oferta'),
    ('realizacje.html',   'Realizacje'),
    ('automatyzacja.html','Agenci'),
    ('akademia.html',     'Akademia'),
    ('warsztat.html',     'Warsztat'),
    ('blog.html',         'Blog'),
    ('kontakt.html',      'Kontakt'),
]

PAGES = [
    dict(file='index.html', active='index.html',
         title='Probatum — strony internetowe, kampanie i social media',
         desc='Wielostronicowe witryny, kampanie lejkowe i prowadzenie profili społecznościowych dla małych i średnich firm w całej Polsce. Pierwsza wersja w 5–7 dni, publikacja w 10–14.'),
    dict(file='o-donie.html', active='o-donie.html',
         title='Metoda — jak powstaje Twoja strona, krok po kroku | Probatum',
         desc='87 zautomatyzowanych elementów w 8 obszarach, cztery role wykonawcze i jedna zasada nadrzędna: żadnej publikacji bez ręcznego zatwierdzenia.'),
    dict(file='oferta.html', active='oferta.html',
         title='Oferta — strony internetowe, kampanie lejkowe, social media | Probatum',
         desc='Trzy usługi, jedna metoda: wielostronicowe witryny pod branżę, kampanie lejkowe z celem na każdym etapie i stałe prowadzenie profili społecznościowych.'),
    dict(file='realizacje.html', active='realizacje.html',
         title='Realizacje — pięć żywych stron, zero mockupów | Probatum',
         desc='Pięć w pełni działających, wielostronicowych witryn osadzonych na żywo. Nie zrzuty ekranu — prawdziwe strony, które możesz otworzyć i sprawdzić.'),
    dict(file='automatyzacja.html', active='automatyzacja.html',
         title='Agenci do automatyzacji — co powstaje | Probatum',
         desc='Wdrożenia agentów automatyzujących powtarzalną pracę w firmie. Jeszcze nie w sprzedaży — trwa lista pierwszeństwa.'),
    dict(file='akademia.html', active='akademia.html',
         title='Akademia AI — kurs po polsku, dla ludzi bez technicznego zaplecza | Probatum',
         desc='62 lekcje praktyczne, 39 prezentacji, 8 prowadzonych projektów i gotowe pakiety dla pięciu branż. Każda lekcja kończy się poleceniem, które wklejasz i używasz tego samego dnia.'),
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
    for href, label in NAV:
        cls = ' class="active"' if href == active else ''
        out.append('    <a href="%s"%s>%s</a>' % (href, cls, label))
    return '\n'.join(out)

def nav_mobile():
    out = []
    for href, label in NAV:
        out.append('  <a href="%s">%s</a>' % (href, label))
    out.append('  <a href="wycena.html">Wyceń projekt</a>')
    return '\n'.join(out)

TPL = '''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#07080b">
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

<!-- 25.08.2026: zdjete Google Fonts. Instrument Serif + Manrope + JetBrains Mono to
     domyslny zestaw generatorow stron — czytelnik rozpoznaje go od pierwszego rzutu oka.
     Teraz czcionka systemowa: strona wyglada jak zwykly serwis, laduje sie natychmiast
     i nie odpytuje serwerow Google przy kazdym wejsciu. -->
<link rel="stylesheet" href="assets/site.css?v={ODCISK_CSS}">
</head>
<body>

<nav class="nav">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="sygnet" aria-hidden="true">P</span>
      <span class="brand-txt">
        <b>Probatum<i>.</i></b>
        <span>przewaga metodą</span>
      </span>
    </a>
    <div class="navlinks">
{navlinks}
    </div>
    <a href="wycena.html" class="navcta">Wyceń projekt</a>
    <button type="button" class="burger" aria-label="Menu" aria-expanded="false" aria-controls="navmobile"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="navmobile" id="navmobile">
{navmobile}
</div>

{body}

<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <span class="sygnet sygnet-lg" aria-hidden="true">P</span>
        <b>Probatum<i>.</i></b>
        <p>Strony internetowe, kampanie lejkowe i prowadzenie profili społecznościowych dla małych i średnich firm. Pracuję zdalnie, z całą Polską.</p>
        <div class="foot-social" data-social-foot></div>
      </div>
      <div>
        <h5>Nawigacja</h5>
        <a href="o-donie.html">Metoda</a>
        <a href="oferta.html">Oferta</a>
        <a href="realizacje.html">Realizacje</a>
        <a href="automatyzacja.html">Agenci</a>
        <a href="akademia.html">Akademia</a>
      </div>
      <div>
        <h5>Rozpocznij</h5>
        <a href="wycena.html">Wyceń projekt</a>
        <a href="kontakt.html">Kontakt</a>
      </div>
      <div>
        <h5>Kontakt</h5>
        <a href="mailto:[[EMAIL]]">[[EMAIL]]</a>
        <a href="tel:[[TEL_LINK]]">[[TEL]]</a>
        <p class="small" style="margin:0">Odpisuję osobiście, zwykle w 1–2 dni robocze.</p>
      </div>
    </div>
    <div class="foot-bottom">
      <span>Probatum © <span data-year>2026</span></span>
      <span>Każda publikacja zatwierdzona ręcznie</span>
    </div>
  </div>
</footer>

<button id="chat-btn" aria-label="Otwórz asystenta strony">Asystent strony</button>
<div id="chat-panel" role="dialog" aria-label="Asystent strony">
  <div class="chat-head">
    <i class="led"></i>
    <div><b>Asystent strony</b><span>Odpowiedzi na najczęstsze pytania</span></div>
    <button class="chat-x" id="chat-x" aria-label="Zamknij">×</button>
  </div>
  <div class="chat-body" id="chat-body">
    <div class="msg bot">Cześć. Odpowiadam na najczęstsze pytania o ofertę, ceny i terminy. Po coś bardziej szczegółowego — napisz przez formularz, odpiszę osobiście.</div>
  </div>
  <div class="chat-sug" id="chat-sug">
    <button>Ile to kosztuje?</button>
    <button>Ile trwa strona?</button>
    <button>Czym są agenci?</button>
  </div>
  <div class="chat-in">
    <input type="text" id="chat-input" placeholder="Napisz pytanie...">
    <button id="chat-send">Wyślij</button>
  </div>
</div>

<script src="assets/site.js?v={ODCISK_JS}"></script>
</body>
</html>
'''

ODCISK_CSS = odcisk(os.path.join(OUT, 'assets', 'site.css'))
ODCISK_JS  = odcisk(os.path.join(OUT, 'assets', 'site.js'))
print('odcisk CSS: %s   odcisk JS: %s' % (ODCISK_CSS, ODCISK_JS))

built = 0
for p in PAGES:
    part = os.path.join(PARTS, p['file'])
    if not os.path.exists(part):
        print('POMINIĘTO (brak części): ' + p['file']); continue
    body = io.open(part, encoding='utf-8').read()
    html = TPL.format(title=p['title'], desc=p['desc'], body=body,
                      navlinks=nav_links(p['active']), navmobile=nav_mobile(),
                      ODCISK_CSS=ODCISK_CSS, ODCISK_JS=ODCISK_JS)
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
        '<button type="submit" class="btn btn-primary">Zapisz mnie</button>'
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
        tytul='Co si\u0119 dzieje w <em>automatyzacji</em>.',
        wstep='Nowo\u015bci, ciekawostki i rzeczy, kt\u00f3re sprawdzi\u0142em w praktyce \u2014 '
              'zar\u00f3wno te, kt\u00f3re zadzia\u0142a\u0142y, jak i te, kt\u00f3re nie.',
        pusto='Pierwsze wpisy pojawi\u0105 si\u0119 w najbli\u017cszych dniach.',
        news_h='Nie przegap tego, co <em>dzia\u0142a</em>.',
        news_p='Dwa razy w tygodniu wysy\u0142am to, co sam sprawdzi\u0142em w praktyce \u2014 '
               'razem z tym, co nie zadzia\u0142a\u0142o. Bez ofert, bez waty, bez codziennego spamu.'),
    'warsztat': dict(
        naglowek='Warsztat',
        tytul='Automatyzacje, kt\u00f3re <em>zbudujesz sam</em>.',
        wstep='Instrukcje krok po kroku, za darmo. Je\u015bli utkniesz \u2014 pomog\u0119 wdro\u017cy\u0107. '
              'A je\u015bli nie masz na to czasu, zrobi\u0119 to za Ciebie.',
        pusto='Pierwsze instrukcje pojawi\u0105 si\u0119 w najbli\u017cszych dniach.',
        news_h='Ka\u017cda nowa instrukcja <em>prosto do Ciebie</em>.',
        news_p='Nowe automatyzacje krok po kroku, zanim trafi\u0105 gdziekolwiek indziej. '
               'Dostajesz te\u017c fragmenty podr\u0119cznika, nad kt\u00f3rym w\u0142a\u015bnie pracuj\u0119.'),
}

for katalog, opis in SEKCJE_LIST.items():
    lista = wpisy.wczytaj_katalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wpisy', katalog))

    karty = ''.join(karta_wpisu(w, katalog) for w in lista) if lista else \
            '<p class="small">%s</p>' % opis['pusto']

    body = (
        '<section class="phead tlo-foto" style="background-image:url(assets/img/sekcje/%s)">'
        '<div class="wrap">'
        '<span class="eyebrow">%s</span>'
        '<h1 class="display">%s</h1>'
        '<p class="lead">%s</p>'
        '</div></section>'
        '<section class="sec"><div class="wrap">'
        '<div class="wpis-lista">%s</div>'
        '%s'
        '</div></section>'
    ) % ('agenci-nocne-biuro.jpg' if katalog == 'blog' else 'metoda-zatwierdzenie.jpg',
         opis['naglowek'], opis['tytul'], opis['wstep'], karty,
         blok_listy(katalog, opis['news_h'], opis['news_p']))

    strona = [x for x in PAGES if x['file'] == katalog + '.html'][0]
    html = TPL.format(title=strona['title'], desc=strona['desc'], body=body,
                      navlinks=nav_links(strona['active']), navmobile=nav_mobile(),
                      ODCISK_CSS=ODCISK_CSS, ODCISK_JS=ODCISK_JS)
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
                          ODCISK_CSS=ODCISK_CSS, ODCISK_JS=ODCISK_JS)
        io.open(os.path.join(kat_out, w['plik'] + '.html'), 'w', encoding='utf-8').write(dane(do_podkatalogu(html)))
        print('   \u2514 %s/%s.html' % (katalog, w['plik']))

print('--- gotowe: %d stron' % built)
