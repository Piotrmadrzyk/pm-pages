# probatum.pl — HANDOFF

## 1. Nazwa projektu
probatum.pl — strona główna firmy Probatum

## 2. Cel
Główna witryna marketingowa Probatum: oferta, cennik, realizacje, blog, strony podrzędne (m.in. Akademia — landing marketingowy, `/p/newage-lewandowska/` — strona klientki). Repo GitHub nazywa się `pm-pages` i pełni rolę "PM Marketing Campaign OS — strony i landingi".

## 3. Status
**ACTIVE, produkcja.**

## 4. Produkcja / domena
`probatum.pl`, hosting Vercel (`vercel.json` w repo, `.vercel/` obecny lokalnie — projekt podłączony).

## 5. Source of truth
Ten katalog. Repo GitHub `Piotrmadrzyk/pm-pages` (PUBLIC), branch `main`. To repo obsługuje TEŻ `/p/newage-lewandowska/` (patrz `~/Projekty/Strony-WWW/newagelewandowska.pl/HANDOFF.md` — tamten folder to tylko kopia podglądowa, prawdziwa edycja odbywa się tutaj).

## 6. Repo / remote / branch
`github.com/Piotrmadrzyk/pm-pages.git`, branch `main`, ostatni commit `02078a1` (10.09.2026, "Dodaj Google Analytics za zgodą — baner cookies"). Status po konsolidacji: 1 niezacommitowana zmiana (sprawdź `git status` przed pracą — mogła powstać podczas nocnej fizycznej reorganizacji, np. dodanie `_worktrees/`).

Ma DWA git worktree (aktywne warianty podglądowe, NIE osobne strony):
- `_worktrees/preview-spring` — branch `preview/probatum-spring-20260907`
- `_worktrees/probatum-full-preview` — branch `preview/probatum-full-v2`

## 7. Technologie
Statyczny HTML/CSS/JS + generator Python (`build/`, `build-v2/`). Aktualny generator to `build-v2/publikuj.py` (stary `build/build.py` jest ZABLOKOWANY — pułapka opisana w pamięci projektowej `probatum-v11-nowa-strona.md`).

## 8. Struktura projektu
```
probatum.pl/
├── *.html                    ← strony (index, oferta, cennik, blog, akademia landing, itd.)
├── darmowy-poradnik-chatgpt.html  ← lead magnet Akademii, pisany ręcznie (NIE przez generator,
│                                    patrz punkt 16), linkowany z akademia.html
├── assets/ebook-gpt/         ← 6 zrzutów ekranu użytych w powyższym poradniku
├── p/newage-lewandowska/     ← strona klientki (osobna domena docelowo, dziś podstrona probatum.pl)
├── build/                     ← STARY generator, ZABLOKOWANY (nie używać)
├── build-v2/                  ← AKTUALNY generator: `python3 build-v2/publikuj.py`
├── assets/, blog/, warsztat/  ← treść/zasoby
├── vercel.json
└── _worktrees/                ← podglądy (patrz punkt 6)
```

## 9. Jak uruchomić lokalnie
Statyczne pliki — otwórz `.html` bezpośrednio w przeglądarce, albo lokalny serwer (`python3 -m http.server` w katalogu).

## 10. Jak zbudować
```bash
python3 build-v2/publikuj.py
```
**NIGDY nie używać `build/build.py`** — zablokowany po incydencie (stary generator nadpisywał nową Akademię starą wersją).

## 11. Jak deployować (OPISANE, NIE WYKONANE)
Wg zasady projektu: **NIGDY `vercel deploy` ręcznie** — tylko przez dedykowany skrypt wdrożeniowy (`wdroz.py` w innych projektach Piotra stosuje tę samą zasadę; dla probatum.pl sprawdź `DO-ZROBIENIA.md`/`JAK-DZIALA-PROBATUM.md` w tym katalogu przed deployem).

## 12. Integracje
Google Analytics (za zgodą, baner cookies, wdrożone 10.09.2026). Subdomeny — patrz `SUBDOMENY.md` w tym katalogu.

## 13. Wymagane sekrety
`.env.local` istnieje lokalnie (niecommitowany) — nazwy zmiennych nie zweryfikowane w tej turze, sprawdź plik lokalnie przed pracą wymagającą API.

## 14. Co działa
Strona produkcyjna, baner cookies/GA, generator `build-v2`. Darmowy poradnik ChatGPT
(`darmowy-poradnik-chatgpt.html`, lead magnet Akademii AI) wdrożony 21.09.2026, linkowany
z `akademia.html`. `build-v2/publikuj.py` ma listę `STRONY_STATYCZNE` — jeśli dojdzie kolejna
taka ręcznie pisana strona w korzeniu, dopisz ją tam, inaczej `validate.py` fałszywie zgłosi
link do niej jako zepsuty.

## 15. Co nie działa
Nieznane w tej turze — nie testowano na żywo podczas nocnej konsolidacji.

## 16. Otwarte zadania
Patrz `DO-ZROBIENIA.md` w tym katalogu (plik istniejący, nie analizowany szczegółowo w tej turze).

## 17. Znane problemy
1 niezacommitowana zmiana po nocnej fizycznej konsolidacji — sprawdź `git status` i `git diff` zanim założysz że to nieistotne.

## 18. Ważne decyzje
Stary `build/build.py` świadomie zablokowany (mina — nadpisywał nową Akademię starą wersją index.html). `build-v2/` to jedyny właściwy generator.

## 19. Czego NIE robić
- Nie używać `build/build.py`.
- Nie robić `vercel deploy` ręcznie.
- Nie mieszać zmian dla `/p/newage-lewandowska/` z resztą strony bez świadomości, że to osobny, wrażliwy projekt klientki (patrz jego HANDOFF).

## 20. Legacy / stare kopie
`build/` — stary, zablokowany generator, zachowany archiwalnie w repo.

## 21. Backup
Pełna historia w `github.com/Piotrmadrzyk/pm-pages` (PUBLIC).

## 22. Data ostatniej weryfikacji
20.09.2026 — fizyczna konsolidacja (przeniesienie z `~/Projekty/pm-pages` wraz z dwoma worktree, `git worktree repair` wykonany i zweryfikowany).

## 23. Instrukcja dla następnego AI

> Najpierw przeczytaj cały HANDOFF.md i sprawdź aktualny git status. Nie pytaj użytkownika o informacje już opisane w projekcie. Nie zaczynaj od zera. Zweryfikuj aktualny stan i kontynuuj pracę.

Ten plik został ODTWORZONY po przypadkowym usunięciu podczas fizycznej reorganizacji `~/Projekty` (20.09.2026) — jeśli coś tu brakuje względem poprzedniej wersji, sprawdź `DO-ZROBIENIA.md`, `JAK-DZIALA-PROBATUM.md`, `SUBDOMENY.md`, `README.md` w tym samym katalogu, które przetrwały nietknięte.
