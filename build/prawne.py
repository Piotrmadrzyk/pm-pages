# -*- coding: utf-8 -*-
"""
build/prawne.py — regulamin, polityka prywatnosci i pasek cookie
                  dla czterech stron demonstracyjnych.

DLACZEGO TO ISTNIEJE
Strony demonstracyjne pokazuja klientowi, jak bedzie wygladac jego wlasna
strona. Klient patrzy takze na to, czy sa tam rzeczy, ktorych bedzie
potrzebowal: informacja o ciasteczkach, regulamin, klauzula RODO. Brak tych
elementow w demie czyta sie jako "tego nie robimy".

Firmy w demach sa zmyslone. Tresci prawne sa realistyczne, ale to szablony —
kazdy blok konczy sie zdaniem, ktore mowi to wprost.

CO ROBI
Dokleja do stron w p/demo-*/ trzy rzeczy, kazda tylko wtedy, gdy jej brakuje:
  1. sekcje z regulaminem,
  2. sekcje z polityka prywatnosci,
  3. plywajacy pasek informacji o ciasteczkach.

Skrypt mozna puszczac wielokrotnie — pomija to, co juz jest.

JAK URUCHOMIC
    cd build && python3 prawne.py

DWIE DROGI WSTAWIANIA
Lawenda i Dom maja bloki prawne w ciemnej stopce. Tam regulamin wchodzi jako
kolejny kafel stopki i dziedziczy jej wyglad — zadnego nowego CSS.
Zawadzcy i Serwis nie maja gdzie tego wpiac, wiec dostaja samodzielna sekcje
z wlasnymi stylami. Zawadzcy sa jasni (krem #f4f0e8), Serwis ciemny (#1c1f24),
dlatego kolory sa podane osobno dla kazdej firmy — jeden zestaw nie zadziala.
"""

import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


# ─────────────────────────────────────────────────────────────────────────
#  TRESCI
# ─────────────────────────────────────────────────────────────────────────

STOPKA_DEMO = (u'Powy\u017cszy regulamin jest tre\u015bci\u0105 pogl\u0105dow\u0105 przygotowan\u0105 na potrzeby '
               u'strony demonstracyjnej. Przed uruchomieniem prawdziwej strony nale\u017cy go '
               u'dostosowa\u0107 do rzeczywistej dzia\u0142alno\u015bci i przedstawi\u0107 do akceptacji.')

# UWAGA: adres kontaktowy jest prawdziwy — Probatum, nie zmyslona firma.
# Zmyslone adresy nie istnieja, wiec kazde pismo w sprawie danych by przepadlo.
FIRMY = {

    'lawenda': {
        'nazwa': u'Studio Lawenda',
        'email': u'kontakt@probatum.pl',
        'tryb': 'stopka',
        'regulamin': [
            (u'Zakres us\u0142ug',
             u'Studio wykonuje zabiegi kosmetyczne i piel\u0119gnacyjne wymienione w cenniku. '
             u'Ceny podane na stronie s\u0105 cenami brutto i mog\u0105 si\u0119 zmieni\u0107 po konsultacji, '
             u'je\u015bli zabieg wymaga wi\u0119kszego nak\u0142adu pracy lub materia\u0142\u00f3w.'),
            (u'Rezerwacja wizyty',
             u'Wizyt\u0119 rezerwuje si\u0119 telefonicznie lub przez formularz. Rezerwacja jest wi\u0105\u017c\u0105ca '
             u'po potwierdzeniu przez studio \u2014 samo wys\u0142anie formularza jeszcze nie rezerwuje terminu.'),
            (u'Odwo\u0142anie i sp\u00f3\u017anienie',
             u'Termin mo\u017cna odwo\u0142a\u0107 bez \u017cadnych konsekwencji do 24 godzin przed wizyt\u0105. '
             u'Sp\u00f3\u017anienie powy\u017cej 15 minut mo\u017ce oznacza\u0107 skr\u00f3cenie zabiegu, \u017ceby nie '
             u'przesuwa\u0107 kolejnych klient\u00f3w \u2014 cena pozostaje bez zmian.'),
            (u'Zdrowie i przeciwwskazania',
             u'Przed pierwszym zabiegiem przeprowadzamy kr\u00f3tk\u0105 konsultacj\u0119. Klient informuje o ci\u0105\u017cy, '
             u'chorobach sk\u00f3ry, alergiach i przyjmowanych lekach. Przy przeciwwskazaniach studio ma prawo '
             u'odm\u00f3wi\u0107 wykonania zabiegu \u2014 to decyzja podejmowana dla bezpiecze\u0144stwa klienta.'),
            (u'P\u0142atno\u015bci i vouchery',
             u'P\u0142atno\u015b\u0107 nast\u0119puje po zabiegu \u2014 got\u00f3wk\u0105, kart\u0105 lub BLIK-iem. Vouchery '
             u'podarunkowe s\u0105 wa\u017cne 6 miesi\u0119cy od daty zakupu i nie podlegaj\u0105 wymianie na got\u00f3wk\u0119.'),
            (u'Reklamacje',
             u'Zastrze\u017cenia do wykonanej us\u0142ugi przyjmujemy w ci\u0105gu 14 dni \u2014 mailem lub osobi\u015bcie. '
             u'Odpowiadamy w ci\u0105gu 14 dni od zg\u0142oszenia.'),
        ],
    },

    'zawadzcy': {
        'nazwa': u'Kancelaria Prawna Zawadzcy i Wsp\u00f3lnicy',
        'email': u'kontakt@probatum.pl',
        'tryb': 'sekcja',
        'kolory': {
            'tlo':      u'#ece7dd',
            'ramka':    u'rgba(11,37,69,.14)',
            'naglowek': u'#18212b',
            'tekst':    u'#58616d',
            'link':     u'#0b2545',
            'font':     u"'Cormorant Garamond',serif",
        },
        'regulamin': [
            (u'Zakres dzia\u0142ania',
             u'Kancelaria \u015bwiadczy pomoc prawn\u0105 w sprawach cywilnych, gospodarczych, rodzinnych '
             u'i spadkowych \u2014 dla firm i klient\u00f3w indywidualnych.'),
            (u'Formularz to jeszcze nie porada',
             u'Wiadomo\u015b\u0107 wys\u0142ana przez formularz s\u0142u\u017cy um\u00f3wieniu rozmowy. Nie jest porad\u0105 '
             u'prawn\u0105 i nie tworzy stosunku klient \u2014 kancelaria. Nie nale\u017cy w niej przesy\u0142a\u0107 '
             u'dokument\u00f3w ani opisywa\u0107 sprawy w spos\u00f3b szczeg\u00f3\u0142owy; od tego jest rozmowa.'),
            (u'Pierwsza konsultacja',
             u'Pierwsza rozmowa jest bezp\u0142atna i s\u0142u\u017cy ustaleniu, czy i jak kancelaria mo\u017ce pom\u00f3c. '
             u'Nie zobowi\u0105zuje \u017cadnej ze stron do dalszej wsp\u00f3\u0142pracy.'),
            (u'Umowa i wynagrodzenie',
             u'Wsp\u00f3\u0142prac\u0119 poprzedza pisemna umowa okre\u015blaj\u0105ca zakres i wynagrodzenie \u2014 stawk\u0119 '
             u'godzinow\u0105 albo rycza\u0142t za spraw\u0119. Wysoko\u015b\u0107 wynagrodzenia ustalamy przed rozpocz\u0119ciem '
             u'pracy, nie po niej. Koszty s\u0105dowe i op\u0142aty urz\u0119dowe s\u0105 wskazywane osobno.'),
            (u'Tajemnica zawodowa',
             u'Wszystko, co klient przekazuje kancelarii \u2014 w tym podczas bezp\u0142atnej rozmowy \u2014 '
             u'obj\u0119te jest tajemnic\u0105 zawodow\u0105, niezale\u017cnie od tego, czy dojdzie do zawarcia umowy.'),
            (u'Konflikt interes\u00f3w',
             u'Kancelaria odmawia prowadzenia sprawy, je\u015bli by\u0142oby to sprzeczne z interesem klienta '
             u'ju\u017c obs\u0142ugiwanego. O takiej sytuacji informujemy niezw\u0142ocznie.'),
        ],
    },

    'dom-i-wnetrze': {
        'nazwa': u'Dom i Wn\u0119trze Warszawa',
        'email': u'kontakt@probatum.pl',
        'tryb': 'stopka',
        'regulamin': [
            (u'Zakres us\u0142ug',
             u'Wykonujemy projektowanie wn\u0119trz oraz remonty i wyko\u0144cz\u00f3wki pod klucz \u2014 '
             u'w mieszkaniach i domach jednorodzinnych.'),
            (u'Wycena',
             u'Wycena po ogl\u0119dzinach jest bezp\u0142atna i niezobowi\u0105zuj\u0105ca. Podana kwota jest wa\u017cna '
             u'30 dni. Wycena zdalna, na podstawie samych zdj\u0119\u0107 czy metra\u017cu, jest zawsze szacunkowa '
             u'\u2014 traktujemy j\u0105 jako orientacj\u0119 w bud\u017cecie, nie jako ofert\u0119.'),
            (u'Umowa i harmonogram',
             u'Przed rozpocz\u0119ciem prac podpisujemy umow\u0119 z zakresem, cen\u0105 i harmonogramem. '
             u'Harmonogram zawiera terminy etap\u00f3w, a nie tylko dat\u0119 ko\u0144cow\u0105 \u2014 dzi\u0119ki temu '
             u'wida\u0107 na bie\u017c\u0105co, czy prace id\u0105 zgodnie z planem.'),
            (u'P\u0142atno\u015bci',
             u'Rozliczenie etapami: zaliczka na materia\u0142y, p\u0142atno\u015bci po odbiorze kolejnych etap\u00f3w, '
             u'ostatnia transza po odbiorze ko\u0144cowym. Nie pobieramy ca\u0142o\u015bci z g\u00f3ry.'),
            (u'Zmiany w trakcie prac',
             u'Ka\u017cda zmiana zakresu \u2014 inne p\u0142ytki, dodatkowa \u015bciana, przeniesienie punktu '
             u'elektrycznego \u2014 wymaga aneksu z now\u0105 cen\u0105 i now\u0105 dat\u0105. Nie dopisujemy koszt\u00f3w '
             u'po cichu i nie robimy zmian bez pisemnej zgody.'),
            (u'Odbi\u00f3r i gwarancja',
             u'Prace ko\u0144cz\u0105 si\u0119 protoko\u0142em odbioru, w kt\u00f3rym spisujemy ewentualne usterki '
             u'i termin ich usuni\u0119cia. Na robocizn\u0119 dajemy 24 miesi\u0105ce gwarancji; na materia\u0142y '
             u'obowi\u0105zuje gwarancja producenta.'),
        ],
    },

    'serwis-podkarpacki': {
        'nazwa': u'Serwis Podkarpacki',
        'email': u'kontakt@probatum.pl',
        'tryb': 'sekcja',
        'kolory': {
            'tlo':      u'#15181c',
            'ramka':    u'rgba(255,255,255,.10)',
            'naglowek': u'#e9edf1',
            'tekst':    u'#aab2bc',
            'link':     u'#ff7a2f',
            'font':     u"'Rajdhani',sans-serif",
        },
        'regulamin': [
            (u'Zakres us\u0142ug',
             u'Warsztat wykonuje mechanik\u0119 pojazdow\u0105, diagnostyk\u0119 komputerow\u0105, obs\u0142ug\u0119 '
             u'klimatyzacji oraz wymian\u0119 i przechowywanie opon.'),
            (u'Wycena przed napraw\u0105',
             u'Przed rozpocz\u0119ciem naprawy podajemy koszt cz\u0119\u015bci i robocizny. Je\u015bli w trakcie '
             u'okazuje si\u0119, \u017ce koszt b\u0119dzie wy\u017cszy, wstrzymujemy prac\u0119 i dzwonimy \u2014 '
             u'nigdy nie przekraczamy ustalonej kwoty bez zgody klienta.'),
            (u'Diagnostyka',
             u'Op\u0142ata za diagnostyk\u0119 jest odliczana od kosztu naprawy, je\u015bli klient zdecyduje si\u0119 '
             u'j\u0105 u nas wykona\u0107. Je\u015bli nie \u2014 p\u0142atna jest sama diagnostyka wed\u0142ug cennika.'),
            (u'Cz\u0119\u015bci',
             u'Montujemy cz\u0119\u015bci nowe: oryginalne albo zamienniki dobrej jako\u015bci. Wyb\u00f3r nale\u017cy do '
             u'klienta i przedstawiamy go razem z r\u00f3\u017cnic\u0105 w cenie. Na \u017cyczenie montujemy cz\u0119\u015bci '
             u'powierzone \u2014 wtedy gwarancja obejmuje wy\u0142\u0105cznie robocizn\u0119.'),
            (u'Gwarancja',
             u'Na robocizn\u0119 udzielamy 12 miesi\u0119cy gwarancji. Na cz\u0119\u015bci obowi\u0105zuje gwarancja '
             u'producenta. Gwarancja nie obejmuje uszkodze\u0144 wynik\u0142ych z dalszej eksploatacji '
             u'wbrew naszym zaleceniom.'),
            (u'Odbi\u00f3r pojazdu',
             u'Po zako\u0144czeniu naprawy informujemy telefonicznie. Pojazd prosimy odebra\u0107 w ci\u0105gu '
             u'7 dni \u2014 po tym terminie mo\u017cemy nalicza\u0107 op\u0142at\u0119 za postojowe wed\u0142ug cennika.'),
        ],
    },
}


def polityka_tresc(f):
    """Klauzula informacyjna RODO — te same punkty dla kazdej firmy."""
    return [
        (u'Kto przetwarza dane',
         u'Administratorem danych podanych w formularzu jest %s. W sprawach dotycz\u0105cych '
         u'danych mo\u017cna pisa\u0107 na <a href="mailto:%s">%s</a>.' % (f['nazwa'], f['email'], f['email'])),
        (u'Po co i na jakiej podstawie',
         u'Dane \u2014 imi\u0119, telefon, adres e-mail i tre\u015b\u0107 wiadomo\u015bci \u2014 przetwarzamy wy\u0142\u0105cznie '
         u'po to, \u017ceby obs\u0142u\u017cy\u0107 zg\u0142oszenie i odpowiedzie\u0107. Podstaw\u0105 jest zgoda osoby, '
         u'kt\u00f3rej dotycz\u0105 (art. 6 ust. 1 lit. a RODO). Podanie danych jest dobrowolne.'),
        (u'Jak d\u0142ugo i komu przekazujemy',
         u'Dane trzymamy przez czas potrzebny do obs\u0142ugi zg\u0142oszenia, nie d\u0142u\u017cej ni\u017c 24 miesi\u0105ce '
         u'od ostatniego kontaktu. Nie sprzedajemy ich i nie przekazujemy nikomu poza dostawcami '
         u'technicznymi, kt\u00f3rzy obs\u0142uguj\u0105 formularz i poczt\u0119.'),
        (u'Twoje prawa',
         u'Masz prawo dost\u0119pu do swoich danych, ich sprostowania, usuni\u0119cia i ograniczenia '
         u'przetwarzania, a tak\u017ce prawo wycofania zgody w dowolnym momencie \u2014 wystarczy jeden '
         u'mail. Wycofanie zgody nie wp\u0142ywa na to, co zdarzy\u0142o si\u0119 wcze\u015bniej. Przys\u0142uguje '
         u'r\u00f3wnie\u017c skarga do Prezesa Urz\u0119du Ochrony Danych Osobowych.'),
        (u'Ciasteczka i pami\u0119\u0107 przegl\u0105darki',
         u'Ta strona nie u\u017cywa ciasteczek reklamowych ani analitycznych \u2014 nie mierzymy ruchu, '
         u'nie profilujemy i nie osadzamy skrypt\u00f3w \u015bledz\u0105cych. W pami\u0119ci przegl\u0105darki zapisujemy '
         u'jedynie informacj\u0119, \u017ce komunikat o ciasteczkach zosta\u0142 zamkni\u0119ty. Mo\u017cesz j\u0105 usun\u0105\u0107 '
         u'w ustawieniach przegl\u0105darki.'),
    ]


# ─────────────────────────────────────────────────────────────────────────
#  SZABLONY HTML
# ─────────────────────────────────────────────────────────────────────────

def blok_stopka(kotwica, tytul, punkty, dopisek=None):
    """Wariant dla Lawendy i Domu: kolejny kafel w ciemnej stopce."""
    p = []
    for naglowek, tresc in punkty:
        p.append(u'      <b style="color:#fff">%s.</b> %s' % (naglowek, tresc))
    ciag = u'<br><br>\n'.join(p)
    if dopisek:
        ciag += u'<br><br>\n      <i style="opacity:.72">%s</i>' % dopisek
    return (u'\n  <div class="wrap" id="%s" style="border-top:1px solid rgba(255,255,255,.13);'
            u'padding-top:26px;padding-bottom:6px">\n'
            u'    <h4>%s</h4>\n'
            u'    <p style="font-size:.83rem;max-width:78ch;line-height:1.7">\n%s\n    </p>\n'
            u'  </div>\n' % (kotwica, tytul, ciag))


def blok_sekcja(kolory, bloki):
    """Wariant dla Zawadzkich i Serwisu: samodzielna sekcja z wlasnym CSS.

    bloki: lista (kotwica, tytul, punkty, dopisek)
    """
    css = (u'\n<style>\n'
           u'  .pm-prawne{background:%(tlo)s;border-top:1px solid %(ramka)s;padding:44px 20px 52px}\n'
           u'  .pm-prawne-in{max-width:900px;margin:0 auto;display:grid;gap:14px}\n'
           u'  .pm-prawne h2{font-family:%(font)s;color:%(naglowek)s;font-size:1.5rem;margin:0;line-height:1.25}\n'
           u'  .pm-prawne details{border:1px solid %(ramka)s;border-radius:12px;background:transparent}\n'
           u'  .pm-prawne summary{cursor:pointer;padding:15px 18px;color:%(naglowek)s;font-weight:700;'
           u'font-family:%(font)s;font-size:1.06rem;list-style:none;display:flex;justify-content:space-between;gap:12px}\n'
           u'  .pm-prawne summary::-webkit-details-marker{display:none}\n'
           u'  .pm-prawne summary::after{content:"+";font-weight:400;opacity:.6}\n'
           u'  .pm-prawne details[open] summary::after{content:"\\2212"}\n'
           u'  .pm-prawne summary:focus-visible{outline:2px solid %(link)s;outline-offset:2px}\n'
           u'  .pm-prawne .tresc{padding:0 18px 18px;color:%(tekst)s;font-size:.9rem;line-height:1.75}\n'
           u'  .pm-prawne .tresc p{margin:0 0 12px;color:%(tekst)s}\n'
           u'  .pm-prawne .tresc p:last-child{margin-bottom:0}\n'
           u'  .pm-prawne .tresc b{color:%(naglowek)s}\n'
           u'  .pm-prawne a{color:%(link)s}\n'
           u'  .pm-prawne .zastrzezenie{opacity:.75;font-style:italic}\n'
           u'</style>\n') % kolory

    czesci = []
    for kotwica, tytul, punkty, dopisek in bloki:
        akapity = u''.join(
            u'          <p><b>%s.</b> %s</p>\n' % (n, t) for n, t in punkty)
        if dopisek:
            akapity += u'          <p class="zastrzezenie">%s</p>\n' % dopisek
        czesci.append(
            u'      <details id="%s">\n'
            u'        <summary>%s</summary>\n'
            u'        <div class="tresc">\n%s        </div>\n'
            u'      </details>\n' % (kotwica, tytul, akapity))

    return (css +
            u'\n<section class="pm-prawne" aria-label="Informacje prawne">\n'
            u'  <div class="pm-prawne-in">\n'
            u'    <h2>Informacje prawne</h2>\n' +
            u''.join(czesci) +
            u'  </div>\n</section>\n'
            u'<script>\n'
            u'(function () {\n'
            u'  /* Link prowadzacy do zwinietego bloku ma go otworzyc, nie tylko\n'
            u'     przewinac — inaczej gosc laduje na zamknietym naglowku. */\n'
            u'  function otworz() {\n'
            u'    var id = (location.hash || "").slice(1);\n'
            u'    if (!id) return;\n'
            u'    var el = document.getElementById(id);\n'
            u'    if (el && el.tagName === "DETAILS") {\n'
            u'      el.open = true;\n'
            u'      el.scrollIntoView({block: "start"});\n'
            u'    }\n'
            u'  }\n'
            u'  window.addEventListener("hashchange", otworz);\n'
            u'  otworz();\n'
            u'})();\n'
            u'</script>\n')


def pasek_cookie(klucz):
    """Plywajacy pasek. Ciemny — czytelny i na jasnej, i na ciemnej stronie."""
    return (u'\n<!-- ————— INFORMACJA O CIASTECZKACH ————— -->\n'
            u'<div class="pm-cookie" id="pm-cookie-bar" role="region" '
            u'aria-label="Informacja o plikach cookie">\n'
            u'  <p>\n'
            u'    Ta strona nie \u015bledzi Ci\u0119 i nie profiluje \u2014 nie ma tu analityki ani reklam.\n'
            u'    W pami\u0119ci przegl\u0105darki zapisujemy jedn\u0105 rzecz: informacj\u0119, \u017ce ten\n'
            u'    komunikat zosta\u0142 zamkni\u0119ty. <a href="#polityka">Szczeg\u00f3\u0142y w informacjach prawnych</a>.\n'
            u'  </p>\n'
            u'  <button type="button" id="pm-cookie-ok">Rozumiem</button>\n'
            u'</div>\n'
            u'<style>\n'
            u'  .pm-cookie{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;\n'
            u'    max-width:720px;margin:0 auto;display:none;gap:16px;align-items:center;\n'
            u'    background:#15171c;color:#e7e8ea;border:1px solid rgba(255,255,255,.14);\n'
            u'    border-radius:14px;padding:15px 18px;font-size:.84rem;line-height:1.6;\n'
            u'    box-shadow:0 18px 44px rgba(0,0,0,.34)}\n'
            u'  .pm-cookie.pokaz{display:flex}\n'
            u'  .pm-cookie p{margin:0}\n'
            u'  .pm-cookie a{color:#c9b6ff}\n'
            u'  .pm-cookie button{flex:0 0 auto;appearance:none;border:none;cursor:pointer;\n'
            u'    padding:.6rem 1.15rem;border-radius:999px;background:#fff;color:#15171c;\n'
            u'    font-weight:700;font-size:.84rem;font-family:inherit}\n'
            u'  .pm-cookie button:hover{opacity:.9}\n'
            u'  .pm-cookie button:focus-visible{outline:2px solid #c9b6ff;outline-offset:3px}\n'
            u'  @media (max-width:560px){.pm-cookie{flex-direction:column;align-items:stretch}\n'
            u'    .pm-cookie button{width:100%%}}\n'
            u'  @media (prefers-reduced-motion:reduce){.pm-cookie{transition:none}}\n'
            u'</style>\n'
            u'<script>\n'
            u'(function () {\n'
            u'  var pasek = document.getElementById("pm-cookie-bar");\n'
            u'  if (!pasek) return;\n'
            u'  var KLUCZ = "%s";\n'
            u'  var widziane = false;\n'
            u'  try { widziane = localStorage.getItem(KLUCZ) === "ok"; } catch (e) {}\n'
            u'  if (widziane) return;\n'
            u'  pasek.classList.add("pokaz");\n'
            u'  var ok = document.getElementById("pm-cookie-ok");\n'
            u'  if (ok) ok.addEventListener("click", function () {\n'
            u'    pasek.classList.remove("pokaz");\n'
            u'    try { localStorage.setItem(KLUCZ, "ok"); } catch (e) {}\n'
            u'  });\n'
            u'})();\n'
            u'</script>\n') % klucz


# ─────────────────────────────────────────────────────────────────────────
#  WSTAWIANIE
# ─────────────────────────────────────────────────────────────────────────

def wstaw_przed(tresc, znacznik, wstawka):
    """Wstawia przed ostatnim wystapieniem znacznika. Zwraca None, gdy brak."""
    i = tresc.rfind(znacznik)
    if i == -1:
        return None
    return tresc[:i] + wstawka + tresc[i:]


def koniec_diva(tresc, poczatek_znacznika):
    """Zwraca pozycje tuz za </div> domykajacym div otwarty na podanym miejscu.

    Liczy zagniezdzenia, wiec nie da sie zwiesc pierwszym lepszym </div>.
    Zwraca None, gdy znacznika nie ma albo dokumentu nie da sie zbilansowac.
    """
    i = tresc.find(poczatek_znacznika)
    if i == -1:
        return None
    poziom = 0
    j = i
    while True:
        otw = tresc.find('<div', j)
        zam = tresc.find('</div>', j)
        if zam == -1:
            return None
        if otw != -1 and otw < zam:
            poziom += 1
            j = otw + 4
        else:
            poziom -= 1
            j = zam + 6
            if poziom == 0:
                return j


def wstaw_po(tresc, poczatek_znacznika, wstawka):
    """Wstawia zaraz za blokiem, ktory zaczyna sie podanym znacznikiem."""
    k = koniec_diva(tresc, poczatek_znacznika)
    if k is None:
        return None
    return tresc[:k] + wstawka + tresc[k:]


def przerob(sciezka, firma):
    with open(sciezka, 'r') as fh:
        t = fh.read()
    przed = t
    zrobione = []

    # Czesc stron ma gotowa polityke, ale bez kotwicy — a pasek cookie linkuje
    # do #polityka. Bez kotwicy ten link prowadzi donikad, wiec ja dorabiamy.
    zrobione_kotwica = False
    if 'id="polityka"' not in t:
        for wzor, zamiana in (
            ('<section class="policy">', '<section class="policy" id="polityka">'),
            (u'<h2>Polityka prywatno\u015bci', u'<h2 id="polityka">Polityka prywatno\u015bci'),
        ):
            if wzor in t:
                t = t.replace(wzor, zamiana, 1)
                zrobione_kotwica = True
                break

    # Uwaga: sam tekst "Polityka prywatnosci" bywa tylko etykieta odnosnika
    # prowadzacego na strone glowna — to nie znaczy, ze polityka jest tutaj.
    # Dlatego liczy sie naglowek albo kotwica, nie samo wystapienie slowa.
    ma_polityke = ('id="polityka"' in t) or (u'<h2>Polityka prywatno\u015bci' in t)
    ma_regulamin = 'id="regulamin"' in t
    ma_cookie = ('id="cookie-bar"' in t) or ('id="pm-cookie-bar"' in t)

    if firma['tryb'] == 'stopka':
        # Lawenda, Dom — regulamin jako kolejny kafel ciemnej stopki.
        if not ma_regulamin:
            blok = blok_stopka('regulamin', u'Regulamin',
                               firma['regulamin'], STOPKA_DEMO)
            # Regulamin ma stanac tuz za polityka, a nie pod linia z copyrightem
            # — inaczej wyglada jak doklejony po stopce.
            nowy = wstaw_po(t, '<div class="wrap" id="polityka"', blok)
            if nowy is None:
                nowy = wstaw_przed(t, '</footer>', blok)
            if nowy:
                t = nowy
                zrobione.append('regulamin')
        if not ma_polityke:
            nowy = wstaw_przed(t, '</footer>',
                               blok_stopka('polityka', u'Polityka prywatno\u015bci',
                                           polityka_tresc(firma), None))
            if nowy:
                t = nowy
                zrobione.append('polityka')
    else:
        # Zawadzcy, Serwis — jedna sekcja przed stopka.
        bloki = []
        if not ma_regulamin:
            bloki.append(('regulamin', u'Regulamin', firma['regulamin'], STOPKA_DEMO))
        if not ma_polityke:
            bloki.append(('polityka', u'Polityka prywatno\u015bci i pliki cookie',
                          polityka_tresc(firma), None))
        if bloki:
            nowy = wstaw_przed(t, '<footer', blok_sekcja(firma['kolory'], bloki))
            if nowy:
                t = nowy
                zrobione += [b[0] for b in bloki]

    if zrobione_kotwica:
        zrobione.append('kotwica-polityki')

    if not ma_cookie:
        nowy = wstaw_przed(t, '</body>', pasek_cookie(firma['klucz']))
        if nowy:
            t = nowy
            zrobione.append('cookie')

    if t != przed:
        with open(sciezka, 'w') as fh:
            fh.write(t)
    return zrobione


def main():
    katalog_p = os.path.join(ROOT, 'p')
    zmienione = 0
    for wpis in sorted(os.listdir(katalog_p)):
        sciezka = os.path.join(katalog_p, wpis, 'index.html')
        if not os.path.isfile(sciezka):
            continue
        firma = None
        for klucz, dane in FIRMY.items():
            if klucz in wpis:
                firma = dict(dane)
                firma['klucz'] = klucz + '-prawne-v1'
                break
        if firma is None:
            continue
        zrobione = przerob(sciezka, firma)
        if zrobione:
            zmienione += 1
            print('  %-42s + %s' % (wpis, ', '.join(zrobione)))
        else:
            print('  %-42s bez zmian' % wpis)
    print('\nZmienionych stron: %d' % zmienione)


if __name__ == '__main__':
    main()
