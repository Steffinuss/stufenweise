"""Üben „Zehnerpartner“ (Z1–Z3): Knopf in der Leiste, alle Stufen mit richtigen Antworten lösbar,
falsche Antwort wird erkannt, Statistik zeigt den Bereich. Dazu: Blitzblick und „Zahl suchen“ – „Neue Aufgabe“ zählt als übersprungen."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p); pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("settings.subject='M'; app.mode='number'; render()"); await pg.wait_for_timeout(300)
        if not await pg.locator('[data-tenpair]').count(): errs.append('Knopf Zehnerpartner fehlt')
        await pg.locator('[data-tenpair]').first.click(); await pg.wait_for_timeout(400)
        n = 0
        for lvl in ['Z1', 'Z2', 'Z3']:
            await pg.click(f'[data-rlvl="{lvl}"]'); await pg.wait_for_timeout(300)
            for k in range(8):
                it = await pg.evaluate("({t:app.read.item.type,f:app.read.item.fields,c:app.read.item.correct,label:app.read.item.label})")
                if it['t'] == 'input':
                    ins = pg.locator('#stage .dg-in'); m = await ins.count()
                    if m != len(it['f']): errs.append(f'{lvl}: {m} Felder statt {len(it["f"])}')
                    for i in range(m): await ins.nth(i).fill(str(it['f'][i]))
                    await ins.nth(m - 1).press('Enter')
                else:
                    await pg.locator('#stage .dg-choice button').nth(it['c']).click(); await pg.click('#r-check')
                await pg.wait_for_timeout(150)
                if not await pg.evaluate("app.read.fb?.ok"): errs.append(f'{lvl} {it["label"]}: richtige Antwort nicht erkannt')
                n += 1
                await pg.click('#r-next'); await pg.wait_for_timeout(150)
        while await pg.evaluate("app.read.item.type") != 'input': await pg.click('#btn-random'); await pg.wait_for_timeout(100)
        ins = pg.locator('#stage .dg-in')
        for i in range(await ins.count()): await ins.nth(i).fill('99')
        await pg.click('#r-check'); await pg.wait_for_timeout(200)
        if await pg.evaluate("app.read.fb?.ok") is not False: errs.append('falsche Antwort nicht erkannt')
        titles = await pg.evaluate("statsSections(data.current||'guest').map(s=>s.title)")
        print(n, 'Zehnerpartner-Aufgaben gelöst; Statistik:', titles)
        if 'Zehnerpartner' not in titles: errs.append('Statistik ohne Zehnerpartner')
        # Blitzblick: Neue Aufgabe oben = übersprungen
        await pg.evaluate("app.mode='blitz'; app.blitz.range=10; app.blitz.phase='idle'; render()"); await pg.wait_for_timeout(300)
        await pg.click('#b-go'); await pg.wait_for_timeout(300)
        before = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).length")
        for i in range(2): await pg.click('#btn-random'); await pg.wait_for_timeout(250)
        after = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).length")
        print('Blitzblick übersprungen:', after - before)
        if after - before != 2: errs.append(f'Blitzblick: {after - before} statt 2 übersprungen')
        # Zahlen: „Zahl suchen“ am Zahlenstrahl überspringen
        await pg.evaluate("app.mode='number'; app.range=100; render()"); await pg.wait_for_timeout(300)
        await pg.click('#btn-random'); await pg.wait_for_timeout(300)
        await pg.evaluate("task().view='line'; render()"); await pg.wait_for_timeout(300)
        await pg.click('#c-find'); await pg.wait_for_timeout(300)
        n0 = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).length")
        await pg.click('#btn-random'); await pg.wait_for_timeout(300)
        last = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).slice(-1)[0]?.task")
        print('Zahl suchen übersprungen:', last)
        if not (last or '').startswith('Zahl '): errs.append('Zahl suchen: Überspringen nicht gezählt')
        # Test: Z3 wird nicht abgefragt, sondern aus R3 übernommen; Z3 beim Üben mit Zerlegungsast
        r = await pg.evaluate("""(()=>{const p={id:'p_t',name:'Tom',created:Date.now()};data.profiles.push(p);
            const d={pid:'p_t',res:{},subj:'M'}; const asked=[]; const it=mathPlan(d); let n=it.next(); let k=0;
            while(!n.done && k++<80){ const key=n.value; asked.push(key); d.res[key]= /R\|R[3-7]/.test(key) ? 'nicht' : 'erreicht'; n=it.next(); }
            for(const [k,v] of Object.entries(d.res)) setCell('p_t',k,{status:v,quelle:'test',sum:'x'}); inferCells('p_t','M');
            const m=matrixOf('p_t'); return {z3:asked.includes('Z|Z3'), zAsked:asked.filter(k=>k[0]==='Z'), z3cell:m['Z|Z3'] && [m['Z|Z3'].status, m['Z|Z3'].quelle]};})()""")
        print('Test-Ablauf Zehnerpartner:', r)
        if r['z3']: errs.append('Test fragt Z3 ab')
        if not r['zAsked']: errs.append('Test fragt keine Zehnerpartner ab')
        if r['z3cell'] != ['nicht', 'abgeleitet']: errs.append(f'Z3 nicht aus R3 übernommen: {r["z3cell"]}')
        ast = await pg.evaluate("(()=>{app.mode='read'; app.read.lvl='Z3'; app.read.item=null; render(); return [!!app.read.item.ast, document.querySelectorAll('#stage .it-ast .dg-in').length]})()")
        print('Z3 mit Zerlegungsast:', ast)
        if ast != [True, 3]: errs.append(f'Z3-Darstellung: {ast}')
        print('ERR', errs); await b.close()
asyncio.run(main())
