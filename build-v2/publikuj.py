#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""publikuj.py — jedyna bezpieczna droga zbudowania publicznej strony probatum.pl.

Jak to dziala:
  1. Liczy sumy kontrolne wszystkiego, czego dotknac nie wolno.
  2. Buduje cala strone w katalogu TYMCZASOWYM poza repozytorium.
  3. Sprawdza wynik walidatorem i testem zachowania skryptow.
  4. Dopiero potem przenosi na publiczny poziom repozytorium WYLACZNIE pliki
     wymienione w manifescie v2.
  5. Ponownie liczy sumy chronionych plikow — kazda zmiana konczy sie bledem.
  6. Kasuje wylacznie osierocone strony po poprzednim manifescie v2.

Czego NIGDY nie dotyka:
  p/ (strony klientow), vercel.json, .vercelignore, SUBDOMENY.md
  oraz assets/katalog.css i assets/katalog.js — na tych dwoch wisza cztery
  katalogi w p/ (katalog-dom, katalog-lawenda, katalog-serwis, katalog-zawadzcy).

Uwaga o zasobach: pliki w assets/ poza flow-data.js to material zrodlowy
strony, nie wynik budowania. Leza na publicznym poziomie na stale i sa
kopiowane do katalogu tymczasowego tylko po to, by generator i walidator
mialy komplet do sprawdzenia.

Uzycie:
    python3 build-v2/publikuj.py            # wersja produkcyjna, do indeksowania
    python3 build-v2/publikuj.py --prywatna # noindex + robots.txt z zakazem
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GENERATOR = Path(__file__).resolve().parent
REPO = GENERATOR.parent
MANIFEST = GENERATOR / 'MANIFEST-v2.txt'

CHRONIONE_PLIKI = [
    'vercel.json',
    '.vercelignore',
    'SUBDOMENY.md',
    'assets/katalog.css',
    'assets/katalog.js',
]
CHRONIONE_KATALOGI = ['p']

# Poza stronami z manifestu generator wytwarza jeszcze te pliki.
DODATKOWE_WYNIKI = ['robots.txt', 'sitemap.xml', 'assets/flow-data.js']


def odcisk(sciezka):
    return hashlib.sha256(sciezka.read_bytes()).hexdigest()


def odciski_chronionych():
    u"""Sumy kontrolne wszystkiego, co ma przetrwac budowanie bez zmian."""
    stan = {}
    for wzgledna in CHRONIONE_PLIKI:
        plik = REPO / wzgledna
        if plik.exists():
            stan[wzgledna] = odcisk(plik)
    for katalog in CHRONIONE_KATALOGI:
        for plik in sorted((REPO / katalog).rglob('*')):
            if plik.is_file():
                stan[str(plik.relative_to(REPO))] = odcisk(plik)
    return stan


def uruchom(polecenie, srodowisko):
    print('  $ ' + ' '.join(str(c) for c in polecenie))
    wynik = subprocess.run([str(c) for c in polecenie], cwd=GENERATOR,
                           env=srodowisko, capture_output=True, text=True)
    if wynik.stdout.strip():
        print('    ' + wynik.stdout.strip().replace('\n', '\n    '))
    if wynik.returncode != 0:
        print('    ' + (wynik.stderr.strip() or 'bez komunikatu na stderr'))
        sys.exit(u'PRZERWANE: %s zakonczylo sie bledem.' % polecenie[-1])


def wczytaj_manifest():
    if not MANIFEST.exists():
        return set()
    return {w.strip() for w in MANIFEST.read_text().splitlines() if w.strip()}


def main():
    prywatna = '--prywatna' in sys.argv

    if not (REPO / 'vercel.json').exists() or not (REPO / 'p').is_dir():
        sys.exit(u'PRZERWANE: to nie wyglada na korzen repozytorium pm-pages.')
    if not (REPO / 'assets' / 'site.css').exists():
        sys.exit(u'PRZERWANE: brak assets/site.css — material zrodlowy strony.')

    print(u'Odciski plikow chronionych...')
    przed = odciski_chronionych()
    print(u'  zabezpieczonych plikow: %d' % len(przed))

    poprzedni_manifest = wczytaj_manifest()

    roboczy = Path(tempfile.mkdtemp(prefix='probatum-v11-'))
    try:
        print(u'\nKatalog roboczy: %s' % roboczy)
        shutil.copytree(REPO / 'assets', roboczy / 'assets')

        srodowisko = dict(os.environ, PROBATUM_OUT=str(roboczy))
        if prywatna:
            srodowisko['PROBATUM_PRIVATE'] = '1'
            print(u'Tryb PRYWATNY: noindex + robots.txt z zakazem.')

        print(u'\nBudowanie i kontrole w katalogu roboczym...')
        uruchom([sys.executable, 'compose.py'], srodowisko)
        uruchom([sys.executable, 'validate.py'], srodowisko)
        uruchom(['node', 'tests/studio-runtime.cjs'], srodowisko)

        nowy_manifest = wczytaj_manifest()
        if not nowy_manifest:
            sys.exit(u'PRZERWANE: generator nie zostawil manifestu.')

        print(u'\nPrzenoszenie na publiczny poziom...')
        przeniesione = 0
        for wzgledna in sorted(nowy_manifest) + DODATKOWE_WYNIKI:
            if wzgledna in CHRONIONE_PLIKI or wzgledna.split('/')[0] in CHRONIONE_KATALOGI:
                sys.exit(u'PRZERWANE: manifest chce nadpisac plik chroniony: %s' % wzgledna)
            zrodlo = roboczy / wzgledna
            if not zrodlo.exists():
                sys.exit(u'PRZERWANE: generator nie wytworzyl %s' % wzgledna)
            cel = REPO / wzgledna
            cel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(zrodlo, cel)
            przeniesione += 1
        print(u'  przeniesionych plikow: %d' % przeniesione)
    finally:
        shutil.rmtree(roboczy, ignore_errors=True)

    print(u'\nPonowne odciski plikow chronionych...')
    po = odciski_chronionych()
    if po != przed:
        zmienione = sorted(set(przed) ^ set(po)) + \
                    sorted(k for k in przed if k in po and przed[k] != po[k])
        sys.exit(u'PRZERWANE: publikacja ruszyla pliki chronione:\n  ' +
                 '\n  '.join(zmienione))
    print(u'  bez zmian — granice nienaruszone')

    osierocone = sorted(poprzedni_manifest - nowy_manifest)
    for wzgledna in osierocone:
        if wzgledna in CHRONIONE_PLIKI or wzgledna.split('/')[0] in CHRONIONE_KATALOGI:
            continue
        plik = REPO / wzgledna
        if plik.exists():
            plik.unlink()
            print(u'  skasowana osierocona strona: %s' % wzgledna)

    print(u'\nGOTOWE: %d stron na publicznym poziomie%s.'
          % (len(nowy_manifest), u' (wersja prywatna)' if prywatna else ''))


if __name__ == '__main__':
    main()
