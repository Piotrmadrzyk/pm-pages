"""Immersive openings and quieter editorial navigation for the existing static Site."""
import re

def artwork(name):
    return f'<picture><source media="(max-width:700px)" srcset="/assets/openings/{name}-small.webp"><img src="/assets/openings/{name}.webp" width="1536" height="1024" alt="" fetchpriority="high"></picture>'

def opening(kind,kicker,title,description,asset,compact=False):
    art=artwork(asset)
    folds=''.join(f'<div class="opening-fold fold-{i}">{art}</div>' for i in range(3))
    return f'''<section class="immersive-opening opening-{kind}{' opening-compact' if compact else ''}" data-opening-motion>
<div class="opening-art" aria-hidden="true">{art}<div class="opening-folds">{folds}</div></div>
<div class="opening-copy container"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="opening-description">{description}</p></div>
<div class="opening-foot container"><span>{'PROBATUM / NOWE MOŻLIWOŚCI' if kind not in ['contact','quote'] else 'PROBATUM / POCZĄTEK WSPÓŁPRACY'}</span><button type="button" data-opening-toggle hidden aria-label="Wstrzymaj animację otwarcia">Wstrzymaj ruch</button></div></section>'''

def gallery_opening():
    photos=[('janusz-original.webp','Oryginalna fotografia z serwisu Edward Janusz'),('silver-pt-3-79-a.webp','Awers oryginalnej pocztówki ze zbioru Silver & Glass'),('silver-pt-3-79-b.webp','Rewers tej samej pocztówki')]
    # Exact local photo basename resolved against the existing archive, never regenerated.
    from pathlib import Path
    import os
    _out=os.environ.get('PROBATUM_OUT')
    live=(Path(_out) if _out else Path(__file__).parent/'dist')/'assets/live'
    if not (live/photos[0][0]).exists():
        original=next(p.name for p in live.glob('*') if 'janusz' in p.name and 'original' in p.name)
        photos[0]=(original,photos[0][1])
    frames=''.join(f'<figure class="gallery-card card-{i}"><img src="/assets/live/{file}" alt="{alt}" width="1600" height="1100" fetchpriority="high"></figure>' for i,(file,alt) in enumerate(photos))
    return f'''<section class="immersive-opening opening-gallery" data-opening-motion><div class="opening-copy container"><p class="eyebrow">PROJEKTY / HISTORIE Z WŁASNYM CHARAKTEREM</p><h1>Warto<br><em>zostać na dłużej.</em></h1><p class="opening-description">Edward Janusz. Silver &amp; Glass.<br>Prawdziwe zbiory, nowe doświadczenia.</p></div><div class="gallery-flight">{frames}</div><div class="opening-foot container"><span>FOTOGRAFIE I POCZTÓWKI / ORYGINALNE ZBIORY</span><button type="button" data-opening-toggle hidden>Wstrzymaj ruch</button></div></section>'''

def drop_intro(body):
    return re.sub(r'^<section class="page-intro studio-intro">.*?</section>','',body,count=1,flags=re.S)

def apply_openings(pages):
    specs={
      'oferta.html':('formation','OFERTA / TWÓJ POTENCJAŁ','Nadajemy<br><em>pomysłom formę.</em>','Strategia, wizerunek, strona i marketing.<br>Elementy jednej, wyrazistej marki.','formation'),
      'marketing.html':('resonance','MARKETING / DAJ SIĘ USŁYSZEĆ','Dobry przekaz.<br><em>Coraz dalej.</em>','Łączymy pomysł, reklamę i drogę do Twojej firmy.','resonance'),
      'social-media.html':('social','SOCIAL MEDIA / WŁASNY CHARAKTER','Twoja marka.<br><em>Żywa opowieść.</em>','Obraz, ruch i treści, do których chce się wracać.','resonance'),
      'akademia.html':('unfold','AKADEMIA AI / NOWE UMIEJĘTNOŚCI','Rozwiń<br><em>swoje możliwości.</em>','Od pierwszego pytania do własnego rezultatu.','unfold'),
      'blog.html':('knowledge','WIEDZA / NOWA PERSPEKTYWA','Dostrzeż więcej.<br><em>Zrozum lepiej.</em>','O stronach, komunikacji i AI. Z praktycznego punktu widzenia.','insight'),
      'warsztat.html':('workshop','WARSZTAT / OD WIEDZY DO DZIAŁANIA','Zacznij od idei.<br><em>Skończ z efektem.</em>','Małe zadanie. Jasna kolejność. Własny rezultat.','formation'),
      'kontakt.html':('contact','KONTAKT / TWOJA FIRMA, NOWY ROZDZIAŁ','Dobry początek?<br><em>Rozmowa.</em>','Opowiedz, co chcesz stworzyć lub zmienić.','encounter'),
      'wycena.html':('quote','WYCENA / OD POMYSŁU DO PLANU','Nadajmy temu<br><em>konkretny kształt.</em>','Trzy krótkie kroki do zapytania o Twój projekt.','unfold')
    }
    for path,spec in specs.items():
        title,desc,body,cls=pages[path]
        body=drop_intro(body)
        if path in ['marketing.html','social-media.html']:
            body=body.replace('campaign-opening','campaign-example')
            body=re.sub(r'<div class="container campaign-heading">.*?</div>','<div class="container campaign-example-title"><p class="eyebrow">JEDEN POMYSŁ / SPÓJNA KAMPANIA</p><h2>Charakter w każdym formacie.</h2></div>',body,count=1,flags=re.S)
        if path=='akademia.html':
            body=re.sub(r'<h1>.*?</h1>','<h2>Lepsze pytanie.<br><em>Lepszy początek.</em></h2>',body,count=1,flags=re.S)
            body=re.sub(r'<a class="button primary"[^>]*>Zapytaj o program.*?</a>','',body,count=1,flags=re.S)
        pages[path]=(title,desc,opening(*spec,compact=path in ['kontakt.html','wycena.html'])+body,cls)
    title,desc,body,cls=pages['realizacje.html']
    pages['realizacje.html']=(title,desc,gallery_opening()+drop_intro(body),cls)
    # The website assembly itself becomes the first full-size scene; no preceding banner.
    title,desc,body,cls=pages['strony-www.html']
    body=body.replace('Wygląd to początek.<br><em>Liczy się doświadczenie.</em>','Pomysł.<br><em>Obraz. Doświadczenie.</em>')
    body=body.replace('Zobacz, jak powstaje strona ↓','PLAN / OBRAZ / CHARAKTER')
    body=re.sub(r'<div><p>Przyciągnij uwagę.*?</div>','',body,count=1,flags=re.S)
    pages['strony-www.html']=(title,desc,body,cls)
    # Article openings use the same visual language, retaining the original article heading.
    for path in ['blog/po-co-agent-malej-firmie.html','warsztat/pierwsza-automatyzacja.html']:
        title,desc,body,cls=pages[path]
        body=body.replace('class="article-head"','class="article-head article-visual-opening" data-opening-motion',1)
        body=body.replace('<div class="article-layout', '<div class="article-layout',1)
        start=body.find('<section class="article-head')
        if start<0:start=body.find('<header class="article-head')
        if start>=0:
            pos=body.find('>',start)+1
            body=body[:pos]+'<div class="article-opening-art" aria-hidden="true">'+artwork('unfold')+'</div>'+body[pos:]
        pages[path]=(title,desc,body,cls)
    for path,(title,desc,body,cls) in list(pages.items()):
        body=calm_markup(body)
        pages[path]=(title,desc,body,cls)

def calm_markup(body):
    # Remove repeated decorative navigation marks, not the SVG paths explaining workflows.
    body=re.sub(r'<span aria-hidden="true">[↗→↓↑]</span>','',body)
    body=body.replace('↗','')
    body=re.sub(r'([→▶↻])\ufe0e*', r'\1'+'\ufe0e', body)
    body=re.sub(r'<a class="image-action"[^>]*aria-label="Zobacz pokaz powstawania strony"[^>]*>.*?</a>','',body)
    body=re.sub(r'<a class="text-link" href="/realizacje.html">Zobacz projekty\s*</a>','',body)
    body=re.sub(r'<a class="spring-next".*?</a>','',body)
    body=re.sub(r'<a class="close-phone".*?</a>','',body)
    for old,new in [('Zobacz, co możemy zrobić','Oferta'),('STRONY WWW / ZOBACZ POWSTAWANIE PROJEKTU','STRONY WWW / OD POMYSŁU DO STRONY'),('Zobacz agentów w działaniu','Agenci AI'),('Zobacz, jak<br><em>pracują agenci.</em>','Twój zespół.<br><em>W ruchu.</em>'),('Zobacz nasze podejście','Nasze podejście'),('Zobacz więcej','Zakres usługi'),('Zobacz koncepcję kampanii','Koncepcja kampanii')]:body=body.replace(old,new)
    return body
