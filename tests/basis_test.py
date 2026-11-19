"""Basis-Test (Schritt 4): drei kurze Teile (V1–V4, V5–V8, O2–O4).
Je Stufe Block a (vormachen, 2–3 Aufgaben einer Art), nur wenn a klappt Block b (vormachen, wenn andere Art).
Geprüft: Ablauf und Einstufung (erreicht / teilweise / nicht), Vormachen nicht gewertet und nicht antippbar,
Förderzone in empfohlener Reihenfolge, ILEB-Sätze, Lernstand mit Matrix und Hinweis bei Mathe I / L1,
Elterninfo, Lernlandkarte, automatische Sichtbarkeit, „Heute für dich“ mit Basis zuerst, Kurztest, Abbrechen."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch, OUT  # noqa: E402

STATE = "(()=>{const d=app.diag; if(!d||d.done) return ['done']; const it=d.items[d.idx]; return [it.demo?'demo':'item', d.key, it.blk, it.type];})()"


async def run(pg, plan, demos, shots=None):
    """plan: {Schlüssel: [richtig?, …]} in der Reihenfolge der gewerteten Aufgaben; zählt Vorführungen je Schlüssel."""
    used = {}
    for _ in range(120):
        st = await pg.evaluate(STATE)
        if st[0] == 'done': return
        kind, key = st[0], st[1]
        if kind == 'demo':
            demos[key] = demos.get(key, 0) + 1
            dis = await pg.evaluate("[document.querySelector('#d-go')?.disabled, !!document.querySelector('#stage .bz-demo'), !!document.querySelector('#d-skip')]")
            if dis != [True, True, False]: raise Exception(f'Vormachen nicht gesperrt/markiert: {dis} bei {key}')
            if shots is not None and not shots.get('demo'):
                await pg.wait_for_timeout(1500); await pg.screenshot(path=str(OUT / 'basis_test_demo.png')); shots['demo'] = 1
                # während des Vormachens nichts antippbar
                before = await pg.evaluate("JSON.stringify(app.diag.resp)")
                el = await pg.query_selector('#stage .bz-c, #stage [data-bz]')
                if el: await el.click(force=True)
                if await pg.evaluate("app.diag.answers.length") != 0: raise Exception('Vormachen wurde gewertet')
                # bis zum Ende abwarten (echte Animation)
                for _ in range(40):
                    if await pg.evaluate("app.diag.dm?.end"): break
                    await pg.wait_for_timeout(250)
                if not await pg.evaluate("app.diag.dm?.end"): raise Exception('Vormachen endet nicht')
            await pg.evaluate("app.diag.dm.end = true; renderDiag()")
            await pg.click('#d-go', force=True); await pg.wait_for_timeout(30)
            continue
        i = used.get(key, 0); used[key] = i + 1
        ok = plan.get(key, [])[i] if i < len(plan.get(key, [])) else False
        if shots is not None and not shots.get('item') and st[3] in ('sort', 'match'):
            await pg.screenshot(path=str(OUT / 'basis_test_item.png')); shots['item'] = 1
        if ok:
            await pg.evaluate("(()=>{const d=app.diag; bzSolve(d.items[d.idx], d.resp ||= {});})()")
            await pg.click('#d-next', force=True)
        else:
            await pg.click('#d-skip', force=True)
        await pg.wait_for_timeout(30)
    raise Exception('Test endet nicht')


async def start(pg, part):
    await pg.evaluate(f"diagStart('{part}')"); await pg.wait_for_timeout(100)
    await pg.click('#d-start'); await pg.wait_for_timeout(60)


async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("(()=>{const p={id:'ka',name:'Ali',created:1};data.profiles.push(p);selectProfile(p.id);})()")
        if 'B' in await pg.evaluate("visSubjects()"): errs.append('Basis sichtbar ohne Einschalten und ohne Test')
        # Teil 1
        await start(pg, 'B1')
        title = await pg.inner_text('#equation')
        if 'Basis-Test Teil 1' not in title: errs.append(f'Titel: {title}')
        secs = await pg.evaluate("[...document.querySelectorAll('.dg-sec')].map(x=>x.textContent).join()")
        if secs != 'Gleiches,passt nicht,Sortieren,Zuordnen': errs.append(f'Abschnitte: {secs}')
        demos, shots = {}, {}
        try:
            await run(pg, {'V|V1': [True, True, True, True], 'V|V2': [True, True, False, False],
                           'V|V3': [False, False], 'V|V4': [True, False, True, True, True]}, demos, shots)
        except Exception as e: errs.append(str(e))
        done = await pg.inner_text('#stage')
        if 'Teil 2 machst du an einem anderen Tag' not in done: errs.append('Hinweis auf Teil 2 fehlt')
        await pg.click('#d-close', force=True); await pg.wait_for_timeout(100)
        m = await pg.evaluate("Object.fromEntries(Object.entries(matrixOf('ka')).map(([k,v])=>[k,[v.status,v.items.length,v.quelle]]))")
        want = {'V|V1': ['erreicht', 4], 'V|V2': ['teilweise', 4], 'V|V3': ['nicht', 2], 'V|V4': ['erreicht', 5]}
        for k, (s, n) in want.items():
            if m.get(k, [None, None])[:2] != [s, n]: errs.append(f'{k}: {m.get(k)} statt {s}, {n} Aufgaben')
        if any(v[2] == 'abgeleitet' for v in m.values()) or set(m) != set(want): errs.append(f'Ableitung oder fremde Zellen: {sorted(m)}')
        if demos != {'V|V1': 2, 'V|V2': 2, 'V|V3': 1, 'V|V4': 2}: errs.append(f'Vorführungen: {demos}')
        # Förderzone, ILEB
        z = await pg.evaluate("zoneReport('ka','B')")
        if [x['key'] for x in z['zones']] != ['V|V2', 'V|V3']: errs.append(f"Förderzone: {[x['key'] for x in z['zones']]}")
        il = z['ileb']
        if 'findet Gleiches, auch wenn nur die Farbe gleich ist' not in il['lernstand'] or 'erkennt, was nicht in eine Reihe passt' not in il['lernstand'] or 'ordnet eins zu eins zu und erkennt, ob es reicht' not in il['lernstand']: errs.append(f"ILEB Lernstand: {il['lernstand']}")
        if 'auch dann, wenn er nur in einem Merkmal liegt' not in il['ziel'] or 'sortiert gleiche Dinge nach der Farbe' not in il['ziel']: errs.append(f"ILEB Ziel: {il['ziel']}")
        if 'Am Material' not in il['massnahmen']: errs.append('ILEB Maßnahmen ohne Material')
        if 'Die leichte Form gelingt' not in z['zones'][0]['why'] or 'gelingt noch nicht' not in z['zones'][1]['why']: errs.append('Begründung ohne a/b')
        # automatisch sichtbar (Förderzone), Startseite: Basis zuerst
        if 'B' not in await pg.evaluate("visSubjects()"): errs.append('Basis nicht automatisch sichtbar')
        await pg.evaluate("curProfile().subjOn = null; app.ctx='practice'; app.mode='home'; app.wz={step:'subj'}; render()")
        cards = await pg.evaluate("[...document.querySelectorAll('.home-card .hc-subj')].map(x=>x.textContent)")
        if not cards or cards[0] != 'Basis': errs.append(f'Heute für dich: {cards}')
        # Lernstand
        sh = await pg.evaluate("teacherSectionHtml('ka').html")
        for t in ['b-mx', 'data-diag="new-B1"', 'data-diag="new-B3"', 'Förderzone und Lernangebote', 'Formulierungsvorschlag ILEB – Basis']:
            if t not in sh: errs.append(f'Lernstand ohne {t}')
        if 'Hinweis: Basis-Test' in sh: errs.append('Hinweis trotz Basis-Test')
        rep = await pg.evaluate("buildReport('ka','teacher').html")
        if 'Basis: Grundlagen' not in rep or 'Vergleichen und Ordnen' not in rep: errs.append('Bericht ohne Basis')
        par = await pg.evaluate("buildReport('ka','parents').html")
        if 'Socken sortieren' not in par or 'Ich finde das Gleiche.' not in par: errs.append('Elterninfo ohne Basis')
        mp = await pg.evaluate("buildReport('ka','map').html")
        if 'Vergleichen und Ordnen' not in mp: errs.append('Lernlandkarte ohne Basis')
        if 'Kompetenzmatrix Basis' not in await pg.evaluate("teacherText('ka')"): errs.append('Text ohne Basis')
        if 'Basis' not in await pg.evaluate("classHtml()"): errs.append('Klassenübersicht ohne Basis')
        # Arbeitsblatt zur Förderzone
        if await pg.evaluate("zoneToSheet('V|V2')?.topic") != 'B:V2': errs.append('Arbeitsblatt zur Förderzone')
        # Teil 2 alles richtig: V6 hat für a und b dieselbe Art → nur einmal vormachen
        demos = {}
        await start(pg, 'B2')
        try: await run(pg, {k: [True] * 6 for k in ['V|V5', 'V|V6', 'V|V7', 'V|V8']}, demos)
        except Exception as e: errs.append(str(e))
        await pg.click('#d-close', force=True); await pg.wait_for_timeout(80)
        if demos != {'V|V5': 2, 'V|V6': 1, 'V|V7': 2, 'V|V8': 2}: errs.append(f'Vorführungen Teil 2: {demos}')
        st2 = await pg.evaluate("['V5','V6','V7','V8'].map(l=>matrixOf('ka')['V|'+l]?.status).join()")
        if st2 != 'erreicht,erreicht,erreicht,erreicht': errs.append(f'Teil 2: {st2}')
        # Teil 3: alles „Weiß ich nicht“ → nach 2 Aufgaben je Stufe „nicht erreicht“
        demos = {}
        await start(pg, 'B3')
        try: await run(pg, {}, demos)
        except Exception as e: errs.append(str(e))
        if 'anderen Tag' in await pg.inner_text('#stage'): errs.append('Teil 3: Hinweis auf weiteren Teil')
        await pg.click('#d-close', force=True); await pg.wait_for_timeout(80)
        st3 = await pg.evaluate("['O2','O3','O4'].map(l=>{const c=matrixOf('ka')['O|'+l]; return c?.status+c?.items.length}).join()")
        if st3 != 'nicht2,nicht2,nicht2': errs.append(f'Teil 3: {st3}')
        z = await pg.evaluate("zoneReport('ka','B').zones.map(z=>z.key).join()")
        if z != 'V|V2,O|O2': errs.append(f'Förderzone nach allen Teilen: {z}')
        # Re-Diagnose: nur offene Stufen
        await pg.evaluate("diagStart('B', true)")
        keys = await pg.evaluate("(()=>{const d=app.diag, out=[d.key]; return out;})()")
        if keys != ['V|V2']: errs.append(f'Re-Diagnose beginnt bei {keys}')
        await pg.evaluate("app.diag=null; app.mode='home'; render()")
        # Kurztest V2
        await pg.evaluate("quickTest('V|V2')"); await pg.wait_for_timeout(80); await pg.click('#d-start')
        try: await run(pg, {'V|V2': [True] * 6}, {})
        except Exception as e: errs.append('Kurztest: ' + str(e))
        if await pg.evaluate("matrixOf('ka')['V|V2'].status") != 'erreicht': errs.append('Kurztest ändert die Stufe nicht')
        await pg.click('#d-close', force=True); await pg.wait_for_timeout(80)
        # Abbrechen: bis dahin Getestetes bleibt
        await pg.evaluate("(()=>{const p={id:'kb',name:'Bea',created:1};data.profiles.push(p);selectProfile(p.id);})()")
        await start(pg, 'B1')
        try:
            for _ in range(20):
                if await pg.evaluate("Object.keys(matrixOf('kb')).length") >= 1: break
                stt = await pg.evaluate(STATE)
                if stt[0] == 'demo': await pg.evaluate("app.diag.dm.end = true; renderDiag()"); await pg.click('#d-go', force=True)
                else: await pg.click('#d-skip', force=True)
                await pg.wait_for_timeout(30)
        except Exception as e: errs.append('Abbrechen: ' + str(e))
        await pg.click('#d-close', force=True); await pg.click('#d-close', force=True); await pg.wait_for_timeout(100)
        if await pg.evaluate("Object.keys(matrixOf('kb')).join()") != 'V|V1' or await pg.evaluate("app.mode") == 'diag': errs.append('Abbrechen: Ergebnis fehlt oder Test läuft weiter')
        if await pg.evaluate("settings.subject") != 'B' or await pg.evaluate("app.mode") != 'read': errs.append(f"nach Abbrechen: {await pg.evaluate('[settings.subject, app.mode, app.read.lvl]')}")
        # V4 „Jedem eins“: frei hinlegen, mehr im Vorrat – man kann sich vertun (Stefan, 19.11.)
        fr = await pg.evaluate("""(()=>{ const out=[]; for(let k=0;k<20;k++){ const it=AXES.V.arts.V4[0][1](k%3); const n=it.up.length;
          const two=evalItem(it,{links:[[0,0],[0,1]]},[]), ok=evalItem(it,{links:it.sol.map(l=>[...l])},[]), none=evalItem(it,{},[]);
          out.push(it.free && it.dn.length>n && two.ok===false && ok.ok===true && none===null); } return out.every(Boolean); })()""")
        if not fr: errs.append('V4 frei hinlegen: falsch gewertet')
        # Hinweis im Lernstand: Mathe „Zahlen bis 10, Stufe I“ nicht erreicht, noch kein Basis-Test
        await pg.evaluate("(()=>{const p={id:'kc',name:'Cem',created:1};data.profiles.push(p);setCell('kc','M|10|I',{status:'nicht',quelle:'test',sum:'0 von 2'});setCell('kc','L|L1',{status:'teilweise',quelle:'test'});})()")
        h = await pg.evaluate("teacherSectionHtml('kc').html")
        if 'Hinweis: Basis-Test' not in h or 'Zahlen bis 10, Stufe I' not in h or 'L1 Schilder und Bilder' not in h: errs.append('Hinweis bei Mathe I / L1 fehlt')
        await pg.evaluate("setCell('kc','M|10|I',{status:'erreicht',quelle:'test'}); setCell('kc','L|L1',{status:'erreicht',quelle:'test'})")
        if 'Hinweis: Basis-Test' in await pg.evaluate("teacherSectionHtml('kc').html"): errs.append('Hinweis trotz erreicht')
        # Lernstand sichtbar machen (Bildschirmfoto)
        await pg.evaluate("selectProfile('ka'); openStats(); statsId='ka'; renderStats()"); await pg.wait_for_timeout(200)
        await pg.evaluate("document.querySelector('.b-mx')?.scrollIntoView()"); await pg.wait_for_timeout(100)
        await pg.screenshot(path=str(OUT / 'basis_test_lernstand.png'))
        print('ERR', errs[:12]); await b.close()
asyncio.run(main())
