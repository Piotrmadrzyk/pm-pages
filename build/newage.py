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
    ('loreal',    u'L’Oréal',   'loreal/'),
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
     u'Brytyjska szkoła, przez którą przeszły pokolenia fryzjerów na całym '
     u'świecie — od lat sześćdziesiątych wyznacza to, co w strzyżeniu uchodzi '
     u'za dobrą robotę. Dyplom podpisany przez ich międzynarodowego dyrektora '
     u'artystycznego.'),
    ('2005-saks-london',    u'2005', u'Saks Academies',
     u'Brytyjska sieć akademii fryzjerskich działająca od 1974 roku, wtedy '
     u'prowadząca zajęcia także w Polsce. Dwa dni o tym, jak strzyżenie '
     u'i koloryzacja pracują ze sobą, a nie osobno.'),
    ('2009-uprawnienia',    u'2009', u'Kurs pedagogiczno-metodyczny',
     u'Razem z tytułem mistrza daje uprawnienia do nauki zawodu. Dzięki niemu '
     u'w salonie mogą uczyć się praktykanci — i dlatego rozmowa o włosach '
     u'z klientką też wychodzi prościej.'),
    ('2013-loreal-h3',      u'2013', u'L’Oréal H³',
     u'Heart, Hand, Head — międzynarodowe grono stylistów L’Oréal Professionnel. '
     u'Wejście do niego oznacza dostęp do szkoleń, na które nie każdy salon '
     u'może się zapisać.'),
    ('2018-loreal-blondy',  u'2018', u'L’Oréal — Blondy',
     u'Całe szkolenie poświęcone wyłącznie rozjaśnianiu. To najtrudniejsza '
     u'i najbardziej ryzykowna część koloryzacji — tu najłatwiej zniszczyć '
     u'włosy i najtrudniej naprawić błąd.'),
    ('2019-adam-reed',      u'2019', u'Cut &amp; Style — Adam Reed',
     u'Fryzjer brytyjskich gwiazd, ambasador L’Oréal Professionnel w Wielkiej '
     u'Brytanii, twórca fryzur na okładki i wybiegi. Certyfikat podpisał '
     u'osobiście — jego podpis widać na zdjęciu.'),
    ('2022-berni-ottjes',   u'2022', u'Master Class — Berni Ottjes',
     u'Holenderski kolorysta z tytułem International Global Artist L’Oréal. '
     u'Część warsztatowa: techniki koloryzacji ćwiczone na modelkach, '
     u'nie na slajdach.'),
    ('2023-min-kim',        u'2023', u'Master Class — Min Kim',
     u'Międzynarodowa artystka L’Oréal, jedna z najbardziej rozpoznawalnych '
     u'kolorystek na świecie. Teoria koloru — dlaczego pigment zachowuje się '
     u'tak, a nie inaczej, i co z tego wynika przy fotelu.'),
]

# Podpisy z konkretem — „Studio" nic nie mowi. Kazdy ma tytul i drugi
# wiersz z rzecza, ktora widz moze zabrac ze soba.
SESJA = [
    ('kadr-1743', u'Sesja wizerunkowa', u'nożyczki, którymi pracuję na co dzień'),
    ('kadr-1718', u'W salonie',         u'jedna osoba na raz, bez pośpiechu'),
    ('kadr-1727', u'Narzędzia',         u'szczotka, grzebień, nożyczki — reszta to wprawa'),
    ('kadr-1741', u'Warsztat',          u'wszystko, co potrzebne do jednej wizyty'),
]

# Cala ta sesja powstala do magazynu SPLOT nr 1 (2017), wydanie limitowane,
# temat numeru „Noszenie a Rodzicielstwo Bliskosci". Wczesniej polowa kadrow
# byla tu podpisana „sesja katalogowa" — to bylo nieprawdziwe.
# Fryzury: Agnieszka Lewandowska. Fotografia: Elzbieta Bednarek.
PORTFOLIO = [
    ('sesja-3506', u'Okładka SPLOT nr 1',      u'wydanie limitowane, 2017'),
    ('sesja-3509', u'Magazyn w druku',          u'temat numeru: noszenie a rodzicielstwo bliskości'),
    ('sesja-3508', u'Rozkładówka',              u'dwie strony z sesji'),
    ('sesja-3552', u'Strona z sesji',           u'stylizacja w plenerze miejskim'),
    ('sesja-3555', u'Rozkładówka',              u'dwie stylizacje obok siebie'),
    ('sesja-3553', u'Strona z sesji',           u'publikacja drukowana'),
    ('sesja-3554', u'Strona z sesji',           u'publikacja drukowana'),
    ('sesja-3501', u'Stylizacja lata dwudzieste', u'fale, opaska z piórem, wnętrza pałacowe'),
    ('sesja-3497', u'Stylizacja lata dwudzieste', u'ujęcie w plenerze'),
    ('sesja-3498', u'Stylizacja lata dwudzieste', u'kadr grupowy'),
    ('sesja-3499', u'Stylizacja lata dwudzieste', u'upięcie z falą wodną'),
    ('sesja-3500', u'Stylizacja lata dwudzieste', u'detal upięcia'),
    ('sesja-3503', u'Sesja do magazynu',        u'stylizacja dzienna'),
    ('sesja-3504', u'Sesja do magazynu',        u'warkocz boczny, ujęcie w ruchu'),
    ('sesja-3505', u'Sesja do magazynu',        u'ujęcie wnętrzarskie'),
    ('sesja-3507', u'Sesja do magazynu',        u'detal fryzury'),
]

def kafle(pozycje, katalog):
    """Podpis lezy NA zdjeciu, pod gradientem — tak jak w Lawendzie
    i Pergoli. Pod spodem drugi wiersz z konkretem. Przy najechaniu
    zdjecie delikatnie sie przybliza i pojawia sie lupa."""
    out = []
    for p in pozycje:
        if len(p) == 4:                       # dyplom: plik, rok, tytul, opis
            plik, rok, tytul, opis = p
            gorny, dolny = u'%s · %s' % (rok, tytul), opis
        elif len(p) == 3:                     # zdjecie: plik, tytul, podpis
            plik, gorny, dolny = p
        else:
            plik, gorny = p
            dolny = u''
        podpis = (u'%s — %s' % (gorny, dolny)) if dolny else gorny
        out.append(
            u'<figure class="kafel">\n'
            u'          <button type="button" class="powieksz" data-pelne="../img/%s/%s.jpg"'
            u' data-podpis="%s" aria-label="Powiększ: %s">\n'
            u'            <img src="../img/%s/%s-mal.jpg" alt="%s" loading="lazy" decoding="async">\n'
            u'            <span class="kafel-lupa" aria-hidden="true">'
            u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">'
            u'<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg></span>\n'
            u'            <figcaption><b>%s</b>%s</figcaption>\n'
            u'          </button>\n'
            u'        </figure>' % (
                katalog, plik, podpis.replace('"', '&quot;'), gorny.replace('"', '&quot;'),
                katalog, plik, podpis.replace('"', '&quot;'),
                gorny, (u'<span>%s</span>' % dolny) if dolny else u''))
    return u'\n        '.join(out)



# ─────────────────────────────────────────────────────────────────
#  OPINIE — PRZEPISANE Z PROFILU GOOGLE, DOSLOWNIE
#
#  ⚠️ Nie wolno tu wpisywac tresci wymyslonych. Falszywe opinie sa
#  w Polsce zakazana nieuczciwa praktyka rynkowa i odpowiada za nie
#  przedsiebiorca, czyli klientka.
#  Zrodlo: https://maps.app.goo.gl/jo2415Nfnjxt4YGC6 (5,0 z 53 opinii)
# ─────────────────────────────────────────────────────────────────
OPINIE = [
    (u'Aneta Orzeł', u'7 miesięcy temu',
     u'Ten salon polecam z całego serca. Każda wizyta u Pani Agnieszki to czysta '
     u'przyjemność. Zawsze wychodzę z salonu zadowolona i zrelaksowana, a włosy '
     u'zadbane i wypielęgnowane. Pani Agnieszka po prostu zna się na swojej robocie. '
     u'Czy to cięcie, modelowanie, koloryzacja lub inny zabieg na włosach — polecam '
     u'wizytę w tym salonie.'),
    (u'Klaudia Muś', u'6 miesięcy temu',
     u'Świetny salon fryzjerski! Już od kilku lat korzystam z usług Pani Agnieszki. '
     u'Można liczyć na profesjonalne doradztwo i ogromną dbałość o włosy podczas '
     u'koloryzacji. Efekt piękny, a włosy po zabiegu zdrowe i lśniące. Miła atmosfera '
     u'i pełen profesjonalizm. Zdecydowanie polecam!'),
    (u'Janina Nowowiejska', u'6 miesięcy temu',
     u'Do New Age Studio chodzę już od 25 lat i nie wyobrażam sobie zmiany tego '
     u'miejsca na inne. Za każdym razem czuję się tu naprawdę dopieszczona — '
     u'z pełną uwagą, spokojem i troską Pani Agnieszki.'),
    (u'Sabina Gruca', u'rok temu',
     u'Do Pani Agnieszki trafiłam ponad osiem lat temu, po nieudanej koloryzacji '
     u'w innym salonie. Pani Agnieszka zaopiekowała się moimi włosami i wyprowadziła '
     u'je z opresji.'),
    (u'Paulina Tryniszewska', u'rok temu',
     u'Pani Agnieszka zajmuje się moimi włosami już od kilku lat. Jej profesjonalne '
     u'podejście i ogromna wiedza są na najwyższym poziomie. Każdej kobiecie polecam '
     u'tę niesamowitą fryzjerkę. Zawsze czuję się zaopiekowana na każdym etapie wizyty.'),
    (u'Agata Morawski', u'rok temu',
     u'Do pani Agnieszki chodzę od dłuższego czasu i za każdym razem wychodzę '
     u'z salonu zachwycona. Ostatnio skorzystałam z botoksu na włosy — efekt '
     u'przerósł moje oczekiwania! Włosy są gładkie, miękkie, lśniące i wyglądają '
     u'na zdecydowanie zdrowsze.'),
    (u'Teresa Bajor', u'11 miesięcy temu',
     u'Z usług Pani Agnieszki korzystam od wielu lat i zawsze wychodzę zadowolona. '
     u'Włosy są uporządkowane, wypielęgnowane, wystylizowane, a ja czuję się '
     u'wyśmienicie.'),
    (u'Maria Różycka', u'11 miesięcy temu',
     u'Do Pani Agnieszki trafiłam dwa lata temu przez przypadek. Moja wieloletnia '
     u'fryzjerka wyjechała na stałe z Polski i szukałam nowego zakładu fryzjerskiego. '
     u'Ten, do którego trafiłam, nie spełnił moich oczekiwań.'),
]

LINK_GOOGLE = u'https://maps.app.goo.gl/jo2415Nfnjxt4YGC6'
LINK_IG = u'https://www.instagram.com/new_age_lewandowska'
LINK_FB = u'https://www.facebook.com/profile.php?id=100057636820418'


def karty_opinii(ile=None, odnosnik=None):
    """Szerokie karty w jednej kolumnie — imie, data, gwiazdki, tresc.
    Wczesniej byly trzy waskie kolumny z drobnym tekstem i wygladalo to zle."""
    lista = OPINIE if ile is None else OPINIE[:ile]
    out = []
    for autor, data, tresc in lista:
        out.append(
            u'<article class="opinia">\n'
            u'        <div class="opinia-glowa">\n'
            u'          <span class="opinia-kto">%s</span>\n'
            u'          <span class="opinia-data">%s</span>\n'
            u'        </div>\n'
            u'        <p class="gwiazdki" aria-label="Ocena: 5 na 5">★★★★★</p>\n'
            u'        <p class="opinia-tresc">%s</p>\n'
            u'      </article>' % (autor, data, tresc))
    return u'\n      '.join(out)


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
      <a class="btn btn-duch" href="%s" target="_blank" rel="noopener">Napisz na Instagramie</a>
    </div>
    <p class="zaproszenie-drobne">
      Rozmowa nic nie kosztuje i do niczego nie zobowiązuje.
      Cenę poznasz przed zabiegiem, nie po.
    </p>
    <div class="spolecznosci">
      <span>Najświeższe prace i wolne terminy wrzucam tutaj:</span>
      <a href="%s" target="_blank" rel="noopener">Instagram</a>
      <a href="%s" target="_blank" rel="noopener">Facebook</a>
    </div>
  </div>
</section>
""" % (naglowek, zdanie, TEL_LINK, TEL_POKAZ, LINK_IG, LINK_IG, LINK_FB)



# ─────────────────────────────────────────────────────────────────
#  L’ORÉAL PROFESSIONNEL
#
#  Agnieszka jest salonem wspolpracujacym z L’Oreal Professionnel —
#  ma pelna linie i dostaje nowosci od razu, a produkty sprzedaje
#  na miejscu. To realna przewaga, ktorej wczesniej na stronie
#  w ogole nie bylo widac.
#
#  ⚠️ Opisy mowia, DO CZEGO dana linia sluzy — to informacje
#  producenta. Nie obiecujemy efektow, ktorych nie da sie dotrzymac,
#  i nie podajemy cen (te ustala salon).
# ─────────────────────────────────────────────────────────────────
PRODUKTY = [
    (u'Metal Detox', u'Ochrona koloru i włosa przed metalami',
     u'W wodzie z kranu są metale — najwięcej wapnia i miedzi. Odkładają się '
     u'we włosie i to one najczęściej odpowiadają za to, że kolor po koloryzacji '
     u'wychodzi inaczej, niż powinien, a włos łamie się przy rozjaśnianiu.',
     u'Linia z cząsteczką Glicoamine neutralizuje te metale. W salonie robię '
     u'zabieg przed koloryzacją, w domu zostaje szampon, maska i olejek. '
     u'To jedna z niewielu rzeczy, które realnie zmieniają trwałość koloru — '
     u'zwłaszcza jeśli mieszkasz tam, gdzie woda jest twarda.',
     [u'Zabieg przed koloryzacją', u'Szampon, maska, olejek', u'Do domu i do salonu']),

    (u'Absolut Repair', u'Włosy zniszczone i przesuszone',
     u'Dla włosów po rozjaśnianiu, prostownicy albo latach domowego farbowania — '
     u'takich, które łamią się w połowie długości i puszą się mimo odżywki.',
     u'Odbudowuje włos od środka, nie tylko wygładza go z wierzchu. Efekt widać '
     u'po kilku myciach, nie po jednym — i tak to powinno działać. Kosmetyk, '
     u'który obiecuje regenerację po jednym użyciu, zwykle tylko oblepia włos.',
     [u'Włosy zniszczone', u'Odbudowa od środka', u'Efekt narastający']),

    (u'Vitamino Color', u'Farbowane włosy, które mają trzymać kolor',
     u'Najczęstsza przyczyna tego, że kolor blaknie po dwóch tygodniach, '
     u'to zwykły szampon z drogerii — jego detergenty wypłukują pigment '
     u'przy każdym myciu.',
     u'Ta linia ma łagodniejsze detergenty i filtr chroniący przed słońcem. '
     u'Nie sprawi, że kolor będzie trwał wiecznie, ale różnica między nią '
     u'a przypadkowym szamponem to zwykle kilka tygodni dłużej.',
     [u'Do włosów koloryzowanych', u'Ochrona pigmentu', u'Filtr UV']),

    (u'Blondifier', u'Blond bez żółtego odcienia',
     u'Po rozjaśnianiu naturalny żółty pigment zawsze wraca — to nie błąd '
     u'koloryzacji, tylko budowa włosa. Pytanie brzmi, jak długo da się '
     u'go trzymać w ryzach.',
     u'Linia do blondu: szampon fioletowy neutralizujący żółć, maska '
     u'odżywiająca rozjaśnione pasma. Uwaga na fiolet — raz, najwyżej dwa razy '
     u'w tygodniu. Codziennie daje szary, przesuszony efekt.',
     [u'Neutralizacja żółci', u'Do włosów rozjaśnianych', u'Maks. 2× w tygodniu']),

    (u'Scalp Advanced', u'Skóra głowy: przetłuszczanie, łupież, podrażnienia',
     u'Włosy zaczynają się w skórze, więc jeśli coś się dzieje u nasady, '
     u'nie naprawi tego kosmetyk na długość.',
     u'Osobne szampony do przetłuszczającej się skóry, do wrażliwej '
     u'i do łupieżu, plus serum na noc. Jeśli włosy tłuszczą się drugiego dnia, '
     u'to najczęściej ta linia, a nie mocniejszy szampon, rozwiązuje problem — '
     u'ostre detergenty tylko pogłębiają przetłuszczanie.',
     [u'Skóra przetłuszczająca się', u'Skóra wrażliwa', u'Łupież']),

    (u'Curl Expression', u'Włosy kręcone i falowane',
     u'Loki potrzebują innej pielęgnacji niż włosy proste: więcej nawilżenia, '
     u'mniej obciążania i produktów, które nie sklejają skrętu.',
     u'Szampon kremowy, odżywka do rozczesywania, żel i krem do stylizacji. '
     u'Przy kręconych włosach dobór produktu robi większą różnicę niż samo '
     u'strzyżenie — pokażę Ci, jak ich używać, żeby skręt się układał.',
     [u'Włosy kręcone', u'Nawilżenie', u'Stylizacja bez sklejania']),
]

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

 ('dobor-szamponu',
  u'Szampon to nie kosmetyk uniwersalny',
  u'Najczęstszy błąd w domowej pielęgnacji: jeden szampon dla całej rodziny, '
  u'kupowany dlatego, że ładnie pachnie.',
  u'jak dobrać szampon, szampon do włosów farbowanych, porowatość włosów',
  u"""
<p>
  Włosy różnią się od siebie bardziej, niż się wydaje. Cienkie i gęste to nie
  to samo. Przetłuszczające się u nasady, ale suche na końcach — to jeszcze
  co innego. Szampon dobrany do jednego typu na innym po prostu nie zadziała,
  a czasem zaszkodzi.
</p>
<h3>Trzy pytania, od których zaczynam</h3>
<p>
  <b>Jak szybko włosy się przetłuszczają?</b> Jeśli drugiego dnia — potrzebny
  jest szampon oczyszczający, ale łagodny; mocne detergenty podrażniają skórę,
  a ta w odpowiedzi produkuje jeszcze więcej sebum. Błędne koło.
</p>
<p>
  <b>Czy są farbowane?</b> Włosy koloryzowane mają uszkodzoną łuskę i szybciej
  tracą pigment. Szampon do włosów farbowanych ma delikatniejsze detergenty
  i mniej się nimi wypłukuje kolor.
</p>
<p>
  <b>Jaka jest porowatość?</b> To najważniejsze, a najrzadziej sprawdzane.
  Włos niskoporowaty ma ciasno przylegającą łuskę — ciężkie maski go obciążają
  i włosy wiszą jak sznurki. Wysokoporowaty ma łuskę otwartą — potrzebuje
  cięższych kosmetyków, bo lekkie nic nie dają.
</p>
<h3>Prosty test porowatości</h3>
<p>
  Wrzuć czysty, suchy włos do szklanki z wodą. Jeśli po kilku minutach pływa
  na powierzchni — niska porowatość. Jeśli powoli tonie — średnia. Jeśli
  opada od razu — wysoka. To nie jest badanie laboratoryjne, ale wystarcza,
  żeby przestać kupować na oślep.
</p>
<h3>Czego nie robić</h3>
<p>
  <b>Nie kupuj szamponu tylko dlatego, że ładnie pachnie.</b> Zapach nie ma
  nic wspólnego z tym, co produkt robi z włosem.
</p>
<p>
  <b>Nie używaj jednego szamponu przez lata bez zastanowienia.</b> Włosy się
  zmieniają — po ciąży, po zmianie koloru, po zimie, z wiekiem. To, co
  działało trzy lata temu, dziś może nie pasować.
</p>
<p>
  <b>Nie nakładaj szamponu na całą długość.</b> Myje się <b>skórę głowy</b>;
  długość i końcówki wystarczająco oczyści piana spływająca przy spłukiwaniu.
</p>
"""),

 ('odzywka-maska-olej',
  u'Odżywka, maska, olej — co, kiedy i po co',
  u'Trzy różne kosmetyki, trzy różne zadania. Najczęściej używa się ich '
  u'w złej kolejności albo wszystkich naraz.',
  u'odżywka czy maska, olejowanie włosów, pielęgnacja włosów w domu',
  u"""
<h3>Odżywka — po każdym myciu</h3>
<p>
  Jej zadanie jest proste: zamknąć łuskę włosa, którą otworzyło mycie.
  Dlatego nakłada się ją <b>zawsze po szamponie</b> i tylko na długość,
  nigdy na skórę głowy. Trzyma się dwie, trzy minuty — dłużej nic nie da,
  bo działa powierzchniowo.
</p>
<h3>Maska — raz, dwa razy w tygodniu</h3>
<p>
  Maska odżywia głębiej i zastępuje odżywkę, a nie jest jej dodatkiem.
  Nakładanie obu naraz to marnowanie produktu. Piętnaście minut wystarczy;
  trzymanie godziny nie daje lepszego efektu, tylko obciąża włos.
</p>
<p>
  Przy niskiej porowatości maski używaj rzadziej — co dziesięć dni, a nie
  co trzy dni. Przeciążone włosy wyglądają gorzej niż niedożywione.
</p>
<h3>Olej — na sam koniec albo przed myciem</h3>
<p>
  Olej nie odżywia — on <b>zabezpiecza</b>. Kropla na wilgotne końcówki
  po myciu zamyka je i ogranicza puszenie. Można też olejować przed myciem,
  żeby ochronić włos przed detergentem — wtedy zostawia się go na godzinę
  i zmywa szamponem.
</p>
<p>
  Najczęstszy błąd: za dużo. Na włosy do ramion wystarczy ilość wielkości
  ziarnka grochu, rozgrzana w dłoniach. Więcej znaczy tłuste, a nie
  nawilżone.
</p>
<h3>Kolejność, o którą pytacie najczęściej</h3>
<p>
  Szampon (skóra głowy) → maska <b>albo</b> odżywka (długość) → spłukanie
  chłodną wodą → olej lub serum na wilgotne końcówki → suszenie.
  Nic więcej nie jest potrzebne, a większość problemów bierze się
  z robienia więcej, nie mniej.
</p>
"""),

 ('wlosy-wypadaja',
  u'Włosy wypadają albo szybko się przetłuszczają',
  u'Dwie rzeczy, z którymi klientki przychodzą najczęściej — i o których '
  u'krąży najwięcej nieprawdziwych porad.',
  u'wypadanie włosów, przetłuszczające się włosy, zdrowa skóra głowy',
  u"""
<h3>Ile włosów dziennie to normalna liczba</h3>
<p>
  Od pięćdziesięciu do stu. To brzmi dużo, dopóki nie zobaczy się ich razem
  w odpływie. Włos ma swój cykl życia i wypadanie jest jego naturalną częścią.
</p>
<p>
  Niepokoić powinno co innego: <b>przerzedzenie widoczne w konkretnym
  miejscu</b>, wyraźnie szersza linia przedziałka albo nagła zmiana
  w ciągu kilku tygodni. To sygnał, żeby pójść do lekarza, nie do fryzjera —
  najczęstsze przyczyny to niedobory żelaza i ferrytyny, tarczyca albo
  silny stres sprzed dwóch, trzech miesięcy.
</p>
<h3>Czego fryzjer nie naprawi</h3>
<p>
  Żaden zabieg w salonie nie zatrzyma wypadania, którego przyczyna siedzi
  w organizmie. Mogę poprawić kondycję tego, co rośnie, dobrać strzyżenie,
  które doda objętości, i pokazać, jak nie osłabiać włosów dodatkowo —
  ale nie zastąpię badania krwi.
</p>
<p>
  Uczciwie: jeśli ktoś obiecuje, że jedna ampułka zatrzyma wypadanie,
  sprzedaje nadzieję, nie efekt.
</p>
<h3>Przetłuszczanie — zwykle sami je pogłębiamy</h3>
<p>
  <b>Za gorąca woda</b> pobudza gruczoły łojowe. Letnia wystarczy.
</p>
<p>
  <b>Zbyt mocne szampony</b> ogałacają skórę, która broni się produkcją
  większej ilości sebum. Efekt: włosy tłuste jeszcze szybciej.
</p>
<p>
  <b>Odżywka przy nasadzie</b> obciąża włos i skraca świeżość o pół dnia.
  Odżywka należy się długości, nie skórze.
</p>
<p>
  <b>Dotykanie włosów.</b> Ile razy dziennie poprawiasz je ręką? Każde
  dotknięcie to trochę sebum z palców.
</p>
<h3>Suchy szampon nie jest złem</h3>
<p>
  Ale jest doraźny. Używany codziennie zapycha ujścia mieszków włosowych
  i pogarsza to, co miał ratować. Raz na jakiś czas — w porządku; zamiast
  mycia przez tydzień — nie.
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
  "description": "Salon fryzjerski w Cz\u0119stochowie. Koloryzacja, strzy\u017cenie i modelowanie u Agnieszki Lewandowskiej \u2014 dwadzie\u015bcia lat do\u015bwiadczenia.",
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
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0",
    "reviewCount": "53", "bestRating": "5" },
  "review": %(opinie_dane)s,
  "hasOfferCatalog": {
    "@type": "OfferCatalog", "name": "Us\u0142ugi fryzjerskie",
    "itemListElement": [
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Koloryzacja w\u0142os\u00f3w \u2014 balayage, rozja\u015bnianie, refleksy"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Dekoloryzacja \u2014 usuwanie farby z w\u0142os\u00f3w"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Strzy\u017cenie damskie i m\u0119skie"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Modelowanie i upi\u0119cia okoliczno\u015bciowe"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Botoks na w\u0142osy, piel\u0119gnacja i regeneracja"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Trwa\u0142a ondulacja wodna i upi\u0119cia okoliczno\u015bciowe"}}
    ]
  },
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


def opinie_dla_wyszukiwarki():
    """Opinie opisane danymi strukturalnymi. To one sprawiaja, ze w wynikach
    Google przy stronie pojawiaja sie gwiazdki — a wynik z gwiazdkami jest
    klikany znacznie czesciej niz sam tytul."""
    import json
    poz = []
    for autor, data, tresc in OPINIE[:6]:
        poz.append({
            '@type': 'Review',
            'author': {'@type': 'Person', 'name': autor},
            'reviewRating': {'@type': 'Rating', 'ratingValue': '5', 'bestRating': '5'},
            'reviewBody': tresc,
        })
    return json.dumps(poz, ensure_ascii=False)


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
        'opinie_dane': opinie_dla_wyszukiwarki(),
    }


def naglowek_strony(nadpis, h1, lead):
    return (u'<section class="tytul-strony">\n  <div class="wrap">\n'
            u'    <p class="nadpis">%s</p>\n    <h1>%s</h1>\n    <p>%s</p>\n'
            u'  </div>\n</section>\n' % (nadpis, h1, lead))


# ─────────────────────────────────────────────────────────────────
#  TRESCI PODSTRON
# ─────────────────────────────────────────────────────────────────

def pas_przewijany():
    """Zdjecia jada same, w petli, zatrzymuja sie pod kursorem.
    Zestaw jest zdublowany — dzieki temu petla nie ma szwu."""
    kadry = [(k, t_, d) for k, t_, d in SESJA] + \
            [(p[0], p[1], p[2] if len(p) > 2 else u'') for p in PORTFOLIO[:8]]
    katalogi = ['sesja'] * len(SESJA) + ['portfolio'] * 8
    elementy = []
    for i, ((plik, tytul, dolny), kat) in enumerate(zip(kadry, katalogi)):
        podpis = (u'%s — %s' % (tytul, dolny)) if dolny else tytul
        elementy.append(
            u'<figure class="tasma-kadr">'
            u'<button type="button" class="powieksz" data-pelne="img/%s/%s.jpg"'
            u' data-podpis="%s" aria-label="Powiększ: %s">'
            u'<img src="img/%s/%s-mal.jpg" alt="%s" decoding="async">'
            u'<span class="kafel-lupa" aria-hidden="true">'
            u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">'
            u'<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg></span>'
            u'<figcaption><b>%s</b><span>%s</span></figcaption>'
            u'</button></figure>' % (
                kat, plik, podpis.replace('"', '&quot;'), tytul.replace('"', '&quot;'),
                kat, plik, podpis.replace('"', '&quot;'), tytul, dolny))
    jeden = u'\n        '.join(elementy)
    return (u'\n<section class="tasma-sekcja" aria-label="Prace i sesje">\n'
            u'  <div class="tasma" role="group">\n'
            u'    <div class="tasma-tor">\n        %s\n        %s\n    </div>\n'
            u'  </div>\n'
            u'  <p class="tasma-podpis">Zatrzymaj kursorem · '
            u'<a href="portfolio/">zobacz całe portfolio</a></p>\n'
            u'</section>\n' % (jeden, jeden))


def strona_start():
    czolowka = u"""
<section class="hero" style="padding-top:clamp(28px,4vw,56px)">
  <div class="wrap">
    <div class="hero-siatka">
      <div>
        <p class="nadpis">Fryzjerstwo · Częstochowa</p>
        <h1>Włosy,<br>które <em>rozumiem</em>.</h1>
        <p class="hero-lead">
          Agnieszka Lewandowska. Ponad dwadzieścia pięć lat przy fotelu, tytuł mistrza fryzjerstwa, dyplomy Toni&amp;Guy
          i Saks, cztery szkolenia w Akademii L'Oréal Professionnel — u artystów,
          którzy uczą fryzjerów na całym świecie.
        </p>
        <div class="hero-akcje">
          <a class="btn" href="tel:%(tel_link)s">Umów wizytę</a>
          <a class="btn btn-duch" href="o-mnie/">Poznaj mnie</a>
        </div>
        <a class="odznaka" href="opinie/">
          <b>5,0</b> <span class="odznaka-gw">★</span> · 53 opinie w Google
          <span class="odznaka-strzalka">→</span>
        </a>
        <p class="hero-drobne">
          <a href="opinie/#wystaw">Byłaś u mnie? Wystaw opinię</a> ·
          <a href="https://www.instagram.com/new_age_lewandowska" target="_blank" rel="noopener">Instagram</a> ·
          <a href="https://www.facebook.com/profile.php?id=100057636820418" target="_blank" rel="noopener">Facebook</a>
        </p>
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
        zajęcia także w Polsce. Od tamtej pory nie przestałam się uczyć.
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
    <h2>Ćwierć wieku, <span class="kursywa">dwadzieścia dyplomów</span>.</h2>
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
      <div class="usluga"><h3>Dekoloryzacja</h3><p>Wyjście z koloru, który już nie służy. Najbardziej wymagający zabieg — zawsze po konsultacji.</p></div>
      <div class="usluga"><h3>Strzyżenie</h3><p>Moja ulubiona część tej pracy. Damskie zawsze z myciem i modelowaniem.</p></div>
      <div class="usluga"><h3>Modelowanie</h3><p>Na co dzień i na okazje. Także nauka układania — żeby dało się to powtórzyć w domu.</p></div>
      <div class="usluga"><h3>Pielęgnacja i botoks</h3><p>Zabiegi dobrane do stanu włosów, nie do cennika. Czasem zamiast koloru potrzebna jest regeneracja.</p></div>
    </div>
    <a class="link-dalej" href="uslugi/">Pełna oferta i dlaczego nie ma cennika</a>
  </div>
</section>

<div class="pas">
  <img src="img/sesja/kadr-1727.jpg" alt="Praca w salonie new age w Częstochowie" loading="lazy">
  <div class="pas-tresc">
    <div class="wrap">
      <p class="nadpis" style="color:var(--srebro-jasne)">Od 2003 roku</p>
      <h2>Jedna osoba przy fotelu.<br><span class="kursywa">Bez pośpiechu.</span></h2>
    </div>
  </div>
</div>

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

<section class="ciemno" id="social">
  <div class="wrap">
    <div class="social-blok">
      <div>
        <p class="nadpis">Na bieżąco</p>
        <h2>Najnowsze prace <span class="kursywa">wrzucam tutaj</span>.</h2>
        <p style="color:var(--srebro-jasne); max-width:52ch">
          Metamorfozy, efekty koloryzacji i wolne terminy pojawiają się najpierw
          na Instagramie i Facebooku — strona nadąża później. Jeśli chcesz
          zobaczyć, co robię w tym tygodniu, zajrzyj tam.
        </p>
      </div>
      <div class="social-przyciski">
        <a class="social-btn" href="https://www.instagram.com/new_age_lewandowska" target="_blank" rel="noopener">
          <span class="social-nazwa">Instagram</span>
          <span class="social-uchwyt">@new_age_lewandowska</span>
        </a>
        <a class="social-btn" href="https://www.facebook.com/profile.php?id=100057636820418" target="_blank" rel="noopener">
          <span class="social-nazwa">Facebook</span>
          <span class="social-uchwyt">New Age Studio</span>
        </a>
      </div>
    </div>
  </div>
</section>

<section class="ciemno" style="padding-top:0">
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
    <div class="hero-akcje" style="margin-top:2.6rem">
      <a class="btn btn-ciemny" href="opinie/">Przeczytaj wszystkie opinie</a>
      <a class="btn btn-duch" href="opinie/#wystaw">Wystaw opinię</a>
    </div>
  </div>
</section>
""" % {'dyplomy': dyplomy_skrot, 'przerywnik': PRZERYWNIK,
      'opinie': karty_opinii(3, 'opinie/')}

    return czolowka + pas_przewijany() + reszta + blok_kontaktu(
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
        Moja droga w fryzjerstwie nie była prosta ani szybka — to lata pracy,
        nauki i cierpliwości. Przez ponad dwadzieścia pięć lat zdobywałam
        doświadczenie, obserwując, jak zmienia się ten zawód: nowe techniki,
        nowe trendy, nowe możliwości.
      </p>
      <p>
        Nigdy nie przestałam się uczyć. Ukończyłam liczne szkolenia, zdobyłam
        <b>tytuł mistrza fryzjerstwa</b> oraz kurs pedagogiczny. To one dają mi
        uprawnienia do <b>nauki zawodu</b> — od lat przyjmuję u siebie
        praktykantów i uczę ich fryzjerstwa od podstaw.
      </p>
      <p>
        Od niemal osiemnastu lat prowadzę <b>New Age Lewandowska</b>
        w Częstochowie — miejsce, które współtworzę z pasją i dbałością
        o każdy detal.
      </p>
      <p>
        Na tym nie poprzestaję. <b>Od 2025 roku studiuję pedagogikę
        — terapię pedagogiczną</b>, żeby móc uczyć zawodu także w szkołach.
        Po dwudziestu pięciu latach przy fotelu wciąż jestem po stronie
        uczących się, nie tylko uczących.
      </p>
      <p>
        Pracuję na profesjonalnych kosmetykach L'Oréal Professionnel, a moją
        ulubioną częścią pracy wciąż pozostaje <b>strzyżenie</b>. To tu
        najbardziej czuję, że mogę dopracować każdy szczegół.
      </p>
    </div>
    <img src="../img/sesja/kadr-1743.jpg" alt="Agnieszka Lewandowska, mistrzyni fryzjerstwa" width="733" height="1100" loading="lazy" class="wejscie">
  </div>
</section>

<section class="ciemno" id="liczby">
  <div class="wrap">
    <div class="liczby">
      <div class="liczba"><b>25+</b><span>lat w zawodzie</span></div>
      <div class="liczba"><b>18</b><span>lat własnego salonu</span></div>
      <div class="liczba"><b>20</b><span>dyplomów i certyfikatów</span></div>
      <div class="liczba"><b>5,0</b><span>ocena z 53 opinii Google</span></div>
      <div class="liczba"><b>2025</b><span>studia pedagogiczne w toku</span></div>
    </div>
  </div>
</section>

<div class="mysl ciemno">
  <blockquote>Ćwierć wieku. Osiemnaście lat własnego salonu. Zero zgadywania.</blockquote>
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
          dwóch albo trzech wizyt, zamiast obiecywać go od ręki.
        </p>
        <p>
          Pracuję na L'Oréal Professionnel <b>od 2002 roku</b>. Dwadzieścia parę lat
          na jednej linii produktów to nie przywiązanie — to wiedza, jak każdy z nich
          zachowa się na konkretnych włosach.
        </p>
        <ul class="u-fakty">
          <li>Odrosty — ok. 2 godz.</li><li>Balayage — 3–5 godz.</li>
          <li>Refleksy i pasemka</li><li>Tonowanie i korekta koloru</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1741.jpg" alt="Dekoloryzacja" loading="lazy"></div>
      <div>
        <span class="u-numer">02 — Dekoloryzacja</span>
        <h3>Wyjście z koloru, który już Ci nie służy</h3>
        <p>
          Dekoloryzacja to usunięcie sztucznego barwnika z włosa — nie to samo co
          rozjaśnianie. Rozjaśnianie działa na naturalny pigment; dekoloryzacja
          zdejmuje farbę, która została po wcześniejszych koloryzacjach.
          Potrzebna wtedy, gdy chcesz zejść o kilka tonów niżej, wyjść z ciemnej
          bazy albo naprawić kolor położony gdzie indziej.
        </p>
        <p>
          To najbardziej wymagający zabieg w całej koloryzacji i nie zawsze da się
          go zrobić za jednym razem. Farba schodzi warstwami i po drodze pojawiają
          się podtony — pomarańczowy, czerwony, żółty — które trzeba wyciszyć.
          Przy mocno przefarbowanych włosach rozpisuję plan na dwie lub trzy wizyty,
          żeby nie dołożyć szkód.
        </p>
        <p>
          <b>Zawsze powiem uczciwie, czego się nie da.</b> Jeśli włosy tego nie
          wytrzymają, usłyszysz to ode mnie przed zabiegiem, a nie po.
        </p>
        <ul class="u-fakty">
          <li>Zawsze po konsultacji</li><li>Często rozłożona na kilka wizyt</li>
          <li>Łączona z regeneracją</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1743.jpg" alt="Strzyżenie" loading="lazy"></div>
      <div>
        <span class="u-numer">03 — Strzyżenie</span>
        <h3>Moja ulubiona część tej pracy</h3>
        <p>
          Tu najbardziej czuję, że mogę dopracować każdy szczegół. Najładniejsze
          cięcie jest jednak do niczego, jeśli wymaga czterdziestu minut i trzech
          urządzeń — dlatego pytam, ile czasu naprawdę masz rano i czego używasz.
        </p>
        <p>
          Strzyżenie damskie zawsze w komplecie z myciem i modelowaniem.
          Jeśli przyniesiesz zdjęcie, powiem uczciwie, czy na Twoich włosach
          to zadziała. Czasem odradzę i zaproponuję coś innego.
        </p>
        <ul class="u-fakty">
          <li>Damskie z myciem i modelowaniem</li><li>Męskie</li>
          <li>Duża zmiana — konsultacja przed</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1718.jpg" alt="Modelowanie i upięcia" loading="lazy"></div>
      <div>
        <span class="u-numer">04 — Modelowanie i upięcia</span>
        <h3>Na wesele, na sesję i na zwykły wtorek</h3>
        <p>
          Modelowanie, fale, objętość, trwała ondulacja wodna. Przy okazji pokazuję,
          jak to powtórzyć w domu — który produkt, w którym momencie, w którą stronę
          prowadzić szczotkę. To zwykle robi większą różnicę niż samo cięcie.
        </p>
        <p>
          Upięcia okolicznościowe robię po wcześniejszej próbie, jeśli okazja jest
          ważna. Mam też za sobą stylizacje do publikacji w magazynie.
        </p>
        <ul class="u-fakty">
          <li>Modelowanie — 30–45 min</li><li>Upięcie — od 1 godz.</li>
          <li>Trwała ondulacja wodna</li><li>Próba przed ślubem</li>
        </ul>
      </div>
    </article>

    <article class="usluga-duza">
      <div class="u-foto"><img src="../img/sesja/kadr-1727.jpg" alt="Pielęgnacja i botoks" loading="lazy"></div>
      <div>
        <span class="u-numer">05 — Pielęgnacja i botoks na włosy</span>
        <h3>Czasem zamiast koloru potrzebna jest przerwa</h3>
        <p>
          Zdarza się, że przychodzisz po koloryzację, a ja proponuję najpierw
          regenerację. Nie dlatego, że tak wygodniej — tylko dlatego, że na
          przesuszonych włosach kolor i tak się nie utrzyma.
        </p>
        <p>
          <b>Botoks na włosy</b> wygładza i wypełnia włos od środka: efekt to
          miękkość, połysk i mniej puszenia. Nie prostuje na stałe i nie zastępuje
          pielęgnacji domowej — dobieram go do stanu włosów, nie do cennika.
        </p>
        <ul class="u-fakty">
          <li>Botoks — 30–60 min</li><li>Regeneracja i odbudowa</li>
          <li>Dobór pielęgnacji domowej</li>
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
            u'Fryzury do <span class="kursywa">magazynu</span>.',
            u'Cała ta sesja powstała do pierwszego numeru kwartalnika SPLOT. '
            u'Włosy przy każdym z tych zdjęć to moja robota.') +
u"""
<section style="padding-top:0">
  <div class="wrap">
    <div class="magazyn">
      <div class="magazyn-foto">
        <button type="button" class="powieksz" data-pelne="../img/portfolio/sesja-3506.jpg"
          data-podpis="Okładka SPLOT nr 1 — wydanie limitowane, 2017" aria-label="Powiększ okładkę magazynu">
          <img src="../img/portfolio/sesja-3506-mal.jpg"
               alt="Okładka magazynu SPLOT nr 1 — Noszenie a Rodzicielstwo Bliskości" loading="eager">
          <span class="kafel-lupa" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
              <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg>
          </span>
        </button>
      </div>
      <div class="magazyn-tresc">
        <p class="nadpis">Publikacja</p>
        <h2>SPLOT nr 1</h2>
        <p>
          Ogólnoświatowy kwartalnik bliskości, wydanie limitowane. Temat numeru:
          <b>noszenie a rodzicielstwo bliskości</b>. Fryzury do całej sesji
          — okładka i wnętrze numeru — robiłam ja.
        </p>
        <p>
          Zdjęcia powstały w dwóch odsłonach: stylizacje w klimacie lat
          dwudziestych w pałacowych wnętrzach oraz sesja miejska.
        </p>
        <ul class="u-fakty">
          <li>Fryzury — Agnieszka Lewandowska</li>
          <li>Fotografia — Elżbieta Bednarek</li>
          <li>Rok 2017</li>
        </ul>
      </div>
    </div>
  </div>
</section>
""" + PRZERYWNIK + u"""
<section style="padding-top:0">
  <div class="wrap">
    <p class="nadpis">Kadry z sesji</p>
    <h2>Cały numer, strona po stronie</h2>
    <p class="wyjasnienie">
      <b>Wszystkie zdjęcia poniżej pochodzą z jednej sesji</b> — tej,
      która ukazała się w pierwszym numerze kwartalnika <b>SPLOT</b>
      (wydanie limitowane, 2017). Fryzury do całego numeru, od okładki
      po ostatnią rozkładówkę, robiłam ja.
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
    <h2>Ja i moje narzędzia</h2>
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
    <div class="google-pasek">
      <div>
        <span class="google-ocena"><b>5,0</b> ★★★★★</span>
        <span class="google-ile">53 opinie w Google</span>
      </div>
      <a class="btn btn-ciemny" href="%(link)s" target="_blank" rel="noopener">
        Zobacz wszystkie w Google
      </a>
    </div>
    <p style="color:var(--srebro-ciemne); font-size:.86rem; margin-top:1.2rem">
      Opinie powyżej są przepisane z profilu Google dosłownie, bez zmian.
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
              <option>Dekoloryzacja — wyjście z koloru</option>
              <option>Koloryzacja + strzyżenie + modelowanie</option>
              <option>Koloryzacja + modelowanie</option>
              <option>Samo strzyżenie</option>
              <option>Modelowanie / upięcie</option>
              <option>Botoks na włosy</option>
              <option>Trwała ondulacja wodna</option>
              <option>Upięcie okolicznościowe</option>
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


def strona_loreal():
    karty = []
    for nazwa, dla_kogo, problem, rozwiazanie, znaczniki in PRODUKTY:
        chipy = u''.join(u'<li>%s</li>' % z for z in znaczniki)
        karty.append(u"""
      <article class="produkt">
        <div class="produkt-glowa">
          <h3>%s</h3>
          <p class="produkt-dla">%s</p>
        </div>
        <p class="produkt-problem">%s</p>
        <p class="produkt-opis">%s</p>
        <ul class="u-fakty">%s</ul>
      </article>""" % (nazwa, dla_kogo, problem, rozwiazanie, chipy))

    return (
        naglowek_strony(u'L’Oréal Professionnel',
            u'Czym pracuję <span class="kursywa">i dlaczego akurat tym</span>.',
            u'Jestem salonem współpracującym z L’Oréal Professionnel. Mam pełną '
            u'linię i nowości trafiają do mnie od razu — poniżej tłumaczę '
            u'po ludzku, do czego która jest.') +
u"""
<section style="padding-top:0">
  <div class="wrap dwie odwrot">
    <div class="tresc">
      <p>
        Na L’Oréal Professionnel pracuję <b>od 2002 roku</b>. Dwadzieścia parę
        lat na jednej linii to nie przywiązanie do marki — to wiedza, jak każdy
        produkt zachowa się na konkretnych włosach. Wiem, co zadziała na włosach
        po hennie, a co je zniszczy.
      </p>
      <p>
        Jako salon współpracujący mam dostęp do pełnej gamy, także do rzeczy,
        które dopiero wchodzą na rynek. W praktyce znaczy to tyle, że nie muszę
        proponować Ci tego, co akurat mam — proponuję to, co pasuje.
      </p>
      <p class="uwaga-sklep">
        <b>To nie jest sklep.</b> Niczego tu nie sprzedaję i nie ma tu cen.
        Opisuję te produkty po to, żebyś wiedziała, co w ogóle istnieje i czemu
        służy. Jeśli któryś Cię zainteresuje — zapytaj przy wizycie, dobiorę
        do Twoich włosów albo powiem wprost, że nie jest Ci potrzebny.
      </p>
    </div>
    <img src="../img/sesja/kadr-1727.jpg" alt="Kosmetyki L’Oréal Professionnel w salonie new age" loading="lazy">
  </div>
</section>

<section class="ciemno">
  <div class="wrap">
    <p class="nadpis">Linie, które mam u siebie</p>
    <h2>Do czego która służy</h2>
    <p style="color:var(--srebro-jasne); max-width:58ch">
      Bez marketingowego języka. Przy każdej piszę, jaki problem rozwiązuje
      i czego się po niej <b style="color:var(--biel)">nie</b> spodziewać.
    </p>
    <div class="produkty">""" + u''.join(karty) + u"""
    </div>
  </div>
</section>

<section id="jak-dobrac">
  <div class="waski">
    <p class="nadpis">Zanim kupisz cokolwiek</p>
    <h2>Trzy rzeczy, które warto wiedzieć</h2>
    <div class="pytania">
      <details open><summary>Dobry kosmetyk nie działa po jednym użyciu</summary>
        <p>Produkt, który obiecuje regenerację po pierwszym myciu, zwykle po prostu
        oblepia włos silikonem — wygląda dobrze przez dzień i wraca do punktu wyjścia.
        Prawdziwa odbudowa jest stopniowa i widać ją po kilku tygodniach.</p></details>
      <details><summary>Więcej nie znaczy lepiej</summary>
        <p>Maska trzymana godzinę zamiast piętnastu minut nie odżywi bardziej — obciąży.
        Fioletowy szampon codziennie zamiast raz w tygodniu daje szary, przesuszony
        efekt. Większość problemów w domowej pielęgnacji bierze się z robienia
        za dużo, nie za mało.</p></details>
      <details><summary>Nie każdy potrzebuje wszystkiego</summary>
        <p>Nie sprzedam Ci pięciu produktów, jeśli wystarczą dwa. Przy większości
        włosów dobrze dobrany szampon i jedna maska robią więcej niż cała półka
        kosmetyków kupionych na wyczucie. <a href="../porady/dobor-szamponu/"
        style="color:var(--biel)">Jak dobrać szampon — osobny tekst w poradniku</a>.</p></details>
    </div>
  </div>
</section>
""" + blok_kontaktu(
        u'Nie wiesz, czego <span class="kursywa">potrzebują Twoje włosy</span>?',
        u'Przyjdź na bezpłatną konsultację. Obejrzę włosy i powiem, co ma sens — '
        u'także wtedy, gdy odpowiedź brzmi „nic nie kupuj”.'))


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
    ('start', '', u'Fryzjer Częstochowa — koloryzacja i strzyżenie | new age Lewandowska',
     u'Salon fryzjerski new age w Częstochowie. Koloryzacja, strzyżenie i modelowanie '
     u'u Agnieszki Lewandowskiej — z dwudziestoletnim doświadczeniem.', strona_start, ''),
    ('o-mnie', 'o-mnie', u'Agnieszka Lewandowska — mistrzyni fryzjerstwa, Częstochowa',
     u'Ponad 25 lat pracy, tytuł mistrza fryzjerstwa, dyplomy Toni&Guy i Saks, '
     u'w Akademii L’Oréal Professionnel.', strona_o_mnie, '../'),
    ('uslugi', 'uslugi', u'Koloryzacja i strzyżenie Częstochowa — cennik po rozmowie | new age',
     u'Koloryzacja, strzyżenie, modelowanie i pielęgnacja w Częstochowie. '
     u'Cena ustalana po rozmowie, zawsze przed zabiegiem.', strona_uslugi, '../'),
    ('loreal', 'loreal', u'Kosmetyki L’Oréal Professionnel — salon współpracujący | Częstochowa',
     u'Metal Detox, Absolut Repair, Vitamino Color, Blondifier i inne linie '
     u'L’Oréal Professionnel — do czego która służy, wytłumaczone prostym językiem.',
     strona_loreal, '../'),
    ('portfolio', 'portfolio', u'Portfolio fryzjerskie — sesje i publikacje | new age Częstochowa',
     u'Fryzury do pierwszego numeru kwartalnika SPLOT — okładka i cała sesja. '
     u'Praca Agnieszki Lewandowskiej, mistrzyni fryzjerstwa z Częstochowy.', strona_portfolio, '../'),
    ('porady', 'porady', u'Poradnik — pielęgnacja i koloryzacja włosów | new age Częstochowa',
     u'Jak naprawić włosy po domowej koloryzacji, ile trzyma balayage, jak dbać '
     u'o blond. Praktyczne odpowiedzi od fryzjerki z Częstochowy.',
     strona_porady, '../'),
    ('opinie', 'opinie', u'Opinie o salonie — fryzjer Częstochowa, ocena 5,0 | new age Lewandowska',
     u'Ocena 5,0 z 53 opinii w Google. Co mówią klientki salonu new age '
     u'w Częstochowie o koloryzacji, strzyżeniu i doradztwie. Dodaj swoją opinię.', strona_opinie, '../'),
    ('prywatnosc', 'prywatnosc', u'Polityka prywatności | new age Lewandowska, Częstochowa',
     u'Kto przetwarza dane z formularzy salonu new age w Częstochowie, '
     u'jak długo je przechowuje i jakie masz prawa.',
     strona_prywatnosc, '../'),
    ('kontakt', 'kontakt', u'Kontakt i wycena — fryzjer Częstochowa, Kilińskiego 55/2 | new age',
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
            'loreal': '0.8', 'portfolio': '0.7', 'opinie': '0.7', 'prywatnosc': '0.3'}
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
