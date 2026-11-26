"""Heft-Assistent (Backlog J, Schritt 1, Stefan 25.11.2026):
- Fach: Mathe, Deutsch oder gemischt (nur Fächer mit Förderzone; gemischt nur bei mehreren)
- Umfang 12/24/36/48 Seiten, 24 vorausgewählt; das gedruckte Heft hat genau so viele Seiten (Deckblatt und Inhalt mitgezählt)
- Vorgriff: nur Förderzone / je eine Stufe weiter / bis das Heft voll ist (Standard); vorweggenommen werden nur Stufen,
  die noch nicht erreicht sind, in Lernreihenfolge; die Förderzone bekommt die meisten Seiten
- Kapitel je Stufe: Inhalt nennt die Kapitel mit Seitenzahl, unten auf jeder Seite „Seite n · Kapitel k“
- Kapitel abwählen und „mehr“/„weniger“ Seiten verteilt die Seiten neu, gemerkt im Heft
Schritt 2: Kapitel = Einstieg mit Beispiel → Üben → „Das kann ich schon“ (drei Stufen zum Ankreuzen); Wiederholung nach je
zwei Kapiteln; Hilfen hinten (Hundertertafel, Anlauttabelle, Einmaleins-Tafel); Lösungsheft. Schritt 3: Mathe-Feinstufen.
Schritt 4: Fortsetzungsgeschichte, mittlere Texte, neue Papier-Formate. Schritt 5: Broschürendruck (A5 aus A4, A4 aus A3), Seiten in Falt-Reihenfolge."""
import asyncio, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

KID = """(z) => { const id = newId('p-'); data.profiles.push({id, name:z.name, created:1, updated:1, world:'HS'}); data.current = id;
  for(const k of z.ok) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of z.part) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  saveData(); return id; }"""
MIA = {'name': 'Mia', 'ok': ['M|10|I', 'M|10|II', 'M|20|I', 'R|R1', 'R|R2', 'L|L1', 'L|L2', 'W|W1', 'R|R5'],
       'part': ['M|20|II', 'R|R3', 'L|L3', 'W|W2', 'U|U1', 'H|H3']}

BEN = {'name': 'Ben', 'ok': ['L|L1', 'L|L2', 'L|L3', 'L|L4', 'L|L5', 'W|W1', 'W|W2', 'W|W3', 'W|W4'], 'part': ['L|L6', 'W|W5']}

async def printed(br, html):
    doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(700)
    n = await doc.evaluate("document.querySelectorAll('.page').length")
    pdf = await doc.pdf(prefer_css_page_size=True, print_background=True)
    await doc.close()
    return n, len(re.findall(rb'/Type\s*/Page[^s]', pdf))

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        mia = await pg.evaluate(KID, MIA)
        await pg.evaluate("app.heft = {title:'Mein Arbeitsheft', pid:'none', items:[], toc:true}; saveHeft()")

        # 1. Planung: Seitenzahlen gehen immer genau auf, Förderzone zuerst und mit den meisten Seiten
        res = await pg.evaluate("""pid => { const out = []; for(const fach of ['mix', 'M', 'D']) for(const pages of [12, 24, 36, 48]) for(const vor of ['zone', 'next', 'voll']) for(const taf of [false, true]){
            const P = heftPlan(pid, {...app.heft, fach, pages, vor, taf}), used = P.chapters.filter(c => c.pages);
            out.push({id:`${fach} ${pages} ${vor} ${taf}`, fach:P.fach, total: 1 + (P.tocOwn ? 1 : 0) + P.wdh + P.helps.length + 2*P.story + used.reduce((s, c) => s + c.pages, 0), N:P.N, wdh:P.wdh, nUsed: used.length,
              zoneFirst: P.chapters.findIndex(c => !c.zone) < 0 || P.chapters.slice(P.chapters.findIndex(c => !c.zone)).every(c => !c.zone),
              zoneMore: Math.min(...used.filter(c => c.zone).map(c => c.pages)) >= Math.max(0, ...used.filter(c => !c.zone).map(c => c.pages)),
              nPrev: P.chapters.filter(c => !c.zone).length, keys: P.chapters.map(c => c.key), subj: [...new Set(P.chapters.map(c => keySubj(c.key)))]}); }
          return out; }""", mia)
        bad = [r['id'] + f" ({r['total']})" for r in res if r['total'] != r['N']]
        check('Seitenzahl geht immer auf', not bad, ', '.join(bad))
        check('Förderzone vor den nächsten Stufen', all(r['zoneFirst'] for r in res))
        bad = [r['id'] for r in res if not r['id'].split()[2] == 'next' and not r['zoneMore']]
        check('Förderzone hat die meisten Seiten (ohne „je eine Stufe weiter“)', not bad, ', '.join(bad))
        check('nur Förderzone: kein Vorgriff', all(r['nPrev'] == 0 for r in res if ' zone ' in r['id']))
        check('je eine Stufe weiter: Vorgriff', all(r['nPrev'] > 0 for r in res if ' next ' in r['id']))
        r48 = next(r for r in res if r['id'] == 'M 48 voll false')
        check('bis voll, 48 Seiten: mehrere Stufen weiter', r48['nPrev'] >= 2, str(r48['keys']))
        check('erreichte Stufen werden nicht vorweggenommen', all('R|R5' not in r['keys'] for r in res), '')
        check('Mathe-Heft nur Mathe', all(r['subj'] == ['M'] for r in res if r['id'].startswith('M ')))
        check('Deutsch-Heft nur Deutsch', all(r['subj'] == ['D'] for r in res if r['id'].startswith('D ')))
        m24 = next(r for r in res if r['id'] == 'M 24 next false')
        check('Wiederholung nach je zwei Kapiteln', all(r['wdh'] == r['nUsed'] // 2 for r in res))
        check('Lernreihenfolge: nach ZR 20 II kommt III, nach R3 kommt R4', 'M|20|III' in m24['keys'] and 'R|R4' in m24['keys'], str(m24['keys']))

        # 2. Oberfläche: Fach, Umfang, Vorgriff, Kapitel abwählen und verlängern
        await pg.evaluate("pid => { app.heft.items = []; openHeftZone(pid); }", mia); await pg.wait_for_timeout(400)
        fach = await pg.evaluate("[...document.querySelectorAll('[data-hffach]')].map(b => b.textContent + (b.getAttribute('aria-pressed') === 'true' ? '*' : ''))")
        check('Fachwahl', fach == ['Mathe', 'Deutsch', 'Gemischt*'], str(fach))
        sel = await pg.evaluate("[document.querySelector('[data-hfpages][aria-pressed=true]').textContent, document.querySelector('#hf-vor').value]")
        check('24 Seiten und „bis voll“ vorausgewählt', sel == ['24', 'voll'], str(sel))
        await pg.click('[data-hffach="D"]'); await pg.click('[data-hfpages="36"]'); await pg.wait_for_timeout(200)
        await pg.select_option('#hf-vor', 'next'); await pg.wait_for_timeout(300)
        rows = await pg.evaluate("[...document.querySelectorAll('.hf-plan li')].map(li => li.textContent.replace(/\\s+/g, ' ').trim())")
        print(rows)
        check('Plan zeigt Kapitel mit Seiten', len(rows) == 4 and all('Seiten' in r for r in rows), str(rows))
        await pg.locator('[data-hfoff="W|W3"]').uncheck(); await pg.wait_for_timeout(300)
        await pg.click('[data-hfadj="L|L3"][data-d="1"]'); await pg.wait_for_timeout(300)
        plan = await pg.evaluate("pid => heftPlan(pid).chapters.map(c => c.key + ':' + c.pages)", mia)
        print(plan)
        pages = {k: int(v) for k, v in (x.split(':') for x in plan)}
        check('abgewählt: 0 Seiten', pages['W|W3'] == 0)
        check('mehr Seiten für L3', pages['L|L3'] > pages['W|W2'] > pages['L|L4'], str(pages))
        P = await pg.evaluate("pid => (P => [P.wdh, P.helps, P.tocOwn])(heftPlan(pid))", mia)
        check('Summe bleibt 36', sum(pages.values()) + 1 + P[0] + len(P[1]) + (1 if P[2] else 0) == 36, f'{sum(pages.values())} {P}')
        check('Anlauttabelle hinten (Deutsch, Anlaute)', P[1] == ['abc'], str(P[1]))
        saved = await pg.evaluate("(h => [h.fach, h.pages, h.vor, h.off, h.adj])(JSON.parse(localStorage.getItem(HEFT_KEY)))")
        check('Einstellungen gemerkt', saved == ['D', 36, 'next', {'W|W3': True}, {'L|L3': 1}], str(saved))

        # 3. Heft erstellen (Deutsch, 36 Seiten): Druck hat genau 36 Seiten, Kapitel im Inhalt, Seitenzahlen
        await pg.click('#hf-zone')
        await pg.wait_for_function("app.heft.book && document.querySelector('#hf-zone') && !document.querySelector('#hf-zone').disabled", timeout=120000)
        H = await pg.evaluate("({items: app.heft.items.filter(i => i.ch !== undefined).map(i => [i.ch, i.title]), kinds: app.heft.items.map(i => (i.ch ?? '-') + (i.kind || '')), chapters: app.heft.chapters, title: app.heft.title, dup: app.heft.items.length - new Set(app.heft.items.map(i => i.html)).size, sol: app.heft.items.filter(i => i.sol?.length).length})")
        print(H['kinds'])
        k = H['kinds']
        check('Kapitel: Einstieg zuerst, „Das kann ich schon“ zuletzt', all(k[[i for i, x in enumerate(k) if x.startswith(str(c))][0]] == f'{c}einstieg' and k[[i for i, x in enumerate(k) if x.startswith(str(c))][-1]] == f'{c}kann' for c in range(3)), str(k))
        check('Wiederholung nach Kapitel 2', '-wdh' in k and k.index('-wdh') == max(i for i, x in enumerate(k) if x.startswith('1')) + 1)
        check('Anlauttabelle ganz hinten', k[-1] == '-hilfe')
        check('Lösungen gesammelt', H['sol'] >= len(k) - 1, str(H['sol']))
        check('Titel Deutsch-Heft', H['title'] == 'Mein Deutsch-Heft', H['title'])
        check('3 Kapitel', len(H['chapters']) == 3, str([c['title'] for c in H['chapters']]))
        check('Kapitel nacheinander', [c for c, _ in H['items']] == sorted(c for c, _ in H['items']))
        check('jede Seite neue Aufgaben', H['dup'] == 0, str(H['dup']))
        html = await pg.evaluate("buildHeft().html")
        n, pr = await printed(br, html)
        check('gedruckt genau 36 Seiten', n == pr == 36, f'{n} Seiten, {pr} gedruckt')
        toc = re.sub(r'<[^>]+>', ' ', re.search(r'<div class="cv-toc">.*?</ol>', html).group(0))
        toc = re.sub(r'\s+', ' ', toc)
        print(toc)
        check('Inhalt mit Kapiteln ab Seite 2', 'Kapitel 1:' in toc and re.search(r'Kapitel 1: [^0-9]+ 2 ', toc) is not None, toc)
        check('Seitenzahlen 2 bis 36, Kapitel in der Fußzeile', '<div class="hf-pn">2</div>' in html and '<div class="hf-pn">36</div>' in html and '<div class="hf-pn">37</div>' not in html and 'Kapitel 1 · Stufenweise' in html)
        doc = await br.new_page(); await doc.emulate_media(media='print'); await doc.set_content(html); await doc.wait_for_timeout(700)
        gaps = await doc.evaluate("[...document.querySelectorAll('.page.hf-p')].map(p => Math.round(p.getBoundingClientRect().bottom - p.querySelector('.hf-pn').getBoundingClientRect().bottom))")
        await doc.close()
        check('Seitenzahl auf jeder Seite gleich hoch (Druck)', len(set(gaps)) == 1, str(sorted(set(gaps))))
        check('Einstieg mit Beispiel', html.count('class="ab-bsp-lab"') == 3 and html.count('class="hf-intro"') == 3)
        check('„Das kann ich schon“ mit drei Stufen zum Ankreuzen', html.count('class="hf-kis"') == 3 and all(t in html for t in ['Das kann ich.', 'Das kann ich fast.', 'Das übe ich noch.']))
        loes = await pg.evaluate("buildLoesung().html")
        check('Lösungsheft mit Seitenzahlen', 'Seite 2 · Einstieg' in loes and loes.count('<section class="ls">') >= 30, str(loes.count('<section class="ls">')))
        nm = await pg.evaluate("""() => { const keep = {...app.sheet}, out = []; for(const t of ['M:plus', 'H:H3', 'K:hundert', 'L:L7']){ Object.assign(app.sheet, {topic:t, n:6}); out.push(buildSheet().html.includes('Stefan Hackl')); } Object.assign(app.sheet, keep); return [out, tafHelp().includes('Stefan Hackl'), buildLoesung().html.includes('Stefan Hackl')]; }""")
        check('Backlog K: kein Name in Heft, Blättern, Hilfen, Lösungsheft', 'Stefan Hackl' not in html and not any(nm[0]) and not nm[1] and not nm[2] and 'stufenweise.app · CC BY-SA 4.0' in html, str(nm))
        check('Lösungsheft-Knöpfe', await pg.locator('#hf-sol-print').count() == 1 and await pg.locator('#hf-sol-save').count() == 1)
        lst = await pg.evaluate("[...document.querySelectorAll('.hf-list li.hf-ch')].map(l => l.textContent)")
        check('Seitenliste mit Kapitelüberschriften', len(lst) == 3, str(lst))

        # 4. Gemischt, 48 Seiten, bis voll, mit Hundertertafel hinten: eigene Inhaltsseite, wieder genau 48 Seiten
        await pg.evaluate("app.heft.fach = 'mix'; app.heft.pages = 48; app.heft.vor = 'voll'; app.heft.off = {}; app.heft.adj = {}; app.heft.taf = true; saveHeft(); renderHeft()")
        await pg.wait_for_timeout(300)
        check('Häkchen Hundertertafel sichtbar', await pg.locator('#hf-taf').count() == 1)
        await pg.evaluate("async pid => { await heftMake(pid); }", mia)
        html = await pg.evaluate("buildHeft().html")
        n, pr = await printed(br, html)
        own = 'class="page tocp"' in html
        print('Kapitel:', await pg.evaluate("app.heft.chapters.length"), 'eigene Inhaltsseite:', own)
        check('48 Seiten gedruckt', n == pr == 48, f'{n} Seiten, {pr} gedruckt')
        tail = await pg.evaluate("app.heft.items.slice(-2).map(i => i.kind + ' ' + i.title)")
        check('Hilfen hinten: Hundertertafel und Anlauttabelle', tail == ['hilfe Hundertertafel zum Nachschauen', 'hilfe Anlauttabelle'], str(tail))
        if own: check('mit Inhaltsseite beginnt Kapitel 1 auf Seite 3', '<div class="hf-pn">3</div>' in html and '<div class="hf-pn">2</div>' not in html)

        # 5. Mathe-Feinstufen: mit Bild → selbst zeichnen → im Kopf, Zahlen werden größer
        await pg.evaluate("app.heft.fach = 'M'; app.heft.pages = 24; app.heft.vor = 'zone'; app.heft.off = {}; app.heft.adj = {}; app.heft.taf = false; saveHeft()")
        await pg.evaluate("async pid => { await heftMake(pid); }", mia)
        st = await pg.evaluate("""() => { const c = app.heft.chapters.findIndex(c => c.key === 'R|R3'), it = app.heft.items.filter(i => i.ch === c && i.kind === 'ueben');
            const big = i => { const ns = i.sol.map(x => Math.max(...(x.match(/\\d+/g) || [0]).map(Number))); return ns.reduce((s, x) => s + x, 0)/ns.length; };
            return {labels: it.map(i => i.title.match(/\\(([^)]*)\\)$/)?.[1]), first: big(it[0]), last: big(it.at(-1))}; }""")
        print(st)
        check('Feinstufen: mit Bild zuerst, im Kopf zuletzt', st['labels'][0] == 'mit Bild' and st['labels'][-1] == 'im Kopf' and 'Bild selbst zeichnen' in st['labels'], str(st['labels']))
        dd = await pg.evaluate("""() => { const keep = {...app.sheet}, m = st => { let s = 0, n = 0; for(let i = 0; i < 12; i++){ Object.assign(app.sheet, {topic:'M:plus', zr:100, ue:'egal', n:6, stufe:st}); buildSheet(); const G = app.sheetGen; G.d.slice(0, 6).forEach(d => { s += d; n++; }); } return s/n; };
            const r = [m(0), m(1)]; Object.assign(app.sheet, keep); return r; }""")
        check('Feinstufen: Stufe 0 wählt kleinere Zahlen als Stufe 1', dd[0] < dd[1] * 0.8, f'{dd[0]:.1f} / {dd[1]:.1f}')

        # 6. Broschürendruck: A5-Heft aus A4-Bögen und A4-Heft aus A3-Bögen, Seiten in Falt-Reihenfolge
        for druck, w, sides in [('a5', 842, 12), ('a3', 1191, 12)]:
            await pg.evaluate("d => { app.heft.druck = d; saveHeft(); renderHeft(); }", druck); await pg.wait_for_timeout(300)
            doc = await pg.evaluate("(d => ({html: d.html, booklet: d.booklet, sheets: d.sheets}))(buildHeft())")
            first = re.search(r'<div class="bk-side"><div class="bk-slot">(.*?)</div><div class="bk-slot"><div class="page cover"', doc['html'], re.S)
            check(f'{druck}: Deckblatt rechts auf dem ersten Bogen, letzte Seite links', first is not None and '<div class="hf-pn">24</div>' in first.group(1))
            dp = await br.new_page(); await dp.set_content(doc['html']); await dp.wait_for_timeout(800)
            pdf = await dp.pdf(prefer_css_page_size=True, print_background=True); await dp.close()
            n = len(re.findall(rb'/Type\s*/Page[^s]', pdf)); box = re.search(rb'/MediaBox\s*\[\s*0 0 ([\d.]+) ([\d.]+)', pdf)
            check(f'{druck}: {sides} Seiten quer gedruckt', n == sides and box and abs(float(box.group(1)) - w) < 3 and float(box.group(1)) > float(box.group(2)), f'{n} Seiten, {box.group(1) if box else None}')
            check(f'{druck}: Hinweis zum Falten', await pg.locator('.hf-bk-note').count() == 1)
        await pg.evaluate("app.heft.druck = 'a4'; saveHeft()")

        # 7. Deutsch-Stoff (Schritt 4): Fortsetzungsgeschichte ab L6/W5, mittlere Texte auf schweren L7-Seiten, neue Papier-Formate
        ben = await pg.evaluate(KID, BEN)
        await pg.evaluate("pid => { app.heft = {title:'Mein Arbeitsheft', pid, items:[], toc:true, fach:'D', pages:36}; saveHeft(); openHeftZone(pid); }", ben); await pg.wait_for_timeout(300)
        check('Auswahl Fortsetzungsgeschichte', await pg.locator('#hf-story option').count() == 4)
        await pg.evaluate("async pid => { await heftMake(pid); }", ben)
        G = await pg.evaluate("app.heft.items.map(i => (i.kind || '') + '|' + i.title)")
        st = [g for g in G if g.startswith('story|')]
        check('4 Teile Geschichte, je Text und Aufgaben', len(st) == 8 and all(st[2*k].startswith(f'story|Geschichte Teil {k + 1}') and st[2*k + 1] == f'story|Aufgaben zu Teil {k + 1}' for k in range(4)), str(st))
        html = await pg.evaluate("buildHeft().html")
        n, pr = await printed(br, html)
        check('mit Geschichte genau 36 Seiten', n == pr == 36, f'{n} {pr}')
        toc = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.search(r'<div class="cv-toc">.*?</ol>', html).group(0)))
        check('Inhalt nennt Geschichte, nicht die Aufgabenseiten', 'Geschichte Teil 1' in toc and 'Aufgaben zu Teil' not in toc, toc)
        check('Aufgabenseite: Fragen, richtig/falsch, Schreiben', 'class="hf-rf"' in html and 'Richtig oder falsch?' in html)
        await pg.evaluate("async pid => { app.heft.story = 'aus'; await heftMake(pid); }", ben)
        check('ohne Geschichte', not any(i.startswith('story') for i in await pg.evaluate("app.heft.items.map(i => i.kind || '')")))
        mid = await pg.evaluate("""() => { const keep = {...app.sheet}; Object.assign(app.sheet, {topic:'L:L7', n:3, stufe:1}); const h1 = buildSheet().html; Object.assign(app.sheet, {stufe:0}); const h0 = buildSheet().html; Object.assign(app.sheet, keep);
            return [TEXTS_MID.some(t => h1.includes(t.text)), TEXTS_MID.some(t => h0.includes(t.text)), TEXTS.length, TEXTS_MID.length, LONG.length]; }""")
        check('L7: mittlere Texte nur auf schweren Seiten', mid[0] and not mid[1], str(mid))
        check('Textmengen (rund 80/40/40)', mid[2] >= 78 and mid[3] >= 38 and mid[4] >= 40, str(mid[2:]))
        fm = await pg.evaluate("""() => { const keep = {...app.sheet}, out = {}; for(const [t, w] of [['L:L4', 'Male ein Bild'], ['L:L6', 'Male ein Bild'], ['L:L7', 'Unterstreiche'], ['L:L7', 'Schreibe 1, 2, 3'], ['W:W3', 'Setze den Buchstaben ein'], ['W:W4', 'Setze die Silben zusammen'], ['W:W6', 'Satz zum Bild'], ['P:P4', 'Kreuze an']]){ let ok = false; for(let i = 0; i < 6 && !ok; i++){ Object.assign(app.sheet, {topic:t, n:12, stufe:null}); ok = buildSheet().html.includes(w); } out[t + ' ' + w] = ok; } Object.assign(app.sheet, keep); return out; }""")
        check('neue Papier-Formate', all(fm.values()), str([k for k, v in fm.items() if not v]))

        # 8. Leeren setzt die Kapitel zurück; Seiten von Hand danach wieder ab 1 gezählt
        await pg.evaluate("renderHeft()"); await pg.click('#hf-clear'); await pg.click('#hf-clear'); await pg.wait_for_timeout(200)
        st = await pg.evaluate("[app.heft.items.length, app.heft.chapters, app.heft.book]")
        check('Leeren setzt Kapitel zurück', st == [0, None, None], str(st))

        await pg.screenshot(path='heft_assistent.png')
        await pg.evaluate("app.heft = {title:'Mein Arbeitsheft', pid:'none', items:[], toc:true}; saveHeft()")
        print('Fehler:', ERR or 'keine')
        await br.close()
        if ERR: raise SystemExit(1)

asyncio.run(main())
