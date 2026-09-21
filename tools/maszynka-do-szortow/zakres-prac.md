# Maszynka do szortsów — zakres prac

Ustalone 21.09.2026, na podstawie transkrypcji szkolenia Akademii
Automatyzacji + rozmowy w pm-pages. To jest zapis tego, co budujemy,
zanim zaczęliśmy kodować — zgodnie z metodą z transkrypcji.

## Cel

Lokalna appka (uruchamiana na Twoim komputerze), która na podstawie
opisanego przez Ciebie briefu generuje krótkie pionowe wideo (MP4) do
social media — tekst + branding Probatum jako główny element, proste
animacje w tle, lektor i efekty dźwiękowe z ElevenLabs.

## W zakresie

- Panel webowy (przeglądarka), uruchamiany lokalnie przez `npm start`.
- Tworzenie projektu/rolki: pole na brief (temat + treść), wybór
  długości docelowej.
- Edycja scen: tekst na ekranie, tekst lektora, typ sceny.
- Reorder scen (przeciąganie), dodawanie, usuwanie.
- Generowanie lektora **per scena** przez ElevenLabs (głos z biblioteki
  na start — nie masz jeszcze sklonowanego głosu).
- Generowanie efektów dźwiękowych przez ElevenLabs (bez muzyki w tle).
- Podgląd sceny w przeglądarce (canvas: tekst + prosta animacja tła).
- Render do MP4 (pion, 1080×1920) i zapis lokalnie w `output/`.
- Bez twarzy/avatara.
- Styl wizualny zgodny z brandem Probatum: font Manrope, paleta z
  `assets/site.css` (`--paper #f4f5f1`, `--ink #1b201e`,
  `--blue #254bfa`, `--lime #d9f975`, `--pale #e9eddf`).

## Poza zakresem (na razie)

- Automatyczna publikacja na social media.
- Avatar / twarz.
- Muzyka w tle.
- Scrapowanie treści z linków — na start brief wpisujesz ręcznie.
- Klonowanie głosu w ElevenLabs (możliwe do dodania później, gdy
  sklonujesz głos — appka i tak liczy się z ID głosu jako parametrem).

## Technologia (dobrana i uzasadniona)

- **Node.js + Express** — lokalny serwer, serwuje panel i proste API.
  Repo już ma zainstalowany Node 22, appka nie wymaga niczego poza
  `npm install`.
- **Zwykłe pliki JSON na dysku** (`data/projects/*.json`) zamiast bazy
  danych — to narzędzie jednoosobowe, nie potrzebuje bazy.
- **Panel: czysty HTML/CSS/JS** (bez frameworka) — spójne z resztą
  repo pm-pages, które też nie używa Reacta ani bundlera do frontu.
- **ElevenLabs REST API** wywoływane z backendu (klucz API trzymany
  lokalnie w pliku `.env`, nigdy nie trafia do gita ani do mnie).
- **Render wideo: `@ffmpeg/ffmpeg` (WASM)** zamiast systemowego
  ffmpeg — sprawdziłem, w tym środowisku nie ma zainstalowanego
  ffmpeg, a Ty jako osoba nietechniczna nie powinnaś musieć niczego
  instalować ręcznie poza `npm install`. WASM-owy ffmpeg działa od
  razu jako paczka npm, łączy klatki z canvasu + ścieżki audio per
  scena w jeden plik MP4.

## Struktura projektu

```
tools/maszynka-do-szortow/
  zakres-prac.md      (ten plik)
  CLAUDE.md            (dopiszę po zbudowaniu — podsumowanie dla kolejnych sesji)
  package.json
  .env.example         (ELEVENLABS_API_KEY=)
  server/              (Express + integracja ElevenLabs + render)
  public/              (panel: HTML/CSS/JS)
  data/                (projekty — gitignored)
  output/              (gotowe MP4 — gitignored)
```

## Jak uruchomić (po zbudowaniu)

```
cd tools/maszynka-do-szortow
npm install
cp .env.example .env   # wklej swój klucz ElevenLabs
npm start               # panel pod http://localhost:3000
```
