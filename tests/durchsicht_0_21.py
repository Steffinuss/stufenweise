"""Randfälle aus der Durchsicht 0.19–0.21:
1. kaputte gemerkte Blatt-Einstellungen → Arbeitsblätter öffnen trotzdem
2. geführte Oberfläche mit Förderzone Zehnerpartner: Knopf da, oben nur erlaubte Stufen
3. Zehnerübergang später sicher → alte offene Zehnerpartner werden abgeleitet erreicht, keine Zone mehr
4. Klassenübersicht zeigt Förderzone auch bei nur Hundertertafel/Zehnerpartner
5. Wiederholungstest fragt Zehnerpartner nicht mehr, wenn R3 sicher ist"""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p); pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        # 1
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("localStorage.setItem('stufenweise.blatt', JSON.stringify({topic:'M:gibtsnicht', zr:'x', rows:['a',99], gross:'ja', n:null}))")
        await pg.reload(); await pg.wait_for_timeout(500)
        await pg.evaluate("openSheets()"); await pg.wait_for_timeout(600)
        st = await pg.evaluate("[app.sheet.topic, app.sheet.zr, app.sheet.gross, sheetRows(), app.sheet.n, !!app.sheetDoc]")
        print('1 kaputte Einstellungen →', st)
        if st[:5] != ['M:plus', 20, False, [2, 5, 10], 'fill'] or not st[5]: errs.append(f'1: {st}')
        await pg.evaluate("localStorage.removeItem('stufenweise.blatt'); document.querySelector('#dlg-sheet').close()")
        # 2
        await pg.evaluate("""(()=>{const p={id:'p_g',name:'Gabi',created:Date.now()};data.profiles.push(p);selectProfile(p.id);
            for(const [k,s] of [['M|10|III','erreicht'],['M|20|III','erreicht'],['R|R1','erreicht'],['R|R2','erreicht'],['R|R3','nicht'],['Z|Z1','erreicht'],['Z|Z2','nicht']]) setCell(p.id,k,{status:s,quelle:'test',sum:'x'});
            inferCells(p.id,'M'); settings.guide='zone'; p.guide='zone'; saveData(); saveSettings(); settings.subject='M'; app.mode='number'; render();})()""")
        await pg.wait_for_timeout(400)
        g = await pg.evaluate("(()=>{const g=guideOf('M'); return g ? {mode:g.mode, z:g.axVisible('Z'), ok:Z_LEVELS.filter(l=>g.lvlOk(l))} : null})()")
        btn = await pg.locator('#modes [data-tenpair]').count()
        print('2 geführt:', g, 'Knopf', btn)
        if g:
            if not btn: errs.append('2: Knopf Zehnerpartner fehlt bei Zone Z2')
            await pg.locator('#modes [data-tenpair]').click(); await pg.wait_for_timeout(300)
            lv = await pg.evaluate("[app.read.lvl, [...document.querySelectorAll('#ranges [data-rlvl]')].map(b=>b.dataset.rlvl)]")
            print('   Stufe', lv)
            if lv[0] != 'Z2' or 'Z3' in lv[1]: errs.append(f'2: Stufen {lv}')
        else:
            print('   (geführte Oberfläche nicht aktiv – Einstellung prüfen)')
        zones = await pg.evaluate("zoneReport('p_g','M').zones.map(z=>z.key)")
        print('   Zonen', zones)
        if 'Z|Z2' not in zones: errs.append(f'2: Zone Z2 fehlt {zones}')
        # 3
        await pg.evaluate("(()=>{ matrixOf('p_g')['Z|Z2'].date = Date.now() - 864e5; setCell('p_g','R|R3',{status:'erreicht',quelle:'test',sum:'x'}); inferCells('p_g','M'); })()")
        r = await pg.evaluate("[matrixOf('p_g')['Z|Z2'].status, matrixOf('p_g')['Z|Z2'].quelle, zoneReport('p_g','M').zones.map(z=>z.key)]")
        print('3 nach R3 erreicht:', r)
        if r[0] != 'erreicht' or any(k.startswith('Z|') for k in r[2]): errs.append(f'3: {r}')
        # 4
        await pg.evaluate("""(()=>{const p={id:'p_h',name:'Hanna',created:Date.now()};data.profiles.push(p); setCell(p.id,'H|H2',{status:'nicht',quelle:'test',sum:'x'}); saveData();})()""")
        h = await pg.evaluate("classHtml()")
        ok4 = 'Hanna' in h and 'Hundertertafel H2' in h
        print('4 Klassenübersicht mit nur Hundertertafel:', ok4)
        if not ok4: errs.append('4: Klassenübersicht ohne Hundertertafel-Zone')
        # 5
        await pg.evaluate("(()=>{ const m=matrixOf('p_g'); m['Z|Z2']={status:'nicht',quelle:'test',sum:'x',date:Date.now()+1000}; })()")
        keys = await pg.evaluate("""(()=>{const d={pid:'p_g',res:{}}; const out=[]; const it=mathRePlan(d); let n=it.next(); while(!n.done && out.length<60){ out.push(n.value); d.res[n.value]='erreicht'; n=it.next(); } return out;})()""")
        print('5 Wiederholungstest fragt:', keys)
        if any(k.startswith('Z|') for k in keys): errs.append('5: Zehnerpartner trotz R3 im Wiederholungstest')
        offers = await pg.evaluate("Z_LEVELS.map(l=>Z_INFO[l].offer.text)")
        print('Angebote:', offers)
        print('ERR', errs); await b.close()
asyncio.run(main())
