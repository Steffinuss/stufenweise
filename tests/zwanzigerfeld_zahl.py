"""Unterricht → Zwanzigerfeld: Zahl vorgeben und verdecken (Backlog B, Stefan 19.11.2026).
Zahl eingeben (Enter oder „Legen“) füllt das Feld neu; „Zufallszahl“ lost eine andere Zahl aus;
„Zahl verdecken“ wirkt auf die Anzahl allein und weiterhin auf das Ergebnis einer Rechnung;
„?“ deckt auf, die aufgedeckte Zahl antippen deckt wieder zu; Zahlen außerhalb des Felds werden abgewiesen."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

EQ = "document.querySelector('.tf-eq')?.textContent"


async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        for vw in [(1180, 820), (390, 844)]:
            pg = await b.new_page(viewport={'width': vw[0], 'height': vw[1]}); pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(400)
            await pg.evaluate("setCtx('class'); setTool('tfield')"); await pg.wait_for_timeout(200)
            await pg.fill('#tf-num', '14'); await pg.press('#tf-num', 'Enter'); await pg.wait_for_timeout(150)
            if await pg.evaluate(f"[app.tf.dots.length, {EQ}]") != [14, '14']: errs.append(f'{vw}: 14 nicht gelegt')
            await pg.click('[data-tfh]'); await pg.wait_for_timeout(150)
            if await pg.evaluate(EQ) != '?': errs.append(f'{vw}: Zahl nicht verdeckt')
            await pg.click('[data-tf-reveal]'); await pg.wait_for_timeout(100)
            if await pg.evaluate(EQ) != '14': errs.append(f'{vw}: Aufdecken')
            await pg.click('[data-tf-cover]'); await pg.wait_for_timeout(100)
            if await pg.evaluate(EQ) != '?': errs.append(f'{vw}: wieder verdecken')
            await pg.click('#tf-rand'); await pg.wait_for_timeout(100)
            n = await pg.evaluate("app.tf.dots.length")
            if not (1 <= n <= 20) or n == 14 or await pg.evaluate(EQ) != '?': errs.append(f'{vw}: Zufallszahl {n}')
            await pg.fill('#tf-num', '25'); await pg.click('#tf-set'); await pg.wait_for_timeout(100)
            if await pg.evaluate("app.tf.dots.length") != n: errs.append(f'{vw}: 25 nicht abgewiesen')
            await pg.click('[data-tfr="10"]'); await pg.wait_for_timeout(100)
            await pg.fill('#tf-num', '7'); await pg.click('#tf-set'); await pg.wait_for_timeout(100)
            if await pg.evaluate("[app.tf.cap, app.tf.dots.length]") != [10, 7]: errs.append(f'{vw}: Zehnerfeld')
            await pg.evaluate("app.tf.cap=20; app.tf.dots=[...Array(7).fill('b'),...Array(5).fill('o')]; app.tf.shown=false; renderTfield()")
            if await pg.evaluate(EQ) != '7 + 5 = ?': errs.append(f'{vw}: Rechnung verdeckt nicht mehr: {await pg.evaluate(EQ)}')
            await pg.close()
        print('ERR', errs); await b.close()
asyncio.run(main())
