# MASZYNKA DO SZORTSÓW — schemat (wersja robocza)

Notatka z 21.09.2026. Na razie **tylko plan** — nic z tego nie jest
zbudowane. Punkt wyjścia: transkrypcja szkolenia „Claude Code od ZERA"
(Akademia Automatyzacji, Kacper, 18.09.2026), gdzie Kacper na żywo buduje
własną maszynkę do shortsów i pokazuje dokładnie, jak brief­ował Claude Code.

---

## Co to jest

Lokalna appka webowa (panel w przeglądarce), budowana i uruchamiana przez
Claude Code, generująca pionowe wideo (shorts) na social media. Działa
w całości lokalnie, w ramach istniejącej subskrypcji Claude Code — jedyna
płatna usługa zewnętrzna to **ElevenLabs** (lektor + efekty dźwiękowe).
Nie jest to SaaS ani narzędzie dla klientów — tylko do własnego użytku.

## Input

Brak stałego źródła treści (na probatum.pl jeszcze nic nie ma do
scrapowania). Za każdym razem ja opisuję w panelu / Claudowi, o czym ma
być dany short i jakie treści ma zawierać.

**Pierwszy test:** short o budowie stron internetowych (oferta z
`strony-www.html`).

## Output

Plik MP4 w pionie, z wybieraną długością docelową. Bez auto-publikacji —
plik ląduje lokalnie, ja sam wrzucam go na social media ręcznie.

## Warstwa wizualna

- **Duży, mocny tekst w kolorach/fontach marki Probatum** jako główny
  nośnik treści (inaczej niż u Kacpra, gdzie to animacje były głównym
  nośnikiem, a tekst dodatkiem).
- Animacje (proste, JS/Three.js — bez drogich zewnętrznych API do wideo)
  jako tło / dopełnienie, nie odwrotnie.
- Branding zawsze wygrywa, jeśli koliduje z efektownością animacji.
- Logotypy narzędzi/marek mogą się pojawiać w scenach, jeśli pasują.

## Audio

- Lektor — docelowo głos sklonowany w ElevenLabs.
- Tylko efekty dźwiękowe z ElevenLabs (**bez muzyki w tle**).
- Klucz API ElevenLabs wklejany w panelu, zapisywany lokalnie w pliku,
  do którego Claude nie ma wglądu.

## Panel / edytor — funkcje

- lista projektów/rolek,
- pole do opisania briefu danego shorta (temat, treść) — zamiast
  wklejania linku,
- edycja scen: tekst na ekranie, tekst lektora, typ sceny,
- przeciąganie kolejności scen, dodawanie, usuwanie,
- generowanie lektora **per scena** (nie całości na raz),
- podgląd/odtwarzanie w przeglądarce,
- przycisk „renderuj MP4",
- wybór długości docelowej rolki.

## Proces budowy (metoda z transkrypcji — do zastosowania, gdy zaczniemy realnie budować)

1. Jeden długi brief do Claude Code: co chcę osiągnąć, co już wiem/mam,
   czego nie chcę, jak Claude ma się zachowywać — pyta zamiast zgadywać,
   tłumaczy wybory prostym językiem, **nic nie buduje bez mojej zgody**.
2. Subagent zbiera branding bezpośrednio ze strony probatum.pl (kolory,
   fonty, styl) — drugi subagent robi research gotowych rozwiązań do
   tego problemu.
3. Runda pytań od Clauda (źródło treści, długość, styl wizualny, priorytet
   brand vs. animacja, logotypy, audio, funkcje panelu) → zapis ustaleń
   do pliku `zakres-prac.md` w projekcie.
4. Akceptacja pliku → komenda `/clear` (czyszczenie kontekstu) → dopiero
   wtedy polecenie budowy „zgodnie z @zakres-prac.md, uruchom lokalny
   serwer".
5. Po zbudowaniu: plik `CLAUDE.md` w projekcie z podsumowaniem (żeby
   kolejne sesje nie musiały niczego tłumaczyć od nowa).
6. Jeśli proces się powtarza (np. generowanie kolejnych shortów wg tego
   samego schematu) — opakować w **skill**, tak jak Kacper zrobił ze
   skillem „meta daily" do raportów reklamowych.

## Otwarte kwestie / do ustalenia przy właściwym briefowaniu

- Czy głos w ElevenLabs ma być sklonowany (mój głos), czy gotowy głos
  z biblioteki na start.
- Dokładna paleta kolorów/fonty do wyciągnięcia ze strony probatum.pl
  (subagent to zrobi automatycznie przy briefowaniu).
- Docelowe platformy publikacji (na pewno ręcznie, ale które — IG, TikTok,
  YT Shorts, LinkedIn?) — wpływa tylko na proporcje/długość, nie na sam
  input.

---

*To jest osobny projekt (lokalna appka), nie część strony probatum.pl —
plik trzymam tutaj tylko jako notatkę roboczą, żeby nie zgubić ustaleń.*
