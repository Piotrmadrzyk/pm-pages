"""Information scoped to the inspected static Site, not a generic consent policy."""

CONTENT = '''<section class="cookie-page container">
<p class="eyebrow">INFORMACJE O STRONIE</p>
<h1>Cookies i dane<br><em>w przeglądarce.</em></h1>
<p class="cookie-lead">Poniżej opisujemy działanie tej wersji strony Probatum, formularzy i podglądów projektów.</p>
<div class="cookie-content">
<h2>Co to są cookies?</h2>
<p>To niewielkie informacje zapisywane przez serwisy w przeglądarce. Mogą służyć na przykład do utrzymania logowania, zapamiętania ustawień lub mierzenia odwiedzin.</p>
<h2>Co zapisuje ta strona?</h2>
<p>Kod strony Probatum sam z siebie nie ustawia żadnych plików cookies. Jedyne cookies, jakie mogą się pojawić, pochodzą z Google Analytics — i tylko wtedy, gdy klikniesz „Akceptuję” w banerze na dole ekranu. Dopóki tego nie zrobisz, żaden skrypt Google się nie wczytuje. Grafiki, filmy i czcionki są wczytywane z tego samego serwisu.</p>
<table class="kv">
<tr><td><b>_ga</b></td><td>Google Analytics — rozróżnia odwiedzających. Wygasa po 2 latach.</td></tr>
<tr><td><b>_ga_&lt;identyfikator&gt;</b></td><td>Google Analytics — utrzymuje stan sesji i statystyki odwiedzin. Wygasa po 2 latach.</td></tr>
</table>
<p>Nie korzystamy z piksela Meta ani innych skryptów reklamowych. Twoją decyzję (zgoda / odmowa) trzymamy w pamięci przeglądarki (localStorage), nie w cookie.</p>
<p>Ta informacja dotyczy funkcji strony. Prywatny podgląd jest udostępniany przez platformę hostingową. Jej mechanizmy dostępu, logowania i zabezpieczeń działają niezależnie od kodu Probatum i podlegają zasadom dostawcy. Nie deklarujemy tutaj nazw ani czasu przechowywania jego cookies.</p>
<h2 id="podglady">Podglądy innych stron</h2>
<p>Serwisy Edward Janusz i Silver &amp; Glass wczytują się w osadzonym podglądzie dopiero po naciśnięciu „Otwórz podgląd”. Wtedy przeglądarka łączy się z wybranym serwisem, który otrzymuje dane połączenia, w tym adres IP, i może korzystać z własnych cookies. Zapoznaj się z informacjami i ustawieniami prywatności na otwartej stronie.</p>
<p>Przycisk „Zamknij podgląd” usuwa osadzoną stronę. Nie usuwa cookies, które mogła już zapisać. Do tego służą ustawienia przeglądarki. Otwarcie odnośnika w nowej karcie również przenosi Cię do osobnego serwisu.</p>
<h2 id="formularze">Co dzieje się z formularzem?</h2>
<p>Formularze kontaktu i wyceny przygotowują treść wiadomości w przeglądarce. Nie wysyłają jej automatycznie i nie zapisują pól na serwerze Probatum. Dopiero wybranie „Otwórz wiadomość w poczcie” przekazuje przygotowaną treść do Twojego programu pocztowego. O wysłaniu decydujesz w tym programie.</p>
<p>Przycisk kopiowania zapisuje wybraną treść w schowku urządzenia. Automatyczne uzupełnianie lub przywracanie pól przez przeglądarkę zależy od jej ustawień.</p>
<h2>Jak zarządzać cookies?</h2>
<p>Swoją decyzję o Google Analytics możesz zmienić w każdej chwili:</p>
<button type="button" class="consent-manage-btn" data-consent-manage>Zmień zgodę na Google Analytics</button>
<p>W ustawieniach prywatności przeglądarki możesz dodatkowo sprawdzić i usunąć dane poszczególnych witryn oraz zablokować cookies stron trzecich. Zmiana tych ustawień może wpłynąć na logowanie i działanie zewnętrznych serwisów.</p>
<p>Zasady przechowywania informacji na urządzeniu opisuje <a href="https://eli.gov.pl/api/acts/DU/2024/1221/text/U/D20241221Lj.pdf" target="_blank" rel="noopener">art. 399 Prawa komunikacji elektronicznej</a>. Zasady przetwarzania danych przez Google opisuje <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">polityka prywatności Google</a>.</p>
<h2>Masz pytanie?</h2>
<p>Napisz na <a href="mailto:kontakt@probatum.pl">kontakt@probatum.pl</a>.</p>
<p class="cookie-updated">Aktualizacja: 10 września 2026 r.</p>
</div></section>'''

def add_cookie_information(pages):
    pages['cookies.html'] = ('Cookies i dane | Probatum', 'Informacje o cookies, formularzach i zewnętrznych podglądach w tej wersji strony Probatum.', CONTENT, 'cookies')
