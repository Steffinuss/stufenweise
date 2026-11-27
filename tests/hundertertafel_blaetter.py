"""Hundertertafel-Blätter H1–H6 (Stefan, 23.11.):
- Titel nennt die Hundertertafel, über den Aufgaben steht „Hundertertafel“ mit Tafel-Bild
- auf Wunsch eine Extraseite mit der ausgefüllten Hundertertafel (vor den Lösungen), Häkchen nur bei H1–H6
- Häkchen wird gemerkt; Tausenderbuch und andere Blätter bleiben ohne Hinweis
- Heft: die Extraseite wird mit übernommen"""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("openSheets()"); await pg.wait_for_timeout(400)

        r = await pg.evaluate("""()=>{const out={};for(const k of ['H1','H2','H3','H4','H5','H6','H7','HM']){
            for(const taf of [false,true]){ Object.assign(app.sheet,{topic:'H:'+k,n:6,sol:true,taf});
              const d=new DOMParser().parseFromString(buildSheet().html,'text/html');
              out[k+(taf?'+':'')]={title:d.querySelector('h1').textContent, hint:!!d.querySelector('.ab-legend .ab-taf'),
                pages:[...d.querySelectorAll('.page')].map(x=>x.className), help:d.querySelector('.page.hilfe .hb-c')?d.querySelectorAll('.page.hilfe .hb-c').length:0}; }}
            return out}""")
        for k, v in r.items(): print(k, v)
        for k in ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']:
            if 'Hundertertafel' not in r[k]['title']: errs.append(f'{k}: Titel ohne Hundertertafel: {r[k]["title"]}')
            if not r[k]['hint']: errs.append(f'{k}: kein Hinweis')
            if any('hilfe' in c for c in r[k]['pages']): errs.append(f'{k}: Extraseite ohne Häkchen')
            if r[k + '+']['pages'] != ['page hf-p', 'page hf-p hilfe', 'page hf-p sol']: errs.append(f'{k}: Seiten {r[k + "+"]["pages"]}')
            if r[k + '+']['help'] < 100: errs.append(f'{k}: Tafel unvollständig ({r[k + "+"]["help"]})')
        for k in ['H7', 'H7+', 'HM+']:
            if r[k]['hint'] or any('hilfe' in c for c in r[k]['pages']): errs.append(f'{k}: Hinweis/Extraseite, soll nicht')

        # Häkchen im Dialog: nur bei H1–H6, wird gemerkt
        await pg.evaluate("app.sheet.taf=false; app.sheet.topic='H:H3'; renderSheets()"); await pg.wait_for_timeout(300)
        if not await pg.locator('#sh-taf').count(): errs.append('Häkchen fehlt bei H3')
        await pg.locator('#sh-taf').check(); await pg.wait_for_timeout(300)
        saved = await pg.evaluate("JSON.parse(localStorage.getItem(SHEET_KEY)).taf")
        if saved is not True: errs.append(f'Häkchen nicht gemerkt: {saved}')
        pages = await pg.evaluate("[...document.querySelector('#sh-frame').contentDocument.querySelectorAll('.page')].map(x=>x.className)")
        print('Vorschau', pages)
        if 'page hf-p hilfe' not in pages: errs.append('Vorschau ohne Extraseite')
        for t in ['H:H7', 'M:plus', 'H:HM']:
            await pg.evaluate(f"app.sheet.topic='{t}'; renderSheets()"); await pg.wait_for_timeout(200)
            if await pg.locator('#sh-taf').count(): errs.append(f'Häkchen bei {t}')

        # Blattsammlung: Blatt mit Extraseite (Backlog U2: statt „Ins Arbeitsheft“)
        await pg.evaluate("app.samml.items=[]; app.sheet.topic='H:H5'; app.sheet.taf=true; renderSheets()"); await pg.wait_for_timeout(300)
        await pg.evaluate("sammlAdd()"); await pg.wait_for_timeout(200)
        items = await pg.evaluate("app.samml.items.map(i=>i.title+' | '+(i.html.match(/class=\"page[^\"]*/g)||[]).join(','))")
        print('Blattsammlung', items)
        if len(items) != 1 or 'hilfe' not in items[0] or 'Nachschauen' not in await pg.evaluate("app.samml.items[0].html"): errs.append(f'Blattsammlung: {items}')
        await pg.evaluate("app.samml.items=[]; saveSamml(); app.sheet.taf=false; sheetSave()")

        print('Fehler:', errs or 'keine')
        await b.close()
        if errs: raise SystemExit(1)

asyncio.run(main())
