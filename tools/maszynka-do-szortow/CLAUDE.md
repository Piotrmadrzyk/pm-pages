# Maszynka do szortsów — pamięć projektu

Lokalne narzędzie (Node.js + panel w przeglądarce) do generowania krótkich
pionowych wideo (shorts) dla Probatum. Zbudowane 21.09.2026 wg
`zakres-prac.md` w tym samym folderze — przeczytaj go, jeśli potrzebujesz
kontekstu decyzji biznesowych (branding, brak twarzy, brak muzyki, źródło
treści itd.).

## Jak uruchomić

```
cd tools/maszynka-do-szortow
npm install
cp .env.example .env   # wklej DONA_N8N_SHARED_SECRET (patrz nizej)
npm start               # http://localhost:3000
```

## Struktura

- `server/index.js` — Express: statyczny panel + REST API (projekty,
  sceny, reorder, ElevenLabs, zapis renderu).
- `server/store.js` — persystencja w plikach JSON (`data/projects/*.json`),
  bez bazy danych.
- `server/elevenlabs.js` — TTS + sound generation, ale **nie woła już
  ElevenLabs bezpośrednio** (patrz sekcja „Integracja z n8n zamiast
  lokalnego klucza ElevenLabs” niżej).
- `public/index.html` + `styles.css` + `app.js` — panel: lista
  projektów, edycja scen (drag&drop reorder przez natywne HTML5 DnD),
  podgląd na `<canvas>`, render do MP4.
- Branding: font Manrope serwowany bezpośrednio z `../../assets/` (repo
  głównej strony probatum.pl) przez `/vendor/manrope`, kolory skopiowane
  z `assets/site.css` (`--paper #f4f5f1`, `--ink #1b201e`, `--blue
  #254bfa`, `--lime #d9f975`, `--pale #e9eddf`).

## Generator scen z briefu (AI) — 21.09.2026

Piotr: „tego typu pola powinno AI wypełniać" — po napisaniu briefu i tytułu,
przycisk **„✨ Wygeneruj sceny z briefu (AI)"** (obok „+ Dodaj scenę") woła
`POST /api/projects/:id/scenes/generate`, który przez n8n:

1. **Szuka linku w briefie** (prosty regex) — jeśli jest, pobiera realną
   treść tej strony przez istniejący subworkflow n8n `otworz_link`
   (Jina Reader, ten sam co Dona już używa do czytania stron). Dzięki temu
   model pisze na podstawie prawdziwej oferty, nie zmyśla cen/gwarancji/
   liczb — to była świadoma decyzja, zgodna z zasadą „nie wymyślaj opinii
   ani liczb" (sprawdź `docs/memory/nie-wymyslaj-opinii.md` w repo Dona).
2. Generuje sceny przez **Anthropic (`claude-sonnet-5`)**, credential
   `Anthropic account` już istniejący w n8n (ten sam co inne narzędzia PM),
   nie osobny klucz. Workflow: `DONA — Integracja: Maszynka do Szortsów
   (Generator scen AI)` (`DlNnrC8j2Rngs2Zn`, folder `DONA — INTEGRATIONS`,
   webhook `maszynka-generuj-sceny`), ten sam sekret co TTS/SFX.
3. **Zawsze DOPISUJE sceny na końcu listy, nigdy nie kasuje istniejących**
   — bezpieczne dla ręcznie już zaczętej pracy.

**Pułapka złapana przy budowie:** odpowiedź Anthropic ma najpierw blok
`{type:"thinking"}`, dopiero potem `{type:"text"}` w `content[]` — zakładanie
`content[0].text` psuło parsowanie za każdym razem. Kod szuka pierwszego
bloku z `type === "text"`, nie indeksu 0.

Przetestowane żywo na prawdziwym projekcie Piotra („Budowa stron www",
brief z linkiem do `probatum.pl/realizacje.html`) — 5 wygenerowanych scen,
treść trzymająca się faktów ze strony, poprawne typy i sumujące się w
przybliżeniu do długości docelowej `durationSeconds`.

`server/scenegen.js` — analogiczny do `server/elevenlabs.js` (sekret
wyciągnięty do wspólnego `server/dona-secret.js`, żeby nie duplikować).

## Render MP4: najpierw serwer (szybko), ffmpeg.wasm tylko jako zapas (21.09.2026)

Pierwsza wersja renderowała WYŁĄCZNIE w przeglądarce przez ffmpeg.wasm
(jednowątkowo, programowo) — dla 30-sekundowej rolki 1080×1920 potrafiło to
trwać wiele minut i **wyglądało jak zawieszona appka** (Piotr zgłosił: „dałem
generowanie rolki i nic nie ma"). Realny stan: przeglądarka faktycznie
liczyła (91% CPU), tylko bez widocznego postępu i bardzo wolno.

Naprawione dwa niezależne problemy:

1. **Brak widocznego postępu** — teraz `statusEl` pokazuje żywy licznik przy
   nagrywaniu (`Nagrywam podgląd: N / total s…`) i realny procent z eventu
   `ffmpeg.on('progress', ...)` przy konwersji w WASM, zamiast statycznego
   napisu przez całą operację.
2. **Sam WASM jest z natury wolny** — `server/render.js` dodaje ścieżkę
   renderu PO STRONIE SERWERA przez natywny `ffmpeg`, jeśli jest zainstalowany
   na komputerze, na którym appka działa (sprawdzane przez `hasNativeFfmpeg()`,
   `ffmpeg -version`). Na tym komputerze `ffmpeg` jest (Homebrew, ze sprzętowym
   przyspieszeniem) — 30-sekundowa rolka: ~30 s nagrywania (to jest realny
   czas trwania rolki, nie da się przyspieszyć — to nagranie na żywo canvas+
   audio) + **~11 s konwersji** (zmierzone), zamiast dziesiątek minut w WASM.

**Kolejność w `public/app.js` (`renderMp4`):** po nagraniu WebM appka najpierw
próbuje `POST /api/projects/:id/render-native` (webm → serwer → natywny
ffmpeg → mp4, appka od razu zapisuje kopię w `output/`). Jeśli serwer
odpowie `501` (brak natywnego ffmpeg na TYM komputerze — appka ma to
sprawdzać za każdym razem, bo może działać na innym komputerze niż ten, na
którym budowano), appka **po cichu** wraca do starej ścieżki ffmpeg.wasm —
zero zmiany zachowania dla kogoś bez zainstalowanego ffmpeg, zgodnie z
pierwotnym założeniem „nie powinnaś musieć niczego instalować ręcznie poza
npm install" z `zakres-prac.md`.

`GET /api/config` zwraca dodatkowo `nativeFfmpeg: boolean` (informacyjne,
front go dziś nie odczytuje — render sam próbuje i się cofa w razie 501).

## Kluczowa decyzja techniczna: render MP4 bez CDN

`@ffmpeg/ffmpeg`, `@ffmpeg/util` i `@ffmpeg/core` są zainstalowane jako
zwykłe zależności npm i serwowane statycznie z `node_modules` przez
Express (`/vendor/ffmpeg`, `/vendor/ffmpeg-util`, `/vendor/ffmpeg-core`).
**Nie** ładujemy ich z unpkg/CDN — ffmpeg.wasm jest importowany leniwie
(dynamic `import()`) dopiero przy kliknięciu „Renderuj MP4", więc awaria
sieci albo brak dostępu do CDN nie blokuje reszty panelu (projekty,
edycja scen działają zawsze offline).

Pipeline renderu (w `app.js`, funkcja `renderMp4`):
1. Web Audio: `AudioContext` + `createMediaStreamDestination()` — lektor
   per scena (jeśli wygenerowany) miksowany w czasie wg scenorysu.
2. `canvas.captureStream(0)` + ręczne `videoTrack.requestFrame()` po
   każdym narysowaniu klatki. **Ważne:** tryb automatyczny
   `captureStream(FPS)` potrafi nie złapać ani jednej klatki w
   headless/bezekranowych przeglądarkach — dlatego tryb ręczny.
3. **Zawsze** podłączamy do `dest` cichy bufor audio na całą długość
   rolki (`silentBuffer`), niezależnie od tego, czy jakakolwiek scena ma
   lektora. Bez tego `MediaRecorder` w niektórych przeglądarkach (m.in.
   headless Chromium — tak znalazłem ten bug) pisze tylko nagłówek WebM
   (~110 bajtów) i milknie, bo audio destination bez żywego sygnału nie
   dostarcza danych do mux-era.
4. `MediaRecorder` nagrywa połączony strumień (wideo + audio) do WebM.
5. `ffmpeg.wasm` transkoduje WebM → MP4 (`libx264` + `aac`).
6. Wynik trafia do pobrania w przeglądarce **oraz** POST-em do
   `/api/projects/:id/render`, który zapisuje kopię w `output/`.

Transkodowanie w ffmpeg.wasm jest jednowątkowe (core bez COOP/COEP, żeby
nie komplikować configu serwera) — na słabszym sprzęcie/w współdzielonym
środowisku bywa bardzo wolne (obserwowane ~0.02x realtime w sandboxie
testowym). Na zwykłym komputerze użytkownika powinno być wyraźnie
szybciej, ale warto o tym uprzedzić, jeśli render dłuższej rolki się
dłuży.

## Co przetestowane (Playwright, lokalnie)

- CRUD projektów i scen przez API (curl) i przez UI.
- Drag-and-drop reorder scen, usuwanie scen.
- Pełny render: 2 sceny bez lektora → poprawny plik MP4 (ISO Media,
  1080×1920) zapisany w `output/`.
- Kontrolowany błąd, gdy brak `DONA_N8N_SHARED_SECRET` w `.env`.
- **21.09.2026, druga sesja (integracja z n8n):** cała trasa
  webhook→sekret→routing tts/sfx przetestowana żywo (patrz sekcja niżej) —
  droga jest poprawna, ale sam klucz ElevenLabs w n8n jest dziś nieważny
  (`401 Invalid API key`), więc realny dźwięk jeszcze nie wyszedł.

**Nieprzetestowane realnie:** wygenerowanie prawdziwego pliku audio —
blokuje to nieważny klucz API w credentialu n8n „PM Marketing OS —
ElevenLabs”, nie kod tego narzędzia ani workflow. Wymaga odświeżenia
klucza przez Piotra w n8n (Credentials → „PM Marketing OS — ElevenLabs”).

## Integracja z n8n zamiast lokalnego klucza ElevenLabs (21.09.2026)

Na prośbę Piotra klucz ElevenLabs przestał żyć w `.env` tego narzędzia.
`server/elevenlabs.js` woła teraz webhook n8n zamiast `api.elevenlabs.io`
bezpośrednio — dokładnie ten wzorzec, którego DONA już używa (panel nigdy
nie trzyma kluczy dostawców, tylko woła webhooki n8n, a sekrety leżą w
credentialach/Data Table n8n).

- **Webhook:** `POST https://pmresearch.app.n8n.cloud/webhook/maszynka-elevenlabs`
  (workflow n8n `DONA — Integracja: Maszynka do Szortsów (ElevenLabs)`,
  id `wy6PQYVvtJ1BXiHg`, folder `DONA — INTEGRATIONS`, projekt „PM Command
  Center”). Body: `{ sekret, operation: "tts"|"sfx", text, voiceId?,
  durationSeconds? }`. Odpowiedź: binarny `audio/mpeg`, albo JSON błędu
  (401 zły sekret, 400 nieznana operacja).
- **Sekret** (`DONA_N8N_SHARED_SECRET` w `.env`) — NIE jest kluczem
  ElevenLabs, tylko hasłem między tym narzędziem a n8n. Trzymany w n8n
  Data Table `PM_sekrety_wspolne`, wiersz `nazwa=maszynka_szortow_sekret`.
  Ta sama konwencja co reszta Dony (np. `panel_haslo` dla `dona-tts`).
- **Klucz ElevenLabs** żyje wyłącznie w istniejącym credentialu n8n „PM
  Marketing OS — ElevenLabs” (`httpHeaderAuth`, id `7MA9n0mrtChwQk8f`) —
  tym samym, którego już używają workflow „Webinar ChatGPT — ElevenLabs
  TTS” i „Zielona Pergola — głos managera”. Nie duplikowano credentiala.
- **Dlaczego tak, a nie n8n `headerAuth` na samym webhooku:** bo cała
  reszta webhooków Dony (np. `dona-tts`, `panel-agent`) sprawdza sekret
  ręcznie w treści żądania, nie przez wbudowaną autoryzację n8n — ten sam
  wzorzec, żeby nie mieszać dwóch konwencji bezpieczeństwa w jednym
  systemie.
- **Funkcje `textToSpeech(text, voiceId)` i `soundEffect(description,
  durationSeconds)` mają identyczną sygnaturę co przed zmianą** —
  `server/index.js` nie wymagał żadnej modyfikacji.

## Co dalej / możliwe rozszerzenia

- Klonowanie głosu w ElevenLabs (appka już liczy się z dowolnym
  `voiceId` per projekt — pole w panelu).
- Więcej typów scen / animacji tła (obecnie: tekst, lista, cytat, CTA;
  animacja to jedno dryfujące koło w kolorze marki).
- Ewentualnie multi-threaded core ffmpeg.wasm (szybszy render), co
  wymagałoby ustawienia nagłówków COOP/COEP na serwerze Express.
