"""Backlog I (Optimierung Deutsch): eindeutige Bilder, „Kenne ich nicht“, Bilder vorher ansehen, Bilder abwählen, Anhören,
W4-Silben, Hören P1–P4 (Üben und Lese-Test), Materialkiste Deutsch, Unterricht Deutsch, W6 Alltag, Hundertertafel verdeckt."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch, FOKUS_AUS

# Gerätestimme nachbilden: eine lokale und eine Online-Stimme (die Online-Stimme darf nie benutzt werden)
SPEECH = """Object.defineProperty(window,'speechSynthesis',{value:{getVoices:()=>[{name:'Anna',lang:'de-DE',localService:true},{name:'Google Deutsch',lang:'de-DE',localService:false}],speak:u=>{window.__said=(window.__said||[]).concat([[u.text,u.voice&&u.voice.name]])},cancel:()=>{},addEventListener:()=>{}}}); window.SpeechSynthesisUtterance=function(t){this.text=t};"""

def check(ok, msg):
    if not ok: raise AssertionError(msg)
    print('ok', msg)

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        ctx = await b.new_context(viewport={'width':1180, 'height':820}, has_touch=True)
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(SPEECH); await pg.add_init_script(FOKUS_AUS)
        await pg.goto(URL); await pg.wait_for_timeout(500)
        if await pg.locator("[data-ctx='practice']").count(): await pg.click("[data-ctx='practice']")
        # H1: nur eindeutige Bilder beim Schreiben
        bad = await pg.evaluate("[...wPool(LAUT_SHORT), ...wPool(LAUT_LONG), ...wPool(MERK), ...wPool(W_POOLS.W2())].filter(w => !CLEAR.includes(w) || W_AMBIG.includes(w))")
        check(bad == [], 'Schreib-Listen nur mit eindeutigen Bildern')
        # H4: abwählen
        await pg.evaluate("settings.wHide = ['Hase', 'Nase']; saveSettings()")
        check(await pg.evaluate("!wPool(LAUT_SHORT).includes('Hase') && !wPool(LAUT_SHORT).includes('Nase')"), 'abgewählte Bilder kommen nicht vor')
        check(await pg.evaluate("(settings.wHide = wAllPics(), wPool(LAUT_SHORT).length >= 3)"), 'alles abgewählt: Rückfall auf alle eindeutigen Bilder')
        await pg.evaluate("settings.wHide = []; saveSettings()")
        # Anhören aus: kein Knopf; an: Knopf mit lokaler Stimme
        await pg.evaluate("setSubject('D'); app.mode='read'; Object.assign(app.read, {lvl:'W3', item:null}); render()"); await pg.wait_for_timeout(200)
        check(await pg.locator('#stage [data-sayw]').count() == 0, 'ohne Einstellung kein Anhören-Knopf')
        await pg.evaluate("settings.anhoeren='on'; saveSettings(); render()"); await pg.wait_for_timeout(200)
        await pg.click('#stage [data-sayw]')
        said = await pg.evaluate("window.__said")
        check(said and said[-1][1] == 'Anna', 'Anhören nutzt nur die Stimme auf dem Gerät')
        # H2 beim Üben: Wort zeigen, abdecken, schreiben → zählt nicht als „auf Anhieb“, Wortschatzliste
        await pg.click('#r-unk'); await pg.click('[data-wmemo]')
        w = await pg.evaluate("app.read.item.target")
        for ch in w.lower(): await pg.click(f'[data-wkey="{ch}"]')
        await pg.evaluate("readCheck()")
        last = await pg.evaluate("data.log.guest.at(-1)")
        check(last.get('unk') == w and last['ok'] is False, '„Kenne ich nicht“ wird mit Hilfe protokolliert')
        check(w in ' '.join(await pg.evaluate("unkWords('guest')")), 'Wortschatzliste enthält das Wort')
        # H3: Bilder vorher ansehen bestimmt die Reihenfolge
        await pg.evaluate("Object.assign(app.read,{item:null}); readNew()"); await pg.click('#r-pics')
        q = await pg.evaluate("app.read.wq.slice()"); await pg.click('#r-pics-go')
        check(await pg.evaluate("app.read.item.target") == q[0], 'nach „Bilder ansehen“ kommt das erste gezeigte Bild')
        # W4: Silbenkarten
        await pg.evaluate("Object.assign(app.read, {lvl:'W4', item:sylCardItem(), r:{}, fb:null, tries:0}); renderRead()")
        t = await pg.evaluate("app.read.item.target"); tiles = await pg.evaluate("app.read.item.tiles")
        for sy in await pg.evaluate(f"sylOf('{t}')"): await pg.click(f'[data-wtile="{tiles.index(sy)}"]')
        await pg.evaluate("readCheck()"); check(await pg.evaluate("app.read.fb.ok"), 'W4 Silbenkarten legen')
        check(await pg.evaluate("WRITE.W4.length === 3"), 'Silbenkarten nicht im Test')
        # W6: eigener Satz
        await pg.evaluate("Object.assign(app.read, {lvl:'W6', item:satzItem(), r:{}, fb:null, tries:0}); app.read.r.text = 'Ich sehe ' + app.read.item.target + '.'; readCheck()")
        check(await pg.evaluate("app.read.fb.ok"), 'W6 eigener Satz wird erkannt')
        # Hören P1–P4
        for lv in ['P1', 'P2', 'P3', 'P4']:
            await pg.evaluate(f"Object.assign(app.read, {{lvl:'{lv}', item:null}}); render()"); await pg.wait_for_timeout(100)
            check(await pg.evaluate("app.read.item.type === 'choice' && app.read.item.label.length > 0"), f'Hören {lv} hat Übungen')
        # Lese-Test: L4 nicht erreicht → Hören wird getestet
        await pg.evaluate("goHome(); diagStart('L'); app.diag.started = true; renderDiag()")
        for i in range(80):
            if not await pg.evaluate("app.diag && !app.diag.done"): break
            await pg.evaluate("diagAnswer(true)")
        check(await pg.evaluate("Object.keys(matrixOf('guest')).some(k => k.startsWith('P|'))"), 'Lese-Test prüft Hören')
        # Schreib-Test: „Kenne ich nicht“ tauscht das Bild
        await pg.evaluate("goHome(); diagStart('W'); app.diag.started = true; renderDiag()")
        for i in range(10):
            if await pg.locator('#d-unk').count(): break
            await pg.evaluate("diagAnswer(true)")
        if await pg.locator('#d-unk').count():
            a = await pg.evaluate("app.diag.items[app.diag.idx].icon"); await pg.click('#d-unk')
            check(await pg.evaluate("app.diag.items[app.diag.idx].unkFrom[0]") == a, 'Test: anderes Bild statt des unbekannten')
        await pg.evaluate("goHome()")
        # Materialkiste und Unterricht Deutsch
        for k in ['abc', 'dict', 'tword']:
            await pg.evaluate(f"kisteGo('{k}')"); await pg.wait_for_timeout(150)
            check(await pg.evaluate("document.querySelector('#stage').innerText.length > 0"), f'Materialkiste {k}')
        await pg.evaluate("kisteHome(); setCtx('class')")
        for k in ['abc', 'tblitz', 'tsatz']:
            await pg.click(f'[data-ctool="{k}"]'); await pg.wait_for_timeout(150)
            check(await pg.evaluate(f"app.mode === '{k}'"), f'Unterricht {k}')
        await pg.click('#tb-next') if await pg.locator('#tb-next').count() else None
        # Hundertertafel verdeckt
        await pg.evaluate("setCtx('practice'); setSubject('M'); app.mode='read'; Object.assign(app.read, {lvl:'H1', item:null}); render()"); await pg.wait_for_timeout(150)
        await pg.click('[data-hcov="2"]'); await pg.wait_for_timeout(150)
        check(await pg.evaluate("[...document.querySelectorAll('#stage [data-hb]')].every(x => !x.textContent.trim())"), 'Hundertertafel verdeckt: keine Zahlen')
        await pg.click('[data-hcov="1"]'); await pg.wait_for_timeout(150)
        check(await pg.evaluate("[...document.querySelectorAll('#stage [data-hb]')].filter(x => x.textContent.trim()).length <= 19"), 'Hundertertafel teilweise verdeckt')
        # Arbeitsblätter
        for t in ['P:P1', 'P:P2', 'P:P3', 'P:P4', 'K:bildk']:
            n = await pg.evaluate(f"(app.sheet.topic = '{t}', buildSheet().html.length)")
            check(n > 1000, f'Arbeitsblatt {t}')
        print('ERR', errs)
        await b.close()

asyncio.run(main())
