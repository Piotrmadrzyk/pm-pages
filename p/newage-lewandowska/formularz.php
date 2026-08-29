<?php
/*  formularz.php — wysyłka formularzy ze strony new age Lewandowska
 *
 *  DO CZEGO TO JEST
 *  Domyślnie formularze na stronie otwierają program pocztowy z gotową
 *  wiadomością. Działa wszędzie, ale wymaga, żeby odwiedzający miał
 *  skonfigurowaną pocztę. Ten plik sprawia, że wiadomość wychodzi w tle.
 *
 *  JAK WŁĄCZYĆ (dwa kroki)
 *  1. Wgraj ten plik obok index.html na hosting z PHP (home.pl ma PHP
 *     w każdym pakiecie).
 *  2. W pliku skrypt.js zmień:
 *         var ADRES_WYSYLKI = '';
 *     na:
 *         var ADRES_WYSYLKI = 'formularz.php';
 *
 *  Poniżej ustaw swój adres — ten, na który mają przychodzić zgłoszenia.
 */

$ADRES_ODBIORCY = 'kontakt@probatum.pl';   // ⚠️ zmień na swój adres
$NAZWA_NADAWCY  = 'Strona new age Lewandowska';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'blad', 'powod' => 'zla metoda']);
    exit;
}

$dane = json_decode(file_get_contents('php://input'), true);
if (!is_array($dane) || empty($dane['tresc'])) {
    http_response_code(400);
    echo json_encode(['status' => 'blad', 'powod' => 'brak tresci']);
    exit;
}

/* Proste zabezpieczenie: nikt nie wysyła dwóch zgłoszeń w ciągu 20 sekund
   z tego samego adresu. Wystarczy przeciw najprostszym robotom. */
session_start();
if (isset($_SESSION['ostatnie']) && time() - $_SESSION['ostatnie'] < 20) {
    http_response_code(429);
    echo json_encode(['status' => 'blad', 'powod' => 'za szybko']);
    exit;
}
$_SESSION['ostatnie'] = time();

$temat = isset($dane['temat']) ? $dane['temat'] : 'Wiadomość ze strony';
$temat = mb_substr(preg_replace('/[\r\n]+/', ' ', $temat), 0, 160);
$tresc = mb_substr($dane['tresc'], 0, 4000);

$naglowki  = 'From: ' . $NAZWA_NADAWCY . ' <' . $ADRES_ODBIORCY . ">\r\n";
$naglowki .= "Content-Type: text/plain; charset=utf-8\r\n";

$wyslano = @mail($ADRES_ODBIORCY, '=?UTF-8?B?' . base64_encode($temat) . '?=',
                 $tresc, $naglowki);

if ($wyslano) {
    echo json_encode(['status' => 'ok']);
} else {
    http_response_code(500);
    echo json_encode(['status' => 'blad', 'powod' => 'poczta odmowila']);
}
