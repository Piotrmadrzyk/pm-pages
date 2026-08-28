# -*- coding: utf-8 -*-
"""
build/demo_sprzedaz.py — strony demonstracyjne maja sie sprzedawac.

DLACZEGO TO ISTNIEJE
Dema wygladaly jak strony prawdziwych firm. Goscia, ktory na nie trafi, nic
nie informowalo, ze taka strone moze zamowic dla siebie — a to jest jedyny
powod, dla ktorego te strony w ogole istnieja. Dodatkowo maile i telefony
w demach byly zmyslone: kto by na nie napisal albo zadzwonil, trafialby
donikad. Zainteresowany klient przepadal w tym miejscu.

CO ROBI
Na kazdej stronie kazdego dema:
  1. dokleja pasek sprzedazowy nad stopka — mowi wprost, ze firma jest
     zmyslona, ze strone mozna zamowic, i daje przycisk rezerwacji,
  2. przestawia maile i telefony na prawdziwe dane Probatum,
  3. przepisuje linijke na samym dole stopki na jednoznaczna.

Skrypt mozna puszczac wielokrotnie — pomija strony, ktore juz maja pasek.

JAK URUCHOMIC
    cd build && python3 demo_sprzedaz.py

WYGLAD PASKA
Pasek jest ciemny i taki sam na wszystkich czterech demach — celowo. To glos
Probatum, a nie zmyslonej firmy, i ma byc rozpoznawalny, gdy ktos oglada
dwa dema po kolei. Jedyne, co sie zmienia miedzy stronami, to kolor przycisku
— bierzemy akcent danej strony, zeby pasek nie wygladal jak wklejony z bledu.

Tresc jest wysrodkowana celowo. Kazde demo ma kontener innej szerokosci,
wiec lewa krawedz paska i tak nie trafilaby w krawedz stopki na wszystkich
czterech — a rozjazd o kilkadziesiat pikseli czyta sie jak blad. Wysrodkowany
blok jest po prostu osobny i pytanie o wyrownanie nie powstaje.

CZEGO SKRYPT NIE RUSZA
Adresow pocztowych zmyslonych firm. Sa czescia scenografii i nikogo nie myla,
skoro pasek mowi wprost, ze firma nie istnieje.
"""

import os

from urllib.parse import quote

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Prawdziwe dane — jedno miejsce, tak jak w build.py.
MAIL = u'kontakt@probatum.pl'
TEL_POKAZ = u'+48 573 569 141'
TEL_LINK = u'+48573569141'

DEMA = {

    'lawenda': {
        'firma':   u'Studio Lawenda',
        'branza':  u'salon urody',
        'komu':    u'kosmetyczka albo właścicielka salonu',
        'akcent':  u'#A8814E',
        'akcent_tekst': u'#1a1520',
        'katalog': u'https://probatum.pl/p/katalog-lawenda.html',
        'mail_stary': u'kontakt@studiolawenda.pl',
        'tel_stary':  u'+48178536214',
        'tel_pokaz_stary': u'17 853 62 14',
        'co_dostaje': u'cennik, zapisy na wizytę, galerię efektów i asystenta, '
                      u'który odpowiada na pytania o zabiegi',
    },

    'zawadzcy': {
        'firma':   u'Kancelaria Zawadzcy i Wspólnicy',
        'branza':  u'kancelaria prawna',
        'komu':    u'prawnik albo wspólnicy kancelarii',
        'akcent':  u'#a89063',
        'akcent_tekst': u'#14161b',
        'katalog': u'https://probatum.pl/p/katalog-zawadzcy.html',
        'mail_stary': u'kontakt@zawadzcy-kancelaria.pl',
        'tel_stary':  u'178501234',
        'tel_pokaz_stary': u'17 850 12 34',
        'co_dostaje': u'obszary praktyki, kalkulator terminów, przejrzysty cennik '
                      u'i asystenta, który wstępnie kwalifikuje sprawy',
    },

    'dom-i-wnetrze': {
        'firma':   u'Dom i Wnętrze Warszawa',
        'branza':  u'firma remontowa',
        'komu':    u'wykonawca albo projektantka wnętrz',
        'akcent':  u'#B8763A',
        'akcent_tekst': u'#14161b',
        'katalog': u'https://probatum.pl/p/katalog-dom.html',
        'mail_stary': u'kontakt@domiwnetrzewarszawa.pl',
        'tel_stary':  u'+48224905218',
        'tel_pokaz_stary': u'22 490 52 18',
        'co_dostaje': u'portfolio realizacji, zakres usług, formularz wyceny '
                      u'i asystenta, który zbiera pierwsze dane o remoncie',
    },

    'serwis-podkarpacki': {
        'firma':   u'Serwis Podkarpacki',
        'branza':  u'warsztat samochodowy',
        'komu':    u'mechanik albo właściciel warsztatu',
        'akcent':  u'#e8590c',
        'akcent_tekst': u'#ffffff',
        'katalog': u'https://probatum.pl/p/katalog-serwis.html',
        'mail_stary': u'kontakt@serwispodkarpacki.pl',
        'tel_stary':  u'178624040',
        'tel_pokaz_stary': u'17 862 40 40',
        'co_dostaje': u'zakres usług, umówienie wizyty, zapisy na wymianę opon '
                      u'i asystenta, który odpowiada na pytania o naprawy',
    },
}

# Linijki na dole stopek, ktore trzeba przepisac. Klucz to fragment, ktory
# wystarczy do rozpoznania — pelne zdania roznia sie miedzy demami.
STARE_DOPISKI = [
    u'Szablon poglądowy — dane do uzupełnienia danymi konkretnej kancelarii',
    u'Szablon poglądowy — dane do uzupełnienia danymi konkretnego warsztatu',
    u'Projekt demonstracyjny (portfolio). Fikcyjna marka, dane i zdjęcia poglądowe. '
    u'Zbudowano z pomocą AI.',
]

NOWY_DOPISEK = (u'Strona demonstracyjna Probatum — firma jest zmyślona. '
                u'<a href="https://probatum.pl" style="color:inherit">probatum.pl</a>')


def pasek(d):
    # Temat trafia do adresu mailto:, wiec musi byc zakodowany w calosci —
    # nie tylko spacje. Polskie znaki zostawione surowo potrafia sie przekrecic
    # w czesci programow pocztowych.
    temat = u'Rezerwuję stronę: %s' % d['firma']
    temat_url = quote(temat, safe='')

    return (u'\n<!-- ————— PASEK SPRZEDAZOWY PROBATUM ————— -->\n'
            u'<section class="pmd-pasek" aria-label="Informacja o stronie demonstracyjnej">\n'
            u'  <div class="pmd-in">\n'
            u'    <p class="pmd-etykieta">Probatum · strona demonstracyjna</p>\n'
            u'    <h2 class="pmd-tytul">Ta strona jest do wzięcia</h2>\n'
            u'    <p class="pmd-opis">\n'
            u'      <b>%(firma)s nie istnieje.</b> To projekt pokazowy — zbudowany po to,\n'
            u'      żeby %(komu)s zobaczył swoją przyszłą stronę, zanim za nią zapłaci.\n'
            u'      Wszystko, co tu działa, działa naprawdę: %(co_dostaje)s.\n'
            u'    </p>\n'
            u'    <p class="pmd-opis">\n'
            u'      Bierzemy ten sam szkielet i przestawiamy go na Twoją firmę — treści,\n'
            u'      zdjęcia, kolory, formularze. Nie zaczynamy od pustej kartki, więc\n'
            u'      wiadomo z góry, jak to będzie wyglądać i ile będzie kosztować.\n'
            u'    </p>\n'
            u'    <div class="pmd-akcje">\n'
            u'      <a class="pmd-btn" href="mailto:%(mail)s?subject=%(temat)s">Zarezerwuj tę stronę</a>\n'
            u'      <a class="pmd-btn2" href="%(katalog)s">Zobacz, co ta strona potrafi</a>\n'
            u'    </div>\n'
            u'    <p class="pmd-kontakt">\n'
            u'      Napisz albo zadzwoń: <a href="mailto:%(mail)s">%(mail)s</a>\n'
            u'      · <a href="tel:%(tel_link)s">%(tel_pokaz)s</a>\n'
            u'    </p>\n'
            u'  </div>\n'
            u'</section>\n'
            u'<style>\n'
            u'  .pmd-pasek{background:#14161b;border-top:3px solid %(akcent)s;\n'
            u'    padding:52px 20px 56px;color:#c9ced8;\n'
            u'    font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}\n'
            u'  .pmd-in{max-width:720px;margin:0 auto;display:grid;gap:16px;text-align:center;\n'
            u'    justify-items:center}\n'
            u'  .pmd-etykieta{margin:0;font-size:.74rem;letter-spacing:.16em;\n'
            u'    text-transform:uppercase;color:%(akcent)s;font-weight:700}\n'
            u'  .pmd-tytul{margin:0;color:#fff;font-size:clamp(1.7rem,4vw,2.3rem);\n'
            u'    line-height:1.15;font-weight:700;letter-spacing:-.02em;\n'
            u'    font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;\n'
            u'    text-wrap:balance}\n'
            u'  .pmd-opis{margin:0;font-size:1rem;line-height:1.72;color:#c9ced8;max-width:62ch}\n'
            u'  .pmd-opis b{color:#fff}\n'
            u'  .pmd-akcje{display:flex;flex-wrap:wrap;gap:12px;margin-top:6px;\n'
            u'    justify-content:center}\n'
            u'  .pmd-btn,.pmd-btn2{display:inline-block;text-decoration:none;\n'
            u'    padding:.85rem 1.5rem;border-radius:999px;font-weight:700;font-size:.94rem;\n'
            u'    transition:transform .18s ease,opacity .18s ease}\n'
            u'  .pmd-btn{background:%(akcent)s;color:%(akcent_tekst)s}\n'
            u'  .pmd-btn2{background:transparent;color:#e7e9ee;\n'
            u'    border:1px solid rgba(255,255,255,.26)}\n'
            u'  .pmd-btn:hover,.pmd-btn2:hover{transform:translateY(-2px)}\n'
            u'  .pmd-btn2:hover{border-color:rgba(255,255,255,.5)}\n'
            u'  .pmd-btn:focus-visible,.pmd-btn2:focus-visible{outline:2px solid #fff;\n'
            u'    outline-offset:3px}\n'
            u'  .pmd-kontakt{margin:4px 0 0;font-size:.92rem;color:#9aa2af}\n'
            u'  .pmd-kontakt a{color:#fff;text-decoration:none;\n'
            u'    border-bottom:1px solid rgba(255,255,255,.35)}\n'
            u'  .pmd-kontakt a:hover{border-bottom-color:#fff}\n'
            u'  @media (prefers-reduced-motion:reduce){\n'
            u'    .pmd-btn,.pmd-btn2{transition:none}\n'
            u'    .pmd-btn:hover,.pmd-btn2:hover{transform:none}}\n'
            u'</style>\n') % {
        'firma': d['firma'], 'komu': d['komu'], 'co_dostaje': d['co_dostaje'],
        'mail': MAIL, 'temat': temat_url, 'katalog': d['katalog'],
        'tel_link': TEL_LINK, 'tel_pokaz': TEL_POKAZ,
        'akcent': d['akcent'], 'akcent_tekst': d['akcent_tekst'],
    }


def przerob(sciezka, d):
    with open(sciezka, encoding='utf-8') as fh:
        t = fh.read()
    przed = t
    zrobione = []

    # 1. Pasek nad stopka.
    if 'pmd-pasek' not in t:
        i = t.rfind('<footer')
        if i != -1:
            t = t[:i] + pasek(d) + t[i:]
            zrobione.append('pasek')

    # 2. Zmyslony mail na prawdziwy. Zmyslone adresy nie istnieja — kto by
    #    na nie napisal, przepadalby bez sladu.
    if d['mail_stary'] in t:
        ile = t.count(d['mail_stary'])
        t = t.replace(d['mail_stary'], MAIL)
        zrobione.append('mail x%d' % ile)

    # 3. Zmyslony telefon na prawdziwy. Numer wymyslony na potrzeby dema moze
    #    nalezec do przypadkowej osoby — nie chcemy jej nasylac telefonow.
    # Podmieniamy dwie dokladnie znane postacie numeru: te z href="tel:"
    # i te wypisana na ekranie. Zadnego zgadywania wzorcem — w dokumencie
    # jest pelno innych cyfr i regex potrafilby trafic w przypadkowa.
    ile_tel = t.count('tel:' + d['tel_stary']) + t.count(d['tel_pokaz_stary'])
    if ile_tel:
        t = t.replace('tel:' + d['tel_stary'], 'tel:' + TEL_LINK)
        t = t.replace(d['tel_pokaz_stary'], TEL_POKAZ)
        # Numer siedzi takze w danych strukturalnych JSON-LD w naglowku
        # ("telephone": "+48..."). Tego nie widac na ekranie, ale wyszukiwarki
        # to czytaja — a numer nadal moze nalezec do przypadkowej osoby.
        t = t.replace('"%s"' % d['tel_stary'], '"%s"' % TEL_LINK)
        zrobione.append('telefon x%d' % ile_tel)

    # 4. Linijka na dole stopki.
    for stary in STARE_DOPISKI:
        if stary in t:
            t = t.replace(stary, NOWY_DOPISEK)
            zrobione.append('dopisek')
            break

    if t != przed:
        with open(sciezka, 'w', encoding='utf-8') as fh:
            fh.write(t)
    return zrobione


def przerob_skrypt(sciezka, d):
    """Maile i telefony siedza takze w assets/site.js — w komunikatach bledu
    asystenta ("Brak polaczenia, zadzwon prosze: ..."). Bez tego zmyslony
    numer wracalby dokladnie w chwili, gdy cos nie zadziala."""
    with open(sciezka, encoding='utf-8') as fh:
        t = fh.read()
    przed = t
    zrobione = []

    if d['mail_stary'] in t:
        zrobione.append('mail x%d' % t.count(d['mail_stary']))
        t = t.replace(d['mail_stary'], MAIL)

    ile = t.count('tel:' + d['tel_stary']) + t.count(d['tel_pokaz_stary'])
    if ile:
        t = t.replace('tel:' + d['tel_stary'], 'tel:' + TEL_LINK)
        t = t.replace(d['tel_pokaz_stary'], TEL_POKAZ)
        zrobione.append('telefon x%d' % ile)

    if t != przed:
        with open(sciezka, 'w', encoding='utf-8') as fh:
            fh.write(t)
    return zrobione


def main():
    katalog_p = os.path.join(ROOT, 'p')
    zmienione = 0
    for wpis in sorted(os.listdir(katalog_p)):
        sciezka = os.path.join(katalog_p, wpis, 'index.html')
        if not os.path.isfile(sciezka):
            continue
        d = None
        for klucz, dane in DEMA.items():
            if klucz in wpis:
                d = dane
                break
        if d is None:
            continue
        zrobione = przerob(sciezka, d)

        skrypt = os.path.join(katalog_p, wpis, 'assets', 'site.js')
        if os.path.isfile(skrypt):
            dodatkowe = przerob_skrypt(skrypt, d)
            if dodatkowe:
                zrobione.append('site.js (%s)' % ', '.join(dodatkowe))

        if zrobione:
            zmienione += 1
            print('  %-42s %s' % (wpis, ', '.join(zrobione)))
        else:
            print('  %-42s bez zmian' % wpis)
    print('\nZmienionych stron: %d' % zmienione)


if __name__ == '__main__':
    main()
