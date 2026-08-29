# DO ZROBIENIA

Kolejka zadań przy probatum.pl. Kto coś kończy — wykreśla i wypycha razem
ze zmianą.

---

## 0. ✅ FORMULARZE DZIAŁAJĄ — naprawione 29 sierpnia 2026

Do 29.08 każde zgłoszenie z probatum.pl przepadało: workflow **Lead Capture
(Etap 3D)** (`HwH2M5e12fug5xLW`) szukał kampanii w `PM_kampanie` po kolumnie
`form_key`, nie znajdował wiersza i odsyłał 422.

**Co zrobiłem:** dopisałem dziewięć wierszy do `PM_kampanie`
(id `NKeLThYjECSaG3fH`) — po jednym na każdy klucz używany na stronach.
Każdy wiersz ma wypełnione `form_key`, `campaign_id`, `kampania_id`, `nazwa`
i `typ`. `sequence_id` zostawiłem **puste celowo**: dopóki jest puste, żadne
zgłoszenie nie uruchamia sekwencji mailowej do klienta.

| klucz | campaign_id | skąd wychodzi | test |
|---|---|---|---|
| `kontakt` | probatum-kontakt | podstrona Kontakt | ✅ 200 |
| `wycena` | probatum-wycena | podstrona Wyceń projekt | ✅ 200 |
| `lista` | probatum-lista | zapis na listę mailową | ✅ 200 |
| `lista-agenty` | probatum-lista-agenty | lista pierwszeństwa, Agenci | ✅ 200 |
| `katalog-lawenda` | katalog-lawenda | katalog Studia Lawenda | ✅ 200 |
| `katalog-zawadzcy` | katalog-zawadzcy | katalog Kancelarii Zawadzcy | ✅ 200 |
| `katalog-dom` | katalog-dom | katalog Dom i Wnętrze | ✅ 200 |
| `katalog-serwis` | katalog-serwis | katalog Serwisu Podkarpackiego | ✅ 200 |
| `opony-sezon` | opony-sezon | zapis na opony, demo Serwisu | ✅ 200 |

Sprawdzone dwa razy: curlem po każdym kluczu **oraz** przez prawdziwy
formularz na żywej stronie `probatum.pl/kontakt.html` — wyszedł komunikat
„Dziękuję za wiadomość".

### ✅ `opony-sezon` też działa — walidacja poluzowana 29.08

Ten klucz **nie był na wcześniejszej liście ośmiu** — znalazłem go przy okazji
w `p/demo-serwis-podkarpacki/index.html`. Formularz „zostaw telefon,
oddzwonimy" wysyła pusty adres e-mail, a walidacja wymagała adresu.

Piotr zgodził się to poluzować. Zmienione trzy węzły w `HwH2M5e12fug5xLW`,
**bez ruszania schematu tabel**:

- **„Walidacja i normalizacja"** — wystarczy poprawny e-mail **albo** numer
  telefonu (min. 9 cyfr). Zgoda nadal obowiązkowa. Adres wpisany z literówką
  nie wchodzi do kolumny `email` (poszłaby na niego przyszła wysyłka), ale nie
  ginie: dopisuje się do treści zgłoszenia.
- **„Szukaj duplikatu"** — filtruje już tylko po `campaign_id`, z Return All.
- **„Decyzja dedup"** — porównanie przeniesione do kodu. Jest e-mail →
  porównuje adresy, dokładnie jak dotąd. Nie ma → porównuje same cyfry
  telefonu. Bez mieszania: dwie osoby z jednego telefonu firmowego, ale
  różnymi adresami, to nadal dwa osobne zgłoszenia.
- **„Odpowiedz: duplikat"** — zdanie zależy od tego, co się powtórzyło.
  Wcześniej komuś, kto zostawił sam numer, wyskakiwało „ten adres e-mail jest
  już zapisany" i wyglądało to na pomyłkę formularza.

Workflow **opublikowany** (`activeVersionId` = `b734b459…`), nie tylko
zapisany jako wersja robocza.

### Sprawdzone po zmianie — siedem ścieżek

| co | wynik |
|---|---|
| samo imię i telefon, bez e-maila | ✅ przechodzi |
| ten sam telefon drugi raz (ze spacjami) | ✅ DUPLIKAT |
| **inny** telefon w tej samej kampanii | ✅ nowy, nie duplikat |
| e-mail bez telefonu (droga wszystkich pozostałych formularzy) | ✅ przechodzi jak dotąd |
| ten sam e-mail drugi raz | ✅ DUPLIKAT |
| ani e-maila, ani telefonu | ✅ 422 z prośbą o jedno z dwóch |
| bez zgody | ✅ 422 o zgodzie |
| e-mail z literówką + poprawny telefon | ✅ przechodzi, adres ląduje w treści |

Na koniec przepuszczona jeszcze raz **cała dziewiątka kluczy** — wszystkie OK.

### Zgłoszenia testowe do skasowania

Testy zapisały dziesięć leadów w `PM_leady` i wysłały tyle samo powiadomień
na skrzynkę. Wszystkie mają w treści „Test" i datę 29.08.2026, adresy w domenie
`@probatum.pl` z przedrostkiem `test-`. Nic nie kasuję — do przejrzenia
i usunięcia ręcznie:

```
lead_1787996565119_28001   kontakt
lead_1787996569833_74690   wycena
lead_1787996573061_75994   lista
lead_1787996577369_53428   lista-agenty
lead_1787996580520_58949   katalog-lawenda
lead_1787996584342_47287   katalog-zawadzcy
lead_1787996588634_28442   katalog-dom
lead_1787996592651_58186   katalog-serwis
lead_1787996612828_55050   opony-sezon
```
plus zgłoszenia z drugiej tury testów (po poluzowaniu walidacji):

```
lead_1787997677803_88117   opony-sezon, sam telefon 600100200
lead_1787997686063_424     opony-sezon, sam telefon 600100999
lead_1787997710286_14136   kontakt, test-po-zmianie@probatum.pl
lead_1787997726354_24174   opony-sezon, telefon 600100777 + literówka w mailu
```

oraz jeden z prawdziwego formularza na stronie (imię „TEST TECHNICZNY —
Claude") i dziewięć z kontroli końcowej — te ostatnie mają imię
„Kontrola koncowa" i adresy `kontrola-…@probatum.pl`.

Razem **dwadzieścia trzy zgłoszenia testowe**. Wszystkie mają w treści słowo
„Test" albo „Kontrola" i datę 29.08.2026. Nic nie kasuję.

### Jak sprawdzić, gdyby znowu przestało działać

```bash
curl -s -X POST "https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture" \
 -H "Content-Type: application/json" \
 -d '{"form_key":"kontakt","imie":"Test","email":"test@probatum.pl",
      "telefon":"000000000","tresc":"Test — mozna skasowac","consent":true}'
```

Ma odpowiedzieć `{"status":"OK","lead_id":"lead_..."}`. Jeśli 422 z komunikatem
o źle skonfigurowanym formularzu — brakuje wiersza w `PM_kampanie` albo klucz
nie zgadza się co do znaku.

---

## 1. Strona Agnieszki Lewandowskiej — pierwsza realna klientka 🟠

Pełny opis: **`NEWAGE-LEWANDOWSKA.md`**. Podgląd:
<https://probatum.pl/p/newage-lewandowska/>

Trzynaście podstron, generator `build/newage.py`. Zrobione: menu, dyplomy,
portfolio, poradnik pod SEO, opinie z Google, formularz wyceny, polityka
prywatności, dane strukturalne, dok na telefonie.

**Czeka:**

1. **Workflow w n8n dla dwóch formularzy** — `newage-kontakt` (zapytanie
   o termin i cenę) oraz `newage-opinia`. Bez nich formularze nie działają.
2. **Zdjęcie `noindex`** przed uruchomieniem — inaczej całe SEO jest bez
   znaczenia. Siedzi w `SZKIELET` w generatorze.
3. **Domena `newagelewandowska.pl`** — sprawdzona w rejestrze NASK
   29.08.2026, **wolna**. Kupuje Agnieszka, na swoje dane.
4. **Zgody na zdjęcia** — metamorfozy klientek oraz prawa do zdjęć
   z magazynu SPLOT (fot. Elżbieta Bednarek).
5. Zdjęcia z sesji w salonie, którą miała w poniedziałek.

---

## 2. Subdomeny dla stron demonstracyjnych ✅ — DNS gotowy

**Stan na 28 sierpnia 2026:** zrobione po obu stronach.

- **Vercel** — cztery domeny dodane w projekcie `przewagametoda-preview`
  (środowisko Production).
- **home.pl** — cztery rekordy CNAME dodane do strefy `probatum.pl`, wszystkie
  na `f159e593438ec538.vercel-dns-017.com.` Rozeszły się od razu; certyfikaty
  HTTPS wystawione. Pozostałe 8 rekordów (MX Zoho, SPF, DKIM, weryfikacja,
  A i www) nietknięte — sprawdzone po zmianie.

**Zostało:** wypchnąć `vercel.json` z regułami przepisania. Do tego czasu
wszystkie cztery subdomeny odpowiadają, ale pokazują stronę główną Probatum
zamiast właściwego demo.

### Co gdzie trafi

| adres | pokazuje |
|---|---|
| `lawenda-demo.probatum.pl` | Studio Lawenda |
| `kancelaria-demo.probatum.pl` | Kancelaria Zawadzcy |
| `remonty-demo.probatum.pl` | Dom i Wnętrze |
| `warsztat-demo.probatum.pl` | Serwis Podkarpacki |

### Dlaczego z końcówką „-demo"

Te firmy są zmyślone, ale ich nazwy są wiarygodne — „Zielona Pergola" mogłaby
istnieć naprawdę. Postawienie pod adresem bez dopisku strony firmy, która nie
istnieje, mogłoby kiedyś wprowadzić kogoś w błąd albo ściągnąć pretensje
prawdziwego lokalu o tej nazwie. Końcówka `-demo` zdejmuje to ryzyko i nic
nie kosztuje.

### Droga B — skrócenie także podstron

Dziś subdomena skraca **tylko adres główny**. Po kliknięciu w „Kontakt" adres
zrobi się `lawenda-demo.probatum.pl/p/demo-studio-lawenda-kontakt/` — działa,
ale nie jest ładny.

Powód: podstrony każdego demo leżą w osobnych katalogach **obok siebie**
(`demo-studio-lawenda`, `demo-studio-lawenda-kontakt`, `-zabiegi`, `-zespol`),
a nie jeden w drugim.

Żeby dostać `lawenda-demo.probatum.pl/kontakt`, trzeba przenieść podstrony
do środka katalogu demo i poprawić odnośniki. To kilka godzin roboty i ma sens
dopiero wtedy, gdy droga A już stoi i wiadomo, że subdomeny się sprawdzają.

### 🟠 Zielona Pergola — projekt gotowy, czeka na JEDEN wpis DNS

**29.08.2026.** Piotr: *„zajmij się zieloną pergolą, bo nie jest jako jedyna
na subdomenie jak pozostałe"*.

Zrobione po stronie Vercela — **zostaje tylko DNS, którego nie mogę dodać sam**
(panel home.pl wymaga hasła, a haseł nie wpisuję).

**Wpis do dodania w home.pl, w DNS domeny `probatum.pl`:**

```
Typ:      CNAME
Nazwa:    pergola-demo
Wartość:  8e964240c76d181b.vercel-dns-016.com.
```

Tyle. Certyfikat Vercel wystawi sam, gdy wpis się rozejdzie. Gdyby po godzinie
nadal pokazywał „Invalid Configuration", trzeba wywołać
`npx vercel certs issue pergola-demo.probatum.pl --scope piotrs-projects-82784815`
— tak było przy `akademia.probatum.pl`.

**Uwaga:** to **inna wartość** niż przy czterech pozostałych demach
(`f159e593438ec538.vercel-dns-017.com`). Każdy projekt Vercela dostaje własną —
nie da się przekopiować tamtej.

### Co zostało zrobione po drodze

- Założony projekt Vercel **`pergola-demo`**, podpięty pod repozytorium
  `piotrmadrzyk/radosc-website-preview`.
- **Pułapka, w którą wpadłem:** Vercel domyślnie wziął gałąź `main`, a na niej
  leży **stara wersja strony** — „Radość — Bistro, Pizza i Catering, Jasionka
  k. Rzeszowa", czyli wcześniejsza, nie-fikcyjna nazwa. Obecne demo („Zielona
  Pergola, Zielony Gaj k. Lipowa") żyje na `preview/redesign-2026`. Projekt
  **wstrzymałem w ciągu paru minut**, żeby ta wersja nie poszła w świat,
  przestawiłem gałąź produkcyjną i dopiero wtedy odwiesiłem.
- Domena `pergola-demo.probatum.pl` dodana do projektu, czeka na DNS.
- **Sprawdzone na Vercelu:** strona główna, `kontakt`, `catering`, `pizza`,
  `opinie`, `realizacje` i zdjęcia — wszystko HTTP 200. 371 MB zbudowało się
  w 28 sekund, więc obawa o rozmiar była nieuzasadniona.
- **GitHub Pages działa dalej bez zmian** i celowo tego nie ruszałem: gdybym
  ustawił tam własną domenę przed dodaniem DNS, obecny adres demo
  przekierowywałby na adres, który jeszcze nie istnieje — czyli demo
  zniknęłoby na czas oczekiwania.

### ⚠️ Do zrobienia PO tym, jak subdomena zacznie działać

W plikach strony siedzi **55 miejsc** z adresami
`https://piotrmadrzyk.github.io/radosc-website-preview/...` — w tagach
`canonical`, Open Graph, danych strukturalnych i mapie strony. Po uruchomieniu
subdomeny trzeba je przepisać na `https://pergola-demo.probatum.pl/...`,
inaczej strona sama wskazuje wyszukiwarkom stary adres.

Nie zrobiłem tego z góry, bo dopóki subdomena nie działa, te adresy byłyby
błędne.

---

## 3. Bloki prawne w demach ✅ — zrobione 28 sierpnia 2026

Wszystkie 17 stron czterech dem ma teraz regulamin, politykę prywatności
i pasek informacji o ciasteczkach. Generuje to `build/prawne.py`
(opis w `JAK-DZIALA-PROBATUM.md`, sekcja 7b).

Treści są szablonowe — firmy w demach są zmyślone — i każdy regulamin kończy
się zdaniem, które mówi to wprost.

**Do przejrzenia przez właściciela:** czy zapisy w regulaminach brzmią tak,
jak chce sprzedawać. Zwłaszcza terminy odwołania wizyty u Lawendy (24 h),
gwarancja u Serwisu (12 miesięcy na robociznę) i gwarancja u Domu i Wnętrza
(24 miesiące). To liczby wzięte z typowej praktyki, nie z jego ustaleń.

---

## 4. Dema sprzedają same siebie ✅ — zrobione 28 sierpnia 2026

Każde z 17 stron ma pasek „Ta strona jest do wzięcia" nad stopką: mówi, że
firma jest zmyślona, i daje przycisk rezerwacji plus link do katalogu funkcji.
Wszystkie maile i telefony w demach prowadzą teraz do Probatum — wcześniej
zainteresowany klient pisał na nieistniejący adres i przepadał.

Generuje to `build/demo_sprzedaz.py` (opis w `JAK-DZIALA-PROBATUM.md`, 7c).

**Do decyzji właściciela:** przycisk prowadzi dziś do maila, bo formularze
nie działają (punkt 0). Po ich naprawie warto go przełączyć na formularz
wyceny — wtedy zgłoszenie trafi do systemu, a nie do skrzynki.

---

## 5. 🔴 Pergola miała publicznie prywatny gmail — naprawione, czeka na push

**Znalezione 28 sierpnia 2026.**

Na 18 stronach Zielonej Pergoli (polskich i angielskich) widniał **prywatny
gmail właściciela i jego numer telefonu** — na ekranie, w odnośnikach
`mailto:` i `tel:`, oraz w danych strukturalnych JSON-LD, które czytają
wyszukiwarki. Strona stoi publicznie na GitHub Pages.

Pergola została pominięta przy poprzednim porządkowaniu kontaktów, bo **mieszka
w osobnym repozytorium** (`piotrmadrzyk/radosc-website-preview`) i na innym
hostingu niż reszta stron. To jest ta pułapka: zmiana zrobiona „wszędzie"
w pm-pages nie dotyka niczego poza pm-pages.

### Co zostało zrobione

- wszystkie kontakty przestawione na `kontakt@probatum.pl` i `573 569 141`,
- dodany pasek sprzedażowy nad stopką (osobna wersja polska i angielska),
- przepisana linijka na dole stopki.

Robi to `build/demo_sprzedaz.py` **w repozytorium Pergoli**, nie tutaj.

### ⚠️ To jeszcze nie jest opublikowane

Zmiana jest zacommitowana lokalnie, ale nie wypchnięta — nie mam dostępu do
GitHuba. Dopóki nie pójdzie push, prywatny adres **nadal jest widoczny w sieci**.

Publikacja odbywa się przez GitHub Actions po pushu na gałąź
`preview/redesign-2026` (workflow `deploy-pages.yml`) — nie na `main`.

### Gdzie leży Pergola

```
~/Projekty/radosc-website-preview     (933 MB, pełna historia — 130 commitów)
```

Sklonowana 28 sierpnia 2026 z `github.com/piotrmadrzyk/radosc-website-preview`.
Wcześniej na dysku jej nie było — w koszu leżały niepełne szczątki bez historii
gita (`~/.Trash/radosc-website-preview`, 6,8 MB, sam katalog `.git` brakujący).
Te szczątki można spokojnie skasować, ale to nie pali się.

**Gałąź robocza to `preview/redesign-2026`**, nie `main`. Na niej wisi automat
publikujący (`.github/workflows/deploy-pages.yml`) — push na tę gałąź stawia
stronę na GitHub Pages i podstawia znaczniki `__RADOSC_BUILD_HASH__`
i `__RADOSC_BUILD_TIME__`. Dlatego plik na żywo różni się kilkuset bajtami
od tego w repozytorium; to nie jest rozjazd, tylko ostemplowanie.

### Pergoli nie ma na Vercelu

Sprawdzone 28 sierpnia 2026: konto Vercel ma osiem projektów
(`przewagametoda-preview`, `akademia`, `obiektywyhistorii`, `edward-janusz`,
`receptury`, `pm-command-center`, `pm-panel`, `skrypty`) — **żaden z nich to
nie Pergola**. Stoi wyłącznie na GitHub Pages.

Ma to znaczenie dla punktu o `pergola-demo.probatum.pl`: żeby dostać tę
subdomenę, Pergola potrzebuje **własnego projektu na Vercelu**, a nie
dopisania domeny do istniejącego. Alternatywa to zostawić ją na GitHub Pages
i wskazać subdomenę rekordem CNAME na `piotrmadrzyk.github.io` — wtedy trzeba
dodać plik `CNAME` w repozytorium.

---

## 6. Prywatny adres — przeglad calosci ✅ 28 sierpnia 2026

Po znalezisku w Pergoli przeszukane wszystkie projekty. Wynik:

| gdzie | co bylo | stan |
|---|---|---|
| Pergola — 18 stron HTML | prywatny gmail + numer | ✅ podmienione |
| Pergola — `assets/data/site-config.js` | to samo, **ladowane przez wszystkie 18 stron** | ✅ podmienione |
| Pergola — `js/main.js`, `js/manager.js` | numer w komunikatach bledu | ✅ podmienione |
| Pergola — `llms.txt` | adres i numer podawane **robotom AI** | ✅ podmienione |
| probatum.pl — `p/pm-test-event/` | gmail x4, strona zywa | ✅ podmienione |
| probatum.pl — `p/test-bridge-guard-0815/wersje/w1/` | gmail x2, strona zywa | ✅ podmienione |
| `obiektywyhistorii`, `receptury`, `pm-command-center`, `pm-panel` | — | czysto |

### Czego nauczylo to znalezisko

Poprawienie samego HTML-a **nie wystarczylo**. `site-config.js` trzymal adres
jako konfiguracje i podstawial go w czasie dzialania strony — prywatny adres
wracalby przy kazdym odswiezeniu, mimo poprawionych 18 plikow HTML.
Przy nastepnym takim porzadkowaniu: szukaj takze w `.js`, `.json` i `.txt`,
nie tylko w `.html`.

### Zostalo do decyzji

**Dwie strony testowe sa publiczne i nie prowadzi do nich zaden odnosnik:**
`p/pm-test-event/` i `p/test-bridge-guard-0815/`. Adres zostal z nich zdjety,
ale same strony nie sluza niczemu — mozna je skasowac. Nie zrobilem tego sam,
bo to kasowanie, a nie poprawka.

**W kopiach zapasowych adres nadal jest:** `~/Projekty/kopie-pm` (40 plikow
z `piotr.aparat`, 15 z `piotr.madrzyk13`) i `~/Projekty/pm-backup` (14 plikow).
To katalogi lokalne, nigdzie nie publikowane — nie ruszalem ich, bo kopia
zapasowa ma pokazywac stan z chwili jej zrobienia.

---

## 7. 🟠 probatum.pl nie ma polityki prywatności

**Znalezione 28 sierpnia 2026 przy okazji dem.**

Sama strona probatum.pl — ta, która zbiera prawdziwe zgłoszenia — nie ma:

- polityki prywatności (sprawdzone na żywo: `/polityka-prywatnosci`,
  `/polityka`, `/prywatnosc` — wszystkie 404),
- klauzuli informacyjnej RODO (nigdzie nie pada słowo „Administrator"),
- dokumentu, do którego prowadziłaby zgoda z formularza kontaktowego —
  checkbox jest, treści za nim nie ma.

Strony katalogów zapisują dodatkowo zaznaczenia w pamięci przeglądarki,
bez żadnej wzmianki.

### Co to znaczy dzisiaj

Nic nie wycieka, bo formularze i tak nie działają (punkt 0). Ale **oba punkty
trzeba zamknąć przed uruchomieniem**, nie po — RODO wymaga klauzuli
informacyjnej w momencie zbierania danych, nie później.

### Dlaczego to nie jest zrobione razem z demami

Klauzula musi wskazywać administratora z nazwy i adresu. Przy działalności
jednoosobowej to imię, nazwisko i adres właściciela — czyli dokładnie to,
czego konsekwentnie nie publikuje. Wyjścia są (adres korespondencyjny,
wirtualne biuro, spółka), ale każde ma cenę i **to jest decyzja właściciela
po rozmowie z prawnikiem**, a nie coś, co da się dopisać za niego.

Szkielet polityki — wszystko poza danymi administratora — jest do zrobienia
w pół godziny, gdy tylko ta decyzja zapadnie.

---

## 8. Katalogi funkcji — treść do przejrzenia ⏳

`build/katalogi.py` zawiera 56 opisów funkcji istniejących i 65 propozycji
rozbudowy. Napisane na podstawie tego, co faktycznie jest w demo, ale **nie
były przeglądane przez właściciela**. Zwłaszcza część „co można dodać" może
wymagać przestawienia — to ma być lista tego, co realnie się sprzedaje,
a nie tego, co technicznie możliwe.

Zmiana jednej pozycji to jedna linijka w `build/katalogi.py`, potem
`cd build && python3 katalogi.py`.

---

## 9. Pergola na wspólnym mechanizmie katalogu ⏳

Katalog Pergoli (`radosc-website-preview/oferta.html`) chodzi na własnym,
starszym mechanizmie — całość wklejona w jeden plik. Pozostałe cztery używają
wspólnego `assets/katalog.{css,js}` i są generowane.

Nie pali się: Pergola działa. Ale dopóki tak zostanie, każda poprawka
mechanizmu wymaga zrobienia jej dwa razy.

---

*Założone 21 sierpnia 2026.*
