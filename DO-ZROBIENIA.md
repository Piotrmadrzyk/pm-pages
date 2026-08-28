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

## 1. Subdomeny dla stron demonstracyjnych ⏳ — czeka na DNS

**Stan na 28 sierpnia 2026:** konfiguracja `vercel.json` jest już w repozytorium
i aktywna. Reguły zadziałają w momencie, w którym subdomeny zaczną kierować
na ten projekt. Do tego czasu plik nic nie zmienia.

### Zostały dwa kroki i oba są po stronie właściciela

**Krok 1 — wpisy w panelu home.pl** (tam siedzi DNS domeny probatum.pl):

```
lawenda-demo      CNAME   cname.vercel-dns.com
kancelaria-demo   CNAME   cname.vercel-dns.com
remonty-demo      CNAME   cname.vercel-dns.com
warsztat-demo     CNAME   cname.vercel-dns.com
```

**Krok 2 — dodanie tych domen w Vercelu**, w projekcie `przewagametoda-preview`,
zakładka **Domains**. Vercel poda tam dokładną wartość CNAME — jeśli będzie inna
niż powyżej, użyj tej z panelu.

Wpisy DNS potrafią się rozchodzić po świecie od kilkunastu minut do kilku godzin.

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
