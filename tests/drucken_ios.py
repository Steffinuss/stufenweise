"""Backlog V (Stefan, 28.11.2026): Drucken auf iPad und iPhone.
- Am Computer: kein Hinweiskasten, Knöpfe heißen „Drucken“ usw.
- iPad/iPhone in Safari: Hinweiskasten am Druck-Knopf („Erlauben“, Kopf-/Fußzeile, Skalierung, Computer); Knöpfe bleiben „Drucken“.
- App vom Home-Bildschirm: Knöpfe heißen „Teilen und drucken“, „Heft teilen und drucken“ …; ein Tipp gibt das Dokument als HTML-Datei
  an das Teilen-Menü (navigator.share); geht Teilen nicht, kommt ein Hinweis auf „Als Datei speichern“.
iPad/iPhone werden mit window.STUFENWEISE_IOS = 'safari' | 'app' nachgestellt, das Teilen-Menü mit einer Attrappe."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

SHARE = """window.__shared = []; window.__canShare = true;
navigator.canShare = (d) => window.__canShare && !!d.files;
navigator.share = async (d) => { const f = d.files[0]; window.__shared.push({name: f.name, type: f.type, size: f.size, head: (await f.text()).slice(0, 15)}); };"""
SEED = "data.profiles.push({id:'k1',name:'Mia'}); data.current='k1'; saveData();"

async def page(br, mode):
    ctx = await br.new_context(viewport={'width': 1180, 'height': 900})
    if mode: await ctx.add_init_script(f"window.STUFENWEISE_IOS = '{mode}';" + SHARE)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
    await pg.goto(URL); await pg.wait_for_timeout(500)
    return ctx, pg

async def sheet(pg, mode):
    await pg.evaluate(f"app.sheetMode = '{mode}'; openSheets('none'); app.sheetMode = '{mode}'; renderSheets()"); await pg.wait_for_timeout(700)

async def main():
    async with async_playwright() as p:
        br = await launch(p)
        # Computer
        ctx, pg = await page(br, None)
        await sheet(pg, 'single')
        check('Computer: kein Hinweiskasten', await pg.locator('.print-ios').count() == 0)
        check('Computer: Knopf „Drucken“', (await pg.inner_text('#sh-print')).strip() == 'Drucken')
        await ctx.close()
        # Safari auf dem iPad
        ctx, pg = await page(br, 'safari')
        await sheet(pg, 'single')
        t = await pg.inner_text('.print-ios') if await pg.locator('.print-ios').count() else ''
        check('Safari: Hinweis mit „Erlauben“, Kopf-/Fußzeile, Skalierung, Computer', all(w in t for w in ['Erlauben', 'Kopf- und Fußzeile', 'Skalierung', 'Computer']), t[:120])
        check('Safari: Knopf bleibt „Drucken“', (await pg.inner_text('#sh-print')).strip() == 'Drucken')
        await ctx.close()
        # App vom Home-Bildschirm
        ctx, pg = await page(br, 'app')
        await pg.evaluate(SEED)
        await sheet(pg, 'single')
        t = await pg.inner_text('.print-ios')
        check('App: Hinweis zum Teilen-Menü', 'Teilen und drucken' in t and 'Als Datei speichern' in t and 'Erlauben' not in t, t[:120])
        check('App: Knopf „Teilen und drucken“', (await pg.inner_text('#sh-print')).strip() == 'Teilen und drucken')
        await pg.click('#sh-print'); await pg.wait_for_timeout(400)
        sh = await pg.evaluate("window.__shared")
        check('App: Blatt als HTML-Datei geteilt', len(sh) == 1 and sh[0]['type'] == 'text/html' and sh[0]['name'].startswith('Arbeitsblatt') and sh[0]['name'].endswith('.html') and sh[0]['size'] > 5000 and sh[0]['head'].lower().startswith('<!doctype html'), sh)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        await sheet(pg, 'samml')
        check('App: „Alle teilen und drucken“', (await pg.inner_text('#sm-print')).strip() == 'Alle teilen und drucken')
        await pg.click('#sm-print'); await pg.wait_for_timeout(400)
        check('App: Blattsammlung geteilt', (await pg.evaluate("window.__shared.at(-1).name")) == 'Blattsammlung.html')
        await pg.evaluate("window.__canShare = false")
        await pg.click('#sm-print'); await pg.wait_for_timeout(400)
        toast = await pg.evaluate("document.querySelector('.toast')?.textContent || document.body.innerText.match(/Teilen geht hier nicht[^\\n]*/)?.[0] || ''")
        check('App: ohne Teilen Hinweis auf „Als Datei speichern“', 'Als Datei speichern' in toast, toast[:100])
        # Bericht
        await pg.evaluate("window.__canShare = true; document.querySelectorAll('dialog[open]').forEach(d => d.close()); openReport('k1')"); await pg.wait_for_timeout(500)
        check('App: Bericht „Teilen und drucken“ mit Hinweis', (await pg.inner_text('#rp-print')).strip() == 'Teilen und drucken' and await pg.locator('#dlg-report .print-ios').count() == 1)
        n = await pg.evaluate("window.__shared.length")
        await pg.click('#rp-print'); await pg.wait_for_timeout(400)
        check('App: Bericht geteilt', await pg.evaluate("window.__shared.length") == n + 1)
        await ctx.close(); await br.close()
    print('FEHLER' if ERR else 'alles ok', ERR)

asyncio.run(main())
