"""Heft-Assistent (Backlog J, Schritt 1, Stefan 25.11.2026):
- Fach: Mathe, Deutsch oder gemischt (nur Fächer mit Förderzone; gemischt nur bei mehreren)
- Umfang 12/24/36/48 Seiten, 24 vorausgewählt; das gedruckte Heft hat genau so viele Seiten (Deckblatt und Inhalt mitgezählt)
- Vorgriff: nur Förderzone / je eine Stufe weiter / bis das Heft voll ist (Standard); vorweggenommen werden nur Stufen,
  die noch nicht erreicht sind, in Lernreihenfolge; die Förderzone bekommt die meisten Seiten
- Kapitel je Stufe: Inhalt nennt die Kapitel mit Seitenzahl, unten auf jeder Seite „Seite n · Kapitel k“
- Kapitel abwählen und „mehr“/„weniger“ Seiten verteilt die Seiten neu, gemerkt im Heft"""
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
            out.push({id:`${fach} ${pages} ${vor} ${taf}`, fach:P.fach, total: 1 + (P.tocOwn ? 1 : 0) + (P.taf ? 1 : 0) + used.reduce((s, c) => s + c.pages, 0), N:P.N,
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
        check('bis voll, 48 Seiten: mehrere Stufen weiter', r48['nPrev'] >= 3, str(r48['keys']))
        check('erreichte Stufen werden nicht vorweggenommen', all('R|R5' not in r['keys'] for r in res), '')
        check('Mathe-Heft nur Mathe', all(r['subj'] == ['M'] for r in res if r['id'].startswith('M ')))
        check('Deutsch-Heft nur Deutsch', all(r['subj'] == ['D'] for r in res if r['id'].startswith('D ')))
        m24 = next(r for r in res if r['id'] == 'M 24 next false')
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
        check('Summe bleibt 36', sum(pages.values()) + 1 == 36, str(sum(pages.values())))
        saved = await pg.evaluate("(h => [h.fach, h.pages, h.vor, h.off, h.adj])(JSON.parse(localStorage.getItem(HEFT_KEY)))")
        check('Einstellungen gemerkt', saved == ['D', 36, 'next', {'W|W3': True}, {'L|L3': 1}], str(saved))

        # 3. Heft erstellen (Deutsch, 36 Seiten): Druck hat genau 36 Seiten, Kapitel im Inhalt, Seitenzahlen
        await pg.click('#hf-zone')
        await pg.wait_for_function("app.heft.book && document.querySelector('#hf-zone') && !document.querySelector('#hf-zone').disabled", timeout=120000)
        H = await pg.evaluate("({items: app.heft.items.map(i => [i.ch, i.title]), chapters: app.heft.chapters, title: app.heft.title, dup: app.heft.items.length - new Set(app.heft.items.map(i => i.html)).size})")
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
        check('Fußzeile Seite und Kapitel', 'Seite 2 · Kapitel 1 · ' in html and 'Seite 36 · Kapitel 3 · ' in html)
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
        check('Hundertertafel ganz hinten', 'Hundertertafel zum Nachschauen' in await pg.evaluate("app.heft.items.at(-1).title"))
        if own: check('mit Inhaltsseite beginnt Kapitel 1 auf Seite 3', 'Seite 3 · Kapitel 1 · ' in html)

        # 5. Leeren setzt die Kapitel zurück; Seiten von Hand danach wieder ab 1 gezählt
        await pg.evaluate("renderHeft()"); await pg.click('#hf-clear'); await pg.click('#hf-clear'); await pg.wait_for_timeout(200)
        st = await pg.evaluate("[app.heft.items.length, app.heft.chapters, app.heft.book]")
        check('Leeren setzt Kapitel zurück', st == [0, None, None], str(st))

        await pg.screenshot(path='heft_assistent.png')
        await pg.evaluate("app.heft = {title:'Mein Arbeitsheft', pid:'none', items:[], toc:true}; saveHeft()")
        print('Fehler:', ERR or 'keine')
        await br.close()
        if ERR: raise SystemExit(1)

asyncio.run(main())
