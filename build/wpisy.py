#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zamienia zwykłe pliki tekstowe na strony wpisów.

Jeden wpis = jeden plik .txt w build/wpisy/blog/ albo build/wpisy/warsztat/.
Nazwa pliku staje się adresem strony, np. pierwszy-agent.txt →
/warsztat/pierwszy-agent.html

Na górze pliku idą dane wpisu, potem trzy myślniki, potem treść:

    tytul: Jak odzyskać godzinę dziennie
    data: 2026-08-20
    opis: Krótkie zdanie, które zobaczy Google i czytelnik na liście.
    ---
    Tu zaczyna się treść.

Warsztat przyjmuje dodatkowo: czas, poziom, narzedzia.

W treści działa:
    ## Nagłówek            ### Mniejszy nagłówek
    - punkt listy          1. punkt numerowany
    **pogrubienie**        *kursywa*
    `kod w linii`          ```blok kodu```
    > cytat / uwaga
    [tekst](adres)         ![opis](assets/img/cos.jpg)
    ---                    (linia oddzielająca)
"""
import io, os, re, html as _html

MIESIACE = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
            'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']


def data_po_polsku(iso):
    """2026-08-20 → 20 sierpnia 2026"""
    try:
        r, m, d = iso.split('-')
        return '%d %s %s' % (int(d), MIESIACE[int(m) - 1], r)
    except Exception:
        return iso


def czytaj_wpis(sciezka):
    """Rozdziela dane wpisu od treści."""
    tekst = io.open(sciezka, encoding='utf-8').read()
    if '\n---' in tekst:
        glowa, tresc = tekst.split('\n---', 1)
        tresc = tresc.lstrip('\n')
    else:
        glowa, tresc = '', tekst

    dane = {}
    for linia in glowa.split('\n'):
        if ':' in linia:
            k, v = linia.split(':', 1)
            dane[k.strip().lower()] = v.strip()

    dane['plik'] = os.path.splitext(os.path.basename(sciezka))[0]
    dane.setdefault('tytul', dane['plik'].replace('-', ' ').capitalize())
    dane.setdefault('data', '')
    dane.setdefault('opis', '')
    dane['tresc'] = tresc
    return dane


# ---------- zamiana treści na HTML ----------

def _wstawki(t):
    """Pogrubienia, kursywa, kod, linki i obrazy wewnątrz akapitu."""
    t = _html.escape(t, quote=False)
    # obrazy muszą iść przed linkami, bo mają ten sam kształt
    t = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
               r'<img src="\2" alt="\1" loading="lazy">', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: '<a href="%s"%s>%s</a>' % (
                   m.group(2),
                   ' target="_blank" rel="noopener"' if m.group(2).startswith('http') else '',
                   m.group(1)), t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    return t


def na_html(tresc):
    linie = tresc.split('\n')
    out, i = [], 0
    while i < len(linie):
        l = linie[i]

        # blok kodu
        if l.strip().startswith('```'):
            i += 1
            blok = []
            while i < len(linie) and not linie[i].strip().startswith('```'):
                blok.append(linie[i]); i += 1
            i += 1
            out.append('<pre class="kod"><code>%s</code></pre>'
                       % _html.escape('\n'.join(blok), quote=False))
            continue

        # linia oddzielająca
        if l.strip() in ('---', '***'):
            out.append('<hr>'); i += 1; continue

        # nagłówki
        n = re.match(r'^(#{2,4})\s+(.*)$', l)
        if n:
            poziom = len(n.group(1))
            out.append('<h%d>%s</h%d>' % (poziom, _wstawki(n.group(2)), poziom))
            i += 1; continue

        # cytat / uwaga
        if l.strip().startswith('> '):
            blok = []
            while i < len(linie) and linie[i].strip().startswith('> '):
                blok.append(linie[i].strip()[2:]); i += 1
            out.append('<blockquote>%s</blockquote>' % _wstawki(' '.join(blok)))
            continue

        # listy
        if re.match(r'^\s*[-*]\s+', l):
            blok = []
            while i < len(linie) and re.match(r'^\s*[-*]\s+', linie[i]):
                blok.append(re.sub(r'^\s*[-*]\s+', '', linie[i])); i += 1
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % _wstawki(x) for x in blok))
            continue

        if re.match(r'^\s*\d+[.)]\s+', l):
            blok = []
            while i < len(linie) and re.match(r'^\s*\d+[.)]\s+', linie[i]):
                blok.append(re.sub(r'^\s*\d+[.)]\s+', '', linie[i])); i += 1
            out.append('<ol>%s</ol>' % ''.join('<li>%s</li>' % _wstawki(x) for x in blok))
            continue

        # akapit
        if l.strip():
            blok = []
            while i < len(linie) and linie[i].strip() \
                    and not re.match(r'^\s*([-*]\s|\d+[.)]\s|#{2,4}\s|>|```)', linie[i]) \
                    and linie[i].strip() not in ('---', '***'):
                blok.append(linie[i].strip()); i += 1
            out.append('<p>%s</p>' % _wstawki(' '.join(blok)))
            continue

        i += 1
    return '\n'.join(out)


def wczytaj_katalog(katalog):
    """Wszystkie wpisy z katalogu, od najnowszego."""
    if not os.path.isdir(katalog):
        return []
    wpisy = [czytaj_wpis(os.path.join(katalog, f))
             for f in os.listdir(katalog) if f.endswith('.txt')]
    return sorted(wpisy, key=lambda w: (w['data'], w['plik']), reverse=True)
