# Probatum v11 — paczka do integracji i publikacji

Data paczki: 8 września 2026 r.  
Źródło wersji: commit `39056a054056770bfa6c6f26965a9d626b0f1bae`.  
Zatwierdzony podgląd: `https://probatum-nowy-rozdzial.piotr-madrzyk13.chatgpt.site`.

## Co jest w paczce

- `site-v11/dist/` — dokładny, gotowy wynik: 17 statycznych stron i wszystkie zasoby.
- `site-v11/*.py` — generator nowej strony; `python3 compose.py` odtwarza `dist/`.
- `site-v11/tests/` i `validate.py` — kontrole struktury oraz zachowania skryptów.
- `site-v11/README.md` — opis komponentów, animacji, pochodzenia materiałów i ograniczeń testów.
- `production-reference/` — kontekst starej produkcji. `vercel.json.REFERENCE-ONLY` służy wyłącznie do porównania; nie wolno kopiować go nad aktualny plik z repozytorium.
- `DIST_SHA256SUMS.txt` — sumy kontrolne gotowego wyniku.

W paczce celowo nie ma `.git`, `node_modules`, sekretów, konfiguracji prywatnego hostingu ani katalogu klientów `p/`.

## Najważniejsze fakty o wersji v11

- Strona jest statyczna: HTML, CSS, JS; generator wymaga tylko biblioteki standardowej Pythona.
- Vite jest wyłącznie wygodnym podglądem deweloperskim.
- Wersja podglądowa ma `noindex,nofollow` i blokujący `robots.txt`. Przed publiczną publikacją trzeba świadomie przygotować produkcyjne SEO.
- Formularze v11 przygotowują wiadomość `mailto:` w przeglądarce i niczego same nie wysyłają.
- Strona nie ma własnej analityki, skryptów reklamowych, `localStorage`, `sessionStorage` ani kodu ustawiającego cookies.
- Podglądy Edward Janusz i Silver & Glass ładują zewnętrzny `iframe` dopiero po kliknięciu. Informacja o tym znajduje się na stronie `cookies.html` i obok przycisku podglądu.
- Nigdzie w publicznej treści nie wolno dodawać imienia i nazwiska właściciela.

## Granice produkcji — bez wyjątków

Aktualnym źródłem prawdy jest bieżący `origin/main` repozytorium `pm-pages`, a nie stary stan z dokumentu referencyjnego.

1. Nie kasować ani nie zastępować aktualnego `strona/vercel.json`.
2. Nie kasować, nie przenosić i nie przebudowywać `strona/p/`.
3. Zachować `.vercelignore`, `SUBDOMENY.md` oraz reguły hostów dla:
   - `lawenda-demo.probatum.pl`,
   - `kancelaria-demo.probatum.pl`,
   - `remonty-demo.probatum.pl`,
   - `warsztat-demo.probatum.pl`.
4. Nie dotykać osobnych projektów Akademii AI, Zielonej Pergoli, Edwarda Janusza ani Silver & Glass.
5. Do `main` zapisuje również inny agent. Bezpośrednio przed finalnym pushem wykonać `git pull --rebase origin main`. Konfliktów w plikach chronionych nie rozwiązywać na skróty.
6. Nie kopiować całego ZIP-a na katalog produkcyjny. Wdrożyć wyłącznie nowy serwis firmowy, zachowując infrastrukturę i katalogi klientów z aktualnego repozytorium.

## Zalecana integracja

1. Rozpakować paczkę do katalogu tymczasowego poza repozytorium.
2. W repozytorium pobrać aktualny `origin/main`, sprawdzić czysty stan i utworzyć osobną gałąź `preview/probatum-v11`.
3. Zachować generator jako źródło nowej wersji, np. w dedykowanym `strona/build-v2/`. Dodać bezpieczny krok publikacyjny, który:
   - generuje wynik do katalogu tymczasowego,
   - kopiuje na publiczny poziom `strona/` tylko pliki wymienione w manifeście nowej strony,
   - nigdy nie operuje na `strona/p/`, `vercel.json`, `.vercelignore` ani innych katalogach klientów,
   - usuwa wyłącznie stare pliki, które były wcześniej zarządzane przez ten sam manifest v2.
4. Nie utrzymywać dwóch rozbieżnych generatorów tej samej strony. Stary generator może pozostać jako archiwum, ale zwykłe polecenie budowania produkcji ma odtwarzać wersję v11, a nie przywracać poprzedni wygląd.
5. Zachować wszystkie 17 tras, zasoby i animacje. Nie przetwarzać ponownie historycznych oryginałów. Koloryzację AI i projekt Horyzont nadal oznaczać jako koncepcyjne.

## Formularze — decyzja techniczna przed publikacją

Produkcja wcześniej korzystała z endpointu n8n `pm-lead-capture` i rozpoznawała `form_key`: `kontakt`, `wycena`, `lista-agenty`. Wersja v11 celowo używa uczciwego `mailto:`.

Najlepszy wariant produkcyjny: zachować wygląd i pola v11, a działającą wysyłkę podłączyć do istniejącego endpointu wyłącznie po potwierdzeniu aktualnego kontraktu. Dla kontaktu i wyceny użyć istniejących kluczy; nie wymyślać nowego `form_key`. Pokazywać sukces dopiero po odpowiedzi 2xx, błąd po niepowodzeniu oraz zachować e-mail i telefon jako wyraźny wariant awaryjny.

Jeśli nie da się potwierdzić kontraktu lub odbioru kontrolnego zgłoszenia, nie udawać działającej wysyłki. Pozostawić `mailto:` dokładnie jak w v11 i odnotować ograniczenie. Po zmianie działania formularzy zaktualizować `cookies.html`, ponieważ obecny opis mówi prawdziwie, że dane nie są wysyłane na serwer.

Nie wysyłać danych prawdziwego klienta w testach. Użyć jednoznacznie oznaczonych danych syntetycznych. Nie uruchamiać innych workflowów.

## Cookies, prywatność i SEO

- Najpierw sprawdzić faktyczne żądania sieciowe i cookies na Vercel Preview. Nie wpisywać nazw ani czasu życia cookies na podstawie przypuszczeń.
- Nie dodawać banera „Akceptuję”, jeśli na stronie nie ma opcjonalnej analityki ani reklamowych cookies. Jeśli zostanie dodana analityka lub piksel, muszą być zablokowane do zgody, z równorzędnymi opcjami akceptacji i odmowy.
- Dopasować `cookies.html` do rzeczywistego hostingu i ostatecznej obsługi formularzy.
- Pełnej polityki prywatności ani danych administratora nie wymyślać. Brak wymaganych danych prawnych zgłosić jako konkretny blocker.
- Dla publicznego `probatum.pl` usunąć `noindex,nofollow`, ustawić `robots.txt` na indeksowanie, dodać sitemapę, poprawne adresy kanoniczne oraz metadane Open Graph. Nie indeksować tras technicznych ani podglądowych.
- Zachować dotychczasowe publiczne adresy lub dodać przekierowania w ramach istniejącego systemu `routes`; nie mieszać niezgodnych sekcji konfiguracji Vercela.

## Kontrola przed `main`

Uruchomić:

```bash
python3 compose.py
python3 validate.py
node tests/studio-runtime.cjs
```

Następnie sprawdzić Vercel Preview co najmniej w szerokościach 320, 390, 768 i 1440 px:

- wszystkie 17 tras i menu,
- start: drzewo bez zielonego przycisku „Oferta”,
- osobne otwarcia Wiedzy, Akademii i Kontaktu,
- samochód, agenci, Horyzont, projekty, pauzy i ponowne odtwarzanie,
- formularze, komunikaty błędów i wariant bez JavaScript,
- brak poziomego przewijania i nachodzenia dolnego paska,
- klawiaturę, fokus i `prefers-reduced-motion`,
- brak danych właściciela w HTML, metadanych i skryptach,
- brak 404 oraz brak niezamierzonych żądań do usług zewnętrznych.

Porównać zawartość `p/` i aktualny `vercel.json` przed i po integracji. Nie mogą się zmienić.

## Publikacja i wycofanie

1. Zapisać identyfikator obecnego wdrożenia produkcyjnego jako punkt powrotu.
2. Opublikować gałąź preview i sprawdzić ją przed finalnym pushem.
3. Tuż przed publikacją: pobrać najnowszy `main`, zrobić rebase, ponownie zbudować i uruchomić kontrole.
4. Wypchnąć zweryfikowany stan do `main` i poczekać na zakończenie wdrożenia Vercela.
5. Sprawdzić `probatum.pl`, `www.probatum.pl` i cztery subdomeny demonstracyjne. Przy regresji natychmiast wycofać wdrożenie do zapisanego punktu.

## Kryterium GOTOWE

Zadanie jest gotowe dopiero wtedy, gdy:

- nowy Probatum działa publicznie pod `probatum.pl` i odpowiada wersji v11;
- wszystkie 17 tras działają, produkcja może być indeksowana, a linki i zasoby nie zwracają 404;
- formularze są albo potwierdzone od początku do odbioru, albo uczciwie pozostawione jako `mailto:`;
- treść o cookies odpowiada faktycznemu działaniu wdrożenia;
- `vercel.json`, `p/` i cztery subdomeny działają bez zmian;
- nie ma danych właściciela w publicznej treści;
- istnieje odnotowany punkt wycofania;
- raport końcowy podaje URL, commit, wdrożenie, wyniki testów oraz wszystkie nierozwiązane ograniczenia.
