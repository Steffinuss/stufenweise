"""Materialkiste (Backlog D, Stefan 20.11.2026): eigener Eingang auf der Startseite, für alle Kinder,
Werkzeuge Rechenhilfe, Taschenrechner, Frei legen, Zwanzigerfeld, Hundertertafel, Zahlenstrahl, Uhr.
Kein Protokoll, keine Runden, keine Lenkung; gezählt wird nur, wie oft ein Werkzeug geöffnet wird (Gast: nichts).
Taschenrechner: + − · :, Zahlen bis 10 000, geteilt mit Rest, Ergebnis wahlweise als Material."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

ADD = """n => { const p = {id: newId('p-'), name: n, created: Date.now(), updated: Date.now(), world: 'HS'}; data.profiles.push(p); saveData(); return p.id; }"""
TOOLS = ['calc', 'tcalc', 'free', 'tfield', 'hboard', 'nline', 'tclock']

async def keys(pg, seq):
    for k in seq: await pg.click(f'[data-trk="{k}"]')
    await pg.wait_for_timeout(60)
    return await pg.evaluate("[document.querySelector('.trc-expr').textContent, document.querySelector('.trc-res').textContent, document.querySelector('.trc-note')?.textContent || '', !!document.querySelector('.trc-mat svg'), document.querySelector('.trc-mat svg')?.getAttribute('aria-label') || '']")

async def main():
    async with async_playwright() as p:
        br = await launch(p)
        pg = await br.new_page(viewport={'width': 1180, 'height': 820})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        ali = await pg.evaluate(ADD, 'Ali'); await pg.evaluate(ADD, 'Bea')
        await pg.reload(); await pg.wait_for_timeout(500)

        # Startseite und Ablauf
        check('vier Kacheln', await pg.locator('.ctx-tile').count() == 4)
        await pg.click('[data-ctx-kiste]'); await pg.wait_for_timeout(150)
        check('erst Wer?', await pg.locator('.home-names [data-home-pick]').count() == 3)
        await pg.click(f'[data-home-pick="{ali}"]'); await pg.wait_for_timeout(150)
        check('Werkzeugauswahl', await pg.locator('.ct-tile[data-kiste]').count() == 7)
        check('Kisten-Leiste auf der Auswahl', await pg.locator('.rail [data-kiste]').count() == 7)

        # jedes Werkzeug öffnet sich, Leiste zeigt es an, Zählen nur beim Öffnen
        for k in TOOLS:
            await pg.click(f'.rail [data-kiste="{k}"]' if k != 'calc' else '.ct-tile[data-kiste="calc"]' if await pg.locator('.ct-tile').count() else '.rail [data-kiste="calc"]'); await pg.wait_for_timeout(150)
            st = await pg.evaluate(f"[app.kiste, '{k}' === 'calc' ? (app.calc && ['add','sub'].includes(app.mode)) : app.mode === '{k}', document.querySelector('.rail [data-kiste=\"{k}\"]').getAttribute('aria-pressed'), document.querySelectorAll('.rail [data-mode]').length, !!document.querySelector('.round-bar')]")
            check(f'Werkzeug {k}', st == [True, True, 'true', 0, False], str(st))
        await pg.click('.rail [data-kiste="tclock"]'); await pg.wait_for_timeout(100)
        cnt = await pg.evaluate(f"JSON.stringify(data.kiste['{ali}'])")
        check('Zählen je Öffnen', cnt == '{' + ','.join(f'"{k}":1' for k in TOOLS) + '}', cnt)

        # Rechenhilfe: kein Protokoll, keine Fehlerzähler, Zahlenraum frei
        await pg.click('.rail [data-kiste="calc"]'); await pg.wait_for_timeout(100)
        await pg.evaluate("() => { logAttempt({mode:'add', task:'1+1', ok:false}); noteError('add', 'zehner'); logSkip(); }")
        check('kein Protokoll', await pg.evaluate(f"[(data.log['{ali}'] || []).length, !!data.errs?.['{ali}'], (data.skips?.['{ali}'] || []).length]") == [0, False, 0])
        check('kein Rundenzähler', await pg.evaluate("roundOn()") is False)

        # geführtes Kind: keine Umlenkung, alle Zahlenräume
        await pg.evaluate(f"() => {{ setCell('{ali}', 'M|10|I', {{status:'teilweise', quelle:'test', sum:''}}); saveData(); }}")
        await pg.click('.rail [data-kiste="free"]'); await pg.wait_for_timeout(100)
        await pg.click('.rail [data-kiste="calc"]'); await pg.wait_for_timeout(150)
        st = await pg.evaluate("[app.mode, !!app.calc, document.querySelectorAll('#ranges [data-range]').length]")
        check('geführt: frei und alle Zahlenräume', st == ['add', True, 5], str(st))

        # Taschenrechner
        await pg.click('.rail [data-kiste="tcalc"]'); await pg.wait_for_timeout(100)
        r = await keys(pg, ['1', '2', '+', '3', '0', '='])
        check('12 + 30', r[0] == '12 + 30' and r[1] == '= 42' and r[3] and '4 Zehner, 2 Einer' in r[4], str(r))
        r = await keys(pg, ['1', '7', ':', '5', '='])
        check('17 : 5 mit Rest', r[1] == '= 3 Rest 2' and not r[3] and 'ohne Rest' in r[2], str(r))
        r = await keys(pg, ['5', '-', '8', '='])
        check('5 − 8', r[1] == '= −3' and 'kleiner als 0' in r[2] and not r[3], str(r))
        r = await keys(pg, ['9', '9', '9', '9', '*', '9', '='])
        check('9999 · 9', r[1] == '= 89.991' and 'bis 10.000' in r[2] and not r[3], str(r))
        r = await keys(pg, ['C', '1', '0', '0', '0', '0', '1'])
        check('Grenze 10 000', r[0] == '10.000' and 'bis 10.000' in r[2], str(r))
        r = await keys(pg, ['C', '4', ':', '0', '='])
        check('durch 0', 'Durch 0' in r[1], str(r))
        r = await keys(pg, ['C', '2', '+', '3', '+', '4', '='])
        check('weiterrechnen', r[0] == '5 + 4' and r[1] == '= 9', str(r))
        r = await keys(pg, ['*', '2', '='])
        check('mit Ergebnis weiter', r[0] == '9 · 2' and r[1] == '= 18', str(r))
        r = await keys(pg, ['7', 'back', '8'])
        check('neue Zahl und Löschtaste', r[0] == '8' and r[1] == '', str(r))
        r = await keys(pg, ['C', '1', '0', '0', '0', '0', '='])
        r = await keys(pg, ['C', '5', '0', '0', '0', '+', '5', '0', '0', '0', '='])
        check('10 000 als Material', r[1] == '= 10.000' and '10 Tausender' in r[4], str(r))
        await pg.click('[data-trk="C"]'); await pg.keyboard.type('7*6'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(80)
        check('Tastatur', await pg.evaluate("document.querySelector('.trc-res').textContent") == '= 42')
        await pg.click('[data-trm]'); await pg.wait_for_timeout(80)
        check('Material aus', await pg.locator('.trc-mat').count() == 0 and await pg.evaluate("app.tr.mat") is False)
        await pg.click('[data-trm]'); await pg.wait_for_timeout(80)

        # Fertig → Auswahl; Startseite → Kiste verlassen
        await pg.click('[data-kiste-end]'); await pg.wait_for_timeout(100)
        check('Fertig', await pg.evaluate("[app.mode, !!app.kiste, !!app.wz?.kiste]") == ['home', False, True])
        await pg.click('.ct-tile[data-kiste="calc"]'); await pg.wait_for_timeout(100)
        await pg.evaluate("goHome()"); await pg.wait_for_timeout(100)
        check('verlassen setzt zurück', await pg.evaluate("[!!app.kiste, !!app.calc]") == [False, False])

        # Lernstand und ILEB
        secs = await pg.evaluate(f"JSON.stringify(statsSections('{ali}'))")
        check('Lernstand', 'Materialkiste (selbst genutzt)' in secs and 'Rechenhilfe 4×' in secs, secs[-160:])
        il = await pg.evaluate(f"zoneReport('{ali}', 'M').ileb?.lernstand || ''")
        check('ILEB Mathe', 'nutzt Hilfen aus der Materialkiste (Rechenhilfe 4×' in il, il)

        # Gast: nichts gezählt
        await pg.evaluate("() => { data.current = null; app.wz = {kiste:true, step:'who'}; app.mode = 'home'; render(); }")
        await pg.click('[data-home-pick=""]'); await pg.wait_for_timeout(100)
        before = await pg.evaluate("JSON.stringify(data.kiste)")
        await pg.click('.ct-tile[data-kiste="tcalc"]'); await pg.wait_for_timeout(100)
        check('Gast zählt nicht', await pg.evaluate("JSON.stringify(data.kiste)") == before and await pg.evaluate("app.kiste") is True)

        # Kind löschen nimmt die Zählung mit
        await pg.evaluate(f"() => {{ const id = '{ali}'; data.profiles = data.profiles.filter(x => x.id !== id); delete data.log[id]; if(data.kiste) delete data.kiste[id]; saveData(); }}")
        check('Löschen', await pg.evaluate(f"!JSON.parse(localStorage.getItem('stufenweise.data')).kiste?.['{ali}']"))
        await pg.close()

        # Zwei Fenster: Zähler addieren sich
        ctx = await br.new_context(); a = await ctx.new_page()
        await a.add_init_script("addEventListener('storage', e => e.stopImmediatePropagation(), true);")
        await a.goto(URL); await a.wait_for_timeout(400); kid = await a.evaluate(ADD, 'Cem')
        b = await ctx.new_page(); await b.goto(URL); await b.wait_for_timeout(400)
        for pgx in (a, b): await pgx.evaluate(f"() => {{ data.current = '{kid}'; kisteGo('tcalc'); }}")
        check('zwei Fenster', await a.evaluate(f"JSON.parse(localStorage.getItem('stufenweise.data')).kiste['{kid}'].tcalc") == 2)
        await ctx.close()

        # Handy: nichts zu breit
        pg = await br.new_page(viewport={'width': 390, 'height': 844}); await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.click('[data-ctx-kiste]'); await pg.click('.ct-tile[data-kiste="tcalc"]'); await pg.wait_for_timeout(100)
        await keys(pg, ['9', '9', '9', '9', '+', '1', '='])
        check('Handy-Breite', await pg.evaluate("document.documentElement.scrollWidth") <= 392)
        await br.close()
    print('FERTIG', 'Fehler: ' + ', '.join(ERR) if ERR else 'alles ok')

asyncio.run(main())
