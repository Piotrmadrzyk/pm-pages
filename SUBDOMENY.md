# Subdomeny stron demonstracyjnych

Konfiguracja siedzi w `vercel.json` w katalogu glownym. Ten plik istnieje
dlatego, ze **`vercel.json` nie moze zawierac komentarzy ani wlasnych kluczy** —
to czysty JSON sprawdzany przez Vercela wzgledem schematu. Wlasny klucz
(np. `_opis` z wyjasnieniem) sprawia, ze Vercel odrzuca **cala** konfiguracje,
zanim cokolwiek zbuduje: wdrozenie konczy sie stanem ERROR i **bez logow
budowania**, bo do budowania w ogole nie dochodzi. Latwo to zle odczytac jako
awarie strony.

## Co robia te reguly

| adres | pokazuje |
|---|---|
| `lawenda-demo.probatum.pl` | Studio Lawenda |
| `kancelaria-demo.probatum.pl` | Kancelaria Zawadzcy |
| `remonty-demo.probatum.pl` | Dom i Wnetrze |
| `warsztat-demo.probatum.pl` | Serwis Podkarpacki |

Regula mowi: jesli gosc wszedl pod danym adresem, pokaz mu zawartosc
odpowiedniego katalogu z `/p/`. Adres w pasku zostaje krotki.

## Czego NIE robia

Przepisywany jest **tylko adres glowny**. Podstrony kazdego demo leza
w osobnych katalogach obok siebie (`demo-studio-lawenda-kontakt` itd.),
wiec po kliknieciu w menu adres bedzie dluzszy:
`lawenda-demo.probatum.pl/p/demo-studio-lawenda-kontakt/`.

Dziala, ale nie jest ladne. Skrocenie takze podstron wymaga przebudowy
struktury katalogow — opisane w `DO-ZROBIENIA.md` jako droga B.

## Warunek dzialania

Reguly dzialaja dopiero wtedy, gdy subdomena naprawde kieruje na ten projekt —
czyli po dodaniu domeny w Vercelu i wpisu CNAME w home.pl. Oba kroki zrobione
28 sierpnia 2026.
