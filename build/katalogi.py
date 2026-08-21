#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Katalogi funkcji dla stron demonstracyjnych.

Jeden mechanizm (assets/katalog.css + assets/katalog.js), cztery pliki treści.
Zmiana mechanizmu = zmiana w assets. Zmiana treści = zmiana tutaj.

Uruchomienie:  cd build && python3 katalogi.py
Wynik:         p/katalog-<demo>.html

Każda pozycja to krotka:
    (skrot, tytul, opis, jak_to_dziala, podglad)

    skrot        — krótki identyfikator, np. 'rezerwacja'
    tytul        — nagłówek slajdu, po ludzku
    opis         — 2–3 zdania: co klient z tego ma
    jak_to_dziala— jedno zdanie techniczne, ale bez żargonu
    podglad      — adres podstrony demo z kotwicą albo None
"""
import io, os, re, html

KAT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(KAT, '..', 'p'))

# ══════════════════════════════════════════════════════════════════════════
#  TREŚĆ
# ══════════════════════════════════════════════════════════════════════════

# Pozycje, które pasują do każdej branży — różnią się tylko przykładem.
# Kolejność ustawiam osobno per demo, bo dla każdego co innego jest ważne.
WSPOLNE_DODATKI = {
    'platnosc': ('Prawdziwa płatność online',
        'Klient płaci od razu — kartą, BLIK-iem albo przelewem — zamiast umawiać się, że zapłaci na miejscu. Zaliczka odsiewa tych, którzy i tak by nie przyszli.',
        'Podpinamy operatora płatności; pieniądze idą prosto na Twoje konto, my nie mamy do nich dostępu.'),
    'voicebot': ('Voicebot telefoniczny',
        'Telefon odebrany także wtedy, gdy pracujesz. Bot podaje godziny, ceny i wolne terminy, a sprawy trudniejsze przekazuje Tobie z gotowym streszczeniem.',
        'Numer przekierowany na asystenta, który rozmawia głosem i zapisuje ustalenia.'),
    'messenger': ('Bot na Messengerze i WhatsAppie',
        'Ten sam asystent, który jest na stronie, odpowiada też tam, gdzie ludzie faktycznie piszą — a piszą wieczorem i w weekend.',
        'Jedna wiedza, trzy kanały. Zmieniasz raz, zmienia się wszędzie.'),
    'social': ('Generator postów na social media',
        'Post na Facebooka i Instagrama z tego, co już masz na stronie — bez wymyślania od zera i bez wynajmowania agencji.',
        'Bierze zdjęcia i teksty ze strony, proponuje kilka wersji, Ty wybierasz i publikujesz.'),
    'opinie_ai': ('Opinie z automatyczną odpowiedzią',
        'Każda nowa opinia w Google dostaje odpowiedź tego samego dnia — także ta niedobra, spokojnym tonem. Odpowiadanie na opinie realnie podnosi pozycję w wyszukiwarce.',
        'Propozycja odpowiedzi trafia do Ciebie do zatwierdzenia — nic nie publikuje się bez Ciebie.'),
    'statystyki': ('Statystyki bez ciasteczek',
        'Widzisz, ile osób weszło, skąd i co oglądały — bez śledzenia ludzi i bez wyskakującego okienka o zgodach.',
        'Licznik po stronie serwera, nie w przeglądarce gościa. Zgodne z RODO bez dodatkowych formalności.'),
    'blog': ('Blog i aktualności',
        'Miejsce na to, co u Ciebie nowego — a przy okazji jedyny sposób, żeby strona z czasem sama zaczęła przyciągać ludzi z Google.',
        'Piszesz zwykły tekst, strona sama robi z niego podstronę i dopisuje ją do listy.'),
    'jezyki': ('Kolejna wersja językowa',
        'Pełne tłumaczenie, nie automat z wtyczki — z własnymi tekstami, które brzmią naturalnie.',
        'Osobne podstrony pod adresem /en/, przełącznik w menu, Google indeksuje obie wersje osobno.'),
    'wcag': ('Tryb wysokiego kontrastu i audyt dostępności',
        'Strona czytelna także dla osób słabowidzących i obsługiwana z klawiatury. Coraz częściej to wymóg, nie uprzejmość.',
        'Pełny przegląd według standardu WCAG plus przełącznik kontrastu w rogu ekranu.'),
    'panel': ('Panel do samodzielnej edycji treści',
        'Zmiana ceny, godzin czy opisu bez dzwonienia do kogokolwiek — z telefonu, w minutę.',
        'Prosty ekran do logowania, tylko te pola, które faktycznie zmieniasz.'),
    'aplikacja': ('Aplikacja bez sklepu z aplikacjami',
        'Klient dodaje stronę do ekranu telefonu i otwiera ją jak aplikację — pełny ekran, własna ikona, działa też bez zasięgu.',
        'Ta sama strona, dodatkowy plik konfiguracyjny. Bez opłat dla Apple i Google, bez czekania na zatwierdzenie.'),
    'wideo': ('Krótkie wideo na stronie',
        'Piętnaście sekund tego, jak naprawdę u Ciebie jest, robi więcej niż akapit tekstu. Ludzie kupują od ludzi, których zobaczyli.',
        'Materiał wgrany na stronę, odtwarzany bez logo obcego serwisu i bez reklam.'),
}


DEMA = {

# ─────────────────────────────────────────────────────────────────────────
'lawenda': dict(
    nazwa='Studio Lawenda',
    branza='salon kosmetyczny',
    baza='demo-studio-lawenda',
    lede='Salon kosmetyczny prowadzony przez trzy specjalistki. Strona ma zapełniać kalendarz i odpowiadać na pytania, zanim ktoś zdąży zadzwonić.',
    dziala=[
        ('rezerwacja', 'Rezerwacja terminu prosto ze strony',
         'Klientka wybiera zabieg, specjalistkę i termin — bez telefonu, o dowolnej porze. Najwięcej rezerwacji spływa wieczorem, kiedy salon jest zamknięty.',
         'Formularz prowadzi krok po kroku i pilnuje, żeby nie dało się wysłać zgłoszenia bez numeru telefonu.',
         'index.html#rezerwacja'),
        ('asystent', 'Asystent, który zna ofertę i ceny',
         'Odpowiada na „ile kosztuje laminacja", „czy robicie ślubny makijaż", „do której jesteście otwarci" — o drugiej w nocy, natychmiast, bez czekania na odpisanie.',
         'Zna treść strony i cennik. Sprawy wykraczające poza to przekazuje do kontaktu z Wami.',
         'index.html'),
        ('zespol', 'Wiesz, kto Cię przyjmie',
         'Trzy specjalistki z imienia, zdjęciem i zakresem zabiegów. Klientka wybiera osobę, nie anonimowy fotel — a raz wybrana osoba wraca.',
         'Osobna podstrona zespołu i kotwice do konkretnej osoby z poziomu cennika.',
         'demo-studio-lawenda-zespol/index.html'),
        ('cennik', 'Ceny bez gwiazdek',
         'Pełny cennik na stronie, bez „cena od" i bez „zapytaj o wycenę". Ukryta cena nie chroni przed konkurencją — odstrasza klientki.',
         'Cennik w jednym miejscu, ten sam na wszystkich podstronach.',
         'demo-studio-lawenda-zabiegi/index.html'),
        ('zabiegi', 'Sześć zakresów, każdy opisany osobno',
         'Twarz, rzęsy, brwi, paznokcie, makijaż, masaż — każdy z opisem, czasem trwania i ceną. Klientka wie, co kupuje, zanim przyjdzie.',
         'Osobna podstrona z kotwicą do każdego zakresu — można wysłać link prosto do jednej usługi.',
         'demo-studio-lawenda-zabiegi/index.html#rzesy'),
        ('bezpieczenstwo', 'Sterylizacja, którą widać',
         'Osobna sekcja o higienie i sprzęcie. Dla części klientek to jest ten jeden argument, który przeważa przy wyborze salonu.',
         'Sekcja wyróżniona graficznie, żeby nie zginęła między zabiegami.',
         'index.html#bezpieczenstwo'),
        ('jedna_klientka', 'Jedna klientka w danym czasie',
         'Zasada napisana wprost na stronie. Kto szuka spokoju zamiast salonu-fabryki, zostaje na tej stronie dłużej.',
         'Wyróżniona sekcja z zasadami obowiązującymi w salonie.',
         'index.html#studio'),
        ('opinie', 'Opinie klientek z imienia',
         'Prawdziwe wypowiedzi zamiast pięciu gwiazdek bez treści. Konkretna opinia o konkretnym zabiegu przekonuje, ogólna pochwała nie.',
         'Sekcja opinii na stronie głównej, na trasie do przycisku rezerwacji.',
         'index.html#opinie'),
        ('przed_wizyta', 'Zanim przyjdziesz',
         'Co zrobić przed zabiegiem, czego nie robić, ile trwa. Mniej telefonów z tymi samymi pytaniami i mniej wizyt, na których czegoś się nie da wykonać.',
         'Zwykła lista przy formularzu rezerwacji, w miejscu, gdzie klientka i tak patrzy.',
         'index.html#rezerwacja'),
        ('dojazd', 'Jak do nas trafić',
         'Mapa, dojazd i parkowanie. Brzmi banalnie, ale to jest najczęstszy powód spóźnień i najczęstsze pytanie w telefonie.',
         'Mapa wczytywana dopiero po kliknięciu — nie spowalnia strony i nie osadza śledzenia na starcie.',
         'demo-studio-lawenda-kontakt/index.html#dojazd'),
        ('telefon', 'Telefon, w który się dotyka',
         'Na komórce numer jest przyciskiem — dotknięcie dzwoni. Brzmi drobno, a przy salonie usługowym to najczęściej klikany element całej strony.',
         'Numer wystawiony jako połączenie, nie jako obrazek czy zwykły tekst.',
         'demo-studio-lawenda-kontakt/index.html#dane'),
        ('rodo', 'Zgoda RODO przy każdym formularzu',
         'Wyraźna zgoda przed wysłaniem, bez ukrywania jej drobnym drukiem. To wymóg prawa, a nie ozdoba.',
         'Pole zgody jest obowiązkowe — bez zaznaczenia formularz się nie wyśle.',
         'demo-studio-lawenda-kontakt/index.html#lead-form'),
        ('mobile', 'Pełna wersja mobilna',
         'Nie „jakoś się otwiera na telefonie", tylko osobno zaprojektowany układ. Do salonu kosmetycznego ludzie wchodzą z telefonu prawie zawsze.',
         'Menu, cennik i formularz przebudowane pod wąski ekran, nie pomniejszone.',
         'index.html'),
        ('animacje', 'Treść pojawia się przy przewijaniu',
         'Sekcje wchodzą płynnie, gdy do nich dojeżdżasz. Strona sprawia wrażenie zrobionej, a nie złożonej z gotowców.',
         'Delikatny efekt, wyłączany automatycznie u osób, które w systemie prosiły o ograniczenie animacji.',
         'index.html#efekty'),
    ],
    dodac=['platnosc', 'przypomnienia', 'karnety', 'lojalnosc', 'kalendarz_online',
           'messenger', 'voicebot', 'opinie_ai', 'social', 'metamorfozy',
           'blog', 'wideo', 'panel', 'aplikacja', 'statystyki', 'jezyki', 'wcag'],
    wlasne_dodatki={
        'przypomnienia': ('Przypomnienie SMS o wizycie',
            'Wiadomość dzień wcześniej. Najtańszy istniejący sposób na ograniczenie nieodwołanych wizyt — a każda pusta godzina to realna strata.',
            'Wysyłka automatyczna po rezerwacji, z możliwością odwołania jednym kliknięciem.'),
        'karnety': ('Karnety i vouchery na prezent',
            'Voucher kupiony online, wysłany mailem, do wydrukowania albo pokazania z telefonu. Grudzień robi na tym pół miesiąca obrotu.',
            'Kod na voucherze sprawdzasz przy wizycie; system pilnuje, żeby nie dało się użyć go dwa razy.'),
        'lojalnosc': ('Program lojalnościowy',
            'Co dziesiąty zabieg taniej albo punkty za wizytę. Utrzymanie stałej klientki kosztuje wielokrotnie mniej niż zdobycie nowej.',
            'Liczy się automatycznie przy rezerwacji, bez papierowych karteczek do stemplowania.'),
        'kalendarz_online': ('Kalendarz z prawdziwą dostępnością',
            'Klientka widzi wolne godziny i sama wybiera — zamiast wysyłać prośbę i czekać na potwierdzenie.',
            'Podpięcie pod kalendarz, którego już używacie; zajęte terminy znikają same.'),
        'metamorfozy': ('Galeria przed i po',
            'Suwak z efektem zabiegu. W tej branży to jest najmocniejszy argument, jaki istnieje — mocniejszy od każdego opisu.',
            'Dwa zdjęcia, jeden suwak. Do każdej metamorfozy krótki opis, co i w jakim czasie.'),
    },
),

# ─────────────────────────────────────────────────────────────────────────
'zawadzcy': dict(
    nazwa='Kancelaria Zawadzcy',
    branza='kancelaria prawna',
    baza='demo-kancelaria-zawadzcy',
    lede='Kancelaria prowadzona przez wspólników. Strona ma budować zaufanie i doprowadzić do pierwszej rozmowy — bez sprzedażowego tonu, który u prawnika działa przeciwko.',
    dziala=[
        ('kalkulator', 'Kalkulator terminów procesowych',
         'Klient dostał pismo z sądu i nie wie, ile ma czasu. Wpisuje datę, wybiera rodzaj pisma i dostaje termin z podstawą prawną. Nikt inny w okolicy tego nie ma.',
         'Liczy dni robocze z pominięciem świąt, w tym Wielkanocy liczonej z kalendarza — nie z listy wpisanej na sztywno.',
         'index.html#terminy'),
        ('asystent', 'Asystent, który nie udaje prawnika',
         'Odpowiada na pytania o zakres spraw, koszty i sposób umówienia się. Przy pytaniu o konkretną sprawę mówi wprost, że to wymaga rozmowy z prawnikiem — i proponuje termin.',
         'Świadomie zawężony zakres. Lepiej odesłać do człowieka niż udzielić porady, która narobi szkody.',
         'index.html'),
        ('poufnosc', 'Co się dzieje z tym, co Państwo przekażą',
         'Osobna sekcja o postępowaniu z dokumentami i danymi. Dla klienta rozważającego sprawę rodzinną albo karną to bywa pytanie numer jeden.',
         'Napisane językiem zrozumiałym, bez cytowania numerów artykułów.',
         'demo-kancelaria-zawadzcy-proces-cennik/index.html'),
        ('rozliczenia', 'Trzy modele rozliczeń, opisane wprost',
         'Za godzinę, ryczałtem, za sukces — z wyjaśnieniem, kiedy który się opłaca. Milczenie o cenach kosztuje kancelarie więcej klientów niż jakikolwiek inny błąd.',
         'Osobna podstrona z modelami i listą czynników wpływających na cenę.',
         'demo-kancelaria-zawadzcy-proces-cennik/index.html#cennik-title'),
        ('sprawy', 'Wybrane sprawy — co udało się osiągnąć i w jakim czasie',
         'Konkretne rezultaty zamiast ogólników o „wieloletnim doświadczeniu". Bez nazwisk, ale z liczbami i terminami.',
         'Krótkie opisy: sytuacja wyjściowa, co zrobiliśmy, jaki był efekt i po jakim czasie.',
         'index.html'),
        ('specjalizacje', 'Specjalizacja zamiast przypadkowego przydziału',
         'Klient widzi, kto w kancelarii zajmuje się jego rodzajem sprawy, i trafia od razu do właściwej osoby.',
         'Podstrona oferty z podziałem na dziedziny i przypisaniem do konkretnych prawników.',
         'demo-kancelaria-zawadzcy-oferta/index.html#specjalizacje'),
        ('proces', 'Jak wygląda współpraca, krok po kroku',
         'Od pierwszego telefonu do zakończenia sprawy. Klient, który wie, co go czeka, dzwoni chętniej — bo nie boi się, że wejdzie w coś bez końca.',
         'Ponumerowane etapy z orientacyjnym czasem trwania każdego.',
         'demo-kancelaria-zawadzcy-proces-cennik/index.html#proces-title'),
        ('konsultacja', 'Do 30 minut rozmowy bez zobowiązań',
         'Wyraźna, konkretna oferta pierwszego kroku. „Zapraszamy do kontaktu" nie jest ofertą — to jest.',
         'Osobny przycisk prowadzący prosto do formularza, z tym samym zdaniem w treści.',
         'demo-kancelaria-zawadzcy-kontakt/index.html#formularz'),
        ('formularz', 'Opisz sprawę w kilku zdaniach',
         'Formularz zbiera to, co potrzebne do przygotowania się do rozmowy — i nic ponadto. Każde zbędne pole to część osób, które rezygnują w połowie.',
         'Zgłoszenie trafia od razu, bez skrzynki pocztowej po drodze.',
         'demo-kancelaria-zawadzcy-kontakt/index.html#lead-form'),
        ('faq', 'FAQ o kosztach',
         'Pytania, które klient i tak zada w pierwszej rozmowie — odpowiedziane wcześniej. Oszczędza kwadrans przy każdym telefonie.',
         'Rozwijana lista, żeby nie zasłaniała reszty strony.',
         'demo-kancelaria-zawadzcy-proces-cennik/index.html#faq-title'),
        ('zespol', 'Zespół z nazwiskami i zakresem',
         'Prawnika wybiera się jak lekarza — do twarzy i nazwiska, nie do szyldu.',
         'Osobna podstrona zespołu, z odesłaniem do specjalizacji każdej osoby.',
         'demo-kancelaria-zawadzcy-zespol/index.html#zespol'),
        ('godziny', 'Kiedy jesteśmy dostępni',
         'Godziny przyjęć i informacja, jak szybko odpisujemy. Klient w kłopocie najgorzej znosi ciszę.',
         'Sekcja przy danych kontaktowych, wraz z deklaracją czasu odpowiedzi.',
         'demo-kancelaria-zawadzcy-kontakt/index.html#godziny-title'),
        ('rodo', 'Zgoda RODO i polityka prywatności',
         'W kancelarii to nie jest formalność — to element wiarygodności. Klient sprawdza, czy jest.',
         'Zgoda obowiązkowa przy formularzu, pełna polityka jako osobna podstrona.',
         'demo-kancelaria-zawadzcy-proces-cennik/index.html#polityka-title'),
        ('spojnosc', 'Pięć podstron, jeden charakter',
         'Nagłówek, stopka, kolory i typografia identyczne wszędzie. Kancelaria, której strona się rozjeżdża, wygląda jak kancelaria, której rozjeżdżają się terminy.',
         'Wspólne elementy w jednym miejscu — poprawka wchodzi na wszystkie podstrony naraz.',
         'index.html'),
    ],
    dodac=['e_teczka', 'podpis', 'platnosc', 'kalendarz_online', 'przypomnienia_sprawy',
           'baza_wiedzy', 'blog', 'newsletter_prawny', 'opinie_ai', 'voicebot',
           'messenger', 'jezyki', 'wcag', 'statystyki', 'panel', 'wideo'],
    wlasne_dodatki={
        'e_teczka': ('Bezpieczne przesyłanie dokumentów',
            'Klient wgrywa skany w chronionym miejscu zamiast wysyłać je zwykłym mailem. Przy sprawach wrażliwych to argument sam w sobie.',
            'Odnośnik ważny przez ograniczony czas, dostęp tylko dla prowadzącego sprawę.'),
        'podpis': ('Umowa podpisywana zdalnie',
            'Pełnomocnictwo i umowa podpisane bez wizyty w kancelarii. Skraca drogę od decyzji do rozpoczęcia sprawy z tygodnia do godziny.',
            'Podpis elektroniczny o mocy prawnej, z zapisem czasu i potwierdzeniem dla obu stron.'),
        'przypomnienia_sprawy': ('Przypomnienia o terminach dla klienta',
            'Klient dostaje wiadomość przed rozprawą i przed upływem terminu, w którym ma coś dostarczyć. Mniej telefonów, mniej spóźnionych dokumentów.',
            'Terminy wpisane raz, przypomnienia idą same, z wyprzedzeniem które ustalacie.'),
        'kalendarz_online': ('Termin konsultacji wybierany online',
            'Klient widzi wolne okienka na rozmowę i rezerwuje sam, zamiast wymieniać cztery maile o to, kiedy komu pasuje.',
            'Podpięcie pod kalendarz kancelarii; zajęte godziny znikają same, potwierdzenie idzie do obu stron.'),
        'baza_wiedzy': ('Baza wiedzy dla klientów',
            'Krótkie wyjaśnienia typowych sytuacji: co zrobić po otrzymaniu nakazu, jak liczyć termin, czym różni się zażalenie od apelacji. Buduje pozycję w Google i zaufanie naraz.',
            'Osobny dział, każde zagadnienie jako podstrona z własnym adresem.'),
        'newsletter_prawny': ('Newsletter ze zmianami w przepisach',
            'Krótka wiadomość, gdy zmienia się coś, co dotyczy Waszych klientów. Przypomina o kancelarii, zanim będzie potrzebna.',
            'Zapis na stronie, treść przygotowywana raz w miesiącu, wysyłka automatyczna.'),
    },
),

# ─────────────────────────────────────────────────────────────────────────
'dom': dict(
    nazwa='Dom i Wnętrze',
    branza='firma remontowa',
    baza='demo-dom-i-wnetrze',
    lede='Firma remontowa robiąca całe mieszkania i pojedyncze zakresy. Strona ma odpowiedzieć na pytanie „ile to będzie kosztować" i zdjąć lęk przed remontem.',
    dziala=[
        ('suwak', 'Suwak przed i po',
         'Klient przesuwa i widzi to samo pomieszczenie przed remontem i po. W tej branży żaden opis nie działa tak mocno jak jedno takie zdjęcie.',
         'Dwa zdjęcia z tego samego ujęcia, jeden suwak. Działa też dotykiem na telefonie.',
         'index.html#efekty'),
        ('realizacje', 'Realizacje z metrażem i czasem',
         'Nie „wykonaliśmy remont", tylko „łazienka 5,4 m² w bloku z lat 70." i „62 m², 11 tygodni". Konkret pozwala klientowi przyłożyć to do siebie.',
         'Osobna podstrona z realizacjami, każda z zakresem prac, metrażem i czasem wykonania.',
         'demo-dom-i-wnetrze-realizacje/index.html#lazienka'),
        ('pakiety', 'Trzy poziomy wykończenia, jedna zasada rozliczeń',
         'Klient wybiera poziom zamiast zgadywać. Widełki wiszą na stronie, więc rozmowa zaczyna się od „który pakiet", a nie od „ile to kosztuje".',
         'Osobna podstrona pakietów, rozliczenie za metr, jednakowe we wszystkich trzech.',
         'index.html#pakiety'),
        ('asystent', 'Asystent, który zna zakres i widełki',
         'Odpowiada na „robicie hydraulikę", „ile trwa łazienka", „jeździcie do Pruszkowa" — natychmiast, także wieczorem, kiedy ludzie planują remonty.',
         'Zna treść strony i cennik. Pytania o konkretną wycenę kieruje do obmiaru.',
         'index.html'),
        ('obmiar', 'Bezpłatny obmiar do 48 godzin',
         'Konkretna obietnica z terminem zamiast „zapraszamy do kontaktu". Klient wie, co się stanie po wysłaniu formularza i kiedy.',
         'Formularz na stronie głównej, zgłoszenie trafia od razu, bez skrzynki po drodze.',
         'index.html#obmiar'),
        ('obawy', 'Wszystko, czego boisz się przy remoncie',
         'Sekcja mówiąca wprost o tym, co ludzi odstrasza: przekroczony termin, rosnący kosztorys, znikająca ekipa. Nazwanie obawy działa lepiej niż jej pomijanie.',
         'Wyróżniona sekcja z odpowiedzią na każdą z obaw.',
         'index.html#umowa'),
    	('umowa', 'Całe mieszkanie, jedna umowa',
         'Jeden wykonawca i jedna odpowiedzialność zamiast pięciu ekip, które wzajemnie się obwiniają. To jest główny powód, dla którego klient wybiera firmę zamiast fachowców z ogłoszeń.',
         'Sekcja z zasadami obowiązującymi przy każdej wycenie.',
         'index.html#umowa'),
        ('proces', 'Od telefonu do odbioru kluczy',
         'Ponumerowane etapy remontu z orientacyjnym czasem. Klient widzi, że to ma początek i koniec — a nie ciągnie się w nieskończoność.',
         'Sekcja procesu na stronie głównej, przed formularzem obmiaru.',
         'index.html#proces'),
        ('uslugi', 'Sześć zakresów, także pojedynczo',
         'Remonty, wykończeniówka, instalacje, stolarka i reszta — każdy opisany osobno, bo nie każdy klient chce od razu całego mieszkania.',
         'Osobna podstrona usług z kotwicą do każdego zakresu.',
         'demo-dom-i-wnetrze-uslugi/index.html#instalacje'),
        ('liczby', 'Dwanaście lat w liczbach',
         'Liczba realizacji, metrów i lat pracy zamiast zapewnień o doświadczeniu. Liczba jest sprawdzalna, przymiotnik nie.',
         'Sekcja liczb na podstronie realizacji.',
         'demo-dom-i-wnetrze-realizacje/index.html#liczby'),
        ('obszar', 'Warszawa i 25 km wokół',
         'Zasięg podany wprost. Oszczędza telefony od ludzi spoza obszaru i buduje zaufanie u tych z niego.',
         'Sekcja zasięgu na podstronie kontaktu, wraz z mapą.',
         'demo-dom-i-wnetrze-kontakt/index.html#obszar'),
        ('opinie', 'Opinie z konkretnym zakresem prac',
         'Nie „polecam", tylko kto, jaki remont i jak długo trwał. Opinia z konkretem przekonuje, opinia ogólna nie robi nic.',
         'Sekcja opinii na stronie głównej, na trasie do formularza.',
         'index.html#opinie'),
        ('telefon', 'Jeden numer do wszystkiego',
         'Bez centrali i bez przekierowań. Na telefonie numer jest przyciskiem — dotknięcie dzwoni.',
         'Numer wystawiony jako połączenie, w stopce każdej podstrony.',
         'demo-dom-i-wnetrze-kontakt/index.html#dane'),
        ('mobile', 'Pełna wersja mobilna',
         'Zdjęcia przed i po, pakiety i formularz przebudowane pod wąski ekran. Remont ogląda się wieczorem na kanapie, z telefonu.',
         'Osobny układ dla telefonu, nie pomniejszony obraz strony komputerowej.',
         'index.html'),
    ],
    dodac=['kosztorys', 'harmonogram_klienta', 'wizualizacje', 'platnosc', 'panel',
           'galeria_3d', 'blog', 'opinie_ai', 'social', 'messenger', 'voicebot',
           'wideo', 'statystyki', 'aplikacja', 'wcag', 'jezyki'],
    wlasne_dodatki={
        'kosztorys': ('Kalkulator kosztu remontu',
            'Klient podaje metraż i zakres, dostaje widełki od ręki. Odsiewa tych, którzy szukają czegoś trzy razy tańszego, zanim zajmiecie się nimi na obmiarze.',
            'Liczy z Waszych stawek za metr, wynik zawsze jako widełki — nigdy jako wiążąca oferta.'),
        'harmonogram_klienta': ('Podgląd postępu prac',
            'Klient widzi na stronie, na jakim etapie jest jego remont i co dalej. Znika połowa telefonów typu „a jak tam u nas".',
            'Prosty pasek etapów, aktualizowany z telefonu przez brygadzistę.'),
        'wizualizacje': ('Wizualizacja przed remontem',
            'Klient widzi swoje pomieszczenie po zmianach, zanim cokolwiek się zacznie. Mniej zmian w trakcie, a każda zmiana w trakcie kosztuje.',
            'Wizualizacja z rzutu i zdjęć, w kilku wariantach kolorystycznych do wyboru.'),
        'galeria_3d': ('Spacer po zrealizowanym wnętrzu',
            'Obrót o 360 stopni zamiast pięciu zdjęć. Klient ogląda realizację tak, jakby w niej stał.',
            'Zdjęcia sferyczne osadzone na stronie, działają też na telefonie.'),
    },
),

# ─────────────────────────────────────────────────────────────────────────
'serwis': dict(
    nazwa='Serwis Podkarpacki',
    branza='warsztat samochodowy',
    baza='demo-serwis-podkarpacki',
    lede='Warsztat samochodowy z obsługą flot i sezonem opon. Strona ma zapełniać stanowiska i rozdzielić dwa zupełnie różne strumienie zgłoszeń.',
    dziala=[
        ('opony', 'Wymiana opon jako osobny strumień zgłoszeń',
         'Sezon opon to inny rytm pracy niż serwis — inna osoba, inny kalendarz, inne pytania. Dlatego ma własny formularz: auto, rozmiar, całe koła czy same opony, czy zamawiamy nowe.',
         'Osobne zgłoszenie od pierwszego kliknięcia, więc nie miesza się z naprawami i trafia do właściwej osoby.',
         'index.html#wymiana-opon'),
        ('umow', 'Umów wizytę bez zbędnych formalności',
         'Klient opisuje objaw, podaje markę i przebieg. Warsztat wie, ile czasu zarezerwować, zanim auto podjedzie.',
         'Formularz pyta tylko o to, co realnie zmienia planowanie stanowiska.',
         'index.html#umow-wizyte'),
        ('asystent', 'Asystent, który zna usługi i widełki',
         'Odpowiada na „ile kosztuje wymiana rozrządu", „robicie klimatyzację", „do której jesteście czynni". Kierowca z awarią pyta natychmiast, nie następnego dnia.',
         'Zna cennik i zakres usług. Diagnozę zostawia mechanikowi — nie zgaduje, co się zepsuło.',
         'index.html'),
        ('cennik', 'Orientacyjne widełki, bez niespodzianek',
         'Ceny podane jako zakres, z wyjaśnieniem, co je podnosi. Kierowcy najbardziej boją się rachunku wyższego niż zapowiedź — to zdejmuje ten strach.',
         'Osobna podstrona cennika, z listą prac wykonywanych najczęściej.',
         'demo-serwis-podkarpacki-uslugi/index.html#cennik'),
        ('uslugi', 'Najważniejsze usługi w jednym miejscu',
         'Mechanika, diagnostyka, klimatyzacja, opony, geometria — kafelki, z których widać zakres w trzy sekundy, bez czytania.',
         'Podstrona usług z krótkim opisem każdego zakresu.',
         'demo-serwis-podkarpacki-uslugi/index.html'),
        ('floty', 'Stała obsługa flot bez chaosu',
         'Osobna oferta dla firm z kilkoma autami. Jeden klient flotowy jest wart tyle, co kilkunastu przypadkowych, a szuka na stronie czego innego.',
         'Wydzielona sekcja z zasadami współpracy i rozliczeń dla firm.',
         'index.html#uslugi'),
        ('jak_dziala', 'Proces prosty dla kierowcy',
         'Cztery kroki od zgłoszenia do odbioru auta. Kierowca wie, kiedy dostanie wycenę i kiedy może odebrać.',
         'Sekcja procesu na stronie głównej, przed formularzem.',
         'index.html#jak-to-dziala'),
        ('zasady', 'Jasne zasady zamiast warsztatowych niedomówień',
         'Wycena przed naprawą, kontakt przy każdej zmianie zakresu, wymienione części do wglądu. To są dokładnie te trzy rzeczy, o które kierowcy mają największy żal.',
         'Wyróżniona sekcja zasad, w widocznym miejscu strony głównej.',
         'index.html#doswiadczenie'),
        ('wyposazenie', 'Sprzęt, który wspiera rzetelną diagnozę',
         'Konkretne urządzenia zamiast zapewnień o nowoczesności. Kierowca, który zna się choć trochę, sprawdza właśnie to.',
         'Sekcja wyposażenia na podstronie o warsztacie.',
         'demo-serwis-podkarpacki-o-nas/index.html#wyposazenie'),
        ('marki', 'Auta europejskie i azjatyckie',
         'Wprost napisane, przy czym pracujecie najczęściej. Kierowca marki spoza listy nie traci czasu, a ten z listy nabiera pewności.',
         'Sekcja marek na podstronie o warsztacie.',
         'demo-serwis-podkarpacki-o-nas/index.html#marki'),
        ('zespol', 'Cztery osoby, cztery role, jeden standard',
         'Warsztat z twarzami zamiast anonimowej hali. Zaufanie do warsztatu jest w tej branży ważniejsze niż cena.',
         'Sekcja zespołu z podziałem ról.',
         'demo-serwis-podkarpacki-o-nas/index.html#zespol'),
        ('historia', 'Od dwuosobowego garażu do hali serwisowej',
         'Krótka historia warsztatu. Buduje wiarygodność szybciej niż jakikolwiek certyfikat na ścianie.',
         'Sekcja historii na podstronie o warsztacie.',
         'demo-serwis-podkarpacki-o-nas/index.html#historia'),
        ('praktyczne', 'Praktyczne informacje przed wizytą',
         'Co zabrać, gdzie zaparkować, ile potrwa. Zmniejsza liczbę telefonów z tymi samymi pytaniami.',
         'Sekcja przy formularzu zgłoszenia.',
         'index.html#umow-wizyte'),
        ('telefon', 'Telefon, godziny i dojazd',
         'Numer klikalny, godziny otwarcia i mapa. Kierowca z awarią szuka dokładnie tych trzech rzeczy i niczego więcej.',
         'Dane kontaktowe w stopce każdej podstrony, mapa wczytywana po kliknięciu.',
         'demo-serwis-podkarpacki-kontakt/index.html'),
    ],
    dodac=['dwa_kalendarze', 'przechowalnia', 'status_naprawy', 'przypomnienie_przeglad',
           'platnosc', 'historia_auta', 'voicebot', 'messenger', 'opinie_ai',
           'panel', 'blog', 'social', 'wideo', 'statystyki', 'aplikacja', 'wcag'],
    wlasne_dodatki={
        'dwa_kalendarze': ('Dwa prawdziwe kalendarze z wolnymi terminami',
            'Kierowca widzi wolne godziny i sam wybiera — osobno na serwis, osobno na opony. W szczycie sezonu to jest różnica między telefonem dzwoniącym bez przerwy a spokojną pracą.',
            'Dwa niezależne kalendarze, każdy ze swoją osobą i swoją długością wizyty.'),
        'przechowalnia': ('Przechowalnia opon z ewidencją',
            'Klient widzi, że ma u Was komplet, jakiego rozmiaru i w jakim stanie. Usługa, za którą warsztaty biorą co roku, a której prawie nikt nie pokazuje na stronie.',
            'Spis kompletów z możliwością sprawdzenia po numerze rejestracyjnym.'),
        'status_naprawy': ('Status naprawy po numerze rejestracyjnym',
            'Kierowca sprawdza sam, zamiast dzwonić. „Czekamy na część", „gotowe do odbioru" — trzy kliknięcia zamiast telefonu.',
            'Status zmieniacie jednym dotknięciem z telefonu na hali.'),
        'przypomnienie_przeglad': ('Przypomnienie o przeglądzie i wymianie',
            'Wiadomość przed badaniem technicznym i przed sezonem opon. Najtańszy sposób, żeby klient wrócił — i najczęściej pomijany.',
            'Terminy liczone z historii wizyt, wiadomość wychodzi automatycznie.'),
        'historia_auta': ('Historia serwisowa auta',
            'Wszystko, co robiliście przy tym samochodzie, w jednym miejscu. Przy sprzedaży auta klient sam się po to zgłosi.',
            'Wpisy przypisane do numeru rejestracyjnego, dostęp po kodzie.'),
    },
),
}


# ══════════════════════════════════════════════════════════════════════════
#  SKŁADANIE
# ══════════════════════════════════════════════════════════════════════════

def odcisk(sciezka):
    """Skrot z zawartosci pliku, doklejany do adresu CSS/JS — zeby po poprawce
    przegladarka nie serwowala starej wersji z pamieci podrecznej."""
    import hashlib
    with open(sciezka, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


def e(s):
    return html.escape(s, quote=False)


def slajd_funkcji(sekcja, nr, ile, poz, baza, licznik_etykieta):
    sid, tytul, opis, jak, podglad = poz
    media = ''
    if podglad:
        adres = baza + '/' + podglad if not podglad.startswith('demo-') else podglad
        media = ('<div class="framecard framecard-live">'
                 '<iframe data-src="%s" title="Podgląd: %s" loading="lazy" '
                 'referrerpolicy="no-referrer"></iframe>'
                 '<span class="zaslona"></span>'
                 '<a class="live-open" href="%s" target="_blank" rel="noopener">'
                 'Otwórz na żywo &rarr;</a></div>') % (e(adres), e(tytul), e(adres))
    return '''<section class="slide slide-content" data-section="%s" id="slide-%s">
      <div class="slide-grid">
        <div class="slide-text">
          <p class="eyebrow">%s &middot; %02d / %d</p>
          <h2>%s</h2>
          <p class="body">%s</p>
          <p class="tech"><span>Jak to działa:</span> %s</p>
          <div class="picker" role="group" aria-label="Twoja decyzja dla tej pozycji" data-slide-id="%s"><span class="picker-label">Twoja decyzja:</span><div class="picker-btns"><button type="button" class="pick pick-yes" data-choice="wybieram">Wybieram</button><button type="button" class="pick pick-maybe" data-choice="zainteresowany">Wstępnie zainteresowany</button></div></div>
        </div>
        <div class="slide-media">%s</div>
      </div>
    </section>''' % (sekcja, e(sid), e(licznik_etykieta), nr, ile,
                     e(tytul), e(opis), e(jak), e(sid), media)


def zbuduj(klucz, d):
    global ODCISK_CSS, ODCISK_JS
    baza = d['baza']
    dziala = d['dziala']
    pula = dict(WSPOLNE_DODATKI); pula.update(d.get('wlasne_dodatki', {}))
    brak = [k for k in d['dodac'] if k not in pula]
    if brak:
        raise SystemExit('BRAK OPISU dla: %s (demo %s)' % (', '.join(brak), klucz))
    dodatki = [(k,) + pula[k] for k in d['dodac']]

    slajdy, toc, pozycje = [], [], []

    # ── tytuł
    slajdy.append('''<section class="slide slide-structural " data-section="title" id="slide-title">
  <div class="title-inner">
    <p class="eyebrow">%s &middot; KATALOG FUNKCJI</p>
    <h1>Czego już użyliśmy<br><em>i co możemy dodać.</em></h1>
    <p class="lede">%s</p>
    <div class="title-stats">
      <div><b>%d</b><span>gotowych funkcji</span></div>
      <div><b>%d</b><span>pomysłów do dodania</span></div>
      <div><b>%d</b><span>podstrony do obejrzenia</span></div>
    </div>
    <button type="button" class="btn-start" id="btn-go-start">Zaczynamy <span aria-hidden="true">&rarr;</span></button>
    <button type="button" class="btn-reset-link" id="btn-reset-top">Zacznij od nowa — wyczyść zaznaczenia</button>
  </div>
</section>''' % (e(d['nazwa'].upper()), e(d['lede']), len(dziala), len(dodatki), d.get('podstron', 4)))
    toc.append('<li class="toc-h">Start</li><li><button data-jump="title">Strona tytułowa</button></li>')

    # ── jak korzystać
    slajdy.append('''<section class="slide slide-structural " data-section="intro" id="slide-intro">
  <div class="title-inner intro-inner">
    <p class="eyebrow">JAK KORZYSTAĆ Z TEGO MATERIAŁU</p>
    <h2>Jedna funkcja na slajd. Dwa przyciski decyzji.</h2>
    <div class="intro-grid">
      <div class="intro-card">
        <span class="pick pick-yes pick-demo">Wybieram</span>
        <p>Chcę to mieć w swojej stronie — traktujemy jako ustalone.</p>
      </div>
      <div class="intro-card">
        <span class="pick pick-maybe pick-demo">Wstępnie zainteresowany</span>
        <p>Podoba mi się, ale decyzja później — do omówienia przy wycenie.</p>
      </div>
    </div>
    <p class="intro-note">Przy każdym slajdzie widać <b>tę funkcję działającą na żywo</b> — to nie są zrzuty ekranu, tylko prawdziwa strona, którą można otworzyć i kliknąć. Zaznaczenia zapisują się w tej przeglądarce i zbierają na ostatnim slajdzie. Nawigacja: strzałki &larr; &rarr;, spacja albo przyciski w rogu. Klawisz <b>M</b> otwiera spis treści.</p>
  </div>
</section>''')
    toc.append('<li><button data-jump="intro">Jak korzystać</button></li>')

    # ── część 1
    slajdy.append('''<section class="slide slide-structural " data-section="divider" id="slide-divider-a">
  <div class="title-inner divider-inner">
    <p class="eyebrow">CZĘŚĆ PIERWSZA</p>
    <h1>Co już <em>działa.</em></h1>
    <p class="lede">%d funkcji, które można obejrzeć na żywo już teraz — każda naprawdę uruchomiona, nie makieta.</p>
  </div>
</section>''' % len(dziala))
    toc.append('<li class="toc-h">Co już działa</li>')
    for i, poz in enumerate(dziala, 1):
        slajdy.append(slajd_funkcji('feature', i, len(dziala), poz, baza, 'CO JUŻ DZIAŁA'))
        toc.append('<li><button data-jump="%s">%02d &middot; %s</button></li>' % (e(poz[0]), i, e(poz[1])))
        pozycje.append([poz[0], poz[1], 'feature'])

    # ── część 2
    slajdy.append('''<section class="slide slide-structural " data-section="divider" id="slide-divider-b">
  <div class="title-inner divider-inner">
    <p class="eyebrow">CZĘŚĆ DRUGA</p>
    <h1>Co można <em>dodać.</em></h1>
    <p class="lede">%d rzeczy, które da się dołożyć do tej strony. Nic z tego nie jest konieczne — wybiera się to, co realnie zarabia w Twojej branży.</p>
  </div>
</section>''' % len(dodatki))
    toc.append('<li class="toc-h">Co można dodać</li>')
    for i, (sid, tytul, opis, jak) in enumerate(dodatki, 1):
        slajdy.append(slajd_funkcji('addition', i, len(dodatki), (sid, tytul, opis, jak, None), baza, 'CO MOŻNA DODAĆ'))
        toc.append('<li><button data-jump="%s">%02d &middot; %s</button></li>' % (e(sid), i, e(tytul)))
        pozycje.append([sid, tytul, 'addition'])

    # ── podsumowanie
    slajdy.append('''<section class="slide slide-structural " data-section="summary" id="slide-summary">
  <div class="title-inner summary-inner">
    <p class="eyebrow">PODSUMOWANIE</p>
    <h2>Co wybrałeś.</h2>
    <div class="summary-cols">
      <div class="summary-col">
        <h3><span class="pick pick-yes pick-demo pick-static">Wybieram</span></h3>
        <ul id="sum-yes" class="summary-list"><li class="summary-empty">Nic jeszcze niezaznaczone.</li></ul>
      </div>
      <div class="summary-col">
        <h3><span class="pick pick-maybe pick-demo pick-static">Wstępnie zainteresowany</span></h3>
        <ul id="sum-maybe" class="summary-list"><li class="summary-empty">Nic jeszcze niezaznaczone.</li></ul>
      </div>
    </div>
    <div class="summary-actions">
      <button type="button" class="btn-start btn-small" id="btn-copy">Kopiuj listę do schowka</button>
      <button type="button" class="btn-reset-link" id="btn-reset-bottom">Wyczyść wszystkie zaznaczenia</button>
    </div>
    <p class="summary-hint" id="copy-hint" aria-live="polite"></p>
  </div>
</section>''')
    toc.append('<li class="toc-h">Koniec</li><li><button data-jump="summary">Podsumowanie</button></li>')

    tytul_strony = '%s — katalog funkcji | Probatum' % d['nazwa']
    opis_strony = ('Funkcje, które ta strona już ma, i te, które można do niej dodać. '
                   'Każda pokazana na żywo. Zaznacz, co Cię interesuje.')

    return SZKIELET % dict(
        tytul=e(tytul_strony), opis=e(opis_strony),
        slajdy='\n'.join(slajdy), toc='\n'.join(toc),
        id=klucz, demo=e(d['nazwa']),
        pozycje=repr(pozycje).replace("'", '"'),
        css=ODCISK_CSS, js=ODCISK_JS,
    )


SZKIELET = '''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>%(tytul)s</title>
<meta name="description" content="%(opis)s">
<link rel="stylesheet" href="../assets/katalog.css?v=%(css)s">
</head>
<body>
<div class="deck">
%(slajdy)s
</div>

<div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
<div class="hud-top">
  <span class="hud-section" id="hud-section"></span>
  <span class="hud-frac" id="hud-frac"></span>
</div>

<button type="button" class="toc-btn" id="toc-btn-open" aria-haspopup="dialog">
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="14" y2="17"/></svg>
  Spis treści <span style="opacity:.6">(M)</span>
</button>

<div class="nav-controls">
  <button type="button" class="nav-btn" id="btn-prev" aria-label="Poprzedni slajd">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
  </button>
  <button type="button" class="nav-btn" id="btn-next" aria-label="Następny slajd">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
  </button>
</div>

<div class="toc-overlay" id="toc-overlay" role="dialog" aria-modal="true" aria-label="Spis treści">
  <div class="toc-panel">
    <div class="toc-head">
      <h3>Spis treści</h3>
      <button type="button" class="toc-close" id="toc-close" aria-label="Zamknij spis treści">&times;</button>
    </div>
    <ul class="toc-list" id="toc-list">
%(toc)s
    </ul>
  </div>
</div>

<script>
window.KATALOG = {
  id: "%(id)s",
  demo: "%(demo)s",
  webhook: "https://pmresearch.app.n8n.cloud/webhook/probatum-katalog-wybory",
  pozycje: %(pozycje)s
};
</script>
<script src="../assets/katalog.js?v=%(js)s"></script>
</body>
</html>
'''


if __name__ == '__main__':
    ASSETS = os.path.abspath(os.path.join(KAT, '..', 'assets'))
    ODCISK_CSS = odcisk(os.path.join(ASSETS, 'katalog.css'))
    ODCISK_JS  = odcisk(os.path.join(ASSETS, 'katalog.js'))
    print('odcisk CSS: %s   odcisk JS: %s' % (ODCISK_CSS, ODCISK_JS))
    ile = 0
    for klucz, d in DEMA.items():
        html_out = zbuduj(klucz, d)
        sciezka = os.path.join(OUT, 'katalog-%s.html' % klucz)
        io.open(sciezka, 'w', encoding='utf-8').write(html_out)
        print('zbudowano: p/katalog-%s.html  (%d gotowych + %d do dodania, %d znakow)'
              % (klucz, len(d['dziala']), len(d['dodac']), len(html_out)))
        ile += 1
    print('--- gotowe: %d katalogow' % ile)
