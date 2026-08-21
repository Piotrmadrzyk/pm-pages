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

## 1. Subdomeny dla stron demonstracyjnych ⏳

**Cel:** żeby demo miały adresy `lawenda.probatum.pl` zamiast
`probatum.pl/p/demo-studio-lawenda/` — krócej, poważniej i bez struktury
katalogów widocznej w pasku adresu.

**Stan na 21 sierpnia 2026:** przygotowane, czeka na dwie rzeczy, których
nie da się zrobić z kodu.

### Co jest już zrobione

Imię i nazwisko zniknęło z adresów. 285 odnośników w 41 plikach zamienionych
na względne — działają na `probatum.pl` i **zadziałają pod subdomenami bez
żadnej kolejnej zmiany w kodzie**. To był warunek konieczny; gdyby linki
zostały sztywne, każda subdomena wyrzucałaby ludzi z powrotem na github.io.

### Co trzeba zrobić — po kolei

**Krok 1 — DNS u rejestratora domeny probatum.pl.**
Dla każdej subdomeny wpis typu CNAME:

```
lawenda      CNAME  cname.vercel-dns.com
kancelaria   CNAME  cname.vercel-dns.com
remonty      CNAME  cname.vercel-dns.com
warsztat     CNAME  cname.vercel-dns.com
```

*(Dokładną wartość CNAME poda Vercel przy dodawaniu domeny — powyższa jest
typowa, ale sprawdź w panelu, bo bywa inna dla różnych kont.)*

**Krok 2 — dodać każdą subdomenę w Vercelu**, w projekcie
`przewagametoda-preview`, zakładka Domains.

**Krok 3 — włączyć przygotowaną konfigurację.**
W repozytorium leży gotowy plik **`vercel.json.przyklad`**. Po wykonaniu
kroków 1 i 2 wystarczy zmienić mu nazwę na `vercel.json` i wypchnąć:

```bash
git mv vercel.json.przyklad vercel.json
git commit -m "Subdomeny demo wlaczone"
git push
```

Od tego momentu `lawenda.probatum.pl` pokazuje stronę główną salonu.

### ⚠️ Czego ta konfiguracja NIE robi — i dlaczego

Skraca **tylko adres główny** subdomeny. Po kliknięciu w „Kontakt" adres
zrobi się `lawenda.probatum.pl/p/demo-studio-lawenda-kontakt/` — działa,
ale nie jest ładny.

Powód: podstrony każdego demo leżą w osobnych katalogach obok siebie
(`demo-studio-lawenda`, `demo-studio-lawenda-kontakt`, `-zabiegi`, `-zespol`),
a nie jeden w drugim. Gdyby przepisywać wszystkie adresy pod subdomeną,
odnośniki prowadzące do `/p/...` zapętliłyby się w kółko.

**Żeby skrócić też podstrony**, trzeba dodatkowo:
1. dopisać reguły `/kontakt → /p/demo-studio-lawenda-kontakt/` dla każdej
   podstrony każdego demo (to jakieś 16 reguł),
2. przerobić odnośniki wewnątrz demo z `../../p/demo-x-kontakt/` na `/kontakt`.

Ale wtedy **demo przestaną działać pod adresem `probatum.pl/p/...`** — będą
działać wyłącznie pod swoimi subdomenami. To jest do zrobienia, tylko musi
być świadomą decyzją: subdomena staje się jedynym adresem demo, a podglądy
w katalogach funkcji trzeba przestawić na nią.

Moja rada: najpierw uruchomić wersję prostą i zobaczyć, czy subdomeny
w ogóle się przyjmą. Skracanie podstron to pół godziny, ale dopiero wtedy,
gdy DNS działa.

### Dlaczego jeden projekt, a nie pięć

Vercel potrafi rozpoznać, spod jakiej domeny przyszedł gość, i podać mu inny
katalog. Dzięki temu **nie trzeba zakładać osobnego projektu na każde demo** —
wszystko zostaje w jednym repozytorium, z jednym wdrożeniem i jedną historią
zmian. Pięć projektów to pięć miejsc do pilnowania.

### ⚠️ Zielona Pergola — osobny przypadek

Pergola nadal linkuje do `piotrmadrzyk.github.io/radosc-website-preview/`,
bo mieszka w innym repozytorium i **waży 367 MB w samych zdjęciach** — nie da
się jej wciągnąć do `pm-pages` bez rozdęcia repozytorium do ponad pół gigabajta.

Do zrobienia osobno: wdrożyć repozytorium `radosc-website-preview` jako własny
projekt na Vercelu i podpiąć pod `pergola.probatum.pl`. Dopiero wtedy zniknie
ostatnie miejsce z nazwiskiem w adresie (3 odnośniki: dwa na stronie głównej
i jeden na Realizacjach).

---

## 2. Katalogi funkcji — treść do przejrzenia ⏳

`build/katalogi.py` zawiera 56 opisów funkcji istniejących i 65 propozycji
rozbudowy. Napisane na podstawie tego, co faktycznie jest w demo, ale **nie
były przeglądane przez właściciela**. Zwłaszcza część „co można dodać" może
wymagać przestawienia — to ma być lista tego, co realnie się sprzedaje,
a nie tego, co technicznie możliwe.

Zmiana jednej pozycji to jedna linijka w `build/katalogi.py`, potem
`cd build && python3 katalogi.py`.

---

## 3. Pergola na wspólnym mechanizmie katalogu ⏳

Katalog Pergoli (`radosc-website-preview/oferta.html`) chodzi na własnym,
starszym mechanizmie — całość wklejona w jeden plik. Pozostałe cztery używają
wspólnego `assets/katalog.{css,js}` i są generowane.

Nie pali się: Pergola działa. Ale dopóki tak zostanie, każda poprawka
mechanizmu wymaga zrobienia jej dwa razy.

---

*Założone 21 sierpnia 2026.*
