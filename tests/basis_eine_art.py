"""Backlog T (Stefan, 27.11.2026): Basis-Arbeitsblätter mit genau einer Aufgabenart je Blatt.
- Jedes Basis-Blatt hat die Auswahl „Aufgabe“ (Arten wie in der App, leichteste zuerst); je Blatt und Art steht auf dem
  ganzen Blatt nur ein Auftragssatz, nichts zum Lesen ankreuzen (kein „ja/nein“, kein „gleich viele“ zum Ankreuzen),
  die Art steht im Titel, die erste Aufgabe ist ganz vorgemacht (und nur sie).
- Alles passt auf die Seite, auch mit großen Aufgaben und in Schwarz-Weiß.
- V6 „Ordnen“: Bastelseite mit leerer Rückseite (Blatt, leer, Bastelseite, leer); Schneideteile so groß wie die Felder der Treppe.
- „Ähnlichkeit“ nur bei Arten, die sie nutzen; die gewählte Art wird je Blatt gemerkt.
- Heft-Assistent: eine Art je Seite (Einstieg leichteste, „Das kann ich schon“ schwerste geübte); Bastelseite in der Broschüre
  auf einer rechten Seite mit leerer Rückseite; A4 ohne Leerseiten; Austauschen nimmt die Bastelseite mit.
- Blattsammlung nimmt die Leerseiten und die Bastelseite mit."""
import asyncio, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

BUILD = """async ([k, ai, opt]) => {
  Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic:'B:' + k, n:'fill', sol:true, bart:{[k]: ai}, ...opt});
  app.sheetDoc = buildSheet();
  const fr = document.createElement('iframe'); fr.style.cssText = 'position:fixed;left:-10000px;top:0;width:820px;height:1200px'; document.body.append(fr);
  const load = html => new Promise(r => { fr.onload = () => setTimeout(r, 30); fr.srcdoc = html; });
  for(let i = 0; i < 25; i++){ await load(app.sheetDoc.html); const G = app.sheetGen; if(!G || !G.fill || G.fitted) break; sheetFit(fr, () => {}); if(G.fitted) break; }
  fr.remove(); return {html: app.sheetDoc.html, title: app.sheetDoc.title}; }"""

INFO = """() => { const ps = [...document.querySelectorAll('.page')], main = ps[0], tasks = [...main.querySelectorAll('.ab-task')];
  const texts = new Set(tasks.map(t => t.querySelector('.ab-ins > span:last-child')?.textContent.replace(/\\s+/g, ' ').trim()));
  const marked = tasks.map(t => /bb-it (ring|weg|grau)|stroke="#888"|bb-box ring/.test(t.innerHTML));
  const mm = (() => { const d = document.createElement('div'); d.style.cssText = 'position:absolute;width:100mm'; document.body.append(d); const w = d.getBoundingClientRect().width/100; d.remove(); return w; })();
  const sz = sel => { const e = document.querySelector(sel); return e ? Math.round(e.getBoundingClientRect().width/mm*10)/10 : null; };
  return {pages: ps.map(p => p.className.replace(/^page\\s*/, '') || 'page'), tasks: tasks.length, texts: [...texts], marked,
    yesno: /\\bja\\b|\\bnein\\b|bb-cb|☐/.test(main.innerHTML.replace(/<svg[^]*?<\\/svg>/g, '')),
    over: ps.filter(p => p.dataset.over).length, leerEmpty: ps.filter(p => p.classList.contains('leer')).every(p => !p.textContent.trim() && !p.querySelector('svg,img')),
    cutRows: document.querySelectorAll('.page.bastel .bb-cutrow').length, slot: sz('.bb-slot'), cut: sz('.bb-cut'), ziel: !!main.querySelector('.bb-ziel')}; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        arts = await pg.evaluate("Object.fromEntries(Object.entries(B_SHEETS).map(([k, d]) => [k, d.arts.map(a => [a[0], !!a[2]?.sim, !!a[2]?.bastel])]))")
        app_arts = await pg.evaluate("Object.fromEntries(Object.entries(B_SHEETS).map(([k]) => [k, (AXES[k[0]].arts[k] || []).map(a => a[0])]))")
        check('alle zehn Blätter haben Arten', len(arts) == 10 and all(len(a) >= 2 for a in arts.values()), {k: len(v) for k, v in arts.items()})
        check('V1 wie in der App: einkreisen vor verbinden', arts['V1'][0][0].endswith('einkreisen') and arts['V1'][1][0].endswith('verbinden'))
        check('V3 beginnt mit Farbe (gleiche Dinge)', arts['V3'][0][0] == 'Nach Farbe' and arts['V3'][-1][0].startswith('Farbe, verschiedene'))
        check('V5 drei Arten', [a[0] for a in arts['V5']] == ['Wo sind mehr?', 'Wo sind weniger?', 'Gleich viele'])
        check('V6 Ordnen mit Bastelseite', arts['V6'][2][0] == 'Ordnen' and arts['V6'][2][2])
        print('Arten der App:', app_arts)

        bad, badfit, n = [], [], 0
        for k, lst in arts.items():
            for ai, (an, sim, bastel) in enumerate(lst):
                for v, opt in enumerate([{}, {'bw': True}, {'gross': True}, {'gross': True, 'bw': True, 'bsim': 2}, {'n': 4}]):
                    r = await pg.evaluate(BUILD, [k, ai, opt]); n += 1
                    doc = await br.new_page(viewport={'width': 794, 'height': 1123}); await doc.set_content(r['html']); await doc.wait_for_timeout(200)
                    i = await doc.evaluate(INFO)
                    pdf = await doc.pdf(prefer_css_page_size=True, print_background=True); await doc.close()
                    pp = len(re.findall(rb'/Type\s*/Page[^s]', pdf))
                    tag = f'{k} {an} {opt}'
                    if an not in r['title']: bad.append(f'{tag}: Art fehlt im Titel ({r["title"]})')
                    if len(i['texts']) != 1: bad.append(f'{tag}: {len(i["texts"])} Aufträge {i["texts"][:3]}')
                    if i['yesno']: bad.append(f'{tag}: ja/nein oder Ankreuzfeld')
                    if not i['marked'] or not i['marked'][0] or any(i['marked'][1:]): bad.append(f'{tag}: Vorgemacht {i["marked"]}')
                    if i['tasks'] < 2: bad.append(f'{tag}: nur {i["tasks"]} Aufgaben')
                    want = ['hf-p'] + (['leer', 'hf-p bastel', 'leer'] if bastel else []) + ['hf-p sol']
                    if i['pages'] != want: bad.append(f'{tag}: Seiten {i["pages"]}')
                    if bastel and (i['cutRows'] != i['tasks'] - 1 or not i['leerEmpty'] or abs((i['slot'] or 0) - (i['cut'] or 0)) > .3):
                        bad.append(f'{tag}: Bastelseite {i["cutRows"]} Reihen bei {i["tasks"]} Aufgaben, leer {i["leerEmpty"]}, Feld {i["slot"]} mm, Teil {i["cut"]} mm')
                    if i['over'] or pp != len(i['pages']): badfit.append(f'{tag}: PDF {pp} Seiten, {len(i["pages"])} erwartet, über {i["over"]}')
        check(f'{n} Blätter: eine Art, ein Auftrag, Titel, ganz vorgemacht, kein ja/nein', not bad, '; '.join(bad[:6]))
        check('alles passt auf die Seite (auch groß und schwarz-weiß)', not badfit, '; '.join(badfit[:6]))
        for k, ai, z in [('O2', 0, True), ('O3', 0, True), ('V3', 2, True), ('V1', 0, False)]:
            r = await pg.evaluate(BUILD, [k, ai, {}])
            check(f'{k}: Ziel groß oben {z}', ('class="bb-ziel"' in r['html']) == z)
        h = [(await pg.evaluate(BUILD, ['O2', 0, {}]))['html'] for _ in range(6)]
        forms = [set(re.findall(r'Kreise alle (\w+) ein', x)) for x in h]
        check('O2: eine Form je Blatt, zufällig', all(len(f) == 1 for f in forms) and len(set.union(*forms)) >= 2, forms)

        # Dialog: Auswahl „Aufgabe“, Ähnlichkeit nur bei Arten mit Ähnlichkeit, je Blatt gemerkt
        await pg.evaluate("openSheets('none'); app.sheetMode = 'single'; app.sheet.topic = 'B:V2'; app.sheet.bart = {}; renderSheets()"); await pg.wait_for_timeout(600)
        opts = await pg.evaluate("[...document.querySelectorAll('#sh-bart option')].map(o => o.textContent)")
        check('Auswahl „Aufgabe“ mit den Arten', opts == ['1. Ganz anders', '2. Andere Farbe', '3. Andere Größe', '4. Gehört nicht dazu'], opts)
        check('Ähnlichkeit bei „Ganz anders“', await pg.locator('#sh-bsim').count() == 1)
        await pg.select_option('#sh-bart', '1'); await pg.wait_for_timeout(600)
        check('keine Ähnlichkeit bei „Andere Farbe“', await pg.locator('#sh-bsim').count() == 0)
        check('Titel mit Art', await pg.evaluate("app.sheetDoc.title") == 'Was passt nicht?: Andere Farbe', await pg.evaluate("app.sheetDoc.title"))
        await pg.evaluate("app.sheet.topic = 'B:V6'; renderSheets()"); await pg.wait_for_timeout(500)
        await pg.select_option('#sh-bart', '2'); await pg.wait_for_timeout(800)
        check('Hinweis auf die Bastelseite', 'Bastelseite' in await pg.inner_text('#sheet-body'))
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        sm = await pg.evaluate("app.samml.items.at(-1).html")
        check('Blattsammlung: Blatt, leer, Bastelseite, leer', re.findall(r'<div class="page ([^"]*)"', sm) == ['hf-p', 'leer', 'hf-p bastel', 'leer'], re.findall(r'<div class="page ([^"]*)"', sm))
        await pg.reload(); await pg.wait_for_timeout(600)
        check('Art je Blatt gemerkt', await pg.evaluate("app.sheet.bart") == {'V2': 1, 'V6': 2}, await pg.evaluate("app.sheet.bart"))

        # Heft-Assistent für einen Bereich: V5 und V6
        async def heft(druck):
            await pg.evaluate(f"app.sheetMode = 'heft'; openSheets('none'); app.sheetMode = 'heft'; Object.assign(app.heft, {{weg:'bereich', bfach:'B', ber:'V', von:'V|V5', bis:'V|V6', pages:24, druck:'{druck}', off:{{}}, adj:{{}}}}); renderSheets()")
            await pg.wait_for_timeout(500)
            await pg.evaluate("app.heft.items = []; app.heft.book = null")
            await pg.click('#hf-zone'); await pg.wait_for_function("app.heft.book && app.heft.items.length > 5 && !document.querySelector('#hf-zone')?.disabled", timeout=180000); await pg.wait_for_timeout(500)
            return await pg.evaluate("""() => { const H = app.heft, f = heftFirst(H); return {total: heftTotal(H), N: H.book.N, items: H.items.map((it, i) => {
              const d = new DOMParser().parseFromString(it.html, 'text/html'); return {p: i + f, kind: it.kind, title: it.title,
              texts: [...new Set([...d.querySelectorAll('.ab-ins > span:last-child')].map(x => x.textContent.replace(/\\s+/g, ' ').trim()))].length}; })}; }""")
        A4 = await heft('a4')
        multi = [x for x in A4['items'] if x['texts'] > 1]
        check('Heft: eine Art je Seite', not multi, [x['title'] for x in multi])
        ks = {x['kind'] for x in A4['items']}
        check('Heft A4: Bastelseite, keine Leerseiten, Umfang wie gewählt', 'bastel' in ks and 'leer' not in ks and A4['total'] == A4['N'], (A4['total'], A4['N'], sorted(ks - {None})))
        ein = [x['title'] for x in A4['items'] if x['kind'] == 'einstieg']; kann = [x['title'] for x in A4['items'] if x['kind'] == 'kann']
        check('Einstieg leichteste Art, „Das kann ich schon“ schwerste geübte', ein == ['Einstieg: Mehr, weniger, gleich viel: Wo sind mehr?', 'Einstieg: Der Größe nach ordnen: Das größte'] and kann == ['Das kann ich schon: Mehr, weniger, gleich viel: Gleich viele', 'Das kann ich schon: Der Größe nach ordnen: Ordnen'], (ein, kann))
        ue = [x['title'] for x in A4['items'] if x['kind'] == 'ueben']
        order = [t.split(': ')[-1] for t in ue]
        L = ['Wo sind mehr?', 'Wo sind weniger?', 'Gleich viele', 'Das größte', 'Das kleinste', 'Ordnen']
        check('Übungsseiten der Reihe nach, alle Arten', [L.index(a) for a in order] == sorted(L.index(a) for a in order) and set(order) == set(L), order)
        hh = await pg.evaluate("buildHeft().html")
        check('Heft A4 druckt nur Seiten mit Inhalt', 'class="page leer' not in hh)
        A5 = await heft('a5')
        badb = [x for i, x in enumerate(A5['items']) if x['kind'] == 'bastel' and (x['p'] % 2 == 0 or A5['items'][i + 1]['kind'] != 'leer' or A5['items'][i - 1]['kind'] not in ('leer',))]
        check('Broschüre: Bastelseite rechts, Rückseite leer, nicht hinter der Treppe', not badb and any(x['kind'] == 'bastel' for x in A5['items']), [(x['p'], x['kind']) for x in A5['items']][10:])
        bk = await pg.evaluate("buildHeft().html")
        check('Broschüre: Leerseiten ohne Kopf und Seitenzahl', bk.count('page leer bk-blank') == sum(1 for x in A5['items'] if x['kind'] == 'leer'))
        sol = await pg.evaluate("buildLoesung().html")
        check('Lösungsheft ohne Leer- und Bastelseiten', 'Leerseite' not in sol and 'Zum Ausschneiden' not in sol)
        # Austauschen der Ordnen-Seite nimmt die Bastelseite mit
        i = next(j for j, x in enumerate(A5['items']) if x['kind'] == 'ueben' and x['title'].endswith('Ordnen'))
        n0 = len(A5['items'])
        bi = next(j for j in range(i + 1, n0) if A5['items'][j]['kind'] == 'bastel')
        before = await pg.evaluate(f"app.heft.items[{bi}].html")
        if not await pg.evaluate("document.querySelector('.hf-pages')?.open"): await pg.click('.hf-pages > summary'); await pg.wait_for_timeout(300)   # Seitenliste anfangs zu
        await pg.click(f'[data-hf-swap="{i}"]'); await pg.wait_for_timeout(300)
        await pg.click(f'[data-hf-swapnew="{i}"]'); await pg.wait_for_timeout(500)
        await pg.wait_for_function(f"!app.heftSwapMenu && app.heft.items.length === {n0}", timeout=60000); await pg.wait_for_timeout(300)
        after = await pg.evaluate(f"[app.heft.items.length, app.heft.items.filter(x => x.kind === 'bastel').length, app.heft.items[{bi}].kind, app.heft.items[{bi}].html]")
        check('Austauschen: neue Bastelseite, keine doppelte', after[0] == n0 and after[1] == sum(1 for x in A5['items'] if x['kind'] == 'bastel') and after[2] == 'bastel' and after[3] != before, after[:3])
        await br.close()
    print('FEHLER' if ERR else 'alles ok', ERR)

asyncio.run(main())
