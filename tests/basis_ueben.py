"""Basis, Schritt 3 (0.28.0, überarbeitet 0.28.1): Üben in der App.
Alle Aufgabenarten (V1–V8, O2–O4, je mindestens 2, in den Schwierigkeiten st = 0, 1, 2) erzeugen gültige
Aufgaben ohne NaN/undefined; bei st = 0 höchstens 4 Dinge (basal);
die vorgemachte Lösung (bzSolve) wird als richtig gewertet, eine falsche Antwort als falsch.
Mit echten Klicks: Bild wählen, Sortieren (Ding, dann Kiste), Verbinden (oben, unten), Reihenfolge,
kurz zeigen (Bild verschwindet von selbst). Fach „Basis“ für Gast sichtbar, für ein Kind erst nach dem
Einschalten in den Einstellungen; die Statistik zählt die Basis-Übungen.
Ablauf (Stefan, 17.11.: nicht mischen): Das Kind bleibt bei einer Aufgabenart; jede neue Art wird zuerst
vorgemacht („Schau zu“, Klicks gesperrt, dann „Jetzt du“); nach 8 richtigen kommt „Nächste Aufgabe“;
nach drei Fehlern in Folge wird es wieder leichter."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

CHECK = r"""(()=>{ const bad = [], n = {};
  for(const ax of ['V', 'O']) for(const l of axLevels(ax)){
    const arts = AXES[ax].arts[l]; if(arts.length < 2) bad.push(l + ' hat nur ' + arts.length + ' Arten');
    if(!AXES[ax].items[l][0]().kern) bad.push(l + ': erste Art ohne kern');
    arts.forEach(([name, g], gi) => { for(let t = 0; t < 45; t++){
      const st = t % 3, it = g(st), id = l + '#' + gi + ' st' + st;
      const nn = (it.cells || it.things || it.up || []).length; if(st === 0 && it.type !== 'order' && !it.label.startsWith('Fehler im Muster') && nn > 4) bad.push(id + ' bei st 0 schon ' + nn + ' Dinge');
      if(!BZ_TYPES.includes(it.type)) { bad.push(id + ' Typ ' + it.type); break; }
      if(!it.prompt || !it.label || !it.tip) bad.push(id + ' ohne Text');
      const h = bzStage(it, {}, {}); if(/NaN|undefined|\[object/.test(h)) { bad.push(id + ' kaputt'); break; }
      const cells = it.cells || it.things || it.up;
      if(it.want && it.want.some(i => !(i >= 0 && i < cells.length))) { bad.push(id + ' want ' + it.want); break; }
      if(it.type === 'pick' && it.single && it.want.length !== 1) bad.push(id + ' single mit ' + it.want.length);
      const r = {}; bzSolve(it, r); const res = bzEval(it, r);
      if(!res || !res.ok) { bad.push(id + ' Lösung falsch: ' + it.label); break; }
      /* falsche Antwort */
      const w = {};
      if(it.type === 'pick'){ const o = cells.findIndex((_, i) => !it.want.includes(i)); if(o >= 0){ w.set = it.single ? [o] : [...it.want, o]; if(bzEval(it, w).ok) bad.push(id + ' falsch als richtig'); } }
      if(it.type === 'glance'){ w.hidden = true; w.set = [(it.want[0] + 1) % cells.length]; if(bzEval(it, w).ok) bad.push(id + ' falsch als richtig'); if(bzEval(it, {set:[it.want[0]]})) bad.push(id + ' wertet vor dem Abdecken'); }
      if(it.type === 'sort'){ w.place = it.things.map(t => 1 - t.box); if(bzEval(it, w).ok) bad.push(id + ' falsch als richtig'); }
      if(it.type === 'order'){ w.seq = [...it.want].reverse(); if(bzEval(it, w).ok) bad.push(id + ' falsch als richtig'); }
      if(it.type === 'match'){ if(it.ask){ w.yes = it.ask.ok ? 0 : 1; if(bzEval(it, w).ok) bad.push(id + ' ja/nein'); }
        else if(new Set(it.up.map(c => c.k)).size > 1){ w.links = it.sol.map(([i, j]) => [i, it.sol[(i + 1) % it.sol.length][1]]); if(bzEval(it, w).ok) bad.push(id + ' falsch verbunden als richtig'); } }
      n[l] = (n[l] || 0) + 1;
    } });
  }
  return {bad, n};
})()"""

async def solve_by_clicks(pg):
    """löst die aktuelle Aufgabe mit echten Klicks"""
    it = await pg.evaluate("(()=>{const it=app.read.item; return {type:it.type, want:it.want, single:it.single, ms:it.ms, things:(it.things||[]).map(t=>t.box), sol:it.sol, ask:it.ask}})()")
    t = it['type']
    if t == 'glance':
        await pg.wait_for_timeout(it['ms'] + 300)
    if t in ('pick', 'glance'):
        for i in it['want']: await pg.click(f'#stage [data-bz="{i}"]')
    if t == 'order':
        for i in it['want']: await pg.click(f'#stage [data-bzo="{i}"]')
    if t == 'sort':
        for i, bx in enumerate(it['things']):
            await pg.click(f'#stage .bz-pool [data-bzt="{i}"]'); await pg.click(f'#stage [data-bzb="{bx}"]')
    if t == 'match':
        for i, j in it['sol']:
            await pg.click(f'#stage [data-bzm="t,{i}"]'); await pg.click(f'#stage [data-bzm="b,{j}"]')
        if it['ask']: await pg.click(f'#stage [data-bzyn="{1 if it["ask"]["ok"] else 0}"]')
    if await pg.is_disabled('#r-check'):
        return [False, 'Prüfen gesperrt: ' + await pg.evaluate("JSON.stringify([app.read.item.label, app.read.r])")]
    await pg.click('#r-check'); await pg.wait_for_timeout(80)
    return await pg.evaluate("[app.read.fb?.ok, document.querySelector('#hint')?.textContent||'']")

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        r = await pg.evaluate(CHECK); errs += r['bad']
        print('Aufgaben geprüft je Stufe:', r['n'])
        # Gast: Fach Basis in der Fachwahl
        await pg.evaluate("settings.roundLen=0; app.ctx='practice'; app.mode='number'; settings.subject='M'; render()")
        subs = await pg.evaluate("[...document.querySelectorAll('.rail .subj button')].map(b=>b.textContent)")
        if subs != ['Mathe', 'Deutsch', 'Basis']: errs.append(f'Fachwahl Gast: {subs}')
        await pg.click('.rail .subj button[data-subj="B"]'); await pg.wait_for_timeout(150)
        st = await pg.evaluate("[app.mode, app.read.lvl, settings.subject, subjOfLvl('O3'), subjOfMode('read')]")
        if st != ['read', 'V1', 'B', 'B', 'B']: errs.append(f'Einstieg Basis: {st}')
        # Jede Stufe, jede Art einmal mit Klicks lösen
        done = 0
        for ax in ['V', 'O']:
            for l in await pg.evaluate(f"axLevels('{ax}')"):
                ng = await pg.evaluate(f"AXES['{ax}'].items['{l}'].length")
                for g in range(ng):
                    await pg.evaluate(f"(()=>{{clearTimeout(app.demoT); Object.assign(app.read,{{lvl:'{l}', item:AXES['{ax}'].items['{l}'][{g}](), r:{{}}, fb:null, tries:0, demo:false}}); render();}})()")
                    ok, hint = await solve_by_clicks(pg)
                    if not ok: errs.append(f'{l}#{g} mit Klicks nicht richtig: {hint}')
                    done += 1
        print('mit Klicks gelöst:', done)
        # Falsch → rot markiert, dann Lösung zeigen nach 2 Versuchen
        await pg.evaluate("(()=>{clearTimeout(app.demoT); Object.assign(app.read,{lvl:'V3', item:AXES.V.items.V3[0](), r:{}, fb:null, tries:0, demo:false}); render();})()")
        boxes = await pg.evaluate("app.read.item.things.map(t=>t.box)")
        for i, bx in enumerate(boxes): await pg.click(f'#stage .bz-pool [data-bzt="{i}"]'); await pg.click(f'#stage [data-bzb="{1 - bx}"]')
        await pg.click('#r-check'); await pg.wait_for_timeout(60)
        red = await pg.evaluate("document.querySelectorAll('#stage .bz-small.fb-no').length")
        if red != len(boxes): errs.append(f'Sortieren: {red} rot statt {len(boxes)}')
        await pg.click('#r-check'); await pg.wait_for_timeout(60)
        if not await pg.query_selector('#r-show'): errs.append('Lösung zeigen fehlt nach 2 Versuchen')
        else:
            await pg.click('#r-show'); await pg.wait_for_timeout(60)
            if await pg.evaluate("document.querySelectorAll('#stage .bz-pool .bz-c').length") != 0: errs.append('Lösung zeigen sortiert nicht ein')
        # Kurz zeigen: verschwindet, „Nochmal zeigen“ zeigt wieder
        await pg.evaluate("(()=>{clearTimeout(app.demoT); Object.assign(app.read,{lvl:'V8', item:AXES.V.items.V8[0](), r:{}, fb:null, tries:0, demo:false}); render();})()")
        if await pg.query_selector('#stage [data-bz]'): errs.append('Kurz zeigen: Auswahl schon sichtbar')
        await pg.wait_for_timeout(1800)
        if not await pg.query_selector('#stage [data-bz]'): errs.append('Kurz zeigen: Bild verschwindet nicht')
        await pg.click('#stage [data-bzagain]'); await pg.wait_for_timeout(100)
        if await pg.query_selector('#stage [data-bz]'): errs.append('Nochmal zeigen geht nicht')
        await pg.wait_for_timeout(1800)
        if not await pg.query_selector('#stage [data-bz]'): errs.append('nach Nochmal zeigen kein Abdecken')
        # Statistik
        await pg.evaluate("(()=>{const p={id:'kb',name:'Bea',created:1};data.profiles.push(p);selectProfile(p.id);})()")
        await pg.evaluate("(()=>{clearTimeout(app.demoT); Object.assign(app.read,{lvl:'V2', item:AXES.V.items.V2[0](), r:{}, fb:null, tries:0, demo:false}); app.mode='read'; settings.subject='B'; render();})()")
        await solve_by_clicks(pg)
        stats = await pg.evaluate("JSON.stringify(statsSections('kb'))")
        if 'Basis' not in stats or 'Was passt nicht?' not in stats: errs.append(f'Statistik ohne Basis: {stats[:200]}')
        # Kind: Basis erst nach Einschalten
        await pg.evaluate("app.mode='number'; settings.subject='M'; render()")
        subs = await pg.evaluate("visSubjects().join()")
        if subs != 'M,D': errs.append(f'Kind sieht ohne Einschalten: {subs}')
        await pg.evaluate("openSettings(); showSetTab('kids')")
        await pg.check('[data-subjon="B"][data-subjon-pid="kb"]'); await pg.wait_for_timeout(100)
        subs = await pg.evaluate("[visSubjects().join(), JSON.stringify(data.profiles.find(p=>p.id==='kb').subjOn)]")
        if subs != ['M,D,B', '{"B":true}']: errs.append(f'nach Einschalten: {subs}')
        await pg.uncheck('[data-subjon="B"][data-subjon-pid="kb"]'); await pg.wait_for_timeout(100)
        if await pg.evaluate("visSubjects().join()") != 'M,D': errs.append('Ausschalten geht nicht')
        # Ablauf: vormachen, bei einer Art bleiben, nächste Art, leichter nach Fehlern
        await pg.evaluate("(()=>{dlgSet.close(); selectProfile('kb'); curProfile().subjOn={B:true}; app.read.seen=new Set(); app.read.artMem={}; settings.subject='B'; app.mode='read'; app.read.lvl='V2'; app.read.item=null; render();})()")
        st = await pg.evaluate("[app.read.demo, !!document.querySelector('#r-try'), document.querySelector('#prompt').textContent.includes('Schau zu'), !!document.querySelector('#r-check')]")
        if st != [True, True, True, False]: errs.append(f'Vormachen am Anfang: {st}')
        await pg.click('#stage [data-bz="0"]', force=True); await pg.wait_for_timeout(50)
        if await pg.evaluate("(app.read.r.set||[]).length > 1"): errs.append('Klicks beim Vormachen nicht gesperrt')
        await pg.wait_for_timeout(2600)
        if not await pg.evaluate("app.read.r.set?.length === 1"): errs.append('Vormachen zeigt die Lösung nicht')
        await pg.click('#r-try'); await pg.wait_for_timeout(80)
        if await pg.evaluate("app.read.demo"): errs.append('Jetzt du beendet das Vormachen nicht')
        names = set()
        for i in range(9):
            names.add(await pg.evaluate("app.read.item.label.split(':')[0]"))
            ok, hint = await solve_by_clicks(pg)
            if not ok: errs.append(f'Ablauf {i}: {hint}')
            if i < 8: await pg.click('#r-next'); await pg.wait_for_timeout(40)
        if names != {'Passt nicht'}: errs.append(f'Aufgabenarten gemischt: {names}')
        if await pg.evaluate("app.read.item.cells.length") != 4: errs.append('nach 8 richtigen nicht schwerer (4 Bilder)')
        if not await pg.query_selector('#r-art-up'): errs.append('nach 8 richtigen keine „Nächste Aufgabe“')
        else:
            await pg.click('#r-art-up'); await pg.wait_for_timeout(80)
            st = await pg.evaluate("[bzMem().art, app.read.demo, app.read.item.label.split(':')[0]]")
            if st != [1, True, 'Passt nicht (Farbe)']: errs.append(f'nächste Aufgabenart: {st}')
            chips = await pg.evaluate("[...document.querySelectorAll('#ranges [data-rart]')].map(b=>b.textContent+':'+b.getAttribute('aria-pressed')).join()")
            if 'Andere Farbe:true' not in chips: errs.append(f'Kopfleiste Aufgabenarten: {chips}')
        await pg.click('#r-try'); await pg.wait_for_timeout(50)
        await pg.evaluate("bzMem().ok = 7; app.read.item = null; render()")
        if await pg.evaluate("app.read.item.cells.length") != 4: errs.append('st 2 erwartet')
        for i in range(3):
            w = await pg.evaluate("app.read.item.cells.findIndex((_, j) => !app.read.item.want.includes(j))")
            await pg.click(f'#stage [data-bz="{w}"]'); await pg.click('#r-check'); await pg.wait_for_timeout(40)
            await pg.evaluate("readNew()")
        if await pg.evaluate("bzMem().ok") > 4: errs.append(f'nach 3 Fehlern nicht leichter: {await pg.evaluate("bzMem().ok")}')
        # Andere Aufgabenart über die Kopfleiste
        await pg.click('#ranges [data-rart="2"]'); await pg.wait_for_timeout(80)
        if await pg.evaluate("[bzMem().art, app.read.demo].join()") != '2,true': errs.append('Kopfleiste wählt Aufgabenart nicht')
        print('ERR', errs[:10]); await b.close()
asyncio.run(main())
