# DO ZROBIENIA

Kolejka zadań przy probatum.pl. Kto coś kończy — wykreśla i wypycha razem
ze zmianą.

---

## 0. 🔴 ŻADEN FORMULARZ NA STRONIE NIE DZIAŁA

**Znalezione 21 sierpnia 2026 przy testowaniu formularza wyceny w katalogu.**

Każde zgłoszenie z probatum.pl jest odrzucane przez n8n z odpowiedzią:

```
HTTP 422
{"status":"BLAD","wiadomosc":"Nieznany lub brakujacy klucz formularza (form_key)."}
```

Sprawdzone na żywo, po kolei, z pełnym poprawnym zgłoszeniem. **Wszystkie
osiem kluczy odrzuconych**, także te używane od dawna.

### Dlaczego

Workflow **PM Agent OS — Lead Capture (Etap 3D)** (`HwH2M5e12fug5xLW`) po
odebraniu zgłoszenia szuka kampanii w tabeli **`PM_kampanie`** po kolumnie
`form_key`. Jeśli nie znajdzie wiersza — odsyła 422 i **zgłoszenie przepada**.

Znaczy to, że w `PM_kampanie` nie ma wierszy z kluczami, których używa strona
(albo mają inne wartości w kolumnie `form_key` — nie mam narzędzia, żeby
odczytać zawartość tabeli, więc tego nie rozstrzygnę z zewnątrz).

### Klucze, które strona wysyła i które muszą mieć swój wiersz

| klucz | skąd wychodzi |
|---|---|
| `kontakt` | formularz na podstronie Kontakt |
| `wycena` | formularz na podstronie Wyceń projekt |
| `lista` | zapis na newsletter |
| `lista-agenty` | lista pierwszeństwa na podstronie Agenci |
| `katalog-lawenda` | prośba o wycenę w katalogu Studia Lawenda |
| `katalog-zawadzcy` | katalog Kancelarii Zawadzcy |
| `katalog-dom` | katalog Dom i Wnętrze |
| `katalog-serwis` | katalog Serwisu Podkarpackiego |

### Jak to naprawić

W tabeli `PM_kampanie` (n8n, id `NKeLThYjECSaG3fH`) dodać po jednym wierszu
na każdy klucz. Minimum, którego wymaga workflow, to wypełnione:

- **`form_key`** — dokładnie jak w tabeli wyżej,
- **`campaign_id`** — dowolny własny identyfikator, np. `probatum-kontakt`;
  po nim odróżnisz źródło leada i po nim działa odsiewanie duplikatów.

Reszta kolumn (`sequence_id`, `slug`, `nadawca`) może zostać pusta — workflow
sobie z tym radzi. `sequence_id` wypełnij tylko wtedy, gdy dane zgłoszenie
ma uruchamiać sekwencję mailową.

### ⚠️ Czego świadomie NIE zrobiłem

**Nie dopisałem tych wierszy sam.** `PM_kampanie` to twoje dane produkcyjne
w systemie, który budujesz równolegle w innym miejscu — dopisanie kampanii
zmienia sposób przypisywania leadów i to jest twoja decyzja, nie moja.
Zgłoszenie testowe, które wysłałem, zostało odrzucone, więc **nic nie zapisało
się w PM_leady**.

### Jak sprawdzić, czy naprawione

```bash
curl -s -X POST "https://pmresearch.app.n8n.cloud/webhook/pm-lead-capture" \
 -H "Content-Type: application/json" \
 -d '{"form_key":"kontakt","imie":"Test","email":"test@probatum.pl",
      "telefon":"000000000","tresc":"Test — mozna skasowac","consent":true}'
```

Ma odpowiedzieć `{"status":"OK","lead_id":"lead_..."}`. Jeśli dalej 422 —
klucz w tabeli nie zgadza się co do znaku.

**Dopóki to nie jest naprawione, uruchomienie strony na właściwej domenie
nie ma sensu — każde zapytanie od klienta przepadnie bez śladu.**

---

## 1. Subdomeny dla stron demonstracyjnych ✅ — DNS gotowy

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

### ⚠️ Zielona Pergola — nadal osobno

Mieszka w repozytorium `radosc-website-preview` i **waży 367 MB w samych
zdjęciach**, więc nie da się jej wciągnąć do `pm-pages`. Potrzebuje własnego
projektu w Vercelu, podpiętego pod `pergola-demo.probatum.pl`.
Do założenia jednym poleceniem — czeka na decyzję właściciela.

---

## 2. Bloki prawne w demach ✅ — zrobione 28 sierpnia 2026

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

## 3. Dema sprzedają same siebie ✅ — zrobione 28 sierpnia 2026

Każde z 17 stron ma pasek „Ta strona jest do wzięcia" nad stopką: mówi, że
firma jest zmyślona, i daje przycisk rezerwacji plus link do katalogu funkcji.
Wszystkie maile i telefony w demach prowadzą teraz do Probatum — wcześniej
zainteresowany klient pisał na nieistniejący adres i przepadał.

Generuje to `build/demo_sprzedaz.py` (opis w `JAK-DZIALA-PROBATUM.md`, 7c).

**Do decyzji właściciela:** przycisk prowadzi dziś do maila, bo formularze
nie działają (punkt 0). Po ich naprawie warto go przełączyć na formularz
wyceny — wtedy zgłoszenie trafi do systemu, a nie do skrzynki.

---

## 4. 🔴 Pergola miała publicznie prywatny gmail — naprawione, czeka na push

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

## 5. 🟠 probatum.pl nie ma polityki prywatności

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

## 6. Katalogi funkcji — treść do przejrzenia ⏳

`build/katalogi.py` zawiera 56 opisów funkcji istniejących i 65 propozycji
rozbudowy. Napisane na podstawie tego, co faktycznie jest w demo, ale **nie
były przeglądane przez właściciela**. Zwłaszcza część „co można dodać" może
wymagać przestawienia — to ma być lista tego, co realnie się sprzedaje,
a nie tego, co technicznie możliwe.

Zmiana jednej pozycji to jedna linijka w `build/katalogi.py`, potem
`cd build && python3 katalogi.py`.

---

## 7. Pergola na wspólnym mechanizmie katalogu ⏳

Katalog Pergoli (`radosc-website-preview/oferta.html`) chodzi na własnym,
starszym mechanizmie — całość wklejona w jeden plik. Pozostałe cztery używają
wspólnego `assets/katalog.{css,js}` i są generowane.

Nie pali się: Pergola działa. Ale dopóki tak zostanie, każda poprawka
mechanizmu wymaga zrobienia jej dwa razy.

---

*Założone 21 sierpnia 2026.*
