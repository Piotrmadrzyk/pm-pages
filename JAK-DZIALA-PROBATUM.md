# JAK DZIAŁA PROBATUM.PL — instrukcja przejęcia

**Stan na:** 21 sierpnia 2026
**Dla kogo:** ktoś, kto przejmuje stronę i nie ma kogo zapytać.

Wszystko poniżej sprawdzone w kodzie, nie z pamięci. Ścieżki są prawdziwe,
polecenia można kopiować.

---

## PIERWSZE 15 MINUT NOWEJ OSOBY

Najkrótsza droga od zera do wypuszczenia drobnej zmiany. Zrób to, zanim ruszysz
cokolwiek poważnego — sprawdzisz, że cały łańcuch działa.

```bash
# 1. Pobierz kod
cd ~
git clone https://github.com/piotrmadrzyk/pm-pages.git
cd pm-pages

# 2. Zmień coś drobnego — np. numer telefonu w jednym miejscu
#    Otwórz build/build.py, znajdź blok KONTAKT (okolice linii 10)
#    i popraw wartość 'TEL'.

# 3. Przebuduj stronę
cd build
python3 build.py
cd ..

# 4. Zobacz, co się zmieniło
git status
git diff --stat

# 5. Obejrzyj lokalnie, zanim wypuścisz
python3 -m http.server 8000
#    → otwórz http://localhost:8000/kontakt.html
#    → Ctrl+C, żeby zatrzymać

# 6. Wypuść
git add -A
git commit -m "Kontakt: poprawiony numer telefonu"
git push
```

Po `git push` Vercel sam publikuje. Nic nie trzeba klikać. Po minucie–dwóch
zmiana jest na probatum.pl.

**Jeśli po kroku 3 `git status` pokazuje zmienione pliki `.html`, których nie
tykałeś — to normalne.** One są generowane. Patrz punkt 3 niżej.

---

## 1. GDZIE LEŻY KOD

| | |
|---|---|
| Repozytorium | `https://github.com/piotrmadrzyk/pm-pages` |
| Gałąź | `main` |
| Widoczność | **publiczne** |
| Właściciel konta | `piotrmadrzyk` |

Pobranie: `git clone https://github.com/piotrmadrzyk/pm-pages.git`

Na koncie GitHub są tylko dwa publiczne repozytoria: `pm-pages`
i `radosc-website-preview`. To pierwsze jest tym właściwym.

---

## 2. STRONA JEST GENEROWANA, NIE PISANA RĘCZNIE

To najważniejsza rzecz w całym dokumencie.

**Generator:** `build/build.py` — zwykły skrypt w Pythonie, bez żadnych
bibliotek do instalowania. Uruchamiasz go tak:

```bash
cd build
python3 build.py
```

Wypisze, co zbudował, np. `zbudowano: index.html (34437 znaków)`.

### Co jest na wejściu

```
build/
  build.py            ← generator: szablon strony, menu, stopka, lista podstron
  wpisy.py            ← zamienia pliki .txt na strony wpisów
  parts/              ← treść podstron (to edytujesz)
      index.html
      o-donie.html
      oferta.html
      realizacje.html
      automatyzacja.html
      wycena.html
      kontakt.html
  wpisy/
      blog/           ← pliki .txt = wpisy na blogu
          po-co-agent-malej-firmie.txt
      warsztat/       ← pliki .txt = instrukcje w Warsztacie
          pierwsza-automatyzacja.txt
```

Pliki w `parts/` zawierają **samą treść** podstrony — bez nagłówka, menu
i stopki. Generator dokleja resztę.

Wpisy to zwykłe pliki tekstowe. Na górze dane wpisu, potem trzy myślniki,
potem treść:

```
tytul: Jak odzyskać godzinę dziennie
data: 2026-08-20
opis: Zdanie, które zobaczy Google i czytelnik na liście.
---
Tu zaczyna się treść. Działa ## nagłówek, - lista, **pogrubienie**,
`kod`, > cytat, [tekst](adres), ![opis](assets/img/cos.jpg).
```

Warsztat przyjmuje dodatkowo pola `czas:`, `poziom:`, `narzedzia:`.

Nazwa pliku staje się adresem: `pierwsza-automatyzacja.txt` →
`/warsztat/pierwsza-automatyzacja.html`.

### Co jest na wyjściu

Gotowe pliki `.html` w katalogu głównym repozytorium — to one trafiają na serwer.

---

## 3. CO EDYTUJESZ, A CO ZOSTANIE NADPISANE ⚠️

**To jest pułapka, w którą wpada każdy nowy.** Plik `index.html` w katalogu
głównym wygląda dokładnie jak plik do edycji. Nim nie jest. Przy najbliższym
uruchomieniu `build.py` twoje zmiany znikną bez ostrzeżenia i bez śladu.

### NIE EDYTUJ — te pliki są nadpisywane przy każdym budowaniu

```
index.html              o-donie.html         oferta.html
realizacje.html         automatyzacja.html   wycena.html
kontakt.html            warsztat.html        blog.html
blog/*.html             warsztat/*.html      p/katalog-*.html
```

### EDYTUJ — to są prawdziwe źródła

```
build/build.py                  ← menu, stopka, dane kontaktowe, tytuły stron
build/parts/*.html              ← treść podstron
build/wpisy/blog/*.txt          ← wpisy na blogu
build/wpisy/warsztat/*.txt      ← instrukcje w Warsztacie
assets/site.css                 ← wygląd (NIE jest generowany)
assets/site.js                  ← zachowanie strony (NIE jest generowany)
p/**                            ← strony demonstracyjne (NIE są generowane)
```

**Zapamiętaj regułę:** jeśli plik `.html` leży w katalogu głównym — jest
generowany. Jeśli leży w `build/parts/` — jest źródłem. Pliki w `assets/`
i `p/` są poza generatorem i edytuje się je wprost.

---

## 4. JAK OPUBLIKOWAĆ ZMIANĘ

```bash
cd build && python3 build.py && cd ..   # 1. przebuduj
git add -A                              # 2. zbierz zmiany
git commit -m "opis zmiany"             # 3. zapisz
git push                                # 4. wyślij
```

**Publikacja jest automatyczna.** Vercel obserwuje gałąź `main` i po każdym
`git push` sam buduje i wystawia stronę. Nic nie trzeba klikać, nigdzie nie
trzeba się logować. Zmiana jest widoczna po minucie–dwóch.

Sprawdzenie przed wysłaniem — zawsze warto:

```bash
python3 -m http.server 8000
# → http://localhost:8000/  ... Ctrl+C żeby zatrzymać
```

---

## 5. MENU I PODSTRONY

Menu jest **w jednym miejscu**: `build/build.py`, lista `NAV` (okolice linii 20):

```python
NAV = [
    ('index.html',        'Start'),
    ('o-donie.html',      'Metoda'),
    ('oferta.html',       'Oferta'),
    ('realizacje.html',   'Realizacje'),
    ('automatyzacja.html','Agenci'),
    ('warsztat.html',     'Warsztat'),
    ('blog.html',         'Blog'),
    ('kontakt.html',      'Kontakt'),
]
```

Menu powtarza się na **wszystkich** podstronach. Zmiana tutaj zmienia je
wszędzie naraz. Zmiana ręcznie w gotowym `.html` zmieni je **na jednej stronie
z jedenastu** i zniknie przy najbliższym budowaniu.

Poza `NAV` w menu jest jeszcze przycisk **„Wyceń projekt"** (`wycena.html`),
dodawany osobno — nie ma go na liście `NAV`, bo wygląda inaczej.

### Jak dodać nową pozycję — np. „Akademia AI"

1. Dopisz do `NAV` w `build/build.py`:
   ```python
   ('akademia.html', 'Akademia AI'),
   ```
2. Dopisz do listy `PAGES` w tym samym pliku (tam są tytuł i opis dla Google):
   ```python
   dict(file='akademia.html', active='akademia.html',
        title='Akademia AI — ... | Probatum',
        desc='Opis do wyników wyszukiwania, 1–2 zdania.'),
   ```
3. Utwórz `build/parts/akademia.html` z samą treścią podstrony.
4. `cd build && python3 build.py`
5. `git add -A && git commit -m "Nowa podstrona: Akademia AI" && git push`

**Uwaga:** jeśli pominiesz krok 3, generator wypisze
`POMINIĘTO (brak części): akademia.html` i po prostu nie zbuduje strony.
Nie wywali się — po cichu pominie. Czytaj to, co wypisuje.

### Ile jest podstron

Jedenaście plików wyjściowych: dziewięć podstron głównych plus po jednej
stronie wpisu w blogu i w Warsztacie. Blog i Warsztat są budowane inaczej —
z plików `.txt`, nie z `parts/` — dlatego generator wypisuje przy nich
`POMINIĘTO (brak części)`. **To nie jest błąd, tak ma być.**

---

## 6. DANE KONTAKTOWE — JEST JEDNO MIEJSCE

Na górze `build/build.py`:

```python
KONTAKT = {
    'EMAIL':    'kontakt@probatum.pl',
    'TEL':      '+48 573 569 141',
    'TEL_LINK': '+48573569141',      # bez spacji — do href="tel:"
}
```

Zmieniasz tutaj, uruchamiasz `build.py`, dane podmieniają się na wszystkich
podstronach naraz.

W szablonach używasz znaczników zamiast wpisywać dane na sztywno:

| gdzie | zapis |
|---|---|
| w plikach `build/parts/*.html` | `{{EMAIL}}` `{{TEL}}` `{{TEL_LINK}}` |
| w szablonie wewnątrz `build.py` (stopka, nagłówek) | `[[EMAIL]]` `[[TEL]]` `[[TEL_LINK]]` |

Dwa różne zapisy, bo szablon w `build.py` przechodzi przez mechanizm, który
zjada pojedyncze klamry. **W `parts/` używaj klamer, w `build.py` nawiasów
kwadratowych.**

### Czego to NIE obejmuje

- **`assets/site.js`** nie jest generowany — adres e-mail w komunikacie
  asystenta strony jest tam wpisany wprost, w okolicach linii 481. Przy zmianie
  adresu trzeba go poprawić osobno.
- **Ceny i widełki** nie mają jednego miejsca. Są wpisane wprost w treści
  `build/parts/oferta.html` i `build/parts/wycena.html`. Trzeba je podmieniać
  w każdym z tych plików osobno. **Mówię wprost, bo to łatwo przeoczyć.**

---

## 7. STRONY DEMONSTRACYJNE

Leżą w katalogu `p/` — **22 katalogi**, bo strony wielostronicowe mają każdą
podstronę w osobnym katalogu:

```
p/demo-studio-lawenda*        p/demo-kancelaria-zawadzcy*
p/demo-dom-i-wnetrze*         p/demo-serwis-podkarpacki*
p/demo-dental-lumea           p/demo-firma-saas
p/demo-gabinet-medyczny       p/demo-kancelaria-prawna
p/demo-salon-urody
p/kancelaria-img/             p/serwis-img/      ← zdjęcia wyjęte z kodu
```

Cztery pierwsze to dopracowane demo pokazywane na „Realizacjach". Pozostałe
to starsze, jednostronicowe przykłady.

**Nie idą z generatora.** To osobne, samodzielne pliki HTML, edytowane wprost.
`build.py` w ogóle ich nie dotyka.

Są wystawiane dwiema drogami: razem z resztą repozytorium na Vercelu oraz przez
GitHub Pages pod adresami `piotrmadrzyk.github.io/pm-pages/p/demo-...`.
Na stronie „Realizacje" są osadzone jako żywe podglądy.

Mają **własne, fikcyjne dane kontaktowe** — sprawdzone, prywatny adres Piotra
nigdzie w nich nie występuje. Przy zmianie danych kontaktowych firmy **nie
ruszaj demo**.

⚠️ W **27 katalogach** `wersje/w1/` leżą starsze kopie tych stron,
z obrazkami wklejonymi wprost w kod (przez co ważą po kilka megabajtów) i bez
późniejszych poprawek. **Nie publikuj z nich niczego** — cofnęłoby to całą
robotę nad demo.

---

## 7a. KATALOGI FUNKCJI (`p/katalog-*.html`)

Przy każdym demo na stronie „Realizacje" jest przycisk **„Zobacz, co ta strona
potrafi →"**. Prowadzi do katalogu: prezentacji, w której klient przechodzi
funkcja po funkcji i przy każdej zaznacza „Wybieram" albo „Wstępnie
zainteresowany". Na końcu dostaje listę, a jego wybory trafiają do n8n.

**To też jest generowane** — nie edytuj `p/katalog-*.html` ręcznie.

```
build/katalogi.py            <- treść wszystkich czterech katalogów (to edytujesz)
assets/katalog.css           <- wygląd, wspólny dla wszystkich
assets/katalog.js            <- mechanizm, wspólny dla wszystkich
p/katalog-lawenda.html       <- WYNIK, nadpisywany
p/katalog-zawadzcy.html      <- WYNIK, nadpisywany
p/katalog-dom.html           <- WYNIK, nadpisywany
p/katalog-serwis.html        <- WYNIK, nadpisywany
```

Budowanie: `cd build && python3 katalogi.py`
(to osobne polecenie niż `build.py` — katalogi nie są częścią strony głównej)

**Jak dodać funkcję do katalogu:** w `build/katalogi.py` znajdź właściwe demo
i dopisz krotkę do listy `dziala` albo nazwę do listy `dodac`. Format opisany
w komentarzu na górze pliku.

**Podglądy po prawej to nie zrzuty ekranu, tylko żywe podstrony demo**
wczytywane w ramce i ustawiane na właściwej sekcji. Dlatego przy każdej funkcji
podaje się adres z kotwicą, np. `index.html#wymiana-opon`. Jeśli w demo zmieni
się nazwa kotwicy, podgląd pokaże górę strony zamiast opisywanej funkcji —
wtedy trzeba poprawić adres w `katalogi.py`.

Wybory klientów idą do jednego wspólnego webhooka
`probatum-katalog-wybory`, a w treści zgłoszenia jest pole `demo`, po którym
poznasz, z którego katalogu przyszło.

Katalog Zielonej Pergoli mieszka w osobnym repozytorium
(`radosc-website-preview/oferta.html`) i ma własny, starszy mechanizm — nie jest
generowany przez `katalogi.py`.

---

## 7b. BLOKI PRAWNE W DEMACH (`build/prawne.py`)

Każda strona demonstracyjna ma regulamin, politykę prywatności i pasek
informacji o ciasteczkach. Robi to `build/prawne.py`:

```bash
cd build && python3 prawne.py
```

Skrypt **dokleja tylko to, czego brakuje** — można go puszczać wielokrotnie,
nie zdubluje niczego. Po każdym uruchomieniu wypisuje, co dodał na której
stronie.

### Dlaczego demo w ogóle potrzebuje regulaminu

Klient ogląda demo, żeby zobaczyć, jak będzie wyglądać jego własna strona.
Patrzy też na to, czy są tam rzeczy, których będzie potrzebował. Brak paska
cookie i regulaminu czyta się jako „tego nie robimy".

Firmy w demach są zmyślone, więc treści są szablonowe — i każdy blok kończy
się zdaniem, które mówi to wprost. To celowe: gdyby ktoś skopiował ten tekst
na prawdziwą stronę bez czytania, zdanie na końcu go zatrzyma.

### Gdzie te bloki lądują

Zależy od strony i to nie jest kaprys — to dopasowanie do tego, co już tam jest:

| demo | paleta | gdzie wchodzi |
|---|---|---|
| Studio Lawenda | ciemna stopka | kolejny kafel stopki, zaraz za polityką |
| Dom i Wnętrze | ciemna stopka | to samo |
| Kancelaria Zawadzcy | jasna (krem `#f4f0e8`) | osobna sekcja przed stopką |
| Serwis Podkarpacki | ciemna (`#1c1f24`) | osobna sekcja przed stopką |

Lawenda i Dom mają w stopce gotowe miejsce na takie treści, więc regulamin
dziedziczy jej wygląd i nie potrzebuje ani linijki nowego CSS. Zawadzcy
i Serwis nie mają gdzie tego wpiąć, więc dostają samodzielną sekcję ze
zwijanymi blokami — z własnymi stylami, bo **jeden zestaw kolorów tu nie
zadziała**: Zawadzcy są jaśni, Serwis ciemny. Kolory obu siedzą w słowniku
`FIRMY` na górze skryptu.

### Jak zmienić treść

Wszystkie teksty są w `build/prawne.py` w słowniku `FIRMY` — osobno regulamin
dla każdej firmy i wspólna klauzula RODO w funkcji `polityka_tresc()`.
Po zmianie: cofnij stare bloki (`git checkout -- p/`) i puść skrypt ponownie,
bo sam z siebie nie nadpisze tego, co już wstawił.

### ⚠️ probatum.pl to osobna sprawa

Ten skrypt dotyczy **wyłącznie stron demonstracyjnych**. Sama strona
probatum.pl nadal nie ma polityki prywatności ani klauzuli informacyjnej,
a formularz kontaktowy ma zgodę, która nie prowadzi do żadnego dokumentu.
Powód jest konkretny i opisany w `DO-ZROBIENIA.md`: klauzula RODO musi
wskazywać administratora z nazwy i adresu, a to decyzja właściciela.

---

## 8. CZEGO NIE ROBIĆ

**Nie edytuj plików `.html` w katalogu głównym.** Wyglądają na źródła, nie są
nimi. Zmiany znikną przy najbliższym `python3 build.py`. To pułapka numer jeden.

**Nie zmieniaj menu w gotowym pliku.** Zmienisz je na jednej stronie
z jedenastu i zrobi się bałagan w nawigacji.

**Nie wgrywaj pojedynczego pliku na Vercel.** Projekt obsługuje probatum.pl
i www.probatum.pl. Wgranie samej jednej podstrony skasuje resztę serwisu.
Publikuje się przez `git push` całego repozytorium.

**Nie usuwaj znacznika `noindex`.** Siedzi w szablonie w `build/build.py`,
okolice linii 98: `<meta name="robots" content="noindex, nofollow">`. Strona ma
być niewidoczna w Google do momentu startu — to świadoma decyzja właściciela,
nie przeoczenie. Zdejmuje się go **dopiero na start**, jednym usunięciem tej
linii i przebudowaniem.

Uwaga: plik `robots.txt` mówi `Allow: /`, czyli niczego nie blokuje — i tak ma
być. Blokada w `robots.txt` byłaby błędem, bo wtedy Google w ogóle nie
zobaczyłoby znacznika `noindex`. Za niewidoczność odpowiada wyłącznie znacznik.

**Nie publikuj z katalogów `wersje/w1/`** — patrz punkt 7.

**Nie zakładaj, że formularz wysyła e-maile.** Nie wysyła — patrz punkt 9.
Zmiana adresu e-mail na stronie **nie zmienia tego, dokąd trafiają zgłoszenia**.

**Nie usuwaj katalogu `build/` z repozytorium.** Do 21 sierpnia 2026 generatora
w repozytorium **nie było** — leżał wyłącznie w katalogu tymczasowym jednej
sesji roboczej. Gdyby ta sesja przepadła, strona zostałaby jako jedenaście
osobnych plików HTML bez żadnego sposobu, by zmienić menu w jednym miejscu.
Teraz jest w repozytorium i ma tam zostać.

---

## 9. GDZIE SĄ DOSTĘPY I DO CZEGO CO JEST PODPIĘTE

Sam dokument nie zawiera haseł — tylko mapę, co gdzie siedzi.

| element | gdzie | uwagi |
|---|---|---|
| Kod | GitHub, `piotrmadrzyk/pm-pages`, gałąź `main` | publiczne |
| Kolejka zadań | `DO-ZROBIENIA.md` w repozytorium | subdomeny demo i reszta |
| Hosting i publikacja | Vercel, projekt `przewagametoda-preview` | podpięty do repozytorium, publikuje sam po `git push` |
| Domena | `probatum.pl` + `www.probatum.pl` | obsługiwane przez ten sam projekt na Vercelu |
| Drugie wystawienie | GitHub Pages | `piotrmadrzyk.github.io/pm-pages/` — stąd idą podglądy demo |
| Formularze | **webhook n8n**: `https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture` | wpisany w `assets/site.js` |
| Poczta | Zoho, `kontakt@probatum.pl` | sprawdzona w obie strony |
| Analityka | **brak** | nic nie jest podpięte |

### Jak naprawdę działa formularz — to zaskakuje

Formularze **nie wysyłają e-maili**. Wysyłają dane do n8n pod adres podany
wyżej. Dopiero tam decyduje się, co się z nimi dzieje.

Wysyłane pola: `form_key`, `imie`, `email`, `telefon`, `tresc`, `consent`,
dane kampanii (UTM) oraz `usluga`, `firma`, `www_klienta`, `social_klienta`.

⚠️ **Pole `strona_www` to pułapka na roboty spamujące.** Jest niewidoczne dla
człowieka i ma zostać puste. Nie używaj go do niczego i nie myl z polem
`www_klienta`, które jest prawdziwym adresem strony klienta.

Żeby zmienić, dokąd trafiają zgłoszenia, trzeba wejść do n8n — nie do kodu
strony.

---

## 10. DROBIAZGI, KTÓRE OSZCZĘDZĄ CI GODZINY

**Adresy plików CSS i JS mają doklejony skrót**, np. `site.css?v=db457c16e1`.
Skrót liczy się z zawartości pliku i zmienia tylko wtedy, gdy plik faktycznie
się zmienił. Dzięki temu przeglądarki nie pokazują starej wersji. Nie ruszaj
tego mechanizmu — bez niego ludzie widzą stary wygląd mimo wgranych zmian.

**Generator nie wywala się przy braku pliku** — wypisuje
`POMINIĘTO (brak części): nazwa.html` i idzie dalej. Czytaj to, co wypisuje,
bo inaczej nie zauważysz, że strona się nie zbudowała.

**Blog i Warsztat zawsze pokazują `POMINIĘTO (brak części)`.** Tak ma być —
są budowane z plików `.txt`, nie z `parts/`.

**Na końcu generator wypisuje `--- gotowe: 7 stron`.** Siedem to liczba stron
z `parts/`. Blog, Warsztat i strony wpisów są liczone osobno, wyżej.

---

*Koniec. Jeśli coś w tym dokumencie okaże się nieprawdą — popraw go i wypchnij
razem ze zmianą, której dotyczy.*
