"""Mehr als zwei Fächer (0.26.0): Ein Probe-Fach „Probe“ wird nur in diesem Test angemeldet
(addSubject, addTest, AXES) – wie später „Basis“ oder Sachthemen. Geprüft wird, dass alle Oberflächen
es ohne weiteren Umbau aufnehmen: Fachwahl, Startseite, Üben, Test, Lernstand, Klassenübersicht,
Berichte, Tabelle; optional nur für eingeschaltete Kinder sichtbar."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

PROBE = r"""(()=>{
  const mk = (q, ok, alt) => () => ({type:'choice', prompt:q, label:q, options:[{a:ok}, {a:alt}], correct:0});
  AXES.Q = {place:'Probe', levels:['Q1', 'Q2'], mode:'probe',
    info:{Q1:{name:'Probe leicht', short:'leicht', kann:'kann die leichte Probe', ziel:'löst die leichte Probe', bp:'Probe 1', offer:{text:'Probe leicht üben', set:{mode:'read', lvl:'Q1'}}},
          Q2:{name:'Probe schwer', short:'schwer', kann:'kann die schwere Probe', ziel:'löst die schwere Probe', bp:'Probe 2', offer:{text:'Probe schwer üben', set:{mode:'read', lvl:'Q2'}}}},
    items:{Q1:[mk('Tippe auf A.', 'A', 'B'), mk('Tippe auf C.', 'C', 'D'), mk('Tippe auf E.', 'E', 'F')],
           Q2:[mk('Tippe auf G.', 'G', 'H'), mk('Tippe auf I.', 'I', 'J'), mk('Tippe auf K.', 'K', 'L')]}};
  addSubject('X', {name:'Probe', long:'Probefach', tests:[], guideAxes:['Q'], optional:true, ill: () => '<svg viewBox="0 0 120 70"><circle cx="60" cy="35" r="25" fill="#888"/></svg>',
    rail: (g, lvOk) => AXES.Q.levels.filter(lvOk).map(l => `<button data-mode="read" data-lvl="${l}" aria-pressed="${app.mode === 'read' && app.read.lvl === l}"><b aria-hidden="true">?</b>${AXES.Q.info[l].short}</button>`).join(''),
    areas: (g, lvOk) => [['', AXES.Q.levels.filter(lvOk).map(l => ({mode:'read', lvl:l, sym:'?', label:AXES.Q.info[l].short}))]],
    enter: () => { app.read.lvl = 'Q1'; app.read.item = null; app.mode = 'read'; }});
  addTest('X', {subj:'X', name:'Probe', long:'Probefach', axes:['Q'], cap:12, start:'beginnt mit der Probe',
    plan: function*(d){ const a = yield* tst(d, 'Q|Q1'); if(isOk(a)) yield* tst(d, 'Q|Q2'); }, rePlan: function*(d){ yield* tst(d, 'Q|Q1'); },
    title: () => 'Probe-Test', log: e => e.mode === 'probe', keys: () => ['Q|Q1', 'Q|Q2'],
    zoneCells: (m, first) => { const k = first(['Q|Q1', 'Q|Q2']); return k ? [k] : []; },
    kann: m => ['Q|Q2', 'Q|Q1'].filter(k => isOk(m[k]?.status)).slice(0, 1).map(k => cellInfo(k).kann),
    matrix: m => `<table class="mx-table probe-mx"><tr>${['Q|Q1', 'Q|Q2'].map(k => cellChip(m, k)).join('')}</tr></table>`,
    mxTable: (m, sym) => `<table class="mx probe-mx"><tr>${['Q|Q1', 'Q|Q2'].map(k => `<td>${sym(k)}</td>`).join('')}</tr></table>`});
  return [SUBJ_IDS.join(), TEST_IDS.join()];
})()"""

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        reg = await pg.evaluate(PROBE)
        if reg != ['B,M,D,X', 'M,L,W,X']: errs.append(f'Anmeldung: {reg}')
        # Gast: alle drei Fächer sichtbar
        await pg.evaluate("app.ctx='practice'; app.mode='number'; render()")
        subs = await pg.evaluate("[...document.querySelectorAll('.rail .subj button')].map(b=>b.textContent)")
        if subs != ['Basis', 'Mathe', 'Deutsch', 'Probe']: errs.append(f'Fachwahl: {subs}')
        await pg.click('.rail .subj button[data-subj="X"]'); await pg.wait_for_timeout(200)
        st = await pg.evaluate("[app.mode, app.read.lvl, settings.subject, !!document.querySelector('#stage [data-opt], #stage .opt, #stage button')]")
        if st[:3] != ['read', 'Q1', 'X'] or not st[3]: errs.append(f'Üben im Probe-Fach: {st}')
        # Startseite: Fach-Schritt und Bereichs-Schritt
        await pg.evaluate("app.mode='home'; app.wz={step:'subj'}; render()")
        hs = await pg.evaluate("[...document.querySelectorAll('[data-home-subj]')].map(b=>b.dataset.homeSubj).join()")
        if hs != 'B,M,D,X': errs.append(f'Startseite Fächer: {hs}')
        lbl = await pg.evaluate("document.querySelector('.wz-stair').innerText")
        if 'Fach?' not in lbl or 'oder' in lbl.split('Fach?')[0][-30:]: errs.append('Treppe: bei mehr als zwei Fächern kurz „Fach?“')
        await pg.click('[data-home-subj="X"]'); await pg.wait_for_timeout(150)
        if 'Probe: Was möchtest du üben?' not in await pg.inner_text('#stage'): errs.append('Bereichs-Schritt Probe fehlt')
        # Kind anlegen, Test machen
        await pg.evaluate("(()=>{const p={id:'kx',name:'Xaver',created:1};data.profiles.push(p);selectProfile(p.id);})()")
        await pg.evaluate("diagStart('X')"); await pg.wait_for_timeout(150); await pg.click('#d-start'); await pg.wait_for_timeout(100)
        title = await pg.inner_text('#equation')
        if 'Probe-Test' not in title: errs.append(f'Testtitel: {title}')
        for i in range(12):
            if await pg.evaluate("app.diag.done"): break
            ok = i < 3  # Q1 richtig, Q2 falsch
            await pg.evaluate(f"app.diag.resp={{choice:{0 if ok else 1}}}"); await pg.click('#d-next'); await pg.wait_for_timeout(60)
        if not await pg.evaluate("app.diag.done"): errs.append('Probe-Test endet nicht')
        await pg.click('#d-close'); await pg.wait_for_timeout(100)
        m = await pg.evaluate("Object.fromEntries(Object.entries(matrixOf('kx')).map(([k,v])=>[k,v.status]))")
        if m.get('Q|Q1') != 'erreicht' or m.get('Q|Q2') not in ('nicht', 'teilweise'): errs.append(f'Matrix: {m}')
        z = await pg.evaluate("zoneReport('kx','X').zones.map(z=>z.key).join()")
        if z != 'Q|Q2': errs.append(f'Förderzone: {z}')
        ileb = await pg.evaluate("zoneReport('kx','X').ileb.lernstand")
        if 'kann die leichte Probe' not in ileb: errs.append(f'ILEB: {ileb}')
        # Lernstand, Klasse, Berichte, Tabelle, Text
        sh = await pg.evaluate("teacherSectionHtml('kx').html")
        if 'Probefach' not in sh or 'probe-mx' not in sh or 'Probe-Test' not in sh: errs.append('Lernstand ohne Probefach')
        if 'Probe' not in await pg.evaluate("classHtml()"): errs.append('Klassenübersicht ohne Spalte Probe')
        rep = await pg.evaluate("buildReport('kx','teacher').html")
        if 'Probefach' not in rep or 'probe-mx' not in rep: errs.append('Lernstandsbericht ohne Probefach')
        for k in ['parents', 'week', 'map']:
            try: await pg.evaluate(f"buildReport('kx','{k}').html")
            except Exception as e: errs.append(f'Bericht {k}: {e}')
        if 'Förderzone Probe' not in await pg.evaluate("classCsv ? classCsv() : ''") if await pg.evaluate("typeof classCsv==='function'") else False: errs.append('Tabelle ohne Probe')
        if 'Kompetenzmatrix Probefach' not in await pg.evaluate("teacherText('kx')"): errs.append('Text ohne Probefach')
        # Für dich zeigt auf das Probefach
        await pg.evaluate("settings.subject='X'; render()")
        fy = await pg.evaluate("forYouOffer()?.key")
        if fy != 'Q|Q2': errs.append(f'Für dich: {fy}')
        # optional: Kind ohne Einschalten sieht Probe nicht; eingeschaltet schon
        await pg.evaluate("(()=>{const p={id:'ky',name:'Yara',created:1};data.profiles.push(p);selectProfile(p.id);app.ctx='practice';app.mode='number';settings.subject='M';render();})()")
        subs = await pg.evaluate("[...document.querySelectorAll('.rail .subj button')].map(b=>b.textContent).join()")
        if subs != 'Mathe,Deutsch': errs.append(f'optional ausgeblendet? {subs}')
        await pg.evaluate("curProfile().subjOn={X:true}; render()")
        subs = await pg.evaluate("[...document.querySelectorAll('.rail .subj button')].map(b=>b.textContent).join()")
        if subs != 'Mathe,Deutsch,Probe': errs.append(f'eingeschaltet sichtbar? {subs}')
        await pg.close()
        # Ohne Probe-Fach: (für Gäste) Basis, Mathe, Deutsch
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300); await pg.evaluate("app.ctx='practice'; app.mode='number'; render()")
        subs = await pg.evaluate("[...document.querySelectorAll('.rail .subj button')].map(b=>b.textContent).join()")
        if subs != 'Basis,Mathe,Deutsch': errs.append(f'Standard: {subs}')
        await pg.close()
        print('ERR', errs); await b.close()
asyncio.run(main())
