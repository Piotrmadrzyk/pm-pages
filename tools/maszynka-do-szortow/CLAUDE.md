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
cp .env.example .env   # wklej ELEVENLABS_API_KEY
npm start               # http://localhost:3000
```

## Struktura

- `server/index.js` — Express: statyczny panel + REST API (projekty,
  sceny, reorder, ElevenLabs, zapis renderu).
- `server/store.js` — persystencja w plikach JSON (`data/projects/*.json`),
  bez bazy danych.
- `server/elevenlabs.js` — wrapper na REST API ElevenLabs (TTS + sound
  generation). Klucz tylko w `.env`, nigdy nie trafia do frontu ani do gita.
- `public/index.html` + `styles.css` + `app.js` — panel: lista
  projektów, edycja scen (drag&drop reorder przez natywne HTML5 DnD),
  podgląd na `<canvas>`, render do MP4.
- Branding: font Manrope serwowany bezpośrednio z `../../assets/` (repo
  głównej strony probatum.pl) przez `/vendor/manrope`, kolory skopiowane
  z `assets/site.css` (`--paper #f4f5f1`, `--ink #1b201e`, `--blue
  #254bfa`, `--lime #d9f975`, `--pale #e9eddf`).

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
- Kontrolowany błąd, gdy brak `ELEVENLABS_API_KEY` w `.env`.

**Nieprzetestowane realnie:** generowanie lektora/efektów przez
ElevenLabs (potrzebny prawdziwy klucz API użytkownika) — kod wywołań API
jest gotowy (`server/elevenlabs.js`), ale nie było czym go odpalić w tej
sesji.

## Co dalej / możliwe rozszerzenia

- Klonowanie głosu w ElevenLabs (appka już liczy się z dowolnym
  `voiceId` per projekt — pole w panelu).
- Więcej typów scen / animacji tła (obecnie: tekst, lista, cytat, CTA;
  animacja to jedno dryfujące koło w kolorze marki).
- Ewentualnie multi-threaded core ffmpeg.wasm (szybszy render), co
  wymagałoby ustawienia nagłówków COOP/COEP na serwerze Express.
