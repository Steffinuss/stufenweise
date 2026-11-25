"""Rückmeldungen aus dem Einsatz an der Tafel (25.11.2026, 0.35.1):
1. Satz legen: vertauschte Teile bei „und“ gelten als richtig (Satz-Baukasten und Schüttelsätze).
2. Smartboard: Solange die eigene Zifferntastatur offen ist, sind Ziffernfelder schreibgeschützt
   (keine Systemtastatur); eine echte Tastatur geht trotzdem; eingerollt wieder normal."""
import asyncio
from common import URL, launch, FOKUS_AUS
from playwright.async_api import async_playwright

RES = []
def chk(name, cond, info=''):
    RES.append(cond); print(('ok ' if cond else 'FEHLER ') + f' [{name}] {info}')


async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}, has_touch=True)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(FOKUS_AUS)
        await pg.goto(URL); await pg.wait_for_timeout(500)

        v = await pg.evaluate("sentVariants('Mia stellt die Tassen und die Teller in den Schrank.'.split(' '))")
        chk('und: Teile tauschen', 'Mia stellt die Teller und die Tassen in den Schrank.' in v, str(len(v)))
        v = await pg.evaluate("sentVariants('Ich koche und Tom spült.'.split(' '))")
        chk('und: kein falscher Tausch', v == ['Ich koche und Tom spült.'], str(v))
        v = await pg.evaluate("sentVariants('Am Freitag kaufen wir Milch, Brot und Käse.'.split(' '))")
        chk('Aufzählung: alle Reihenfolgen', len(v) == 6 and 'Am Freitag kaufen wir Käse, Brot und Milch.' in v)

        # weitere sinnvolle Wortstellungen (25.11. abends)
        def order_js(target, given):
            return f"""(()=>{{ const w = {target!r}.split(' '), want = {given!r}.split(' '), used = new Set();
              const norm = x => x;
              const o = want.map(g => {{ const i = w.findIndex((x, k) => norm(x) === norm(g) && !used.has(k)); used.add(i); return i; }});
              return [sentOk(w, o), sentMatch(w, o)]; }})()"""
        for target, given, want in [
            ('Morgen früh fahren wir mit dem Zug in die Stadt.', 'Morgen fahren wir früh mit dem Zug in die Stadt.', True),
            ('Morgen früh fahren wir mit dem Zug in die Stadt.', 'Wir fahren morgen früh mit dem Zug in die Stadt.', False),
            ('In der Küche schneiden wir Gurke und Tomate.', 'In der Küche schneiden wir Tomate und Gurke.', False),
            ('Wenn es regnet, nehme ich eine Jacke mit.', 'Ich nehme eine Jacke mit, wenn es regnet.', False),
            ('Am Freitag kaufen wir Milch, Brot und Käse.', 'Am Freitag kaufen wir Käse, Milch und Brot.', False),
            ('Lea hat Hunger.', 'Hunger hat Lea.', False),
            ('Mia stellt die Tassen und die Teller in den Schrank.', 'Mia stellt die Teller und die Tassen in den Schrank.', True),
            ('Morgen früh fahren wir mit dem Zug in die Stadt.', 'Morgen früh wir fahren mit dem Zug in die Stadt.', False),
            ('Der Bus ist gelb.', 'Ist der Bus gelb.', False)]:
            ok, m = await pg.evaluate(order_js(target, given))
            chk(f'Umstellung {"richtig" if want else "falsch"}: {given}', ok is want, str(m))
        r = await pg.evaluate("(()=>{ const it = shakeItem(['Die','Banane','ist','gelb.'], 'Banane'); return [evalWrite(it, {order:[3,2,0,1]}).ok, evalWrite(it, {order:[0,1,2,3]}).ok]; })()")
        r = r == [False, True]
        chk('Bildsatz: Anfang und Punkt bleiben („Gelb ist die Banane.“ zählt nicht)', r is True)

        # Tafel: erst alle Sätze einer Länge, dann wieder von vorn
        r = await pg.evaluate("""(()=>{ const T = app.ts, seen = []; T.len = 'lang'; T.queue = {}; const n = SATZ_BANK.lang.length;
          for(let k = 0; k < n; k++){ tsGen(); seen.push(T.words.join(' ')); } const all = new Set(seen).size === n;
          tsGen(); const next = T.words.join(' '); return [all, next !== seen[n - 1], SATZ_BANK.kurz.length, SATZ_BANK.mittel.length, n]; })()""")
        chk('Tafel: jeder Satz einmal, bevor einer wiederkommt', r[0] is True and r[1] is True, str(r))
        chk('mehr Sätze (40/40/25)', r[2:] == [40, 40, 25], str(r[2:]))
        # Satz-Baukasten an der Tafel
        r = await pg.evaluate("""(()=>{ tsSet('Mia stellt die Tassen und die Teller in den Schrank.'); const T = app.ts;
          const want = 'Mia stellt die Teller und die Tassen in den Schrank.'.split(' '), used = new Set();
          T.order = want.map(w => { const i = T.words.findIndex((x, k) => x === w && !used.has(k)); used.add(i); return i; });
          return sentOk(T.words, T.order); })()""")
        chk('Satz-Baukasten: Teller und Tassen richtig', r is True)
        r = await pg.evaluate("(()=>{ const w = 'Mia stellt die Tassen und die Teller in den Schrank.'.split(' '); return sentOk(w, [1,0,2,3,4,5,6,7,8,9]); })()")
        chk('Satz-Baukasten: falsche Reihenfolge bleibt falsch', r is False)
        r = await pg.evaluate("(()=>{ const it = {type:'sent', words:'Mia stellt die Tassen und die Teller in den Schrank.'.split(' ')}; return evalWrite(it, {order:[0,1,5,6,4,2,3,7,8,9]}).ok; })()")
        chk('Schüttelsatz: Teller und Tassen richtig', r is True)

        # Zifferntastatur: schreibgeschützt, solange offen
        await pg.evaluate("settings.numpad='on'; saveSettings()")
        if await pg.locator("[data-ctx='practice']").count(): await pg.click("[data-ctx='practice']")
        await pg.evaluate("kisteGo('calc')"); await pg.wait_for_timeout(200)
        await pg.click('[data-range="100"]'); await pg.wait_for_timeout(200); await pg.evaluate('startRandom()'); await pg.wait_for_timeout(300)
        if await pg.locator('#c-join').count(): await pg.click('#c-join'); await pg.wait_for_timeout(1500)
        if await pg.locator('#guess').count():
            await pg.click('#guess'); await pg.wait_for_timeout(200)
            st = await pg.evaluate("(()=>{const e=document.querySelector('#guess'); return [e.readOnly, e.getAttribute('inputmode'), !document.getElementById('numpad').hidden]})()")
            chk('Feld schreibgeschützt bei offener Tastatur', st == [True, 'none', True], str(st))
            await pg.click('#numpad [data-np="1"]'); await pg.click('#numpad [data-np="2"]')
            chk('Bildschirmtastatur schreibt', await pg.evaluate("document.querySelector('#guess').value") == '12')
            await pg.keyboard.press('Backspace'); await pg.keyboard.type('5')
            chk('echte Tastatur geht trotzdem', await pg.evaluate("document.querySelector('#guess').value") == '15')
            await pg.click('#numpad [data-np="min"]'); await pg.wait_for_timeout(150)
            st = await pg.evaluate("(()=>{const e=document.querySelector('#guess'); return [e.readOnly, e.getAttribute('inputmode')]})()")
            chk('eingerollt: wieder normal', st == [False, 'numeric'], str(st))
            await pg.click('#numpad [data-np="max"]'); await pg.wait_for_timeout(150)
            chk('ausgeklappt: wieder geschützt', await pg.evaluate("document.querySelector('#guess').readOnly") is True)
        else:
            chk('Ergebnisfeld gefunden', False)
        chk('keine Fehler', not errs, str(errs))
        await b.close()
    print('ERR', [] if all(RES) else ['siehe oben'])

asyncio.run(main())
