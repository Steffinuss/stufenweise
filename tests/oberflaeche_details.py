"""Kleine Oberflächen-Details:
1. Fachwahl „Mathe/Deutsch“ ist in beiden Fächern mittig (in Deutsch ist die Leiste breiter und linksbündig)
2. Lineal-Aufgaben: Gegenstände haben realistische Längen (Radiergummi 3–6 cm, Schlüssel 4–8 cm, Kreide 5–10 cm …)"""
import asyncio, re
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p); pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        for subj, mode in [('M', 'number'), ('D', 'read')]:
            await pg.evaluate(f"settings.subject='{subj}'; app.mode='{mode}'; render()"); await pg.wait_for_timeout(400)
            off = await pg.evaluate("""[...document.querySelectorAll('#modes .subj button')].map(b=>{const t=document.createRange(); t.selectNodeContents(b); const tr=t.getBoundingClientRect(), br=b.getBoundingClientRect(); return Math.round((tr.left-br.left)-(br.right-tr.right));})""")
            print('Fachwahl', subj, 'Versatz', off)
            if any(abs(x) > 2 for x in off): errs.append(f'Fachwahl {subj} nicht mittig: {off}')
        res = await pg.evaluate("""(()=>{const out={}; for(let i=0;i<400;i++){ const it=pick(G_ITEMS.G1)(); const m=it.label.match(/: (\\S+) (\\d+) cm/); if(m){ (out[m[1]] ??= new Set()).add(+m[2]); } }
            return Object.fromEntries(Object.entries(out).map(([k,v])=>[k,[Math.min(...v),Math.max(...v)]]));})()""")
        print('Längen beim Üben/Test:', res)
        lim = await pg.evaluate("RULER_LEN")
        for k, (lo, hi) in res.items():
            a, z = lim[k]
            if lo < a or hi > z: errs.append(f'{k}: {lo}–{hi} cm außerhalb {a}–{z}')
        print('ERR', errs); await b.close()
asyncio.run(main())
