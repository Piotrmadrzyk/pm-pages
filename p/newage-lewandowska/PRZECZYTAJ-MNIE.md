# Twoja strona — instrukcja

> ⚠️ **SZKIC ROBOCZY.** Strona jest jeszcze poprawiana. Ten dokument
> zostanie uzupełniony i sprawdzony, zanim trafi do Agnieszki razem
> z gotowym pakietem.


Cześć Agnieszko. To jest wszystko, co potrzebne, żeby ta strona była
naprawdę Twoja: żebyś mogła ją zmieniać, przenieść gdzie chcesz i nie
zależeć od nikogo.

---

## Najważniejsze w trzech zdaniach

**Ta strona nie potrzebuje niczyjego konta.** Żadnej subskrypcji, żadnej
usługi, która może wygasnąć. To zwykłe pliki — działają na każdym hostingu.

**Wszystko, co widzisz, jest w tym katalogu.** Skopiuj go w całości na swój
hosting i strona działa. Skopiuj na pendrive — masz kopię zapasową.

**Masz Claude'a. On umie te pliki czytać i zmieniać.** Niżej jest gotowy
tekst, który mu wklejasz na start.

---

## Co wkleić Claude'owi, gdy chcesz coś zmienić

Skopiuj poniższe i wklej jako pierwszą wiadomość, a potem dołącz pliki
strony (albo wskaż folder, jeśli używasz Claude Code):

```
Zajmujesz się moją stroną internetową. Jestem Agnieszka Lewandowska,
prowadzę salon fryzjerski new age w Częstochowie. Nie jestem
programistką — tłumacz mi skutki, nie kod.

JAK ZBUDOWANA JEST STRONA

To zwykłe pliki HTML, bez żadnego systemu zarządzania treścią.
Każda podstrona to osobny folder z plikiem index.html:

  index.html          strona główna
  o-mnie/             o mnie i dyplomy
  uslugi/             usługi i dlaczego nie ma cennika
  portfolio/          sesje i publikacje
  porady/             poradnik (5 osobnych artykułów w podfolderach)
  opinie/             opinie i formularz
  kontakt/            kontakt, mapa, formularz wyceny
  prywatnosc/         polityka prywatności

  styl.css            wygląd całej strony — jeden plik dla wszystkich
  skrypt.js           zachowania: menu, powiększanie zdjęć, formularze
  img/                wszystkie zdjęcia
  formularz.php       wysyłka formularzy (opis w środku pliku)

WAŻNE: nagłówek, menu i stopka powtarzają się na każdej podstronie.
Jeśli zmieniasz coś w menu albo w stopce, zmień to we WSZYSTKICH
plikach index.html, inaczej strona się rozjedzie.

CZEGO NIE WOLNO ZMIENIAĆ BEZ MOJEJ ZGODY

- opinie — są przepisane z mojego profilu Google dosłownie. Nie wolno
  dopisywać wymyślonych. Fałszywe opinie to w Polsce zakazana praktyka
  i odpowiadam za nią ja, nie wykonawca strony.
- liczby: ocena 5,0 z 53 opinii. Nie „setki".
- akademie Toni&Guy i Saks — szkolenia odbywały się w POLSCE, nie
  w Londynie. Adres londyński jest tylko na papierze firmowym dyplomu.
- nie pisz, że prowadziłam szkolenia dla fryzjerów. Nie prowadziłam.
- telefon: 507 330 730. Kod pocztowy: 42-218.

CO ZROBIĆ NAJPIERW
Przeczytaj pliki i powiedz mi własnymi słowami, gdzie się co znajduje.
Dopiero potem bierzemy się za zmiany.
```

---

## Rzeczy, które będziesz chciała zmieniać najczęściej

**Godziny otwarcia** — są w `kontakt/index.html` i w `skrypt.js`
(w skrypcie liczą napis „otwarte / zamknięte" w nagłówku).

**Cena, opisy usług** — `uslugi/index.html`.

**Nowe zdjęcia** — wrzuć do `img/`, potem poproś Claude'a, żeby dodał je
do galerii. Każde zdjęcie powinno mieć dwie wersje: pełną i mniejszą
z końcówką `-mal` (miniatura ładuje się w galerii, pełna po kliknięciu).

**Nowa opinia** — gdy ktoś napisze przez formularz albo w Google.
Poproś Claude'a o dopisanie do `opinie/index.html`. Podaj imię, datę
i treść dokładnie taką, jaka jest.

---

## Formularze

Są dwa: opinia i zapytanie o termin z ceną. Domyślnie otwierają program
pocztowy z gotową wiadomością — działa wszędzie i nic nie może przestać
działać.

Gdy strona stanie na Twoim hostingu (home.pl ma PHP w każdym pakiecie),
możesz je przełączyć tak, żeby wiadomość wychodziła w tle:

1. wgraj `formularz.php` obok `index.html`
2. w `skrypt.js` zmień `var ADRES_WYSYLKI = '';`
   na `var ADRES_WYSYLKI = 'formularz.php';`
3. w `formularz.php` ustaw swój adres e-mail

Instrukcja jest też w środku samego pliku `formularz.php`.

---

## ⚠️ Zanim strona ruszy publicznie

**Zdejmij `noindex`.** W każdym pliku `index.html` jest linijka:

```html
<meta name="robots" content="noindex, nofollow">
```

Ona mówi Google: nie pokazuj tej strony. Póki tam jest, strony nie da się
znaleźć w wyszukiwarce. **Usuń ją ze wszystkich plików**, gdy strona
będzie gotowa — Claude zrobi to jednym poleceniem.

**Zmień adres bazowy.** W każdym `index.html` są linijki z adresem
`https://probatum.pl/p/newage-lewandowska/` — to adres roboczy. Po
przeniesieniu na własną domenę trzeba je podmienić na Twój adres.
To też jedno polecenie dla Claude'a.

**Zmień adres e-mail w formularzach** z `kontakt@probatum.pl` na swój.

---

## Zgody na zdjęcia

Zdjęcia z magazynu SPLOT i sesji katalogowych są autorstwa fotografki
i pokazują twarze modelek. Przed publikacją potrzebna jest zgoda
fotografki i osób na zdjęciach.

Zdjęcia metamorfoz klientek — dopiero po pisemnych zgodach. Dlatego
tej sekcji jeszcze nie ma na stronie.

---

## Kopia zapasowa

Skopiuj cały ten folder w dwa miejsca: na swój dysk i na pendrive albo
do chmury. To wszystko, czego potrzeba, żeby postawić stronę od nowa
u dowolnego dostawcy.

---

*Strona zbudowana w sierpniu 2026.*
