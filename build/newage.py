# -*- coding: utf-8 -*-
"""
build/newage.py — strona new age Lewandowska (Czestochowa).

DLACZEGO GENERATOR, A NIE PIEC RECZNYCH PLIKOW
Strona ma szesc podstron ze wspolnym naglowkiem, menu i stopka. Gdyby kazda
byla pisana osobno, zmiana jednej pozycji w menu oznaczalaby szesc poprawek
i szanse, ze gdzies sie rozjedzie. Tutaj menu jest w jednym miejscu.

JAK URUCHOMIC
    cd build && python3 newage.py

CO POWSTAJE
    p/newage-lewandowska/index.html          Start
    p/newage-lewandowska/o-mnie/index.html   O mnie + osiem dyplomow
    p/newage-lewandowska/uslugi/index.html   Uslugi i dlaczego nie ma cennika
    p/newage-lewandowska/portfolio/index.html Sesje i praca w magazynie
    p/newage-lewandowska/opinie/index.html   Opinie + formularz
    p/newage-lewandowska/kontakt/index.html  Kontakt i mapa
    p/newage-lewandowska/styl.css            wspolne style
    p/newage-lewandowska/skrypt.js           wspolne zachowania

ADRESY SA KROTKIE — /o-mnie/, /uslugi/ — bo ta strona docelowo idzie na
wlasny hosting klientki, a nie zostaje pod probatum.pl. Przy przenoszeniu
wystarczy skopiowac caly katalog.

ZDJECIA
Kazde zdjecie ma dwie wersje: pelna i miniature (-mal). W galeriach laduje
sie miniatura, pelna dopiero po klknieciu. Bez tego strona z 34 zdjeciami
wazylaby kilkanascie megabajtow.
"""

import os
import io
import shutil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CEL = os.path.join(ROOT, 'p', 'newage-lewandowska')

TEL_POKAZ = u'+48 506 116 008'
TEL_LINK = u'+48506116008'
ADRES = u'ul. Jana Kilińskiego 55, 42-200 Częstochowa'

# ─────────────────────────────────────────────────────────────────
#  MENU — jedno miejsce dla wszystkich podstron
# ─────────────────────────────────────────────────────────────────
MENU = [
    ('start',     u'Start',     ''),
    ('o-mnie',    u'O mnie',    'o-mnie/'),
    ('uslugi',    u'Usługi',    'uslugi/'),
    ('portfolio', u'Portfolio', 'portfolio/'),
    ('opinie',    u'Opinie',    'opinie/'),
    ('kontakt',   u'Kontakt',   'kontakt/'),
]


def nawigacja(aktywna, korzen):
    poz = []
    for klucz, nazwa, sciezka in MENU:
        biezaca = ' aria-current="page"' if klucz == aktywna else ''
        poz.append(u'<a href="%s%s"%s>%s</a>' % (korzen, sciezka, biezaca, nazwa))
    return u'\n        '.join(poz)


def menu_mobilne(aktywna, korzen):
    poz = []
    for i, (klucz, nazwa, sciezka) in enumerate(MENU, 1):
        biezaca = ' aria-current="page"' if klucz == aktywna else ''
        poz.append(u'<a href="%s%s"%s><b>%02d</b>%s</a>' % (korzen, sciezka, biezaca, i, nazwa))
    return u'\n    '.join(poz)


# ─────────────────────────────────────────────────────────────────
#  DYPLOMY — osiem dokumentow, dwadziescia lat
# ─────────────────────────────────────────────────────────────────
DYPLOMY = [
    ('2003-toni-guy',       u'2003', u'Toni&amp;Guy Academy',
     u'Dyplom akademii, podpisany przez międzynarodowego dyrektora artystycznego'),
    ('2005-saks-london',    u'2005', u'Saks Academies — Londyn',
     u'Covent Garden. Szkolenie ze strzyżenia i koloryzacji'),
    ('2009-uprawnienia',    u'2009', u'Uprawnienia dla instruktorów',
     u'Kurs pedagogiczno-metodyczny dla wykładowców — formalne prawo do szkolenia innych'),
    ('2013-loreal-h3',      u'2013', u'L’Oréal H³',
     u'Dołączenie do międzynarodowego grona stylistów, Akademia L’Oréal Professionnel'),
    ('2018-loreal-blondy',  u'2018', u'L’Oréal — Blondy',
     u'Szkolenie z rozjaśniania w Akademii L’Oréal Professionnel'),
    ('2019-adam-reed',      u'2019', u'Cut &amp; Style — Adam Reed',
     u'Certyfikat podpisany osobiście przez Adama Reeda'),
    ('2022-berni-ottjes',   u'2022', u'Master Class — Berni Ottjes',
     u'Techniki koloryzacji, warsztaty praktyczne'),
    ('2023-min-kim',        u'2023', u'Master Class — Min Kim',
     u'Techniki koloryzacji z międzynarodową artystką L’Oréal'),
]

SESJA = [
    ('kadr-3609', u'Sesja na schodach'),
    ('kadr-1743', u'W salonie'),
    ('kadr-1727', u'Narzędzia pracy'),
    ('kadr-1738', u'Narzędzia pracy'),
    ('kadr-1741', u'Warsztat'),
    ('kadr-1719', u'Warsztat'),
    ('kadr-1718', u'Studio'),
    ('kadr-1720', u'Studio'),
    ('kadr-1726', u'Studio'),
]

PORTFOLIO = [
    ('sesja-3552', u'Magazyn SPLOT — sesja okładkowa'),
    ('sesja-3555', u'Magazyn SPLOT — rozkładówka'),
    ('sesja-3553', u'Magazyn SPLOT'),
    ('sesja-3554', u'Magazyn SPLOT'),
    ('sesja-3501', u'Stylizacja w klimacie lat 20.'),
    ('sesja-3497', u'Stylizacja w klimacie lat 20.'),
    ('sesja-3498', u'Stylizacja w klimacie lat 20.'),
    ('sesja-3499', u'Stylizacja w klimacie lat 20.'),
    ('sesja-3500', u'Stylizacja w klimacie lat 20.'),
    ('sesja-3503', u'Sesja katalogowa'),
    ('sesja-3504', u'Sesja katalogowa'),
    ('sesja-3505', u'Sesja katalogowa'),
    ('sesja-3506', u'Sesja katalogowa'),
    ('sesja-3507', u'Sesja katalogowa'),
    ('sesja-3508', u'Sesja katalogowa'),
    ('sesja-3509', u'Sesja katalogowa'),
]


def kafle(pozycje, katalog, klasa='galeria-siatka'):
    """Miniatury otwierajace pelne zdjecie po klknieciu."""
    out = []
    for p in pozycje:
        if len(p) == 4:
            plik, rok, tytul, opis = p
            podpis = u'%s · %s' % (rok, tytul)
            alt = u'%s — %s' % (tytul, opis)
        else:
            plik, podpis = p
            alt = podpis
        out.append(
            u'<figure class="kafel">\n'
            u'          <button type="button" class="powieksz" data-pelne="../img/%s/%s.jpg"'
            u' data-podpis="%s" aria-label="Powiększ: %s">\n'
            u'            <img src="../img/%s/%s-mal.jpg" alt="%s" loading="lazy" decoding="async">\n'
            u'          </button>\n'
            u'          <figcaption>%s</figcaption>\n'
            u'        </figure>' % (katalog, plik, podpis.replace('"', '&quot;'),
                                    podpis.replace('"', '&quot;'), katalog, plik,
                                    alt.replace('"', '&quot;'), podpis))
    return u'\n        '.join(out)


# ─────────────────────────────────────────────────────────────────
#  SZKIELET STRONY
# ─────────────────────────────────────────────────────────────────
SZKIELET = u"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>%(tytul)s</title>
<meta name="description" content="%(opis)s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@200;300;400;500&display=swap">
<link rel="stylesheet" href="%(korzen)sstyl.css">
</head>
<body>

<header class="naglowek">
  <div class="naglowek-in">
    <a class="marka" href="%(korzen)s" aria-label="new age Lewandowska — strona główna">
      <img src="%(korzen)simg/logo-biale.png" alt="new age Lewandowska" width="900" height="357">
    </a>
    <nav class="menu" aria-label="Nawigacja główna">
        %(menu)s
    </nav>
    <a class="naglowek-tel" href="tel:%(tel_link)s">%(tel_pokaz)s</a>
    <button class="hamburger" id="hamburger" type="button"
      aria-label="Otwórz menu" aria-expanded="false" aria-controls="menu-mobilne">
      <span></span><span></span><span></span>
    </button>
  </div>
  <nav class="menu-mobilne" id="menu-mobilne" aria-label="Menu">
    %(menu_mobilne)s
  </nav>
</header>

%(tresc)s

<footer class="stopka">
  <div class="wrap">
    <div class="stopka-siatka">
      <div>
        <img src="%(korzen)simg/logo-biale.png" alt="new age Lewandowska" width="900" height="357">
        <p style="max-width:34ch">
          Salon fryzjerski w Częstochowie. Koloryzacja, strzyżenie i modelowanie —
          po rozmowie, nie na skróty.
        </p>
      </div>
      <div>
        <h4>Na stronie</h4>
        %(stopka_menu)s
      </div>
      <div>
        <h4>Kontakt</h4>
        <a href="tel:%(tel_link)s">%(tel_pokaz)s</a>
        <span style="display:block; padding:.2rem 0">ul. Jana Kilińskiego 55<br>42-200 Częstochowa</span>
        <a href="https://www.instagram.com/new_age_lewandowska" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.facebook.com/profile.php?id=100057636820418" target="_blank" rel="noopener">Facebook</a>
      </div>
    </div>
    <div class="stopka-dol">
      <span>© 2026 new age Lewandowska</span>
      <span>Wersja robocza — strona w budowie</span>
    </div>
  </div>
</footer>

<script src="%(korzen)sskrypt.js"></script>
</body>
</html>
"""

PRZERYWNIK = u"""
<div class="przerywnik">
  <svg class="kosmyk" viewBox="0 0 560 60" aria-hidden="true">
    <path d="M4 30 C 90 30, 120 4, 190 12 C 262 20, 250 52, 310 50 C 372 48, 390 14, 452 22 C 508 29, 520 30, 556 30"/>
  </svg>
</div>
"""


def stopka_menu(korzen):
    return u'\n        '.join(
        u'<a href="%s%s">%s</a>' % (korzen, s, n) for _, n, s in MENU)


def zbuduj(klucz, tytul, opis, tresc, korzen):
    return SZKIELET % {
        'tytul': tytul, 'opis': opis, 'korzen': korzen,
        'menu': nawigacja(klucz, korzen),
        'menu_mobilne': menu_mobilne(klucz, korzen),
        'stopka_menu': stopka_menu(korzen),
        'tel_link': TEL_LINK, 'tel_pokaz': TEL_POKAZ,
        'tresc': tresc,
    }


def naglowek_strony(nadpis, h1, lead):
    return (u'<section class="tytul-strony">\n  <div class="wrap">\n'
            u'    <p class="nadpis">%s</p>\n    <h1>%s</h1>\n    <p>%s</p>\n'
            u'  </div>\n</section>\n' % (nadpis, h1, lead))


# ─────────────────────────────────────────────────────────────────
#  TRESCI PODSTRON
# ─────────────────────────────────────────────────────────────────

def strona_start():
    czolowka = u"""
<section class="hero" style="padding-top:clamp(28px,4vw,56px)">
  <div class="wrap">
    <div class="hero-siatka">
      <div>
        <p class="nadpis">Fryzjerstwo · Częstochowa</p>
        <h1>Włosy, które<br>ktoś <em>rozumie</em>.</h1>
        <p class="hero-lead">
          Agnieszka Lewandowska. Dwadzieścia lat przy fotelu, dyplomy Toni&amp;Guy
          i londyńskiego Saks, cztery szkolenia w Akademii L'Oréal Professionnel —
          i lata uczenia innych fryzjerek tego, co sama robi.
        </p>
        <div class="hero-akcje">
          <a class="btn" href="tel:%(tel_link)s">Umów wizytę</a>
          <a class="btn btn-duch" href="o-mnie/">Poznaj mnie</a>
        </div>
        <div class="odznaka"><b>5,0</b> ★ · setki opinii w Google</div>
      </div>
      <div class="hero-foto">
        <img src="img/hero.jpg" alt="Agnieszka Lewandowska" width="1024" height="1024" fetchpriority="high">
      </div>
    </div>
  </div>
</section>
""" % {'tel_link': TEL_LINK}

    dyplomy_skrot = u'\n      '.join(
        u'<img src="img/dyplomy/%s-mal.jpg" alt="%s — %s" loading="lazy">' % (p[0], p[1], p[2])
        for p in DYPLOMY)

    reszta = u"""
<section>
  <div class="wrap dwie">
    <img src="img/portret.jpg" alt="Agnieszka Lewandowska w salonie" width="733" height="1100" loading="lazy" class="wejscie">
    <div class="tresc wejscie">
      <p class="nadpis">O mnie</p>
      <h2>Nie zgaduję. <span class="kursywa">Wiem, co robię</span> — i umiem to wytłumaczyć.</h2>
      <p>
        Zaczynałam w 2003 roku dyplomem Toni&amp;Guy, dwa lata później szkoliłam się
        w Saks Academies w londyńskim Covent Garden. W 2009 zdobyłam uprawnienia
        pedagogiczne dla instruktorów — i przez lata prowadziłam warsztaty
        dla innych fryzjerek jako edukatorka L'Oréal Professionnel.
      </p>
      <p>
        Zanim cokolwiek zrobię z Twoimi włosami, rozmawiamy. O tym, co chcesz osiągnąć,
        co da się osiągnąć na Twoich włosach, ile to potrwa i ile będzie kosztować.
      </p>
      <a class="link-dalej" href="o-mnie/">Cała droga i osiem dyplomów</a>
    </div>
  </div>
</section>

<section class="ciemno">
  <div class="wrap">
    <p class="nadpis">Dowód</p>
    <h2>Dwadzieścia lat, <span class="kursywa">osiem dokumentów</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      Toni&amp;Guy, londyński Saks, uprawnienia instruktorskie, cztery szkolenia
      w Akademii L'Oréal Professionnel — u Adama Reeda, Berniego Ottjesa i Min Kim.
      Wszystkie do obejrzenia, także w salonie.
    </p>
    <div class="pasek-dyplomow wejscie">
      %(dyplomy)s
    </div>
    <a class="link-dalej" href="o-mnie/#dyplomy">Zobacz dyplomy z bliska</a>
  </div>
</section>
%(przerywnik)s
<section style="padding-top:0">
  <div class="wrap">
    <p class="nadpis">Usługi</p>
    <h2>Co robię <span class="kursywa">i jak</span>.</h2>
    <div class="uslugi">
      <div class="usluga"><h3>Koloryzacja</h3><p>Balayage, rozjaśnianie, refleksy, korekta koloru. Zawsze po rozmowie o tym, co Twoje włosy wytrzymają.</p></div>
      <div class="usluga"><h3>Strzyżenie</h3><p>Fryzura, która trzyma formę także wtedy, gdy układasz ją sama, w pośpiechu, przed wyjściem.</p></div>
      <div class="usluga"><h3>Modelowanie</h3><p>Na co dzień i na okazje. Także nauka układania — żeby dało się to powtórzyć w domu.</p></div>
      <div class="usluga"><h3>Pielęgnacja</h3><p>Zabiegi dobrane do stanu włosów, nie do cennika. Czasem zamiast koloru potrzebna jest regeneracja.</p></div>
    </div>
    <a class="link-dalej" href="uslugi/">Pełna oferta i dlaczego nie ma cennika</a>
  </div>
</section>

<section class="ciemno">
  <div class="wrap">
    <p class="nadpis">Opinie</p>
    <h2>Pięć na pięć, <span class="kursywa">setki razy</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:54ch">
      Ocena 5,0 w Google i tytuł Złotej Firmy pięć lat z rzędu — od 2022 do 2026.
      Najczęściej wraca jedno zdanie: że słucham, zanim wezmę nożyczki.
    </p>
    <div class="opinie-siatka">
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Chodzę do Agnieszki od kilkunastu lat i nigdy nie wyszłam niezadowolona. Zawsze doradzi, nigdy nie robi niczego na siłę.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Kolor dokładnie taki, jak chciałam — a przy okazji usłyszałam, czego nie robić, żeby się nie zniszczył.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Efekt naturalny, dokładnie o to mi chodziło. Indywidualne podejście, nie taśmowa robota.</p>
        <p class="kto">Klientka Google</p></article>
    </div>
    <a class="link-dalej" href="opinie/">Przeczytaj więcej i dodaj swoją</a>
  </div>
</section>
""" % {'dyplomy': dyplomy_skrot, 'przerywnik': PRZERYWNIK}

    return czolowka + reszta


def strona_o_mnie():
    return (
        naglowek_strony(u'O mnie',
            u'Nie zgaduję. <span class="kursywa">Wiem, co robię</span>.',
            u'Agnieszka Lewandowska. Dwadzieścia lat przy fotelu i osiem dokumentów, '
            u'które mówią, skąd to się wzięło.') +
u"""
<section style="padding-top:0">
  <div class="wrap dwie odwrot">
    <div class="tresc wejscie">
      <p>
        Zaczynałam w 2003 roku dyplomem akademii Toni&amp;Guy. Dwa lata później
        szkoliłam się w Saks Academies w londyńskim Covent Garden — strzyżenie
        i koloryzacja, u ludzi, którzy uczyli wtedy pół Europy.
      </p>
      <p>
        W 2009 zdobyłam uprawnienia pedagogiczne dla wykładowców i instruktorów.
        To nie jest papier dla ozdoby: przez lata prowadziłam warsztaty
        dla innych fryzjerek jako edukatorka L'Oréal Professionnel.
      </p>
      <p>
        Do dziś jeżdżę na szkolenia. Techniki koloryzacji u Min Kim i Berniego Ottjesa,
        strzyżenie u Adama Reeda — to nie są nazwiska z ulotki, tylko ludzie,
        którzy uczą fryzjerów na całym świecie.
      </p>
      <p>
        Praktycznie znaczy to jedno: zanim cokolwiek zrobię z Twoimi włosami,
        rozmawiamy. O tym, co chcesz osiągnąć, co da się osiągnąć na Twoich włosach,
        ile to potrwa i ile będzie kosztować. Bez niespodzianek w lustrze.
      </p>
    </div>
    <img src="../img/sesja/kadr-1743.jpg" alt="Agnieszka Lewandowska" width="733" height="1100" loading="lazy" class="wejscie">
  </div>
</section>

<section class="ciemno" id="droga">
  <div class="waski">
    <p class="nadpis">Droga</p>
    <h2>Od Londynu <span class="kursywa">do dziś</span>.</h2>
    <ol class="droga" style="margin-top:3rem">
""" +
        u'\n'.join(
            u'      <li><span class="rok">%s</span><p class="co">%s<span>%s</span></p></li>'
            % (p[1], p[2], p[3]) for p in DYPLOMY) +
u"""
    </ol>
  </div>
</section>

<section id="dyplomy">
  <div class="wrap">
    <p class="nadpis">Dyplomy</p>
    <h2>Wszystkie <span class="kursywa">do przeczytania</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      Kliknij, żeby powiększyć. Oryginały wiszą w salonie — te dwa najstarsze
      wystawione są jeszcze na nazwisko panieńskie, Dziuk.
    </p>
    <div class="galeria-siatka galeria-dyplomy">
        """ + kafle(DYPLOMY, 'dyplomy') + """
    </div>
  </div>
</section>
""")


def strona_uslugi():
    return (
        naglowek_strony(u'Usługi',
            u'Co robię <span class="kursywa">i jak</span>.',
            u'Cztery obszary, jedna zasada: najpierw rozmowa, potem nożyczki.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="uslugi" style="margin-top:0">
      <div class="usluga">
        <h3>Koloryzacja</h3>
        <p>Od delikatnego odświeżenia po pełną zmianę. Zawsze zaczynamy od rozmowy o tym, co Twoje włosy wytrzymają.</p>
        <ul><li>Balayage i rozjaśnianie</li><li>Refleksy, pasemka, sombré</li>
            <li>Koloryzacja globalna i odrosty</li><li>Tonowanie i korekta koloru</li></ul>
      </div>
      <div class="usluga">
        <h3>Strzyżenie</h3>
        <p>Fryzura, która trzyma formę także wtedy, gdy układasz ją sama, w pośpiechu, przed wyjściem.</p>
        <ul><li>Strzyżenie damskie i męskie</li><li>Zmiana fryzury po konsultacji</li>
            <li>Podcięcie i odświeżenie linii</li></ul>
      </div>
      <div class="usluga">
        <h3>Modelowanie</h3>
        <p>Na co dzień i na okazje. Także nauka układania — żeby dało się to powtórzyć w domu.</p>
        <ul><li>Modelowanie po zabiegu</li><li>Fale, prostowanie, objętość</li>
            <li>Upięcia i stylizacje okolicznościowe</li></ul>
      </div>
      <div class="usluga">
        <h3>Pielęgnacja</h3>
        <p>Zabiegi dobrane do stanu włosów, nie do cennika. Czasem zamiast koloru potrzebna jest regeneracja.</p>
        <ul><li>Regeneracja i odbudowa</li><li>Zabiegi nawilżające</li>
            <li>Dobór pielęgnacji domowej</li></ul>
      </div>
    </div>

    <div class="nota-cena">
      <p><b>Dlaczego nie ma tu cennika.</b></p>
      <p>
        Bo uczciwie się nie da. Ta sama koloryzacja na włosach do ramion i na włosach
        do pasa to dwie różne ilości farby, dwa różne czasy pracy i dwie różne ceny.
        Do tego dochodzi grubość i gęstość włosów oraz to, co było na nich wcześniej.
      </p>
      <p>
        Dlatego pracuję w pakietach — na przykład koloryzacja ze strzyżeniem i modelowaniem
        albo sama koloryzacja z modelowaniem — a <b>cenę podaję po rozmowie</b>, kiedy
        zobaczę włosy albo usłyszę, o co chodzi. Zawsze <b>przed</b> zabiegiem, nigdy po.
      </p>
      <p style="margin-top:1.4rem">
        <a class="btn btn-ciemny" href="tel:%(tel_link)s">Zadzwoń i zapytaj o cenę</a>
      </p>
    </div>
  </div>
</section>
""" % {'tel_link': TEL_LINK})


def strona_portfolio():
    return (
        naglowek_strony(u'Portfolio',
            u'Praca, która <span class="kursywa">wyszła poza salon</span>.',
            u'Sesje wizerunkowe, stylizacje do magazynu i katalogu. '
            u'Włosy przy tych zdjęciach to moja robota.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <p class="nadpis">Magazyn i katalog</p>
    <h2>Sesje <span class="kursywa">publikowane</span></h2>
    <p style="color:var(--srebro-jasne); max-width:58ch">
      Stylizacje fryzur do magazynu <b style="color:var(--biel)">SPLOT</b> i do katalogu
      marek odzieżowych — sesja w klimacie lat dwudziestych w pałacowych wnętrzach
      oraz zdjęcia miejskie.
    </p>
    <div class="galeria-siatka">
        """ + kafle(PORTFOLIO, 'portfolio') + """
    </div>
  </div>
</section>
""" + PRZERYWNIK + u"""
<section style="padding-top:0">
  <div class="wrap">
    <p class="nadpis">Sesja wizerunkowa</p>
    <h2>Ja i moje <span class="kursywa">narzędzia</span></h2>
    <div class="galeria-siatka">
        """ + kafle(SESJA, 'sesja') + """
    </div>
    <p style="color:var(--srebro-ciemne); font-size:.9rem; margin-top:2rem">
      Metamorfozy klientek pojawią się tutaj, gdy będą podpisane zgody na publikację.
    </p>
  </div>
</section>
""")


def strona_opinie():
    return (
        naglowek_strony(u'Opinie',
            u'Pięć na pięć, <span class="kursywa">setki razy</span>.',
            u'Ocena 5,0 w Google i tytuł Złotej Firmy pięć lat z rzędu — od 2022 do 2026.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="opinie-siatka" style="margin-top:0">
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Chodzę do Agnieszki od kilkunastu lat i nigdy nie wyszłam niezadowolona. Zawsze doradzi, nigdy nie robi niczego na siłę.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Kolor dokładnie taki, jak chciałam — a przy okazji usłyszałam, czego nie robić, żeby się nie zniszczył. Profesjonalizm pełną gębą.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Efekt naturalny, dokładnie o to mi chodziło. Indywidualne podejście do każdej osoby, nie taśmowa robota.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Byłam po nieudanej koloryzacji z innego miejsca. Agnieszka nie obiecywała cudów od razu — rozpisała plan na trzy wizyty i wszystko się zgadzało.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Salon mały, ale czuć, że osoba wie, co robi. Wychodzę z fryzurą, którą potrafię sama ułożyć następnego dnia.</p>
        <p class="kto">Klientka Google</p></article>
      <article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>
        <p>Doradziła mi krótsze niż planowałam i miała rację. Umie powiedzieć „to nie będzie dobrze wyglądać", a to rzadkość.</p>
        <p class="kto">Klientka Google</p></article>
    </div>

    <div class="form-opinia">
      <h3 style="margin-bottom:.6rem">Byłaś u mnie? Napisz, jak było.</h3>
      <p style="color:var(--srebro-jasne); font-size:.95rem; max-width:52ch">
        Nie każdy ma konto w Google, a chcę wiedzieć, co poszło dobrze,
        a co mogłoby pójść lepiej. Opinia trafia prosto do mnie.
      </p>
      <form id="form-opinia" novalidate style="margin-top:2rem">
        <div class="pola">
          <div class="pola dwa">
            <div><label for="op-imie">Imię</label>
              <input type="text" id="op-imie" name="imie" autocomplete="given-name" required maxlength="60"></div>
            <div><label for="op-email">E-mail <span style="text-transform:none;letter-spacing:0">(nieobowiązkowo)</span></label>
              <input type="email" id="op-email" name="email" autocomplete="email" maxlength="120"></div>
          </div>
          <div>
            <label id="etykieta-ocena">Ocena</label>
            <div class="ocena-gwiazdki" role="radiogroup" aria-labelledby="etykieta-ocena">
              <input type="radio" name="ocena" id="ocena-1" value="1"><label for="ocena-1" title="1 z 5">★</label>
              <input type="radio" name="ocena" id="ocena-2" value="2"><label for="ocena-2" title="2 z 5">★</label>
              <input type="radio" name="ocena" id="ocena-3" value="3"><label for="ocena-3" title="3 z 5">★</label>
              <input type="radio" name="ocena" id="ocena-4" value="4"><label for="ocena-4" title="4 z 5">★</label>
              <input type="radio" name="ocena" id="ocena-5" value="5" checked><label for="ocena-5" title="5 z 5">★</label>
            </div>
          </div>
          <div><label for="op-tresc">Opinia</label>
            <textarea id="op-tresc" name="tresc" required maxlength="1200"
              placeholder="Co się podobało, a co można poprawić?"></textarea></div>
          <div class="zgoda">
            <input type="checkbox" id="op-zgoda" name="zgoda" required>
            <label for="op-zgoda">Zgadzam się na przetwarzanie podanych danych w celu obsługi tej opinii
              i na jej publikację na stronie. <span style="color:var(--srebro-ciemne)">*</span></label>
          </div>
          <div class="pulapka" aria-hidden="true">
            <label for="op-strona">Nie wypełniaj tego pola</label>
            <input type="text" id="op-strona" name="strona" tabindex="-1" autocomplete="off">
          </div>
          <div>
            <button class="btn btn-ciemny" type="submit" id="op-wyslij">Wyślij opinię</button>
            <p class="status" id="op-status" role="status" aria-live="polite"></p>
          </div>
        </div>
      </form>
    </div>
  </div>
</section>
""")


def strona_kontakt():
    return (
        naglowek_strony(u'Kontakt',
            u'Umów się <span class="kursywa">telefonicznie</span>.',
            u'Najprościej zadzwonić — od razu ustalimy, ile czasu zarezerwować '
            u'i ile to będzie kosztować.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="kontakt-siatka">
      <div>
        <ul class="dane">
          <li><span class="etykieta">Telefon</span>
            <a href="tel:%(tel_link)s" style="font-size:1.35rem">%(tel_pokaz)s</a></li>
          <li><span class="etykieta">Adres</span>
            ul. Jana Kilińskiego 55<br>42-200 Częstochowa</li>
          <li><span class="etykieta">Godziny</span>
            <span class="godziny">
              wtorek – piątek &nbsp;10:00 – 18:00<br>
              sobota &nbsp;8:00 – 13:00<br>
              <span style="color:var(--srebro-ciemne)">poniedziałek i niedziela — nieczynne</span>
            </span></li>
          <li><span class="etykieta">W sieci</span>
            <a href="https://www.instagram.com/new_age_lewandowska" target="_blank" rel="noopener">Instagram</a>
            <a href="https://www.facebook.com/profile.php?id=100057636820418" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
      <div>
        <iframe class="mapa" title="Mapa — ul. Jana Kilińskiego 55, Częstochowa" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q=Jana%%20Kili%%C5%%84skiego%%2055,%%2042-200%%20Cz%%C4%%99stochowa&output=embed"></iframe>
      </div>
    </div>
  </div>
</section>
""" % {'tel_link': TEL_LINK, 'tel_pokaz': TEL_POKAZ})


# ─────────────────────────────────────────────────────────────────
STRONY = [
    ('start', '', u'new age Lewandowska — fryzjerstwo, Częstochowa',
     u'Salon fryzjerski new age w Częstochowie. Koloryzacja, strzyżenie i modelowanie '
     u'u Agnieszki Lewandowskiej — edukatorki L’Oréal Professionnel.', strona_start, ''),
    ('o-mnie', 'o-mnie', u'O mnie — Agnieszka Lewandowska | new age',
     u'Dwadzieścia lat pracy, dyplomy Toni&Guy i Saks London, cztery szkolenia '
     u'w Akademii L’Oréal Professionnel.', strona_o_mnie, '../'),
    ('uslugi', 'uslugi', u'Usługi — koloryzacja, strzyżenie, modelowanie | new age',
     u'Koloryzacja, strzyżenie, modelowanie i pielęgnacja w Częstochowie. '
     u'Cena ustalana po rozmowie, zawsze przed zabiegiem.', strona_uslugi, '../'),
    ('portfolio', 'portfolio', u'Portfolio — sesje i publikacje | new age Lewandowska',
     u'Stylizacje fryzur do magazynu SPLOT i sesji katalogowych.', strona_portfolio, '../'),
    ('opinie', 'opinie', u'Opinie klientek | new age Lewandowska',
     u'Ocena 5,0 w Google, Złota Firma 2022–2026. Zostaw swoją opinię.', strona_opinie, '../'),
    ('kontakt', 'kontakt', u'Kontakt — Częstochowa, ul. Kilińskiego 55 | new age',
     u'Telefon, adres, godziny otwarcia i mapa dojazdu.', strona_kontakt, '../'),
]


def main():
    for klucz, katalog, tytul, opis, budowniczy, korzen in STRONY:
        sciezka = os.path.join(CEL, katalog) if katalog else CEL
        if not os.path.isdir(sciezka):
            os.makedirs(sciezka)
        html = zbuduj(klucz, tytul, opis, budowniczy(), korzen)
        # Podstrony siegaja po zdjecia o poziom wyzej; strona glowna nie.
        if not korzen:
            html = html.replace('src="../img/', 'src="img/').replace('data-pelne="../img/', 'data-pelne="img/')
        with io.open(os.path.join(sciezka, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(html)
        print('  %-26s %6d znakow' % ((katalog or '/') + '/index.html', len(html)))
    print('\nGotowe: %d podstron' % len(STRONY))


if __name__ == '__main__':
    main()
