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

# ⚠️ PRZY PRZENOSINACH NA WLASNA DOMENE zmien tylko te jedna linie —
# stad biora sie adresy kanoniczne, mapa strony i podglad przy udostepnianiu.
BAZA = u'https://probatum.pl/p/newage-lewandowska/'

TEL_POKAZ = u'+48 507 330 730'
TEL_LINK = u'+48507330730'
ADRES = u'ul. Jana Kilińskiego 55/2, 42-218 Częstochowa'

# ─────────────────────────────────────────────────────────────────
#  MENU — jedno miejsce dla wszystkich podstron
# ─────────────────────────────────────────────────────────────────
MENU = [
    ('start',     u'Start',     ''),
    ('o-mnie',    u'O mnie',    'o-mnie/'),
    ('uslugi',    u'Usługi',    'uslugi/'),
    ('portfolio', u'Portfolio', 'portfolio/'),
    ('porady',    u'Poradnik',  'porady/'),
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
    ('2005-saks-london',    u'2005', u'Saks Academies',
     u'Szkolenie ze strzyżenia i koloryzacji — polski oddział '
     u'brytyjskiej akademii'),
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

# Klientka przyslala kazde ujecie w dwoch wersjach — kolorowej i czarno-bialej.
# W galerii zostaje po JEDNEJ z kazdej pary, w kolorze: to samo zdjecie dwa razy
# to zapychanie galerii, nie portfolio. Czarno-biale zostaje wylacznie zdjecie
# glowne na stronie startowej, bo ten konkretny kadr wybrala wprost.
#   1743 = 1720   |   1718 = 1726   |   1727 = 1738   |   1741 = 1719
SESJA = [
    ('kadr-1743', u'W salonie'),
    ('kadr-1718', u'Studio'),
    ('kadr-1727', u'Narzędzia pracy'),
    ('kadr-1741', u'Warsztat'),
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
#  OPINIE — PRZEPISANE Z PROFILU GOOGLE, DOSLOWNIE
#
#  Zrodlo: profil "New Age Studio" w Mapach Google (5,0 z 53 opinii).
#  Cytaty sa dokladne. Tam, gdzie opinia jest dluzsza niz to, co widac
#  w profilu bez rozwijania, cytat urwany jest na granicy zdania —
#  NIC nie jest dopisane ani przeredagowane.
#
#  ⚠️ Nie wolno tu wpisywac tresci wymyslonych. Falszywe opinie sa
#  w Polsce zakazana nieuczciwa praktyka rynkowa i odpowiada za nie
#  przedsiebiorca, czyli klientka.
# ─────────────────────────────────────────────────────────────────
OPINIE = [
    (u'Aneta Orzeł',
     u'Ten salon polecam z całego serca. Każda wizyta u Pani Agnieszki to czysta '
     u'przyjemność. Zawsze wychodzę z salonu zadowolona i zrelaksowana, a włosy '
     u'zadbane i wypielęgnowane. Pani Agnieszka po prostu zna się na swojej robocie.'),
    (u'Klaudia Muś',
     u'Świetny salon fryzjerski! Już od kilku lat korzystam z usług Pani Agnieszki. '
     u'Można liczyć na profesjonalne doradztwo i ogromną dbałość o włosy podczas '
     u'koloryzacji. Efekt piękny, a włosy po zabiegu zdrowe i lśniące.'),
    (u'Janina Nowowiejska',
     u'Do New Age Studio chodzę już od 25 lat i nie wyobrażam sobie zmiany tego '
     u'miejsca na inne. Za każdym razem czuję się tu naprawdę dopieszczona — '
     u'z pełną uwagą, spokojem i troską Pani Agnieszki.'),
    (u'Agata Morawski',
     u'Do pani Agnieszki chodzę od dłuższego czasu i za każdym razem wychodzę '
     u'z salonu zachwycona. Ostatnio skorzystałam z botoksu na włosy — efekt '
     u'przerósł moje oczekiwania! Włosy są gładkie, miękkie, lśniące.'),
    (u'Teresa Bajor',
     u'Z usług Pani Agnieszki korzystam od wielu lat i zawsze wychodzę zadowolona, '
     u'włosy są uporządkowane, wypielęgnowane, wystylizowane, a ja czuję się '
     u'wyśmienicie.'),
    (u'Maria Różycka',
     u'Do Pani Agnieszki trafiłam dwa lata temu przez przypadek. Moja wieloletnia '
     u'fryzjerka wyjechała na stałe z Polski i szukałam nowego zakładu fryzjerskiego. '
     u'Ten, do którego trafiłam, nie spełnił moich oczekiwań.'),
]

LINK_GOOGLE = (u'https://www.google.com/maps/place/New+Age+Studio/'
               u'@50.8196257,19.1136929,17z/data=!4m8!3m7'
               u'!1s0x4710b5ce3d07422f:0x4cc4e3755647bc1!9m1!1b1')


def karty_opinii(ile=None, odnosnik=None):
    """Na stronie glownej karty prowadza do zakladki z opiniami — inaczej
    goscia nic nie zabiera dalej i utyka na trzech cytatach."""
    lista = OPINIE if ile is None else OPINIE[:ile]
    if odnosnik:
        return u'\n      '.join(
            u'<a class="opinia opinia-klik" href="%s">'
            u'<div class="gwiazdki" aria-label="5 na 5">★★★★★</div>'
            u'<p>%s</p><p class="kto">%s · Google</p>'
            u'<span class="opinia-wiecej">Przeczytaj wszystkie</span></a>'
            % (odnosnik, tresc, autor) for autor, tresc in lista)
    return u'\n      '.join(
        u'<article class="opinia"><div class="gwiazdki" aria-label="5 na 5">★★★★★</div>'
        u'<p>%s</p><p class="kto">%s · Google</p></article>' % (tresc, autor)
        for autor, tresc in lista)


# ─────────────────────────────────────────────────────────────────
#  BLOK ZAPRASZAJACY DO KONTAKTU — konczy kazda podstrone
# ─────────────────────────────────────────────────────────────────
def blok_kontaktu(naglowek, zdanie):
    return u"""
<section class="zaproszenie">
  <div class="waski" style="text-align:center">
    <p class="nadpis" style="justify-self:center">Umów wizytę</p>
    <h2>%s</h2>
    <p class="zaproszenie-lead">%s</p>
    <div class="zaproszenie-akcje">
      <a class="btn btn-ciemny" href="tel:%s">Zadzwoń: %s</a>
      <a class="btn btn-duch" href="https://www.instagram.com/new_age_lewandowska"
         target="_blank" rel="noopener">Napisz na Instagramie</a>
    </div>
    <p class="zaproszenie-drobne">
      Rozmowa nic nie kosztuje i do niczego nie zobowiązuje.
      Cenę poznasz przed zabiegiem, nie po.
    </p>
  </div>
</section>
""" % (naglowek, zdanie, TEL_LINK, TEL_POKAZ)



# ─────────────────────────────────────────────────────────────────
#  PORADNIK
#
#  Po co: ludzie nie wpisuja w Google "fryzjer Czestochowa" — wpisuja
#  "czy da sie naprawic wlosy po domowym farbowaniu" albo "ile trzyma
#  balayage". Kazdy taki tekst to osobne wejscie na strone od kogos,
#  kto ma dokladnie ten problem. A Agnieszka szkolila fryzjerki, wiec
#  ma czym te teksty wypelnic.
#
#  Zasada: konkret, nie lanie wody. Kazdy tekst konczy sie zaproszeniem.
# ─────────────────────────────────────────────────────────────────
PORADY = [
 ('domowa-koloryzacja',
  u'Farbowałam włosy w domu. Czy da się to naprawić?',
  u'Najczęstsze pytanie, jakie słyszę. Odpowiedź brzmi: prawie zawsze tak, '
  u'ale rzadko za jednym razem.',
  u'jak naprawić włosy po domowej koloryzacji, farbowanie w domu, korekta koloru',
  u"""
<p>
  Farba z drogerii nie jest zła sama w sobie. Problem polega na tym, że jest
  <b>uniwersalna</b> — ma zadziałać na każdych włosach, więc jest mocniejsza,
  niż potrzeba na Twoich. Nakłada się ją na całą długość, także tam, gdzie
  kolor już jest, i przy trzecim, czwartym farbowaniu końcówki robią się
  ciemniejsze i matowe.
</p>
<h3>Co widzę najczęściej</h3>
<p>
  <b>Ciemna, martwa końcówka przy jasnych odrostach.</b> Efekt nakładania
  farby raz za razem na to samo miejsce. Wymaga rozjaśnienia końcówek, nie
  przyciemnienia odrostów.
</p>
<p>
  <b>Zieleń albo miedź po zmianie na jaśniejszy.</b> Ciemny pigment nie schodzi
  równo — najpierw ustępuje niebieski, zostaje żółto-czerwony. To się naprawia
  tonowaniem, ale trzeba wiedzieć czym.
</p>
<p>
  <b>Henna.</b> Osobna kategoria. Henna osadza się w włosie inaczej niż farba
  i potrafi zareagować z rozjaśniaczem w sposób, którego nie da się przewidzieć.
  Jeśli kiedykolwiek robiłaś hennę — powiedz o tym, nawet jeśli było to trzy lata
  temu. To zmienia cały plan.
</p>
<h3>Dlaczego rzadko da się to zrobić w jeden dzień</h3>
<p>
  Bo każde rozjaśnienie to obciążenie dla włosa. Można wszystko zrobić za jednym
  razem i wyjść z kolorem, o który prosiłaś — a za dwa tygodnie zobaczyć, że
  włosy się łamią. Wolę rozpisać to na dwie albo trzy wizyty w odstępach
  kilku tygodni i dojść do celu w całości.
</p>
<p>
  Na pierwszej wizycie powiem wprost, ile to potrwa i ile będzie kosztować —
  <b>zanim</b> cokolwiek zacznę.
</p>
"""),

 ('ile-trzyma-balayage',
  u'Ile trzyma balayage i jak go przedłużyć',
  u'Dobrze zrobiony balayage wygląda dobrze przez trzy, cztery miesiące. '
  u'To, ile faktycznie wytrzyma, zależy głównie od tego, co robisz w domu.',
  u'ile trzyma balayage, jak dbać o balayage, koloryzacja Częstochowa',
  u"""
<p>
  Balayage ma nad klasycznymi pasemkami jedną przewagę: <b>nie ma ostrej granicy
  odrostu</b>. Przy pasemkach po sześciu tygodniach widać linię i trzeba wracać.
  Przy balayage przejście jest miękkie, więc włosy wyglądają dobrze znacznie dłużej.
</p>
<h3>Realne terminy</h3>
<p>
  <b>3–4 miesiące</b> — tyle zwykle mija do wizyty odświeżającej. Nie dlatego,
  że kolor znika, tylko dlatego, że włosy odrastają i proporcje przestają się
  zgadzać.
</p>
<p>
  <b>6–8 tygodni</b> — tyle trzyma tonowanie, czyli chłodny odcień blondu.
  To osobna, krótsza i tańsza wizyta, którą można wcisnąć między pełne
  koloryzacje.
</p>
<h3>Co skraca ten czas najbardziej</h3>
<p>
  <b>Za gorąca woda.</b> Otwiera łuskę włosa i wypłukuje pigment.
  Myj letnią, ostatnie spłukanie chłodną — to jedna z niewielu rad,
  które działają natychmiast i nic nie kosztują.
</p>
<p>
  <b>Szampony z silnymi detergentami.</b> Sprawdź, czy na etykiecie
  nie ma <i>sodium lauryl sulfate</i> na drugim miejscu składu.
  Do koloryzowanych włosów potrzebny jest łagodniejszy.
</p>
<p>
  <b>Prostownica bez ochrony termicznej.</b> 200 stopni na suchym włosie
  wypala pigment szybciej niż mycie. Jeśli prostujesz codziennie, licz się
  z tonowaniem co sześć tygodni zamiast co osiem.
</p>
<p>
  <b>Basen.</b> Chlor plus blond to klasyczny zielony refleks. Przed wejściem
  do wody zmocz włosy czystą wodą i nałóż odżywkę — nasiąknięty włos przyjmie
  mniej chloru.
</p>
"""),

 ('blond-bez-zolknienia',
  u'Jak dbać o blond, żeby nie żółkł',
  u'Żółknięcie to nie wina koloryzacji. To naturalny pigment, który wraca — '
  u'i da się go trzymać w ryzach prostymi sposobami.',
  u'jak dbać o blond, fioletowy szampon, żółty odcień włosów, rozjaśnianie',
  u"""
<p>
  Kiedy rozjaśniamy włosy, usuwamy pigment warstwami: najpierw czarny,
  potem czerwony, na końcu żółty. Ten żółty siedzi najgłębiej i praktycznie
  nigdy nie znika do końca — dlatego po rozjaśnieniu nakłada się toner,
  który go neutralizuje. Toner z czasem się zmywa i żółty wraca. To normalne,
  a nie błąd fryzjera.
</p>
<h3>Fioletowy szampon — jak go używać, żeby pomagał</h3>
<p>
  Fiolet neutralizuje żółć, bo leży po przeciwnej stronie koła barw. Ale to
  narzędzie, nie codzienna pielęgnacja.
</p>
<p>
  <b>Raz, najwyżej dwa razy w tygodniu.</b> Codzienne używanie daje siwy,
  szarawy odcień i wysusza włosy.
</p>
<p>
  <b>Trzymaj 3–5 minut, nie dłużej.</b> „Zostawię na dziesięć, będzie lepiej"
  kończy się fioletowymi końcówkami, zwłaszcza na porowatych włosach.
</p>
<p>
  <b>Nakładaj na mokre, ale odciśnięte włosy.</b> Na ociekających rozcieńcza
  się i nie działa.
</p>
<h3>Czego unikać</h3>
<p>
  Twarda woda z dużą zawartością żelaza potrafi dać rudy nalot — jeśli
  mieszkasz tam, gdzie woda jest twarda, warto raz na jakiś czas użyć
  szamponu oczyszczającego.
</p>
<p>
  Zbyt częste rozjaśnianie całej długości też szkodzi bardziej niż pomaga.
  Odrosty rozjaśniamy, długość tylko tonujemy — inaczej po roku końcówki
  będą przezroczyste.
</p>
"""),

 ('siwe-wlosy',
  u'Siwe włosy: farbować czy przejść na naturalne?',
  u'Nie ma jednej dobrej odpowiedzi. Jest natomiast kilka rzeczy, które warto '
  u'wiedzieć, zanim podejmiesz decyzję.',
  u'siwe włosy farbowanie, przejście na siwe, koloryzacja siwych włosów',
  u"""
<p>
  To decyzja, którą klientki odkładają latami — zwykle dlatego, że boją się
  etapu przejściowego. Słusznie, bo to on jest najtrudniejszy. Ale da się go
  skrócić i uczynić znośnym.
</p>
<h3>Jeśli farbujesz i chcesz farbować dalej</h3>
<p>
  Siwy włos jest inny w budowie — grubszy, bardziej oporny, gorzej przyjmuje
  pigment. Dlatego przy dużym udziale siwizny stosuje się mocniejszą bazę
  i dłuższy czas działania. Odrost przy siwiźnie widać po trzech, czterech
  tygodniach, nie po sześciu — to trzeba wliczyć w budżet i kalendarz.
</p>
<h3>Jeśli myślisz o przejściu na naturalne</h3>
<p>
  Najgorsze wyjście to odpuścić farbowanie i czekać. Przez rok masz wtedy
  wyraźną, ciemną granicę, której nie da się ukryć.
</p>
<p>
  Lepiej działa <b>rozjaśnienie długości pasemkami</b> tak, żeby zbliżyć ją
  do koloru odrostu. Granica się rozmywa i po kilku miesiącach po prostu
  przestaje być widoczna. To kilka wizyt, ale wychodzisz z każdej z fryzurą,
  którą można pokazać.
</p>
<h3>Kolor to nie wszystko</h3>
<p>
  Siwe włosy mają inną strukturę — bywają bardziej szorstkie i sztywne.
  Dobre cięcie i regularna pielęgnacja robią przy nich większą różnicę
  niż przy włosach pigmentowanych. Naturalna siwizna wygląda świetnie,
  ale zadbana; zaniedbana wygląda po prostu na zaniedbaną.
</p>
"""),

 ('pierwsza-wizyta',
  u'Idziesz do nowego fryzjera. Jak się przygotować?',
  u'Kilka rzeczy, które zrobisz przed wizytą, potrafi zdecydować o tym, '
  u'czy wyjdziesz zadowolona.',
  u'pierwsza wizyta u fryzjera, jak przygotować się do koloryzacji',
  u"""
<h3>Przynieś zdjęcia — ale nie jedno</h3>
<p>
  Jedno zdjęcie mówi mało, bo nie wiadomo, co dokładnie Ci się w nim podoba:
  kolor, cięcie, a może tylko modelka. Przynieś trzy albo cztery. Warto też
  pokazać zdjęcie tego, czego <b>nie</b> chcesz — to często bardziej pomocne.
</p>
<h3>Powiedz całą historię włosów</h3>
<p>
  Henna sprzed dwóch lat, keratyna, domowe rozjaśnianie, jedna nieudana wizyta,
  po której „coś dziwnego się działo" — wszystko to ma znaczenie i wszystko
  wpływa na to, co da się dziś zrobić. Nie ma tu czego się wstydzić; im więcej
  wiem, tym mniejsza szansa niespodzianki.
</p>
<h3>Nie myj włosów w dniu koloryzacji</h3>
<p>
  Naturalna warstwa tłuszczu chroni skórę głowy przed podrażnieniem. Włosy
  umyte dzień wcześniej to idealny stan. Nie stosuj też mocnych lakierów
  ani suchego szamponu przed wizytą.
</p>
<h3>Zarezerwuj więcej czasu, niż myślisz</h3>
<p>
  Koloryzacja to od dwóch do pięciu godzin, zależnie od tego, co robimy.
  Jeśli masz coś zaplanowane dwie godziny później, presja czasu odbije się
  na efekcie. Przy umawianiu podaję realny czas — warto go potraktować poważnie.
</p>
<h3>Powiedz, ile masz czasu rano</h3>
<p>
  To pytanie zadaję każdej nowej klientce i wiele osób się dziwi. A to jedna
  z najważniejszych informacji: fryzura, która wymaga czterdziestu minut
  i trzech urządzeń, jest bezużyteczna, jeśli rano masz dziesięć minut.
</p>
"""),
]

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
<link rel="canonical" href="%(kanon)s">
<link rel="stylesheet" href="%(korzen)sstyl.css">

<link rel="icon" href="%(korzen)simg/ikona-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="%(korzen)simg/ikona-180.png">
<link rel="manifest" href="%(korzen)smanifest.json">
<meta name="theme-color" content="#0A0A0B">

<meta property="og:type" content="website">
<meta property="og:site_name" content="new age Lewandowska">
<meta property="og:title" content="%(tytul)s">
<meta property="og:description" content="%(opis)s">
<meta property="og:image" content="%(baza)simg/hero.jpg">
<meta property="og:url" content="%(kanon)s">
<meta property="og:locale" content="pl_PL">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HairSalon",
  "name": "new age Lewandowska",
  "alternateName": "New Age Studio",
  "description": "Salon fryzjerski w Cz\u0119stochowie. Koloryzacja, strzy\u017cenie i modelowanie u Agnieszki Lewandowskiej \u2014 edukatorki L\u2019Or\u00e9al Professionnel.",
  "image": "%(baza)simg/hero.jpg",
  "url": "%(baza)s",
  "telephone": "%(tel_pokaz)s",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Jana Kili\u0144skiego 55/2",
    "addressLocality": "Cz\u0119stochowa",
    "postalCode": "42-218",
    "addressCountry": "PL"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 50.8196257, "longitude": 19.1136929 },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "53" },
  "priceRange": "$$",
  "sameAs": [
    "https://www.instagram.com/new_age_lewandowska",
    "https://www.facebook.com/profile.php?id=100057636820418"
  ],
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday"],
      "opens": "10:00", "closes": "18:00" },
    { "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00" }
  ]
}
</script>
%(okruszki)s
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
    <div class="naglowek-prawo">
      <span class="stan" id="stan" hidden></span>
      <a class="naglowek-tel" href="tel:%(tel_link)s">%(tel_pokaz)s</a>
    </div>
  </div>
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
        <span style="display:block; padding:.2rem 0">ul. Jana Kilińskiego 55/2<br>42-218 Częstochowa</span>
        <a href="https://www.instagram.com/new_age_lewandowska" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.facebook.com/profile.php?id=100057636820418" target="_blank" rel="noopener">Facebook</a>
      </div>
    </div>
    <div class="stopka-dol">
      <span>© 2026 new age Lewandowska</span>
      <span><a href="%(korzen)sprywatnosc/" style="color:inherit">Polityka prywatności</a>
        · Wersja robocza — strona w budowie</span>
    </div>
  </div>
</footer>

<nav class="dok" aria-label="Szybkie akcje">
  <a class="glowna" href="tel:%(tel_link)s">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>
    Zadzwoń
  </a>
  <a href="%(korzen)skontakt/#wycena">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M9 15h6M9 11h3"/></svg>
    Wyceń
  </a>
  <button id="dok-menu" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="panel">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    Menu
  </button>
</nav>

<div class="zaslona" id="zaslona" aria-hidden="true"></div>
<div class="panel" id="panel" role="dialog" aria-modal="true" aria-labelledby="panel-tytul">
  <div class="panel-uchwyt" aria-hidden="true"></div>
  <div class="panel-glowa">
    <h2 id="panel-tytul">Menu</h2>
    <button class="panel-zamknij" id="panel-zamknij" type="button" aria-label="Zamknij menu">✕</button>
  </div>
  <nav class="panel-lista" aria-label="Nawigacja">
    %(menu_mobilne)s
  </nav>
  <div class="panel-stopka">
    <a class="a1" href="tel:%(tel_link)s">Zadzwoń</a>
    <a class="a2" href="https://www.instagram.com/new_age_lewandowska" target="_blank" rel="noopener">Instagram</a>
  </div>
</div>

<div class="cookie" id="cookie" role="region" aria-label="Informacja o plikach cookie" hidden>
  <p>
    Ta strona nie śledzi Cię i nie profiluje — nie ma tu analityki ani reklam.
    W pamięci przeglądarki zapisujemy jedną rzecz: informację, że ten komunikat
    został zamknięty. <a href="%(korzen)sprywatnosc/">Polityka prywatności</a>.
  </p>
  <button type="button" id="cookie-ok">Rozumiem</button>
</div>

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


def okruszki(nazwa, sciezka):
    """Sciezka nawigacyjna dla wyszukiwarek — pokazuje sie w wynikach
    zamiast golego adresu."""
    if not sciezka:
        return u''
    return (u'<script type="application/ld+json">\n'
            u'{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            u'{"@type":"ListItem","position":1,"name":"Strona g\u0142\u00f3wna","item":"%s"},'
            u'{"@type":"ListItem","position":2,"name":"%s","item":"%s%s/"}]}\n'
            u'</script>' % (BAZA, nazwa, BAZA, sciezka))


def zbuduj(klucz, tytul, opis, tresc, korzen, sciezka='', nazwa=''):
    return SZKIELET % {
        'tytul': tytul, 'opis': opis, 'korzen': korzen,
        'menu': nawigacja(klucz, korzen),
        'menu_mobilne': menu_mobilne(klucz, korzen),
        'stopka_menu': stopka_menu(korzen),
        'tel_link': TEL_LINK, 'tel_pokaz': TEL_POKAZ,
        'tresc': tresc,
        'baza': BAZA,
        'kanon': BAZA + (sciezka + '/' if sciezka else ''),
        'okruszki': okruszki(nazwa, sciezka),
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
          i Saks, cztery szkolenia w Akademii L'Oréal Professionnel — i lata
          uczenia innych fryzjerek tego, co sama robi.
        </p>
        <div class="hero-akcje">
          <a class="btn" href="tel:%(tel_link)s">Umów wizytę</a>
          <a class="btn btn-duch" href="o-mnie/">Poznaj mnie</a>
        </div>
        <div class="odznaka"><b>5,0</b> ★ · 53 opinie w Google</div>
      </div>
      <div class="hero-foto">
        <img src="img/hero.jpg" alt="Agnieszka Lewandowska" width="1024" height="1024" fetchpriority="high">
      </div>
    </div>
  </div>
</section>
""" % {'tel_link': TEL_LINK}

    dyplomy_skrot = u'\n      '.join(
        u'<button type="button" class="powieksz" data-pelne="img/dyplomy/%s.jpg"'
        u' data-podpis="%s · %s" aria-label="Powiększ: %s">'
        u'<img src="img/dyplomy/%s-mal.jpg" alt="%s — %s" loading="lazy"></button>'
        % (p[0], p[1], p[2], p[2], p[0], p[1], p[2])
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
        w Saks Academies — to brytyjskie szkoły fryzjerstwa, które prowadziły wtedy
        zajęcia także w Polsce. W 2009 zdobyłam uprawnienia pedagogiczne dla
        instruktorów i przez lata prowadziłam warsztaty dla innych fryzjerek
        jako edukatorka L'Oréal Professionnel.
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
    <h2>Dwadzieścia lat, <span class="kursywa">dwadzieścia dyplomów</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      Toni&amp;Guy, Saks, uprawnienia instruktorskie, cztery szkolenia
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
      <div class="usluga"><h3>Koloryzacja</h3><p>Balayage, rozjaśnianie, refleksy, korekta koloru. Zawsze po rozmowie o tym, czy kondycja Twoich włosów na to pozwoli.</p></div>
      <div class="usluga"><h3>Strzyżenie</h3><p>Fryzura, która trzyma formę także wtedy, gdy układasz ją sama, w pośpiechu, przed wyjściem.</p></div>
      <div class="usluga"><h3>Modelowanie</h3><p>Na co dzień i na okazje. Także nauka układania — żeby dało się to powtórzyć w domu.</p></div>
      <div class="usluga"><h3>Pielęgnacja</h3><p>Zabiegi dobrane do stanu włosów, nie do cennika. Czasem zamiast koloru potrzebna jest regeneracja.</p></div>
    </div>
    <a class="link-dalej" href="uslugi/">Pełna oferta i dlaczego nie ma cennika</a>
  </div>
</section>

<section id="sytuacje">
  <div class="wrap">
    <p class="nadpis">Z czym przychodzą</p>
    <h2>Poznajesz się <span class="kursywa">w którymś z tych zdań</span>?</h2>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      To cztery sytuacje, z którymi najczęściej trafiają do mnie nowe klientki
      w Częstochowie. Przy każdej napisałam, co da się z tym zrobić.
    </p>

    <div class="sytuacje">
      <a class="sytuacja" href="porady/domowa-koloryzacja/">
        <span class="s-cyt">„Farbowałam w domu i teraz końcówki są ciemne."</span>
        <span class="s-odp">Prawie zawsze da się naprawić — rzadko za jednym razem.</span>
        <span class="opinia-wiecej">Co z tym zrobić</span>
      </a>
      <a class="sytuacja" href="porady/blond-bez-zolknienia/">
        <span class="s-cyt">„Blond mi żółknie po dwóch tygodniach."</span>
        <span class="s-odp">To wraca naturalny pigment. Da się go trzymać w ryzach.</span>
        <span class="opinia-wiecej">Co z tym zrobić</span>
      </a>
      <a class="sytuacja" href="porady/siwe-wlosy/">
        <span class="s-cyt">„Chcę przestać farbować siwe, ale boję się przejścia."</span>
        <span class="s-odp">Da się je skrócić i przejść przez nie z fryzurą, nie z granicą.</span>
        <span class="opinia-wiecej">Co z tym zrobić</span>
      </a>
      <a class="sytuacja" href="porady/pierwsza-wizyta/">
        <span class="s-cyt">„Nie wiem, czego chcę — po prostu mi się nie podoba."</span>
        <span class="s-odp">To dobry punkt wyjścia. Od tego zaczyna większość wizyt.</span>
        <span class="opinia-wiecej">Co z tym zrobić</span>
      </a>
    </div>
  </div>
</section>

<section class="ciemno">
  <div class="wrap">
    <p class="nadpis">Opinie</p>
    <h2>Pięć na pięć, <span class="kursywa">53 razy</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:54ch">
      Pięć na pięć z 53 opinii w Google. Najczęściej wraca jedno zdanie:
      że słucham, zanim wezmę nożyczki.
    </p>
    <div class="opinie-siatka">
      %(opinie)s
    </div>
    <div class="hero-akcje" style="margin-top:2.4rem">
      <a class="btn btn-ciemny" href="opinie/#wystaw">Wystaw opinię</a>
      <a class="btn btn-duch" href="opinie/">Przeczytaj wszystkie</a>
    </div>
  </div>
</section>
""" % {'dyplomy': dyplomy_skrot, 'przerywnik': PRZERYWNIK,
      'opinie': karty_opinii(3, 'opinie/')}

    return czolowka + reszta + blok_kontaktu(
        u'Zadzwoń, zanim <span class="kursywa">zdecydujesz</span>.',
        u'Nie musisz wiedzieć, czego chcesz. Wystarczy, że powiesz, co Ci się '
        u'w Twoich włosach nie podoba — resztę wymyślimy razem.')


def strona_o_mnie():
    rzedy = []
    for i, (plik, rok, tytul, opis) in enumerate(DYPLOMY, 1):
        rzedy.append(u"""
    <article class="usluga-duza dyplom">
      <div class="u-foto">
        <button type="button" class="powieksz" data-pelne="../img/dyplomy/%s.jpg"
          data-podpis="%s · %s" aria-label="Powiększ dyplom: %s">
          <img src="../img/dyplomy/%s-mal.jpg" alt="%s — %s" loading="lazy">
        </button>
      </div>
      <div>
        <span class="u-numer">%s</span>
        <h3>%s</h3>
        <p>%s</p>
      </div>
    </article>""" % (plik, rok, tytul, tytul, plik, tytul, opis, rok, tytul, opis))

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
        szkoliłam się w Saks Academies — strzyżenie i koloryzacja. To brytyjskie
        szkoły fryzjerstwa, które prowadziły wtedy zajęcia także w Polsce.
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
        rozmawiamy. Bez niespodzianek w lustrze.
      </p>
    </div>
    <img src="../img/sesja/kadr-1743.jpg" alt="Agnieszka Lewandowska" width="733" height="1100" loading="lazy" class="wejscie">
  </div>
</section>

<div class="mysl ciemno">
  <blockquote>Dwadzieścia lat. Dwadzieścia dyplomów. Zero zgadywania.</blockquote>
  <cite>Droga zawodowa — 2003–2023</cite>
</div>

<section id="dyplomy" style="padding-top:clamp(28px,4vw,52px)">
  <div class="wrap">
    <p class="nadpis">Droga</p>
    <h2>Od pierwszego dyplomu <span class="kursywa">do dziś</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:58ch">
      Dyplomów uzbierało się przez te lata około dwudziestu. Poniżej osiem,
      które są dla mnie najważniejsze — każdy można powiększyć i przeczytać.
      Oryginały wiszą w salonie; dwa najstarsze wystawione są jeszcze
      na nazwisko panieńskie, Dziuk.
    </p>
""" + u''.join(rzedy) + u"""
  </div>
</section>
""" + blok_kontaktu(
        u'Chcesz, żeby ktoś taki <span class="kursywa">zajął się Twoimi włosami</span>?',
        u'Zadzwoń i opowiedz, co chcesz zmienić. Doradzę, co da się zrobić '
        u'i czego lepiej nie robić.'))


def strona_uslugi():
    return (
        naglowek_strony(u'Usługi',
            u'Co robię, ile to trwa <span class="kursywa">i czego się spodziewać</span>.',
            u'Bez ogólników. Przy każdej usłudze piszę, jak wygląda, ile zajmuje '
            u'i dla kogo ma sens — żebyś wiedziała, na co się umawiasz.') +
u"""
<section style="padding-top:0">
  <div class="wrap">

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1727.jpg" alt="Koloryzacja" loading="lazy"></div>
      <div>
        <span class="u-numer">01 — Koloryzacja</span>
        <h3>Kolor dobrany do kondycji Twoich włosów</h3>
        <p>
          Zaczynamy od obejrzenia włosów i rozmowy o tym, co było na nich wcześniej.
          Henna, domowe farbowanie z drogerii, rozjaśnianie sprzed pół roku — to wszystko
          zmienia, co da się dziś zrobić. Powiem wprost, jeśli wymarzony efekt wymaga
          dwóch albo trzech wizyt, zamiast obiecywać go od ręki i zniszczyć włosy.
        </p>
        <p>
          Pracuję na L'Oréal Professionnel — na tych produktach szkoliłam się od 2013 roku
          i wiem, jak się zachowują na różnych włosach.
        </p>
        <ul class="u-fakty">
          <li>Odrosty — ok. 2 godz.</li><li>Balayage — 3–5 godz.</li>
          <li>Korekta koloru — po konsultacji</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1743.jpg" alt="Strzyżenie" loading="lazy"></div>
      <div>
        <span class="u-numer">02 — Strzyżenie</span>
        <h3>Fryzura, którą ułożysz sama w czwartek rano</h3>
        <p>
          Najładniejsze cięcie jest do niczego, jeśli wymaga czterdziestu minut
          i trzech urządzeń. Dlatego pytam, ile czasu naprawdę masz rano i czego
          używasz — i dobieram fryzurę do tego, a nie do zdjęcia z internetu.
        </p>
        <p>
          Jeśli przyniesiesz zdjęcie, powiem uczciwie, czy na Twoich włosach
          i przy Twoim typie urody to zadziała. Czasem odradzę i zaproponuję coś innego.
        </p>
        <ul class="u-fakty">
          <li>Strzyżenie damskie — ok. 1 godz.</li><li>Męskie — ok. 40 min</li>
          <li>Duża zmiana — konsultacja przed</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1741.jpg" alt="Modelowanie" loading="lazy"></div>
      <div>
        <span class="u-numer">03 — Modelowanie i upięcia</span>
        <h3>Na wesele, na sesję i na zwykły wtorek</h3>
        <p>
          Modelowanie po zabiegu, fale, prostowanie, objętość. Przy okazji pokazuję,
          jak to powtórzyć w domu — który produkt, w którym momencie, w którą stronę
          prowadzić szczotkę. To zwykle robi większą różnicę niż samo cięcie.
        </p>
        <p>
          Upięcia okolicznościowe robię po wcześniejszej próbie, jeśli okazja jest ważna.
          Do sesji zdjęciowych i stylizacji — mam za sobą pracę przy publikacjach
          w magazynie i katalogach.
        </p>
        <ul class="u-fakty">
          <li>Modelowanie — 30–45 min</li><li>Upięcie — od 1 godz.</li>
          <li>Próba przed ślubem — możliwa</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1718.jpg" alt="Pielęgnacja" loading="lazy"></div>
      <div>
        <span class="u-numer">04 — Pielęgnacja i regeneracja</span>
        <h3>Czasem zamiast koloru potrzebna jest przerwa</h3>
        <p>
          Zdarza się, że przychodzisz po koloryzację, a ja proponuję najpierw
          regenerację. Nie dlatego, że tak wygodniej — tylko dlatego, że na
          przesuszonych włosach kolor i tak się nie utrzyma i wyjdziesz rozczarowana.
        </p>
        <p>
          Zabiegi dobieram do stanu włosów, nie do cennika. Dostaniesz też
          konkretne wskazówki, czego używać w domu — i czego zdecydowanie nie.
        </p>
        <ul class="u-fakty">
          <li>Zabieg — 30–60 min</li><li>Często łączony z koloryzacją</li>
          <li>Dobór pielęgnacji domowej — gratis</li>
        </ul>
      </div>
    </article>

  </div>
</section>

<section class="ciemno" id="bon">
  <div class="wrap dwie">
    <div class="tresc">
      <p class="nadpis">Bon podarunkowy</p>
      <h2>Prezent, którego <span class="kursywa">nie trzeba wymieniać</span>.</h2>
      <p>
        Bon na dowolną kwotę albo na konkretną usługę — do wykorzystania
        przez pół roku. Sprawdza się na urodziny, Dzień Matki i święta,
        zwłaszcza dla kogoś, kto „ma już wszystko".
      </p>
      <p>
        Wystawiam go od ręki w salonie albo wysyłam w wersji do wydruku,
        jeśli prezent jest na ostatnią chwilę.
      </p>
      <p style="margin-top:1.8rem">
        <a class="btn btn-ciemny" href="tel:%(tel_link)s">Zamów bon telefonicznie</a>
      </p>
    </div>
    <img src="../img/sesja/kadr-1727.jpg" alt="Salon new age w Częstochowie" loading="lazy">
  </div>
</section>

<div class="mysl">
  <blockquote>Wolę odradzić, niż zrobić coś, czego obie pożałujemy.</blockquote>
  <cite>Agnieszka Lewandowska</cite>
</div>

<section id="jak-to-wyglada">
  <div class="waski">
    <p class="nadpis">Jak wygląda wizyta</p>
    <h2>Cztery kroki, <span class="kursywa">bez niespodzianek</span>.</h2>
    <div class="kroki">
      <div class="krok">
        <h3>Rozmowa</h3>
        <p>Oglądam włosy, pytam o historię koloryzacji, o to, ile masz czasu rano
        i czego oczekujesz. Zajmuje to kilka minut i oszczędza mnóstwo rozczarowań.</p>
      </div>
      <div class="krok">
        <h3>Cena i czas</h3>
        <p>Zanim cokolwiek zacznę, wiesz, ile to będzie kosztować i ile potrwa.
        Jeśli w trakcie okaże się, że potrzeba czegoś więcej — pytam, nie dopisuję.</p>
      </div>
      <div class="krok">
        <h3>Praca</h3>
        <p>Jedna osoba na raz. Nie biegam między trzema fotelami, więc nie zostajesz
        z farbą na głowie na czterdzieści minut dłużej, niż trzeba.</p>
      </div>
      <div class="krok">
        <h3>Co dalej</h3>
        <p>Na koniec pokazuję, jak ułożyć fryzurę w domu, i mówię, kiedy wrócić.
        Jeśli coś jest nie tak — wróć, poprawię.</p>
      </div>
    </div>
  </div>
</section>

<section class="ciemno" id="cennik">
  <div class="waski">
    <p class="nadpis">Cennik</p>
    <h2>Dlaczego nie ma tu <span class="kursywa">tabelki z cenami</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      Bo uczciwie się nie da. Ta sama koloryzacja na włosach do ramion i na włosach
      do pasa to dwie różne ilości farby, dwa różne czasy pracy i dwie różne ceny.
      Do tego dochodzi grubość i gęstość włosów oraz to, co było na nich wcześniej.
    </p>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      Tabelka „od 150 zł" nie znaczy nic — poza tym, że przy kasie usłyszysz
      inną kwotę. Wolę powiedzieć prawdę wcześniej.
    </p>

    <div class="pytania" style="margin-top:2.6rem">
      <details><summary>Jak w takim razie poznam cenę?</summary>
        <p>Trzy sposoby, każdy działa: zadzwoń i opisz włosy, wypełnij
        <a href="../kontakt/#wycena" style="color:var(--biel)">formularz wyceny</a>
        — pyta dokładnie o długość i gęstość — albo wpadnij na bezpłatną konsultację.
        W każdym przypadku cenę podaję <b>przed</b> zabiegiem.</p></details>
      <details><summary>Pracuję w pakietach — co to znaczy?</summary>
        <p>Najczęściej łączy się koloryzację ze strzyżeniem i modelowaniem albo samą
        koloryzację z modelowaniem. Wychodzi taniej niż każda usługa osobno
        i zajmuje jedną wizytę zamiast dwóch.</p></details>
      <details><summary>Czy cena może wzrosnąć w trakcie?</summary>
        <p>Tylko wtedy, gdy w trakcie okaże się, że potrzeba czegoś, czego nie
        dało się przewidzieć — i wtedy <b>pytam, zanim to zrobię</b>. Nigdy nie
        dopisuję kwot po fakcie.</p></details>
    </div>

    <p style="margin-top:2.4rem">
      <a class="btn btn-ciemny" href="tel:%(tel_link)s">Zadzwoń i zapytaj o cenę</a>
    </p>
  </div>
</section>
""" % {'tel_link': TEL_LINK} + blok_kontaktu(
        u'Nie wiesz, ile to <span class="kursywa">u Ciebie</span> wyjdzie?',
        u'Jeden telefon wystarczy. Opiszesz włosy, powiem cenę — jeszcze zanim '
        u'usiądziesz w fotelu.'))


def strona_portfolio():
    return (
        naglowek_strony(u'Portfolio',
            u'Praca, która <span class="kursywa">wyszła poza salon</span>.',
            u'Sesje wizerunkowe, stylizacje do magazynu i katalogu. '
            u'Włosy przy tych zdjęciach to moja robota — robiona w Częstochowie.') +
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
""" + blok_kontaktu(
        u'Taką robotę mogę zrobić <span class="kursywa">i Tobie</span>.',
        u'Sesja, ślub, ważne wyjście albo zwykły czwartek — zadzwoń i ustalmy termin.'))


def strona_opinie():
    return (
        naglowek_strony(u'Opinie',
            u'Pięć na pięć, <span class="kursywa">53 razy</span>.',
            u'Pięć na pięć z 53 opinii w Google — od klientek salonu new age '
            u'przy Kilińskiego w Częstochowie.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="dwie odwrot" style="margin-bottom:clamp(40px,6vw,72px)">
      <div class="tresc">
        <h2 style="font-size:clamp(1.7rem,3.4vw,2.6rem)">
          Najczęściej wraca <span class="kursywa">to samo zdanie</span>.
        </h2>
        <p>
          Że słucham, zanim wezmę nożyczki. Że mówię wprost, czego na tych
          włosach lepiej nie robić. I że po wyjściu z salonu fryzura daje się
          ułożyć samodzielnie następnego dnia.
        </p>
        <p>
          Najstarsza klientka przychodzi tu od dwudziestu pięciu lat.
          To dla mnie ważniejsze niż każda pojedyncza opinia.
        </p>
      </div>
      <img src="../img/sesja/kadr-1727.jpg" alt="Agnieszka Lewandowska przy pracy"
           width="1400" height="933" loading="lazy">
    </div>

    <div class="opinie-siatka" style="margin-top:0">
      %(opinie)s
    </div>
    <p style="color:var(--srebro-ciemne); font-size:.88rem; margin-top:1.6rem">
      Opinie przepisane z profilu Google — dosłownie, bez zmian.
      <a href="%(link)s" target="_blank" rel="noopener"
         style="color:var(--srebro-jasne)">Zobacz wszystkie 53 w Google</a>.
    </p>

    <div class="form-opinia" id="wystaw">
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
""" % {'opinie': karty_opinii(), 'link': LINK_GOOGLE} + blok_kontaktu(
        u'Przekonana? <span class="kursywa">Umów się</span>.',
        u'Najbliższy wolny termin ustalimy przez telefon w dwie minuty.'))


def strona_kontakt():
    return (
        naglowek_strony(u'Kontakt',
            u'Zadzwoń albo <span class="kursywa">napisz</span>.',
            u'Najprościej zadzwonić. Ale jeśli wolisz napisać — poniżej jest '
            u'formularz, który pyta dokładnie o to, czego potrzebuję, żeby '
            u'podać Ci cenę bez oglądania włosów na żywo.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="kontakt-siatka">
      <div>
        <ul class="dane">
          <li><span class="etykieta">Telefon</span>
            <a href="tel:%(tel_link)s" style="font-size:1.45rem">%(tel_pokaz)s</a>
            <span style="display:block; color:var(--srebro-ciemne); font-size:.86rem; margin-top:.5rem">
              Jeśli nie odbieram, jestem przy kimś w fotelu — oddzwonię.
            </span></li>
          <li><span class="etykieta">Adres</span>
            ul. Jana Kilińskiego 55/2<br>42-218 Częstochowa
            <span style="display:block; color:var(--srebro-ciemne); font-size:.86rem; margin-top:.5rem">
              Wejście od podwórza, parter. Parking przed budynkiem.
            </span></li>
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
        <iframe class="mapa" title="Mapa — ul. Jana Kilińskiego 55/2, Częstochowa" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q=Jana%%20Kili%%C5%%84skiego%%2055,%%2042-218%%20Cz%%C4%%99stochowa&output=embed"></iframe>
      </div>
    </div>
  </div>
</section>

<section class="ciemno" id="wycena">
  <div class="wrap">
    <p class="nadpis">Zapytanie o termin i cenę</p>
    <h2>Odpowiem <span class="kursywa">konkretną kwotą</span>.</h2>
    <p style="color:var(--srebro-jasne); max-width:56ch">
      Cena zależy od długości i grubości włosów — dlatego pytam o to od razu.
      Dzięki temu nie musisz przyjeżdżać na samą wycenę.
    </p>

    <form class="form-opinia" id="form-wycena" novalidate style="margin-top:2.6rem">
      <div class="pola">
        <div class="pola dwa">
          <div><label for="k-imie">Imię</label>
            <input type="text" id="k-imie" name="imie" autocomplete="given-name" required maxlength="60"></div>
          <div><label for="k-tel">Telefon</label>
            <input type="text" id="k-tel" name="telefon" autocomplete="tel" required maxlength="20"
              inputmode="tel" placeholder="żebym mogła oddzwonić"></div>
        </div>

        <div class="pola dwa">
          <div><label for="k-usluga">Co chcesz zrobić</label>
            <select id="k-usluga" name="usluga">
              <option>Koloryzacja</option>
              <option>Koloryzacja + strzyżenie + modelowanie</option>
              <option>Koloryzacja + modelowanie</option>
              <option>Samo strzyżenie</option>
              <option>Modelowanie / upięcie</option>
              <option>Pielęgnacja i regeneracja</option>
              <option selected>Jeszcze nie wiem — poradź mi</option>
            </select></div>
          <div><label for="k-dlugosc">Długość włosów</label>
            <select id="k-dlugosc" name="dlugosc">
              <option>Krótkie — nad uchem</option>
              <option selected>Do ramion</option>
              <option>Do łopatek</option>
              <option>Do pasa lub dłuższe</option>
            </select></div>
        </div>

        <div class="pola dwa">
          <div><label for="k-grubosc">Gęstość włosów</label>
            <select id="k-grubosc" name="grubosc">
              <option>Cienkie, mało gęste</option>
              <option selected>Przeciętne</option>
              <option>Gęste i grube</option>
            </select></div>
          <div><label for="k-termin">Kiedy najlepiej</label>
            <select id="k-termin" name="termin">
              <option selected>Jak najszybciej</option>
              <option>W tym tygodniu</option>
              <option>W przyszłym tygodniu</option>
              <option>Termin nie jest pilny</option>
            </select></div>
        </div>

        <div><label for="k-tresc">Coś jeszcze, o czym powinnam wiedzieć</label>
          <textarea id="k-tresc" name="tresc" maxlength="1200"
            placeholder="Np. włosy po rozjaśnianiu, farbowane henną, alergia, ważne wyjście za dwa tygodnie…"></textarea></div>

        <div class="zgoda">
          <input type="checkbox" id="k-zgoda" name="zgoda" required>
          <label for="k-zgoda">Zgadzam się na przetwarzanie podanych danych w celu odpowiedzi
            na to zgłoszenie. <span style="color:var(--srebro-ciemne)">*</span></label>
        </div>

        <div class="pulapka" aria-hidden="true">
          <label for="k-strona">Nie wypełniaj tego pola</label>
          <input type="text" id="k-strona" name="strona" tabindex="-1" autocomplete="off">
        </div>

        <div>
          <button class="btn btn-ciemny" type="submit" id="k-wyslij">Wyślij zapytanie</button>
          <p class="status" id="k-status" role="status" aria-live="polite"></p>
          <p style="color:var(--srebro-ciemne); font-size:.86rem; margin-top:1rem">
            Odpowiadam zwykle tego samego dnia. Zapytanie nie rezerwuje terminu —
            termin potwierdzam telefonicznie.
          </p>
        </div>
      </div>
    </form>
  </div>
</section>

<section id="pytania">
  <div class="waski">
    <p class="nadpis">Dobrze wiedzieć</p>
    <h2>Pytania, które <span class="kursywa">słyszę najczęściej</span>.</h2>
    <div class="pytania">
      <details><summary>Ile trwa koloryzacja?</summary>
        <p>Od dwóch do nawet pięciu godzin. Odrosty to zwykle dwie, rozjaśnianie
        ciemnych włosów albo korekta nieudanego koloru — znacznie dłużej.
        Dokładny czas podam przy umawianiu, żebyś mogła zaplanować dzień.</p></details>
      <details><summary>Czy muszę się umawiać?</summary>
        <p>Tak. Pracuję sama i przy jednej osobie na raz — bez umówienia
        najprawdopodobniej nie będę mogła Cię przyjąć. Zadzwoń nawet dzień wcześniej,
        czasem zwalniają się terminy.</p></details>
      <details><summary>Ile to kosztuje?</summary>
        <p>Zależy od długości i grubości włosów oraz od tego, co było na nich
        wcześniej. Dlatego nie ma tu cennika z sufitu — cenę podaję po rozmowie
        albo po wypełnieniu formularza wyżej. Zawsze <b>przed</b> zabiegiem.</p></details>
      <details><summary>Mam nieudaną koloryzację z innego miejsca. Naprawisz?</summary>
        <p>Najczęściej tak, ale rzadko za jednym razem. Przy mocno zniszczonych
        włosach rozpisuję plan na dwie–trzy wizyty, żeby nie dołożyć szkód.
        Powiem wprost, czego się nie da zrobić.</p></details>
      <details><summary>Jak przygotować włosy przed wizytą?</summary>
        <p>Przy koloryzacji nie myj ich w dniu wizyty — naturalna warstwa
        ochronna pomaga skórze głowy. Nie stylizuj mocno lakierem. Weź zdjęcia
        efektu, który Ci się podoba; łatwiej rozmawiać na konkretach.</p></details>
      <details><summary>Robisz konsultacje bez zabiegu?</summary>
        <p>Tak. Jeśli nie wiesz, czego chcesz, albo zastanawiasz się nad dużą
        zmianą — przyjdź porozmawiać. Konsultacja jest bezpłatna i do niczego
        nie zobowiązuje.</p></details>
    </div>
  </div>
</section>
""" % {'tel_link': TEL_LINK, 'tel_pokaz': TEL_POKAZ})


def strona_prywatnosc():
    return (
        naglowek_strony(u'Polityka prywatności',
            u'Krótko i <span class="kursywa">bez prawniczego bełkotu</span>.',
            u'Na tej stronie są dwa formularze. Poniżej piszę dokładnie, co się '
            u'dzieje z danymi, które w nich zostawisz.') +
u"""
<section style="padding-top:0">
  <div class="waski">
    <div class="pytania" style="margin-top:0; border-top:0">

      <details open><summary>Kto przetwarza dane</summary>
        <p>Administratorem danych podanych w formularzach jest <b>Agnieszka
        Lewandowska, prowadząca salon fryzjerski new age</b>, ul. Jana Kilińskiego 55/2,
        42-218 Częstochowa. W sprawach dotyczących danych najprościej zadzwonić:
        <a href="tel:%(tel_link)s" style="color:var(--biel)">%(tel_pokaz)s</a>.</p></details>

      <details><summary>Jakie dane i po co</summary>
        <p><b>Formularz zapytania o termin i cenę:</b> imię, telefon, rodzaj usługi,
        długość i gęstość włosów, preferowany termin oraz to, co sama dopiszesz.
        Wykorzystuję je wyłącznie po to, żeby oddzwonić i podać cenę.</p>
        <p><b>Formularz opinii:</b> imię, opcjonalnie adres e-mail, ocena i treść
        opinii. Wykorzystuję je, żeby przeczytać opinię i — jeśli wyrazisz na to
        zgodę — opublikować ją na stronie.</p>
        <p>Podstawą jest Twoja zgoda (art. 6 ust. 1 lit. a RODO). Podanie danych
        jest dobrowolne, ale bez telefonu nie oddzwonię.</p></details>

      <details><summary>Jak długo je trzymam</summary>
        <p>Dane z zapytania o wycenę — przez czas potrzebny do obsługi zgłoszenia
        i umówienia wizyty, nie dłużej niż <b>12 miesięcy</b> od ostatniego kontaktu.
        Opinie — dopóki są opublikowane na stronie albo dopóki nie poprosisz
        o ich usunięcie.</p></details>

      <details><summary>Komu je przekazuję</summary>
        <p>Nikomu poza dostawcami technicznymi, którzy obsługują stronę i formularze —
        firmie hostingowej oraz usłudze przyjmującej zgłoszenia. Nie sprzedaję danych,
        nie przekazuję ich do celów marketingowych i nie profiluję.</p></details>

      <details><summary>Twoje prawa</summary>
        <p>Masz prawo dostępu do swoich danych, ich sprostowania, usunięcia
        i ograniczenia przetwarzania, a także prawo wycofania zgody w dowolnym
        momencie — wystarczy jeden telefon albo wiadomość. Wycofanie zgody nie
        wpływa na to, co zdarzyło się wcześniej.</p>
        <p>Przysługuje Ci również skarga do Prezesa Urzędu Ochrony Danych Osobowych.</p></details>

      <details><summary>Ciasteczka i pamięć przeglądarki</summary>
        <p>Ta strona <b>nie używa ciasteczek reklamowych ani analitycznych</b>.
        Nie mierzę ruchu, nie profiluję i nie osadzam skryptów śledzących.
        W pamięci przeglądarki zapisuje się jedna informacja: że komunikat
        o ciasteczkach został zamknięty. Możesz ją usunąć w ustawieniach
        przeglądarki.</p>
        <p>Mapa dojazdu jest osadzona z Map Google — po jej wyświetleniu Google
        może zapisać własne pliki na Twoim urządzeniu, na zasadach opisanych
        w polityce prywatności Google.</p></details>

      <details><summary>Zdjęcia na stronie</summary>
        <p>Zdjęcia metamorfoz publikuję wyłącznie za pisemną zgodą osób, które
        są na nich widoczne. Jeśli rozpoznajesz siebie na którymkolwiek zdjęciu
        i nie życzysz sobie publikacji — napisz, zdejmę je tego samego dnia.</p></details>

    </div>
  </div>
</section>
""" % {'tel_link': TEL_LINK, 'tel_pokaz': TEL_POKAZ})


def strona_porady():
    kafle_porad = []
    for slug, tytul, lead, _slowa, _tresc in PORADY:
        kafle_porad.append(u"""
      <a class="porada-kafel" href="../porady/%s/">
        <h3>%s</h3>
        <p>%s</p>
        <span class="opinia-wiecej">Czytaj</span>
      </a>""" % (slug, tytul, lead))

    return (
        naglowek_strony(u'Poradnik',
            u'To, co i tak <span class="kursywa">mówię w fotelu</span>.',
            u'Pytania, które słyszę najczęściej — z odpowiedziami dłuższymi niż '
            u'te, na które starcza czasu przy myjce. Bez sprzedawania cudów.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="porady-siatka">""" + u''.join(kafle_porad) + u"""
    </div>
  </div>
</section>
""" + blok_kontaktu(
        u'Masz pytanie, <span class="kursywa">którego tu nie ma</span>?',
        u'Zadzwoń. Odpowiem, nawet jeśli miałoby się skończyć na tym, że nie '
        u'musisz nic robić.'))


def strona_porady_jedna(slug, tytul, lead, tresc):
    """Kazdy poradnik to osobny adres — ludzie trafiaja tu z wyszukiwarki
    na konkretne pytanie, nie na hub z listą."""
    inne = [(s, ty) for s, ty, _, _, _ in PORADY if s != slug][:3]
    dalej = u'\n      '.join(
        u'<a class="porada-maly" href="../%s/"><span>%s</span></a>' % (s, ty)
        for s, ty in inne)
    return (
        naglowek_strony(u'Poradnik', tytul, lead) +
u"""
<section style="padding-top:0">
  <div class="waski artykul">
%s
  </div>
</section>

<section class="ciemno">
  <div class="waski">
    <p class="nadpis">Przeczytaj też</p>
    <div class="porady-inne">
      %s
    </div>
  </div>
</section>
""" % (tresc, dalej) + blok_kontaktu(
        u'Wolisz zapytać <span class="kursywa">o swój przypadek</span>?',
        u'Każde włosy są inne. Zadzwoń i opisz swoje — powiem, co da się zrobić.'))


# ─────────────────────────────────────────────────────────────────
STRONY = [
    ('start', '', u'new age Lewandowska — fryzjerstwo, Częstochowa',
     u'Salon fryzjerski new age w Częstochowie. Koloryzacja, strzyżenie i modelowanie '
     u'u Agnieszki Lewandowskiej — edukatorki L’Oréal Professionnel.', strona_start, ''),
    ('o-mnie', 'o-mnie', u'O mnie — Agnieszka Lewandowska | new age',
     u'Dwadzieścia lat pracy, dyplomy Toni&Guy i Saks, cztery szkolenia '
     u'w Akademii L’Oréal Professionnel.', strona_o_mnie, '../'),
    ('uslugi', 'uslugi', u'Usługi — koloryzacja, strzyżenie, modelowanie | new age',
     u'Koloryzacja, strzyżenie, modelowanie i pielęgnacja w Częstochowie. '
     u'Cena ustalana po rozmowie, zawsze przed zabiegiem.', strona_uslugi, '../'),
    ('portfolio', 'portfolio', u'Portfolio — sesje i publikacje | new age Lewandowska',
     u'Stylizacje fryzur do magazynu SPLOT i sesji katalogowych — praca '
     u'Agnieszki Lewandowskiej, fryzjerki z Częstochowy. Sesje wizerunkowe i portfolio.', strona_portfolio, '../'),
    ('porady', 'porady', u'Poradnik — pielęgnacja i koloryzacja włosów | new age Częstochowa',
     u'Jak naprawić włosy po domowej koloryzacji, ile trzyma balayage, jak dbać '
     u'o blond. Praktyczne odpowiedzi od fryzjerki z Częstochowy.',
     strona_porady, '../'),
    ('opinie', 'opinie', u'Opinie klientek | new age Lewandowska',
     u'Ocena 5,0 z 53 opinii w Google. Co mówią klientki salonu new age '
     u'w Częstochowie o koloryzacji, strzyżeniu i doradztwie. Dodaj swoją opinię.', strona_opinie, '../'),
    ('prywatnosc', 'prywatnosc', u'Polityka prywatności | new age Lewandowska',
     u'Kto przetwarza dane z formularzy salonu new age w Częstochowie, '
     u'jak długo je przechowuje i jakie masz prawa.',
     strona_prywatnosc, '../'),
    ('kontakt', 'kontakt', u'Kontakt — Częstochowa, ul. Kilińskiego 55 | new age',
     u'Telefon, adres, godziny otwarcia i mapa dojazdu. Kilińskiego 55/2, Częstochowa.', strona_kontakt, '../'),
]


def schemat_pytan(html):
    """Wyszukiwarki potrafia pokazac pytania i odpowiedzi wprost w wynikach,
    ale tylko wtedy, gdy sa opisane w danych strukturalnych. Wyciagamy je
    z gotowego HTML-a, zeby nie trzymac tresci w dwoch miejscach."""
    import re, json
    pary = re.findall(
        r'<details[^>]*>\s*<summary>(.*?)</summary>\s*(.*?)</details>', html, re.S)
    if not pary:
        return u''
    pozycje = []
    for pytanie, odpowiedz in pary:
        p_czysto = re.sub(r'<[^>]+>', '', pytanie).strip()
        o_czysto = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', odpowiedz)).strip()
        if not p_czysto or len(o_czysto) < 20:
            continue
        pozycje.append({
            '@type': 'Question', 'name': p_czysto,
            'acceptedAnswer': {'@type': 'Answer', 'text': o_czysto}})
    if not pozycje:
        return u''
    dane = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': pozycje}
    return (u'\n<script type="application/ld+json">\n%s\n</script>\n'
            % json.dumps(dane, ensure_ascii=False, indent=1))


def mapa_strony(adresy):
    """sitemap.xml — lista wszystkich podstron dla wyszukiwarek."""
    wiersze = [u'<?xml version="1.0" encoding="UTF-8"?>',
               u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for sciezka, waga in adresy:
        wiersze.append(u'  <url><loc>%s%s</loc><priority>%s</priority></url>'
                       % (BAZA, (sciezka + '/' if sciezka else ''), waga))
    wiersze.append(u'</urlset>')
    return u'\n'.join(wiersze) + u'\n'


def nazwa_w_menu(klucz):
    for k, nazwa, _ in MENU:
        if k == klucz:
            return nazwa
    return {'prywatnosc': u'Polityka prywatności'}.get(klucz, u'')


def main():
    for klucz, katalog, tytul, opis, budowniczy, korzen in STRONY:
        sciezka = os.path.join(CEL, katalog) if katalog else CEL
        if not os.path.isdir(sciezka):
            os.makedirs(sciezka)
        html = zbuduj(klucz, tytul, opis, budowniczy(), korzen,
                      sciezka=katalog, nazwa=nazwa_w_menu(klucz))
        # Podstrony siegaja po zdjecia o poziom wyzej; strona glowna nie.
        if not korzen:
            html = html.replace('src="../img/', 'src="img/').replace('data-pelne="../img/', 'data-pelne="img/')
        # Pytania i odpowiedzi opisane dla wyszukiwarek
        pytania = schemat_pytan(html)
        if pytania:
            html = html.replace('</body>', pytania + '</body>', 1)
        with io.open(os.path.join(sciezka, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(html)
        print('  %-26s %6d znakow' % ((katalog or '/') + '/index.html', len(html)))
    # Kazdy poradnik jako osobny adres
    for slug, tytul, lead, slowa, tresc in PORADY:
        sciezka = os.path.join(CEL, 'porady', slug)
        if not os.path.isdir(sciezka):
            os.makedirs(sciezka)
        html = zbuduj('porady', u'%s | new age Lewandowska, Częstochowa' % tytul,
                      lead[:158], strona_porady_jedna(slug, tytul, lead, tresc),
                      '../../', sciezka='porady/' + slug, nazwa=tytul)
        pytania = schemat_pytan(html)
        if pytania:
            html = html.replace('</body>', pytania + '</body>', 1)
        with io.open(os.path.join(sciezka, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(html)
        print('  porady/%-18s %6d znakow' % (slug + '/', len(html)))

    # Mapa strony i wskazowki dla robotow
    wagi = {'': '1.0', 'uslugi': '0.9', 'kontakt': '0.9', 'o-mnie': '0.8',
            'portfolio': '0.7', 'opinie': '0.7', 'prywatnosc': '0.3'}
    with io.open(os.path.join(CEL, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        adresy = [(k, wagi.get(k, '0.5')) for _, k, _, _, _, _ in STRONY]
        adresy += [('porady/' + s, '0.6') for s, _, _, _, _ in PORADY]
        fh.write(mapa_strony(adresy))
    with io.open(os.path.join(CEL, 'robots.txt'), 'w', encoding='utf-8') as fh:
        fh.write(u'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BAZA)
    print('  sitemap.xml + robots.txt')
    print('\nGotowe: %d podstron' % len(STRONY))


if __name__ == '__main__':
    main()
