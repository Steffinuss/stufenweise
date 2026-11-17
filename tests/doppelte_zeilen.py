"""Prüft alle Arbeitsblätter: Innerhalb einer Aufgabe darf keine Zeile doppelt vorkommen
(z. B. zweimal „7 = 4 + □“ untereinander), und zwei gleiche Aufgaben dürfen nicht direkt aufeinander folgen."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

RUNS = 25
JS = """(topic) => {
  const isM = topic.startsWith('M:');
  const zrs = isM ? [10, 20, 100, 1000] : [null];
  const found = [];
  for (const zr of zrs) for (let r = 0; r < %d; r++) {
    app.sheet.topic = topic; app.sheet.sol = false; app.sheet.n = 'fill'; app.sheet.htp = '0';
    if (zr) app.sheet.zr = zr;
    const doc = new DOMParser().parseFromString(buildSheet().html, 'text/html');
    let prev = null;
    for (const t of doc.querySelectorAll('.ab-task')) {
      const rows = [...t.querySelectorAll('.ab-row')].map(e => [...e.childNodes].map(c => c.textContent.trim() || '○').join(' ').replace(/\\s+/g, ' ').trim()).filter(Boolean); /* Kreise/Kästchen als Trenner, sonst sind „11 ○ 3“ und „1 ○ 13“ gleich */
      const dup = rows.find((x, i) => rows.indexOf(x) !== i);
      if (dup) found.push(`${topic} bis ${zr}: Zeile doppelt „${dup}“`);
      const c = t.cloneNode(true); c.querySelectorAll('.nr').forEach(e => e.remove());
      const body = c.innerHTML;
      if (prev !== null && body && body === prev) found.push(`${topic} bis ${zr}: gleiche Aufgabe direkt nacheinander`);
      prev = body;
    }
  }
  return [...new Set(found)];
}""" % RUNS

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("openSheets()"); await pg.wait_for_timeout(500)
        topics = await pg.evaluate("sheetTree().flatMap(f=>f.areas.flatMap(a=>a.items.map(x=>x[0]))).filter(t=>!t.startsWith('K:'))")
        bad = []
        for t in topics:
            bad += await pg.evaluate(JS, t)
        for x in bad: print('DOPPELT', x)
        print(len(topics), 'Themen geprüft,', len(bad), 'Funde')
        if bad: errs.append(f'{len(bad)} doppelte Zeilen oder Aufgaben')
        print('ERR', errs); await b.close()
asyncio.run(main())
