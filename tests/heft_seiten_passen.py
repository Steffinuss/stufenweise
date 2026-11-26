"""Arbeitsheft: jede Heftseite passt auf ein Blatt (Stefan, 26.11.2026: Testheft hatte als PDF 54 statt 48 Seiten,
weil die Einstiegsseite „Kalender und Termine“ mit großen Aufgaben überlief; in der Broschüre war sie abgeschnitten).
Für jede Stufe mit Arbeitsblatt werden Einstieg, Übungsseite (leicht und schwer), „Das kann ich schon“ und eine
Wiederholung gebaut; keine Seite darf überlaufen, gedruckt hat das Heft genau so viele Blätter wie Seiten."""
import asyncio, os, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

GROSS = os.environ.get('HEFT_GROSS') == '1'   # Backlog N: dasselbe mit „Große Aufgaben“ (tests/heft_seiten_gross.py)

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        res = await pg.evaluate("""async (GROSS) => {
            const id = newId('p-'); data.profiles.push({id, name:'Test', created:1, updated:1, world:'HS'}); saveData();
            const keys = TEST_IDS.flatMap(t => TESTS[t].axes || []).flatMap(ax => ax === 'M' ? ZR.flatMap(z => N_LEVELS.map(l => `M|${z}|${l}`)) : ax === 'V' || ax === 'O' ? B_ZONE_ORDER.filter(k => k.startsWith(ax)) : ({S:S_LEVELS, U:U_LEVELS, G:G_LEVELS, H:H_LEVELS, R:R_LEVELS, Z:Z_LEVELS, L:L_LEVELS, W:W_LEVELS, P:P_LEVELS}[ax] || []).map(l => `${ax}|${l}`));
            const seen = new Set(), ts = [];
            for(const k of keys){ const t = zoneToSheet(k); if(!sheetOk(t) || seen.has(sheetSig(t)) || sheetDef(t)?.mat) continue; seen.add(sheetSig(t)); ts.push({k, t}); }
            app.heft = {title:'Test', pid:id, items:[], toc:false, gross: GROSS}; saveHeft();   /* Inhalt mit 100+ Einträgen wäre hier unrealistisch lang */
            const specs = [];
            ts.forEach(({t}, i) => { specs.push({kind:'einstieg', t, ch:i}, {kind:'ueben', t, ch:i, o:heftStufe(t, 0)}, {kind:'ueben', t, ch:i, o:heftStufe(t, 1)}, {kind:'kann', t, ch:i}); if(i % 2) specs.push({kind:'wdh', parts:[{t: ts[i - 1].t, ch:i - 1}, {t, ch:i}]}); });
            const t0 = Date.now(), items = await heftPages(id, specs);
            app.heft.items = items; app.heft.chapters = ts.map(({k, t}) => ({key:k, label:k, zone:true, title:k})); app.heft.book = {N: items.length + 1, fach:'mix'}; saveHeft();
            return {n: ts.length, ms: Date.now() - t0, items: items.length, over: items.filter(i => i.over).map(i => i.title), low: items.filter(i => (i.cls || '').includes('fitlow')).map(i => i.title),
              gross: items.filter(i => i.kind === 'ueben' && i.html.includes('ab-grid gross')).length, ueben: items.filter(i => i.kind === 'ueben').length};
        }""", GROSS)
        if GROSS: print(f"große Aufgaben auf {res['gross']} von {res['ueben']} Übungsseiten"); check('große Aufgaben: die meisten Übungsseiten groß', res['gross'] >= .8*res['ueben'], f"{res['gross']}/{res['ueben']}")
        print(f"{res['n']} Stufen, {res['items']} Seiten in {res['ms']/1000:.0f} s; stark verkleinert: {res['low']}")
        check('keine Seite läuft über (auch nicht nach Verkleinern)', not res['over'], str(res['over']))
        lone = await pg.evaluate("""() => app.heft.items.filter(i => ['einstieg', 'kann', 'wdh'].includes(i.kind)).flatMap(i => { const d = new DOMParser().parseFromString(`<div>${i.html}</div>`, 'text/html');
            return [...d.querySelectorAll('.ab-grid')].map(g => { const c = +(g.style.gridTemplateColumns.match(/repeat\\((\\d+)/)?.[1] || 1), n = g.querySelectorAll(':scope > .ab-task').length; return n > 1 && n % c ? `${i.title} (${n} in ${c} Spalten)` : null; }).filter(Boolean); })""")
        check('Einstieg, „Das kann ich schon“, Wiederholung: nur ganze Reihen', not lone, str(lone[:5]))
        html = await pg.evaluate("buildHeft().html")
        doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(1500)
        info = await doc.evaluate("[document.querySelectorAll('.page').length, [...document.querySelectorAll('.page')].filter(p => p.dataset.over).map(p => p.querySelector('h1')?.textContent), [...document.querySelectorAll('.page.fitlow')].map(p => p.querySelector('h1')?.textContent + ' ' + p.dataset.fit)]")
        print('Verkleinerung der stark verkleinerten Seiten:', info[2])
        check('stark verkleinert höchstens auf 70 %', all(float(x.split()[-1] or 1) >= 0.7 for x in info[2]), str(info[2]))
        pdf = await doc.pdf(prefer_css_page_size=True, print_background=True); await doc.close()
        n = len(re.findall(rb'/Type\s*/Page[^s]', pdf))
        check('Druck: keine Seite mit Überlauf', not info[1], str(info[1]))
        check('Druck: so viele Blätter wie Seiten', n == info[0], f'{info[0]} Seiten, {n} gedruckt')
        # Broschüre A5: dieselben Seiten, nichts abgeschnitten (jede Seite passt in ihre Hälfte)
        await pg.evaluate("app.heft.druck = 'a5'; saveHeft()")
        html = await pg.evaluate("buildHeft().html")
        doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(1500)
        cut = await doc.evaluate("[...document.querySelectorAll('.bk-slot')].filter(s => s.scrollHeight > s.clientHeight + 2).length")
        await doc.close()
        check('A5-Broschüre: keine Seite abgeschnitten', cut == 0, str(cut))
        await pg.evaluate("app.heft = {title:'Mein Arbeitsheft', pid:'none', items:[], toc:true}; saveHeft()")
        print('Fehler:', ERR or 'keine')
        await br.close()
        if ERR: raise SystemExit(1)

asyncio.run(main())
