"""Public, editorial diagrams based on inspected workflows; no live system data."""
from html import escape as esc

ICONS = {
    'mail': '<rect x="3" y="5" width="22" height="17" rx="3"/><path d="m4 7 10 8L24 7"/>',
    'search': '<circle cx="12" cy="12" r="7"/><path d="m17 17 7 7"/>',
    'person': '<circle cx="14" cy="8" r="4"/><path d="M5 25v-3a9 9 0 0 1 18 0v3"/>',
    'folder': '<path d="M3 8V5h8l3 4h11v15H3Z"/>',
    'write': '<path d="m18 3 7 7-13 13-8 2 2-8Z M15 6l7 7"/>',
    'check': '<path d="M6 14l5 5L23 7"/>',
    'send': '<path d="m3 4 22 10-22 10 4-10Z M7 14h18"/>',
    'pause': '<path d="M10 5v18M19 5v18"/>',
    'play': '<rect x="3" y="3" width="22" height="22" rx="5"/><path d="m11 8 8 6-8 6Z"/>',
    'sound': '<path d="M4 11v6m5-11v16m5-19v22m5-19v16m5-12v8"/>',
    'cut': '<circle cx="6" cy="7" r="3"/><circle cx="6" cy="21" r="3"/><path d="m9 9 16 15M9 19 25 4"/>',
    'web': '<rect x="2" y="4" width="24" height="20" rx="3"/><path d="M2 10h24M7 7h1m3 0h1M7 15h6m-6 4h13"/>',
    'chart': '<path d="M4 24h21M7 20v-6m7 6V8m7 12V3"/>',
    'brand': '<path d="m14 2 12 12-12 12L2 14Z M14 8l6 6-6 6-6-6Z"/>',
    'core': '<path d="M14 2v6m0 12v6M2 14h6m12 0h6M5 5l4 4m10 10 4 4M5 23l4-4M19 9l4-4"/><circle cx="14" cy="14" r="6"/>',
}

def node(key, title, sub, icon, stage, pos, mobile=None, detail='', kind=''):
    return dict(key=key,title=title,sub=sub,icon=icon,stage=stage,pos=pos,mobile=mobile,detail=detail,kind=kind)

FLOWS = {
 'poczta': dict(label='Poczta', lead='Jedna wiadomość. Cały proces w ruchu.',
    summary='Zapytanie trafia do systemu. Agent zbiera kontekst i przygotowuje odpowiedź. O wysyłce decydujesz Ty.',
    phases=[('Wiadomość','Klient pisze. Proces rusza.','System sprawdza, czy wiadomość wymaga odpowiedzi.'),('Kontekst','Informacje znajdują swoje miejsce.','Temat, dane nadawcy i dostępna historia pomagają przygotować odpowiedź.'),('Przygotowanie','Nie zaczynasz od pustej kartki.','Agent tworzy szkic, a system sprawdza jego format przed przekazaniem do decyzji.'),('Twoja decyzja','Gotowy szkic. Ostatnie słowo należy do Ciebie.','Po zatwierdzeniu system wysyła odpowiedź. Odrzucenie zatrzymuje wysyłkę.')],
    nodes=[
      node('in','Nowe zapytanie','WIADOMOŚĆ E-MAIL','mail',0,(120,265),(210,45),'Wiadomość uruchamia recepcję poczty. Powiadomienia systemowe mogą zostać pominięte.','entry'),
      node('topic','Rozpoznanie tematu','CZEGO POTRZEBA?','search',1,(365,100),(95,145),'System analizuje treść i sprawdza, czy potrzebna jest odpowiedź.'),
      node('client','Kontekst klienta','KTO DO NAS PISZE?','person',1,(365,265),(325,145),'Dostępne dane nadawcy pomagają rozpoznać klienta i jego markę.'),
      node('history','Dane i historia','PORZĄDEK W DANYCH','folder',1,(365,430),None,'Proces zbiera informacje o firmie i może przygotować dossier klienta.'),
      node('core','Recepcja AI','KONTEKST → ODPOWIEDŹ','core',2,(690,265),(210,250),'Zebrany kontekst trafia do etapu tworzenia propozycji odpowiedzi.','hub'),
      node('draft','Szkic odpowiedzi','GOTOWY DO PRZECZYTANIA','write',2,(970,130),(95,360),'Agent przygotowuje propozycję odpowiedzi, którą można ocenić przed wysyłką.'),
      node('quality','Kontrola szkicu','CZY MOŻNA IŚĆ DALEJ?','check',2,(970,400),(325,360),'Sprawdzenie formatu zatrzymuje niepoprawny szkic. Nie zastępuje oceny jego treści.'),
      node('approval','Twoja decyzja','ZATWIERDŹ LUB ODRZUĆ','person',3,(1225,265),(210,480),'Odpowiedź wymaga zatwierdzenia. Brak zgody oznacza brak wysyłki.','result'),
      node('send','Odpowiedź wysłana','PO ZATWIERDZENIU','send',3,(1460,130),None,'Tą drogą proces idzie wyłącznie po uzyskaniu zgody.'),
      node('stop','Bez wysyłki','PO ODRZUCENIU','pause',3,(1460,400),None,'Odrzucenie propozycji zatrzymuje wysyłkę.')],
    edges=[('in','topic'),('in','client'),('in','history'),('topic','core'),('client','core'),('history','core'),('core','draft'),('draft','quality'),('quality','approval'),('approval','send'),('approval','stop')],
    mobile_edges=[('in','topic'),('in','client'),('topic','core'),('client','core'),('core','draft'),('draft','quality'),('quality','approval')]),
 'media': dict(label='Media',lead='Z materiału — więcej możliwości.',
    summary='Agent mediów ma pod ręką analizę nagrań, rozpoznawanie mówców, przygotowanie rolki i podglądu. Dobiera narzędzia do zadania.',
    phases=[('Materiał','Wszystko zaczyna się od materiału.','Nagranie, spotkanie lub wideo jest punktem wyjścia do zadania.'),('Rozpoznanie','Najpierw treść, potem format.','Agent może analizować materiał, wideo i występujących w nim mówców.'),('Narzędzia','Jedno centrum. Wiele specjalizacji.','Wybiera potrzebne narzędzia: rolkę, podgląd, protokół spotkania lub pracę z kanałem YouTube.'),('Rezultat','Efekt, który możesz obejrzeć.','Rezultat zależy od zleconego zadania. Schemat pokazuje dostępne ścieżki, a nie automatyczne wykonanie wszystkich naraz.')],
    nodes=[
      node('in','Twój materiał','WIDEO / NAGRANIE','play',0,(120,265),(210,45),'Materiał i polecenie trafiają do agenta mediów.','entry'),
      node('analysis','Analiza materiału','CO JEST W ŚRODKU?','search',1,(365,100),(95,145),'Narzędzie do opracowania zawartości dostarczonego materiału.'),
      node('video','Analiza wideo','OBRAZ I TREŚĆ','play',1,(365,265),(325,145),'Analiza wideo pomaga rozpoznać materiał przed dalszą pracą.'),
      node('speakers','Rozpoznanie mówców','KTO MÓWI?','sound',1,(365,430),None,'Agent może uruchomić narzędzie identyfikujące mówców w materiale.'),
      node('core','Agent mediów','DOBIERA NARZĘDZIA','core',0,(690,265),(210,250),'Centrum tej gałęzi wybiera narzędzia odpowiednie do polecenia. Nie musi używać wszystkich.','hub'),
      node('reel','Krótka rolka','NOWY FORMAT','cut',2,(1010,70),(95,360),'Ścieżka przygotowania rolki z materiału. Zakres i efekt zależą od wejścia oraz konfiguracji.'),
      node('preview','Podgląd wideo','ZOBACZ REZULTAT','play',3,(1320,155),(210,480),'Narzędzie renderowania podglądu pozwala zobaczyć przygotowany materiał.','result'),
      node('notes','Protokół spotkania','USTALENIA W JEDNYM MIEJSCU','write',2,(1010,265),(325,360),'Osobna ścieżka dla nagrań spotkań i ich ustaleń.'),
      node('youtube','Kanał YouTube','PRACA Z KANAŁEM','web',2,(1010,460),None,'Agent ma dostęp do odrębnego narzędzia obsługi zadań związanych z kanałem.'),
      node('library','Biblioteka materiałów','PRZYPISANIE DO KLIENTA','folder',3,(1320,380),None,'Dostępne narzędzia pomagają przypisać materiał do klienta i odszukać materiały.')],
    edges=[('in','core'),('core','analysis'),('core','video'),('core','speakers'),('core','reel'),('core','preview'),('core','notes'),('core','youtube'),('core','library')],
    mobile_edges=[('in','core'),('core','analysis'),('core','video'),('core','reel'),('core','notes'),('core','preview')]),
 'www': dict(label='WWW i kampanie',lead='Od pomysłu do spójnej obecności.',
    summary='Strona, materiały, branding, SEO i kampanie spotykają się w jednej gałęzi. Zobacz, jak można połączyć je wokół Twojego celu.',
    phases=[('Cel','Powiedz, co ma się zmienić.','Wywiad i materiały są punktem wyjścia do pracy nad stroną.'),('Kierunek','Marka ma własny charakter.','Agent ma dostęp do narzędzi pracy z brandingiem, materiałami i grafiką.'),('Realizacja','Z pomysłu powstaje coś konkretnego.','Dobiera narzędzia do przygotowania strony, kampanii i sprawdzenia wybranych elementów.'),('Rozwój','Strona i marketing zaczynają współpracować.','Dostępne ścieżki obejmują też analizę kampanii i SEO. Ich zakres ustalamy dla projektu.')],
    nodes=[
      node('in','Twój pomysł','CEL I MATERIAŁY','write',0,(120,265),(210,45),'Zadanie zaczyna się od celu, potrzeb firmy i dostępnych materiałów.','entry'),
      node('brief','Wywiad o stronie','POZNAJEMY POTRZEBY','person',1,(365,100),(95,145),'Narzędzie wywiadu pomaga zebrać informacje potrzebne do przygotowania strony.'),
      node('brand','Spójność marki','JEDEN KIERUNEK','brand',1,(365,265),(325,145),'Kontrola brandingu pomaga ocenić zgodność projektu z kierunkiem marki.'),
      node('image','Materiały wizualne','OBRAZ MA ZNACZENIE','play',1,(365,430),None,'Agent może zlecić generowanie obrazu do projektu.'),
      node('core','Agent WWW','ŁĄCZY KOMPETENCJE','core',0,(690,265),(210,250),'Gałąź WWW i kampanii dobiera narzędzia do zadania. To mapa możliwości, nie automatyczna obietnica gotowego projektu.','hub'),
      node('website','Projekt strony','OD TREŚCI DO WDROŻENIA','web',2,(1010,70),(95,360),'Dostępne są ścieżki tworzenia strony i pracy z dostarczonych materiałów.'),
      node('campaign','Kampania','DOTARCIE DO ODBIORCÓW','send',2,(1010,265),(325,360),'Narzędzie kampanii łączy działania marketingowe z zadaniem.'),
      node('seo','Widoczność w Google','SEO STRONY','search',2,(1010,460),None,'Osobny specjalista pomaga w zadaniach dotyczących SEO.'),
      node('results','Wyniki kampanii','DANE DO KOLEJNYCH DECYZJI','chart',3,(1320,155),(210,480),'Dostęp do wyników kampanii pomaga oceniać dalsze działania.','result'),
      node('checks','Sprawdzenie strony','KONTROLA WYBRANYCH ELEMENTÓW','check',3,(1320,380),None,'Gałąź ma narzędzia sprawdzania strony. Zakres kontroli i odpowiedzialność ustalamy w projekcie.')],
    edges=[('in','core'),('core','brief'),('core','brand'),('core','image'),('core','website'),('core','campaign'),('core','seo'),('core','results'),('core','checks')],
    mobile_edges=[('in','core'),('core','brief'),('core','brand'),('core','website'),('core','campaign'),('core','results')]),
}

def path_between(a,b,mobile=False):
    x,y=a; u,v=b
    if mobile:
        if abs(v-y)<25:
            return f'M{x},{y} C{x},{y+90} {u},{v+90} {u},{v}'
        mid=(y+v)/2
        return f'M{x},{y} C{x},{mid} {u},{mid} {u},{v}'
    if abs(x-u)<40:
        return f'M{x},{y} C{x+135},{y} {u+135},{v} {u},{v}'
    mid=(x+u)/2
    return f'M{x},{y} C{mid},{y} {mid},{v} {u},{v}'

def diagram(key, mobile=False):
    flow=FLOWS[key]; ns={n['key']:n for n in flow['nodes'] if not mobile or n['mobile']}
    pos={k:n['mobile' if mobile else 'pos'] for k,n in ns.items()}
    edges=flow['mobile_edges' if mobile else 'edges']
    parts=[]
    for i,(a,b) in enumerate(edges):
        stage=max(ns[a]['stage'],ns[b]['stage'])
        decision=b if key=='poczta' and b in ('send','stop') else ''
        d=path_between(pos[a],pos[b],mobile)
        # Agent tools branch from a central router; pulse order illustrates selection,
        # not the execution topology of every possible sub-workflow.
        parts.append(f'<g class="flow-edge" data-edge-stage="{stage}" data-decision="{decision}"><path class="flow-wire" d="{d}"/><path class="flow-trace" pathLength="100" d="{d}"/><circle class="flow-packet-halo" r="10"/><circle class="flow-packet" r="3.8"/></g>')
    for n in ns.values():
        x,y=pos[n['key']]; hub=n['kind']=='hub'; w=170 if hub else 180; h=122 if hub else 82
        if mobile:w=160 if hub else 166;h=104 if hub else 72
        content=(f'<g class="flow-hub-rings" aria-hidden="true"><circle r="90"/><circle r="119"/><circle r="150"/></g>' if hub else '')
        content+=f'<rect class="flow-node-shadow" x="{-w/2}" y="{-h/2+7}" width="{w}" height="{h}" rx="{22 if hub else 14}"/>'
        content+=f'<rect class="flow-node-surface" x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{22 if hub else 14}"/>'
        icon_y=-43 if hub else -31
        content+=f'<g class="flow-icon" transform="translate(-14,{icon_y})">{ICONS[n["icon"]]}</g>'
        content+=f'<text class="flow-node-title" text-anchor="middle" y="{16 if hub else 16}">{esc(n["title"])}</text><text class="flow-node-sub" text-anchor="middle" y="{37 if hub else 32}">{esc(n["sub"])}</text>'
        content+=f'<circle class="flow-port" cx="{-w/2}" r="3"/><circle class="flow-port" cx="{w/2}" r="3"/>'
        parts.append(f'<g class="flow-node {n["kind"]}" role="button" tabindex="0" aria-label="{esc(n["title"])} — pokaż opis" data-node="{n["key"]}" data-decision="{n["key"] if key=="poczta" and n["key"] in ("send","stop") else ""}" data-node-stage="{n["stage"]}" transform="translate({x},{y})">{content}</g>')
    vb='0 0 420 525' if mobile else '0 0 1600 530'
    return f'<svg class="flow-map flow-map-{"mobile" if mobile else "desktop"}" viewBox="{vb}" aria-label="{esc(flow["lead"])}" role="group"><g class="flow-camera">{"".join(parts)}</g></svg>'

def flow_scene(uid='opening',hero=False,initial='poczta'):
    flow=FLOWS[initial]
    if hero:
        heading='''<div class="flow-heading container"><div><p class="eyebrow">STRONY WWW / MARKETING / AGENCI AI</p><h1>Wpraw swoją<br><span>markę w ruch.</span></h1></div><div class="flow-intro"><p>Strona, która przyciąga.<br>Marketing, który prowadzi do rozmowy.<br>Technologia, która daje Ci więcej czasu.</p><a class="button primary" href="/kontakt.html">Zacznijmy nowy rozdział <span aria-hidden="true">↗</span></a><a class="text-link" href="/oferta.html">Poznaj ofertę <span aria-hidden="true">↗</span></a></div></div>'''
    else:
        heading='''<div class="flow-heading container"><div><p class="eyebrow">DONA / CYFROWY ZESPÓŁ W RUCHU</p><h2>Jedno zadanie.<br><span>Zobacz, co uruchamia.</span></h2></div><p class="flow-intro">Wybierz proces i dotknij dowolnego etapu. Zobaczysz, co robi system i gdzie potrzebna jest Twoja decyzja.</p></div>'''
    tabs=''.join(f'<button type="button" role="tab" id="{uid}-tab-{key}" aria-controls="{uid}-panel-{key}" aria-selected="{str(key==initial).lower()}" tabindex="{0 if key==initial else -1}" data-flow-tab="{key}"><span>0{i+1}</span> {f["label"]}</button>' for i,(key,f) in enumerate(FLOWS.items()))
    panels=''
    for key,f in FLOWS.items():
        panels+=f'<div class="flow-panel" role="tabpanel" id="{uid}-panel-{key}" aria-labelledby="{uid}-tab-{key}" data-flow-panel="{key}" {"hidden" if key!=initial else ""}>{diagram(key)}{diagram(key,True)}</div>'
    steps=''.join(f'<button type="button" data-flow-step="{i}" aria-pressed="false"><span>0{i+1}</span><span data-step-label>{p[0]}</span><i aria-hidden="true"></i></button>' for i,p in enumerate(flow['phases']))
    return f'''<section class="flow-scene {"flow-hero" if hero else "flow-explorer"}" data-flow-scene="{initial}" data-hero="{str(hero).lower()}" id="{uid}">
{heading}<div class="flow-toolbar container"><div class="flow-tabs" role="tablist" aria-label="Wybierz proces">{tabs}</div><p><span class="flow-dot" aria-hidden="true"></span> Zobacz, jak pracuje system</p></div>
<div class="flow-stage"><div class="flow-atmosphere" aria-hidden="true"></div>{panels}<div class="flow-scene-index" aria-hidden="true">PROBATUM / SYSTEM W RUCHU</div></div>
<div class="flow-caption container"><div class="flow-caption-copy"><span class="flow-phase-index" data-flow-index>01 / 04</span><div><h3 data-flow-title>{flow['phases'][0][1]}</h3><p data-flow-description>{flow['phases'][0][2]}</p><div class="flow-approval" data-flow-approval hidden><button type="button" data-flow-decision="send">Zatwierdź w przykładzie <span aria-hidden="true">✓</span></button><button type="button" data-flow-decision="stop">Odrzuć <span aria-hidden="true">×</span></button></div></div></div><div class="flow-controls"><button type="button" data-flow-pause aria-pressed="false">Wstrzymaj <span aria-hidden="true">Ⅱ</span></button><button type="button" data-flow-replay aria-label="Odtwórz od początku">Powtórz <span aria-hidden="true">↻</span></button></div></div>
<div class="flow-bottom container"><div class="flow-steps" aria-label="Etapy wizualizacji">{steps}</div><p>Skrócona wizualizacja naszych workflowów.<br>Przebieg poglądowy, bez danych klientów.</p></div><p class="sr-only" data-flow-live aria-live="polite"></p><noscript><p class="container flow-nojs">{flow['summary']} Animację i wybór procesów włącza JavaScript.</p></noscript></section>'''

def public_data():
    return {k:dict(phases=f['phases'],nodes={n['key']:dict(title=n['title'],detail=n['detail'],stage=n['stage']) for n in f['nodes']}) for k,f in FLOWS.items()}
