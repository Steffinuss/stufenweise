"""Arbeitshefte stringenter (Backlog U, Stefan 27.11.2026):
- U1 Hefte nur noch über den Heft-Assistenten, mit zwei Wegen: „Für ein Kind“ (Förderzone) und „Für einen Bereich“ ohne Kind und Test:
  Fach → Bereich → Stufen von … bis …, alle Kapitel gleich viele Seiten, Themenwelt wählbar, Namenszeile auf dem Deckblatt leer.
- U2 „Ins Arbeitsheft“ wird „Zur Blattsammlung“: lose Blätter wie in der Vorschau (mit Name), hinter jedem Blatt sein Lösungsblatt,
  ↑ ↓ ✕ zum Ordnen; kein Mischen mit Heften. Alte Hefte werden aufgeteilt (angehängte Blätter → Blattsammlung).
- U3 Übungsseite im Heft austauschen (neue Aufgaben oder anderes Blatt), die Seitenzahl bleibt; ↑ ↓ ✕ gibt es im Heft nicht mehr."""
import asyncio, json, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

async def pdf_pages(br, html):
    doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(700)
    pdf = await doc.pdf(prefer_css_page_size=True, print_background=True)
    await doc.close()
    return len(re.findall(rb'/Type\s*/Page[^s]', pdf))

OLD_BOOK = {'title': 'Mein Mathe-Heft', 'pid': 'none', 'toc': True, 'book': {'N': 12, 'fach': 'M'},
            'chapters': [{'key': 'M|20|I', 'label': 'ZR 20: Zählzahl', 'zone': True, 'title': 'Zählen bis 20'}],
            'items': [{'title': 'Einstieg: Zählen bis 20', 'kind': 'einstieg', 'ch': 0, 'html': '<p>E</p>'},
                      {'title': 'Plus bis 20', 'html': '<div class="ab-grid"><p>angehängt</p></div>', 'cls': ''},
                      {'title': 'Hundertertafel zum Nachschauen', 'kind': 'hilfe', 'cls': 'hilfe', 'html': '<p>T</p>'},
                      {'title': 'Blatt mit Lösung', 'html': '<p>B</p>', 'sol': ['3', '4']}]}
OLD_LOOSE = {'title': 'Mein Arbeitsheft', 'pid': 'none', 'toc': True,
             'items': [{'title': 'A', 'html': '<p>A</p>'}, {'title': 'B', 'html': '<p>B</p>'}, {'title': 'C', 'html': '<p>C</p>', 'cls': 'hilfe'}]}

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        toasts = []
        await pg.goto(URL); await pg.wait_for_timeout(400)

        # ---- U2: Umstellung alter Hefte ----
        await pg.evaluate("([h]) => { localStorage.setItem('stufenweise.heft', h); localStorage.removeItem('stufenweise.sammlung'); }", [json.dumps(OLD_BOOK)])
        await pg.reload(); await pg.wait_for_timeout(500)
        r = await pg.evaluate("({h: app.heft.items.map(i => i.title), s: app.samml.items.map(i => [i.title, !!i.alt, i.sol.includes('page sol')])})")
        check('Altes Assistenten-Heft: Kapitelseiten und Hilfe bleiben im Heft', r['h'] == ['Einstieg: Zählen bis 20', 'Hundertertafel zum Nachschauen'], r['h'])
        check('Altes Assistenten-Heft: angehängte Blätter in der Blattsammlung', [x[0] for x in r['s']] == ['Plus bis 20', 'Blatt mit Lösung'] and all(x[1] for x in r['s']), r['s'])
        check('Altes Blatt mit Lösungen: Lösungsblatt dahinter', r['s'][1][2] and not r['s'][0][2])
        stored = await pg.evaluate("JSON.parse(localStorage.getItem('stufenweise.heft')).items.length")
        check('Umstellung gespeichert', stored == 2, stored)
        await pg.evaluate("([h]) => { localStorage.setItem('stufenweise.heft', h); localStorage.removeItem('stufenweise.sammlung'); }", [json.dumps(OLD_LOOSE)])
        await pg.reload(); await pg.wait_for_timeout(500)
        r = await pg.evaluate("({h: app.heft.items.length, s: app.samml.items.map(i => i.title)})")
        check('Altes Heft ohne Assistent: ganz zur Blattsammlung', r['h'] == 0 and r['s'] == ['A', 'B', 'C'], r)
        await pg.reload(); await pg.wait_for_timeout(500)
        r = await pg.evaluate("app.samml.items.length")
        check('Umstellung nur einmal', r == 3, r)

        # ---- U2: Blattsammlung ----
        await pg.evaluate("app.samml.items = []; saveSamml(); app.heft = {title:'Mein Arbeitsheft', pid:'none', items:[], toc:true}; saveHeft();"
                          "data.profiles.push({id:'k1', name:'Lea', created:1, updated:1, world:'HS'}); saveData();"
                          "app.sheet.topic = 'M:plus'; app.sheet.zr = 20; app.sheet.sol = true; app.sheetMode = 'single'; openSheets('k1')")
        await pg.wait_for_timeout(1200)
        check('Einzelblatt: Knopf „Zur Blattsammlung“, kein „Ins Arbeitsheft“', await pg.locator('#sh-samml').count() == 1 and await pg.locator('#sh-heft').count() == 0)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        await pg.evaluate("app.sheet.topic = 'L:L2'; app.sheet.sol = false; renderSheets()"); await pg.wait_for_timeout(1200)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        await pg.evaluate("app.sheet.topic = 'K:zehner'; app.sheet.sol = true; renderSheets()"); await pg.wait_for_timeout(1200)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        check('Heft bleibt unberührt', await pg.evaluate("app.heft.items.length") == 0)
        await pg.click('[data-shmode="samml"]'); await pg.wait_for_timeout(800)
        lab = await pg.evaluate("document.querySelector('[data-shmode=\"samml\"]').textContent")
        check('Moduswahl zeigt die Zahl der Blätter', '(3)' in lab, lab)
        lst = await pg.evaluate("[...document.querySelectorAll('.sm-list li span')].map(s => s.textContent)")
        check('Liste der Blattsammlung', len(lst) == 3 and 'ohne Lösung' in lst[1], lst)
        html = await pg.evaluate("buildSamml().html")
        order = re.findall(r'<div class="page( [^"]*)?"', html)
        cls = [o.strip() for o in order]
        print('Seiten:', cls)
        sol = ['sol' in c.split() for c in cls]
        check('Lösungsblatt direkt hinter seinem Blatt', sol == [False, True, False, False, True], cls)
        check('Blätter mit Name', html.count('Lea') >= 2, html.count('Lea'))
        n = await pdf_pages(br, html)
        check('Gedruckt: jede Seite ein Blatt', n == len(cls), f'{n} PDF-Seiten, {len(cls)} Seiten')
        await pg.click('[data-sm-down="0"]'); await pg.wait_for_timeout(300)
        t = await pg.evaluate("app.samml.items.map(i => i.title)")
        check('↓ verschiebt', t[1].startswith('Plus'), t)
        await pg.click('[data-sm-del="2"]'); await pg.wait_for_timeout(300)
        await pg.reload(); await pg.wait_for_timeout(500)
        check('Blattsammlung gemerkt', await pg.evaluate("app.samml.items.length") == 2)

        # ---- U1: Heft für einen Bereich ----
        await pg.evaluate("app.sheetMode = 'heft'; app.heft.weg = 'bereich'; app.heft.pages = 12; openSheets('none'); app.sheetMode = 'heft'; renderSheets()")
        await pg.wait_for_timeout(600)
        check('Wahl „Für ein Kind“ / „Für einen Bereich“', await pg.locator('[data-hfweg]').count() == 2)
        ber = await pg.evaluate("Object.fromEntries(heftFaecher().map(f => [f, heftBereiche(f).map(b => b.name + ' ' + b.keys.length)]))")
        print('Bereiche:', ber)
        check('Bereiche in Mathe, Deutsch und Basis', all(ber.get(f) for f in ['M', 'D', 'B']) and any(x.startswith('Zahlen bis 20') for x in ber['M']), ber)
        await pg.click('[data-hfbfach="M"]'); await pg.wait_for_timeout(300)
        await pg.select_option('#hf-ber', 'M|20'); await pg.wait_for_timeout(300)
        await pg.select_option('#hf-von', 'M|20|I'); await pg.wait_for_timeout(300)
        await pg.select_option('#hf-bis', 'M|20|III'); await pg.wait_for_timeout(300)
        P = await pg.evaluate("(() => { const P = heftPlan('none'); return {ch: P.chapters.map(c => [c.key, c.pages]), fach: P.fach, N: P.N}; })()")
        print('Plan:', P)
        pages = [x[1] for x in P['ch']]
        check('Drei Kapitel I bis III', [x[0] for x in P['ch']] == ['M|20|I', 'M|20|II', 'M|20|III'], P['ch'])
        check('Alle Kapitel gleich viele Seiten', max(pages) - min(pages) <= 1, pages)
        check('Kein „Förderzone“ und kein „Wie weit nach vorne“', await pg.locator('.hf-assist .hf-tag').count() == 0 and await pg.locator('#hf-vor').count() == 0)
        await pg.click('#hf-zone'); await pg.wait_for_function("app.heft.book && app.heft.items.length > 5", timeout=120000); await pg.wait_for_timeout(800)
        H = await pg.evaluate("({n: app.heft.items.length, ch: app.heft.chapters.length, book: app.heft.book, t: heftTotal(app.heft)})")
        check('Bereichs-Heft erstellt', H['ch'] == 3 and H['book']['fach'] == 'M' and H['t'] == 12, H)
        html = await pg.evaluate("buildHeft().html")
        name = re.search(r'<span class="v">([^<]*)</span>', html)
        check('Namenszeile auf dem Deckblatt leer', name and name.group(1) == '', name and name.group(1))
        n = await pdf_pages(br, html)
        check('Gedruckt genau 12 Seiten', n == 12, n)
        # Rückmeldung Stefan 27.11. 12:39: Broschüre lief auf Handy und altem iPad über (Safari vergrößert kleine Schrift selbst)
        bk = await pg.evaluate("(() => { const d = app.heft.druck; app.heft.druck = 'a5'; try { return buildHeft().html; } finally { app.heft.druck = d; } })()")
        check('Broschüre: keine automatische Schriftvergrößerung', 'text-size-adjust:100%' in bk and 'bk-side' in bk)
        check('Blattsammlung: keine automatische Schriftvergrößerung', 'text-size-adjust:100%' in await pg.evaluate("buildSamml().html"))
        check('Lösungsheft', 'ls' in await pg.evaluate("buildLoesung().html"))
        # Themenwelt wirkt (Lineatur „passend zur Stufe“: Grundstufe Haus, sonst eine Linie)
        for welt, lin in [('GS', 'lin-haus'), ('HS', 'lin-eins')]:
            await pg.evaluate(f"Object.assign(app.heft, {{bfach:'D', ber:'W', von:'W|W5', bis:'W|W6', welt:'{welt}', pages:12, lin:'auto', off:{{}}, adj:{{}}}}); renderHeft()")
            await pg.wait_for_timeout(300)
            await pg.click('#hf-zone'); await pg.wait_for_function(f"app.heft.book && app.heft.book.fach === 'D' && app.heft.chapters[0].key === 'W|W5' && !document.querySelector('#hf-zone')?.disabled", timeout=120000)
            await pg.wait_for_timeout(500)
            h = await pg.evaluate("app.heft.items.map(i => i.html).join('')")
            check(f'Themenwelt {welt}: Lineatur', lin in h and ('lin-eins' if welt == 'GS' else 'lin-haus') not in h)

        # ---- U3: Übungsseite austauschen ----
        await pg.evaluate("Object.assign(app.heft, {bfach:'M', ber:'M|20', von:'M|20|I', bis:'M|20|II', pages:12, off:{}, adj:{}}); renderHeft()"); await pg.wait_for_timeout(300)
        await pg.click('#hf-zone'); await pg.wait_for_function("app.heft.book && app.heft.book.fach === 'M' && !document.querySelector('#hf-zone')?.disabled", timeout=120000); await pg.wait_for_timeout(500)
        check('Heft: kein ↑ ↓ ✕ mehr', await pg.locator('[data-hf-up],[data-hf-down],[data-hf-del]').count() == 0)
        # Stefan 27.11. 17:54: Seitenliste ausblendbar, anfangs zu
        check('Seitenliste anfangs zu', await pg.evaluate("!document.querySelector('.hf-pages').open") and not await pg.locator('[data-hf-swap]').first.is_visible())
        await pg.click('.hf-pages > summary'); await pg.wait_for_timeout(300)
        check('Seitenliste aufklappbar', await pg.evaluate("document.querySelector('.hf-pages').open"))
        info = await pg.evaluate("({n: app.heft.items.length, u: app.heft.items.map((it, i) => it.kind === 'ueben' ? i : -1).filter(i => i >= 0), b: document.querySelectorAll('[data-hf-swap]').length})")
        check('Austauschen nur bei Übungsseiten', info['b'] == len(info['u']) and info['b'] > 0, info)
        i = info['u'][0]
        before = await pg.evaluate(f"app.heft.items[{i}]")
        await pg.click(f'[data-hf-swap="{i}"]'); await pg.wait_for_timeout(300)
        await pg.click(f'[data-hf-swapnew="{i}"]'); await pg.wait_for_function(f"app.heft.items[{i}].html !== {json.dumps(before['html'])}", timeout=60000); await pg.wait_for_timeout(300)
        after = await pg.evaluate(f"app.heft.items[{i}]")
        n2 = await pg.evaluate("app.heft.items.length")
        check('Neue Aufgaben: gleiche Stelle, gleiches Kapitel, gleiche Seitenzahl', after['ch'] == before['ch'] and after['kind'] == 'ueben' and n2 == info['n'] and after['base'] == before['base'], (after['title'], before['title']))
        await pg.click(f'[data-hf-swap="{i}"]'); await pg.wait_for_timeout(300)
        await pg.click(f'[data-hf-swapother="{i}"]'); await pg.wait_for_timeout(1200)
        check('Anderes Blatt: Einzelblatt mit Austausch-Leiste', await pg.evaluate("app.sheetMode") == 'single' and await pg.locator('#sh-swap').count() == 1)
        await pg.evaluate("app.sheet.topic = 'K:zehner'; renderSheets()"); await pg.wait_for_timeout(1000)
        await pg.click('#sh-swap'); await pg.wait_for_timeout(300)
        check('Legeblatt wird nicht eingesetzt', await pg.evaluate("app.sheetMode") == 'single' and await pg.evaluate(f"app.heft.items[{i}].title") == after['title'])
        await pg.evaluate("app.sheet.topic = 'M:minus'; app.sheet.zr = 20; app.sheet.n = 'fill'; renderSheets()"); await pg.wait_for_timeout(1500)
        nt = await pg.evaluate("(app.sheetDoc.html.match(/class=\"ab-task/g) || []).length")
        await pg.click('#sh-swap'); await pg.wait_for_timeout(600)
        it = await pg.evaluate(f"app.heft.items[{i}]")
        check('Anderes Blatt eingesetzt', await pg.evaluate("app.sheetMode") == 'heft' and it['title'].startswith('Minus') and it['ch'] == before['ch'] and it['kind'] == 'ueben' and it.get('eigen'), it['title'])
        nh = it['html'].count('class="ab-task')
        check('Dieselben Aufgaben wie in der Vorschau, mit Lösungen', nh == nt and len(it['sol']) == nt, f"{nh} / {nt} / {len(it['sol'])}")
        check('Seitenzahl bleibt', await pg.evaluate("app.heft.items.length") == info['n'])
        check('Seitenliste bleibt nach dem Austausch offen', await pg.evaluate("document.querySelector('.hf-pages')?.open === true"))
        await pg.evaluate("openSheets('none'); app.sheetMode = 'heft'; renderSheets()"); await pg.wait_for_timeout(400)
        check('Beim nächsten Öffnen wieder zu', await pg.evaluate("document.querySelector('.hf-pages')?.open === false"))
        html = await pg.evaluate("buildHeft().html")
        check('Ausgetauschte Seite mit Heft-Rahmen', html.count('class="hf-foot"') >= info['n'] - 2)
        check('Ausgetauschte Seite ohne Namenszeile', 'Name:' not in html)
        n = await pdf_pages(br, html)
        check('Heft gedruckt weiter 12 Seiten', n == 12, n)

        # ---- U1: Heft für ein Kind ----
        await pg.evaluate("""(() => { setCell('k1', 'M|20|I', {status:'erreicht', quelle:'test', sum:''}); setCell('k1', 'M|20|II', {status:'teilweise', quelle:'test', sum:''}); saveData(); })()""")
        await pg.click('[data-hfweg="kind"]'); await pg.wait_for_timeout(300)
        await pg.select_option('#hf-kid', 'k1'); await pg.wait_for_timeout(400)
        t = await pg.evaluate("document.querySelector('.hf-assist b')?.textContent")
        check('Für ein Kind: Assistent wie bisher', t == 'Heft-Assistent für Lea' and await pg.locator('#hf-vor').count() == 1, t)
        check('Für ein Kind: Name auf dem Deckblatt', 'Lea' in await pg.evaluate("buildHeft().html"))
        await pg.screenshot(path='heft_stringent.png')
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')
    if ERR: raise SystemExit(1)

asyncio.run(main())
