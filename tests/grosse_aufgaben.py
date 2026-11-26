"""„Große Aufgaben“ und „Umtausch schon im Bild zeigen“ (Minus mit Zehnerübergang).
1. Große Aufgaben: bei allen Themen läuft nichts über den Rand der Aufgabenkarte, und die Karten sind wirklich größer.
2. Umtausch: das Bild zeigt immer genau die Zahl a, und nach dem Umtausch reichen die Einer und Zehner zum Wegstreichen."""
import asyncio, re
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("openSheets()"); await pg.wait_for_timeout(400)
        # Schalter im Dialog
        await pg.evaluate("app.sheet.topic='M:minus'; app.sheet.zr=100; app.sheet.mat=true; app.sheet.ue='mit'; renderSheets()")
        await pg.wait_for_timeout(300)
        for cb in ['#sh-gross', '#sh-tausch']:
            if not await pg.locator(cb).count(): errs.append(f'Schalter {cb} fehlt')
        await pg.check('#sh-gross'); await pg.check('#sh-tausch'); await pg.wait_for_timeout(500)
        st = await pg.evaluate("[app.sheet.gross, app.sheet.tausch, /ab-grid gross/.test(app.sheetDoc.html), /ab-tausch/.test(app.sheetDoc.html)]")
        print('Schalter', st)
        if not all(st): errs.append(f'Schalter wirken nicht: {st}')
        await pg.evaluate("app.sheet.tausch=false; app.sheet.ue='egal'")

        topics = await pg.evaluate("sheetTree().flatMap(f=>f.areas.flatMap(a=>a.items.map(x=>x[0]))).filter(t=>!t.startsWith('K:') && !/^H:H[TML]$/.test(t))")
        pp = await b.new_page(viewport={'width': 900, 'height': 1200}); over = []; small = []
        for t in topics:
            for zr in ([20, 100, 1000] if t.startswith('M:') else [None]):
                sizes = []
                for g in ('false', 'true'):
                    h = await pg.evaluate("([t,zr,g])=>{app.sheet.topic=t;app.sheet.gross=g;app.sheet.n=8;app.sheet.sol=false;if(zr)app.sheet.zr=zr;return buildSheet().html}", [t, zr, g == 'true'])
                    await pp.set_content(h); await pp.wait_for_timeout(30)
                    r = await pp.evaluate("""()=>{let o=0;for(const task of document.querySelectorAll('.ab-task')){const tb=task.getBoundingClientRect();
                        for(const e of task.querySelectorAll('*')){const b=e.getBoundingClientRect();if(b.width&&(b.right>tb.right+1||b.left<tb.left-1)){o++;break}}}
                        const f=document.querySelector('.ab-task .ab-ins .nr'); return {o, fs: f ? f.getBoundingClientRect().height : 0}}""")
                    if r['o']: over.append(f'{t} bis {zr} groß={g}: {r["o"]} Aufgaben zu breit')
                    sizes.append(r['fs'])
                if sizes[1] < sizes[0]*1.2: small.append(f'{t} bis {zr}: nicht größer ({sizes})')
        for x in over + small: print('PRÜFEN', x)
        print(len(topics), 'Themen geprüft')
        if over or small: errs.append(f'{len(over)} zu breit, {len(small)} nicht größer')

        # Umtausch: Bild = a, und nach dem Tausch kann man b wegstreichen
        bad = 0; n = 0
        for zr in (100, 1000):
            res = await pg.evaluate("""(zr)=>{const out=[];for(let r=0;r<40;r++){app.sheet.topic='M:minus';app.sheet.zr=zr;app.sheet.mat=true;app.sheet.tausch=true;app.sheet.ue='mit';app.sheet.gross=false;app.sheet.n=8;
                const d=new DOMParser().parseFromString(buildSheet().html,'text/html');
                for(const t of d.querySelectorAll('.ab-task')){const m=t.querySelector('.ab-row.big').textContent.match(/(\\d+)\\s*−\\s*(\\d+)/);const svg=t.querySelector('svg.matp');
                  out.push([+m[1],+m[2],svg.getAttribute('aria-label'),!!t.querySelector('.ab-tausch'),t.querySelectorAll('rect[stroke-dasharray]').length])}}return out}""", zr)
            for a, bb, label, hint, frames in res:
                n += 1
                h = int((re.search(r'(\d+) Hunderter', label) or [0, 0])[1]); z = int(re.search(r'(\d+) Zehner', label)[1]); e = int(re.search(r'(\d+) Einer', label)[1])
                ok = h*100 + z*10 + e == a and e >= bb % 10 and z*10 + e >= bb % 100 and h*100 + z*10 + e >= bb
                need = a % 10 < bb % 10 or (a % 100) // 10 < (bb % 100) // 10 or (a % 100) < (bb % 100)
                if not ok or hint != need or (hint and not frames):
                    bad += 1
                    if bad <= 5: print('FALSCH', a, bb, label, hint, frames)
        print(n, 'Minus-Aufgaben mit Umtausch geprüft,', bad, 'falsch')
        if bad: errs.append(f'{bad} Umtausch-Bilder falsch')
        print('ERR', errs); await b.close()
asyncio.run(main())
