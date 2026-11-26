"""Mehrere Fenster derselben App (z. B. installierte App und Browser-Tab) teilen sich den Speicher.
Ein Fenster darf nie Kinder oder Ergebnisse löschen, die es nur nicht kennt (Fehler bis 0.29.0).

„Veraltet“ heißt hier: Das Fenster bekommt keine Nachricht über Änderungen anderer Fenster
(wie ein Fenster, das lange im Hintergrund lag). Es muss trotzdem richtig zusammenführen."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

ADD = """n => { const p = {id: newId('p-'), name: n, created: Date.now(), updated: Date.now(), rec: null, screening: null, world: 'HS'};
  data.profiles.push(p); data.current = p.id; saveData(); return p.id; }"""
STORED = "() => JSON.parse(localStorage.getItem('stufenweise.data') || '{}')"
NAMES = "() => (JSON.parse(localStorage.getItem('stufenweise.data') || '{}').profiles || []).map(p => p.name).sort().join(',')"
PICK = "n => { data.current = data.profiles.find(p => p.name === n).id; }"
LOG = "t => { app.ctx = 'learn'; logAttempt({mode:'add', task:t, ok:true}); }"
DEAF = "addEventListener('storage', e => e.stopImmediatePropagation(), true);"

async def win(ctx, stale=False):
    pg = await ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append('pageerror') or print('ERR [pageerror]', e))
    if stale: await pg.add_init_script(DEAF)
    await pg.goto(URL); await pg.wait_for_timeout(700)
    return pg

RAW = "() => localStorage.getItem('stufenweise.data')"
async def sync(src, *dst):
    """Warten, bis die anderen Fenster den Stand von src sehen. Chrome gibt Änderungen an localStorage erst nach kurzer Zeit
    an andere Fenster weiter; unter Last (Tests laufen parallel) kann das dauern. Im Unterricht liegen zwischen zwei
    Eingaben in verschiedenen Fenstern immer Sekunden."""
    raw = await src.evaluate(RAW)
    for d in dst: await d.wait_for_function("r => localStorage.getItem('stufenweise.data') === r", arg=raw, timeout=10000)

async def fresh(br):
    ctx = await br.new_context(viewport={'width': 1100, 'height': 800})
    return ctx

async def main():
    async with async_playwright() as p:
        br = await launch(p)

        # 1. Leeres, länger offenes Fenster + „Jetzt aktualisieren“ (der gemeldete Fall)
        ctx = await fresh(br); a = await win(ctx, stale=True); b = await win(ctx)
        for n in ['Ali', 'Bea', 'Cem']: await b.evaluate(ADD, n)
        await a.evaluate("() => { UPD.found = {version:'9.9.9'}; doUpdate(); }"); await a.wait_for_timeout(1500)
        check('aktualisieren im alten Fenster', await b.evaluate(NAMES) == 'Ali,Bea,Cem', await b.evaluate(NAMES))
        await ctx.close()

        # 2. Veraltetes Fenster übt mit einem alten Kind, anderes Fenster hat ein Kind dazu
        ctx = await fresh(br); a = await win(ctx, stale=True)
        await a.evaluate(ADD, 'Ali'); b = await win(ctx); await b.evaluate(ADD, 'Bea'); await sync(b, a)
        await a.evaluate(PICK, 'Ali'); await a.evaluate(LOG, '1+1')
        st = await a.evaluate(STORED); ali = next(q['id'] for q in st['profiles'] if q['name'] == 'Ali')
        check('neues Kind bleibt', await a.evaluate(NAMES) == 'Ali,Bea', await a.evaluate(NAMES))
        check('Übung des alten Fensters bleibt', len(st['log'].get(ali, [])) == 1)
        check('altes Fenster kennt jetzt beide', await a.evaluate('data.profiles.length') == 2)
        await ctx.close()

        # 3. Kind im anderen Fenster gelöscht – veraltetes Fenster bringt es nicht zurück
        ctx = await fresh(br); b = await win(ctx)
        await b.evaluate(ADD, 'Ali'); await b.evaluate(ADD, 'Bea'); await b.evaluate(PICK, 'Bea'); await b.evaluate(LOG, '2+2')
        a = await win(ctx, stale=True)
        await b.evaluate("() => { const id = data.profiles.find(p => p.name === 'Bea').id; data.profiles = data.profiles.filter(x => x.id !== id); delete data.log[id]; data.current = null; saveData({empty: true}); }"); await sync(b, a)
        await a.evaluate(PICK, 'Ali'); await a.evaluate(LOG, '3+3')
        st = await a.evaluate(STORED)
        check('gelöschtes Kind bleibt gelöscht', await a.evaluate(NAMES) == 'Ali', await a.evaluate(NAMES))
        check('Übungen des gelöschten Kindes weg', len(st['log']) == 1, str(list(st['log'])))
        await ctx.close()

        # 4. „Daten löschen“ im anderen Fenster – nur die neue Übung des veralteten Fensters kommt dazu
        ctx = await fresh(br); b = await win(ctx)
        await b.evaluate(ADD, 'Ali')
        for t in ['1+1', '1+2', '1+3']: await b.evaluate(LOG, t)
        a = await win(ctx, stale=True)
        await b.evaluate("() => { delete data.log[data.current]; saveData(); }"); await sync(b, a)
        await a.evaluate(LOG, '9+9')
        st = await a.evaluate(STORED); L = list(st['log'].values())[0] if st['log'] else []
        check('Daten löschen gilt weiter', [e['task'] for e in L] == ['9+9'], str([e['task'] for e in L]))
        await ctx.close()

        # 5. Einstufung im anderen Fenster entfernt, veraltetes Fenster setzt eine andere
        ctx = await fresh(br); b = await win(ctx)
        await b.evaluate(ADD, 'Ali')
        await b.evaluate("() => { setCell(data.current, 'M|10|I', {status:'erreicht', quelle:'lehrkraft', sum:''}); saveData(); }")
        a = await win(ctx, stale=True)
        await b.evaluate("() => { delete matrixOf(data.current)['M|10|I']; saveData(); }"); await sync(b, a)
        await a.evaluate(PICK, 'Ali'); await a.evaluate("() => { setCell(data.current, 'M|10|II', {status:'teilweise', quelle:'lehrkraft', sum:''}); saveData(); }")
        st = await a.evaluate(STORED); m = list(st['matrix'].values())[0]
        check('Einstufung entfernt bleibt entfernt', sorted(m) == ['M|10|II'], str(sorted(m)))
        await ctx.close()

        # 6. Fehlerzähler aus beiden Fenstern zusammenzählen
        ctx = await fresh(br); b = await win(ctx); await b.evaluate(ADD, 'Ali')
        await b.evaluate("() => noteError('add', 'zehner')")
        a = await win(ctx, stale=True)
        await a.evaluate(PICK, 'Ali'); await b.evaluate("() => noteError('add', 'zehner')"); await sync(b, a); await a.evaluate("() => noteError('add', 'zehner')")
        st = await a.evaluate(STORED); n = list(st['errs'].values())[0]['add']['zehner']
        check('Fehlerzähler', n == 3, str(n))
        await ctx.close()

        # 7. Sicherheitsnetz: Stand ohne Kinder überschreibt keinen Stand mit Kindern
        ctx = await fresh(br); a = await win(ctx, stale=True)
        await a.evaluate(ADD, 'Ali'); await a.evaluate(ADD, 'Bea')
        await a.evaluate("() => { data.profiles.length = 0; saveData(); }")
        check('kein Leeren ohne Absicht', await a.evaluate(NAMES) == 'Ali,Bea' and await a.evaluate('data.profiles.length') == 2)
        await a.evaluate("() => { data.profiles.length = 0; data.log = {}; saveData({empty: true}); }")
        check('letztes Kind löschen geht', await a.evaluate(NAMES) == '')
        await ctx.close()

        # 8. Offenes Fenster übernimmt Änderungen anderer Fenster sofort (auch ein ganz neues Fenster)
        ctx = await fresh(br); a = await win(ctx); b = await win(ctx)
        await b.evaluate(ADD, 'Ali')
        try: await a.wait_for_function('data.profiles.length === 1', timeout=10000)
        except Exception: pass
        check('Fenster übernimmt neues Kind', await a.evaluate('data.profiles.length') == 1)
        c = await win(ctx); await c.evaluate("() => saveData()")
        check('neues Fenster löscht nichts', await a.evaluate(NAMES) == 'Ali')
        await a.evaluate("() => { settings.world = 'BSS'; saveSettings(); }")
        try: await b.wait_for_function("settings.world === 'BSS'", timeout=10000)
        except Exception: pass
        check('Einstellungen übernommen', await b.evaluate('settings.world') == 'BSS')
        await ctx.close()

        # 9. Nicht lesbarer Stand wird vor dem Überschreiben aufgehoben
        ctx = await fresh(br); a = await win(ctx)
        await a.evaluate("() => localStorage.setItem('stufenweise.data', '{kaputt')")
        a2 = await win(ctx); await a2.evaluate(ADD, 'Ali')
        check('defekter Stand aufgehoben', await a2.evaluate("() => localStorage.getItem('stufenweise.data.defekt')") == '{kaputt')
        await ctx.close()

        # 10. Testversion und richtige App bleiben getrennt (Schlüssel mit „test:“ lösen nichts aus)
        ctx = await fresh(br); a = await win(ctx); await a.evaluate(ADD, 'Ali')
        await a.evaluate("() => localStorage.setItem('test:stufenweise.data', JSON.stringify({profiles:[]}))")
        b = await win(ctx); await b.evaluate("() => localStorage.setItem('test:stufenweise.data', JSON.stringify({profiles:[{id:'x', name:'Test'}]}))")
        await a.wait_for_timeout(300)
        check('Testschlüssel ignoriert', await a.evaluate('data.profiles.map(p => p.name).join()') == 'Ali')
        await ctx.close()

        await br.close()
    print('FERTIG', 'Fehler: ' + ', '.join(ERR) if ERR else 'alles ok')

asyncio.run(main())
