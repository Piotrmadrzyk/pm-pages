# DO ZROBIENIA

Kolejka zadań przy probatum.pl. Kto coś kończy — wykreśla i wypycha razem
ze zmianą.

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
