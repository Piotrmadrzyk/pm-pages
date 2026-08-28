# new age Lewandowska — strona Agnieszki Lewandowskiej

Pierwsza **realna klientka** Probatum. Salon fryzjerski w Częstochowie,
ul. Jana Kilińskiego 55/2. Strona docelowo idzie na jej własny hosting.

Podgląd: <https://probatum.pl/p/newage-lewandowska/>

---

## 1. Jak to jest zbudowane

Trzynaście podstron generuje **`build/newage.py`**:

```bash
cd build && python3 newage.py
```

| adres | co tam jest |
|---|---|
| `/` | hero, o mnie w skrócie, pasek 8 dyplomów, usługi, „z czym przychodzą", opinie |
| `/o-mnie/` | historia + osiem dyplomów w rzędach na przemian |
| `/uslugi/` | cztery usługi rozpisane, bon podarunkowy, jak wygląda wizyta, cennik |
| `/portfolio/` | 20 kadrów: magazyn SPLOT, sesje katalogowe, sesja wizerunkowa |
| `/porady/` | hub poradnika |
| `/porady/{5 artykułów}/` | osobne adresy — to one łapią ruch z wyszukiwarki |
| `/opinie/` | 6 prawdziwych opinii z Google + formularz wystawienia |
| `/kontakt/` | dane, mapa, formularz wyceny, sześć pytań |
| `/prywatnosc/` | polityka prywatności (są dwa formularze zbierające dane) |

Style i zachowania są **wspólne**: `styl.css` i `skrypt.js` w katalogu strony.
Menu jest w jednym miejscu w generatorze — zmiana pozycji to jedna linijka,
a nie trzynaście poprawek.

### Zdjęcia

Każde ma dwie wersje: pełną i miniaturę (`-mal`). W galeriach ładuje się
miniatura, pełna dopiero po kliknięciu. Bez tego strona z 34 zdjęciami
ważyłaby kilkanaście megabajtów.

---

## 2. ⚠️ Rzeczy, których nie wolno zmienić bez sprawdzenia

**Nie pisz, że akademie Toni&Guy i Saks odbyły się w Londynie.** Na dyplomie
Saks jest londyński adres na papierze firmowym, ale **szkolenia odbywały się
w Polsce**. Agnieszka wyłapała to sama i wprost prosiła, żeby nie wprowadzać
odbiorców w błąd. Ja ten błąd popełniłem — nie powtarzaj go.

**Telefon to 507 330 730** — numer salonu. `506 116 008` to jej numer
**prywatny**, z którego pisze do Piotra. Nie może trafić na stronę.

**Kod pocztowy to 42-218**, nie 42-200.

**Nie wpisuj wymyślonych opinii.** Sześć opinii na stronie jest przepisanych
dosłownie z profilu Google, z imieniem i nazwiskiem. Fałszywe opinie są
w Polsce zakazaną nieuczciwą praktyką rynkową i odpowiada za nie
przedsiębiorca, czyli Agnieszka. Prawdziwe są tutaj:
<https://www.google.com/maps/place/New+Age+Studio>

**Liczby: 5,0 z 53 opinii.** Nie „setki". Wcześniejszy brief podawał 245 i 325
z katalogu `zlotafirma.pl` — te liczby są błędne. Wyróżnienie „Złota Firma"
nie zostało potwierdzone i dlatego nie ma go na stronie.

**Dyplomów jest około dwudziestu.** Osiem na stronie to te, które Agnieszka
uznała za najważniejsze.

---

## 3. Co jest zrobione pod SEO

- adres kanoniczny na każdej podstronie, z jednego miejsca (stała `BAZA`)
- `sitemap.xml` i `robots.txt` generowane razem ze stroną
- dane strukturalne **HairSalon**: adres, godziny, telefon, ocena, współrzędne
- dane strukturalne **FAQPage** — wyciągane wprost z gotowego HTML-a
- okruszki nawigacyjne **BreadcrumbList**
- `og:image`, `og:title`, `og:url` — podgląd przy wrzucaniu linku na Facebooka
- ikona strony i `manifest.json`
- pięć artykułów poradnika pod długi ogon zapytań

### ⚠️ `noindex` jest włączony

Zgodnie ze stałą zasadą — strona jest wersją roboczą. **Przed uruchomieniem
trzeba go zdjąć**, inaczej całe SEO jest bez znaczenia. Siedzi w `SZKIELET`
w generatorze.

---

## 4. Co czeka

**Formularze nie działają.** Dwa formularze — wyceny (`newage-kontakt`)
i opinii (`newage-opinia`) — celują w webhooki n8n, których jeszcze nie ma.
Do czasu założenia workflow zgłaszają uczciwie błąd zamiast udawać, że wysłały.

**Domena.** Agnieszka chce `newagelewandowska.pl`. Sprawdzone w rejestrze
NASK 29 sierpnia 2026 — **wolna**. Kupuje ją ona, na swoje dane, razem
z hostingiem (patrz brief na Dysku, sekcja 6).

**Metamorfozy.** Brak sekcji ze zdjęciami klientek do czasu podpisania zgód.
Agnieszka załatwia je sama.

**Zdjęcia z sesji w salonie** — miała ją w poniedziałek, zdjęcia dojdą.

**Prawa do portfolio.** Zdjęcia z magazynu SPLOT i katalogów są autorstwa
Elżbiety Bednarek, z widocznymi twarzami modelek. Agnieszka deklaruje,
że załatwi zgody.

**Przy przenosinach na własną domenę** zmień stałą `BAZA` w generatorze —
stąd biorą się adresy kanoniczne, mapa strony i podgląd przy udostępnianiu.

---

*Spisane 29 sierpnia 2026.*
