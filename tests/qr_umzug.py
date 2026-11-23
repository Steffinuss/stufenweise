"""QR-Umzug (Backlog E, 23.11.2026): große Codes (700 Bytes, L) oder kleine (230 Bytes, M), Übungen spaltenweise gepackt
(Format 2), Empfang liest Format 1 und 2, neuere Formate werden mit Hinweis übergangen. Fehler F2: „die letzten 0 Übungen“
übertrug bis 0.30 alle Übungen (slice(-0)).
Der Umzug läuft echt: Codes auf Gerät A als Bild, auf Gerät B mit dem eingebauten Leser gelesen."""
import asyncio, json
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

FILL = """([kids, n]) => { const ids = [];
  for(let k = 0; k < kids; k++){ const id = newId('p-'); ids.push(id); data.profiles.push({id, name:'Kind' + k, created: Date.now(), updated: Date.now(), world:'HS'});
    let ts = 1795000000000 + k*1000; const L = data.log[id] = [];
    for(let i = 0; i < n; i++){ ts += 3000 + ((i*7919 + k*31) % 40000); const m = ['add','sub','read','number','times'][(i*3 + k) % 5];
      const e = {ts, mode:m, task: m === 'read' ? ['Nagel','Tulpe','Hose','Mama','Lampe'][(i + k) % 5] : `${(i*13 + k) % 20} + ${(i*7) % 10}`, ok: (i*k + i) % 4 > 0, tries: 1 + ((i + k) % 6 === 0)};
      if(m === 'read') e.lvl = 'L' + (1 + i % 6); if(i % 11 === 0) e.shown = true; L.push(e); }
    setCell(id, 'M|10|I', {status:'erreicht', quelle:'test', sum:'2 von 2'}); setCell(id, 'M|20|I', {status:'teilweise', quelle:'test', sum:'1 von 3'});
    data.skips ??= {}; data.skips[id] = [{ts: 1795000000000 + k, mode:'add', task:'1 + 1'}]; }
  saveData(); return ids; }"""
SCAN = r"""async (svg) => { const img = new Image(), url = URL.createObjectURL(new Blob([svg], {type:'image/svg+xml'}));
  await new Promise(r => { img.onload = r; img.src = url; });
  const W = 960, cv = document.createElement('canvas'); cv.width = W; cv.height = W; const cx = cv.getContext('2d', {willReadFrequently:true});
  cx.fillStyle = '#fff'; cx.fillRect(0, 0, W, W); cx.drawImage(img, 60, 60, 840, 840);
  const d = cx.getImageData(0, 0, W, W).data, g = new Uint8Array(W*W); for(let i = 0; i < W*W; i++) g[i] = (d[4*i]*77 + d[4*i+1]*150 + d[4*i+2]*29) >> 8;
  const r = QR.scan(g, W, W); return r ? [...r.bytes] : null; }"""
RECV = """() => { QRX.rx = null; QRX.oldSeen = 0; $('#qr-title').textContent = 'Per QR-Code empfangen';
  $('#qr-body').innerHTML = '<div class="qr-dots" id="qr-rdots"></div><p class="note" id="qr-state"></p>'; $('#dlg-qr').showModal(); }"""

async def send(pg, ids, small=False):
    await pg.evaluate(f"settings.qrSmall = {'true' if small else 'false'}")
    await pg.evaluate("() => openQrSend()"); await pg.wait_for_timeout(100)
    await pg.evaluate("ids => document.querySelectorAll('[data-qr-kid]').forEach(i => i.checked = ids.includes(i.dataset.qrKid))", ids)
    await pg.click('#qr-go'); await pg.wait_for_function("QRX.parts && document.querySelector('#qr-box svg')")
    return await pg.evaluate("[...QRX.parts]"), await pg.evaluate("document.querySelector('#qr-body .note').textContent")

async def receive(pg, parts):
    await pg.evaluate(RECV)
    for i in list(range(1, len(parts), 2)) + list(range(0, len(parts), 2)):   # andere Reihenfolge als gesendet
        b = await pg.evaluate(SCAN, parts[i])
        if b is None: return f'Teil {i + 1} nicht lesbar'
        await pg.evaluate("b => qrGot(new Uint8Array(b))", b)
    await pg.wait_for_selector('#qr-take', timeout=5000); await pg.click('#qr-take'); await pg.wait_for_timeout(200)
    return None

async def main():
    async with async_playwright() as p:
        br = await launch(p)
        ca, cb = await br.new_context(), await br.new_context()
        a, b = await ca.new_page(), await cb.new_page()
        for pg in (a, b): pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await a.goto(URL); await b.goto(URL); await a.wait_for_timeout(500); await b.wait_for_timeout(500)

        # 1. Sechs Kinder mit je 800 Übungen, große Codes: alles kommt exakt an
        ids = await a.evaluate(FILL, [6, 800])
        parts, note = await send(a, ids)
        small_parts, _ = await send(a, ids, small=True)
        check('große Codes: weniger Teile', len(parts) * 2.5 < len(small_parts), f'{len(parts)} groß, {len(small_parts)} klein')
        check('Text: alle Übungen', 'mit allen Übungen' in note, note[:120])
        check('Wechsel klein 0,65 s', await a.evaluate("qrMode().ms") == 650)  # zuletzt klein gewählt
        await a.evaluate("settings.qrSmall = false")
        check('Wechsel groß 0,4 s', await a.evaluate("qrMode().ms") == 400)
        err = await receive(b, parts)
        check('alle Teile lesbar', err is None, err or '')
        same = await b.evaluate("ids => JSON.stringify(ids.map(id => data.log[id]))", ids) == await a.evaluate("ids => JSON.stringify(ids.map(id => data.log[id]))", ids)
        check('Übungen exakt gleich', same)
        check('Lernstand und Verlauf', await b.evaluate("ids => JSON.stringify(ids.map(id => [data.matrix[id], data.mhist[id], data.skips[id]]))", ids)
              == await a.evaluate("ids => JSON.stringify(ids.map(id => [data.matrix[id], data.mhist[id], data.skips[id]]))", ids))
        await b.evaluate(RECV)
        for i in range(len(parts)): await b.evaluate("b => qrGot(new Uint8Array(b))", await b.evaluate(SCAN, parts[i]))
        await b.click('#qr-take'); await b.wait_for_timeout(200)
        check('zweimal empfangen: keine Doppelten', await b.evaluate("ids => ids.every(id => data.log[id].length === 800)", ids))

        # 2. Fehler F2: zu groß → gekürzt, ehrlich angezeigt; „0“ heißt wirklich keine Übungen
        await a.evaluate("QR_MODES.big.maxParts = 3")
        p2, note2 = await send(a, ids)
        check('gekürzt und ehrlich', len(p2) <= 3 and ('die letzten' in note2 or 'ohne Übungen' in note2), f'{len(p2)} Teile · {note2[:110]}')
        pay = await a.evaluate("ids => qrPayload(ids, false, 0)", ids)
        check('keep 0 = keine Übungen', all(v['n'] == 0 for v in pay['data']['log'].values()))
        await a.evaluate("QR_MODES.big.maxParts = 60")

        # 3. Älteres Format 1 (Übungen als Liste) wird weiter gelesen
        cc = await br.new_context(); c = await cc.new_page(); await c.goto(URL); await c.wait_for_timeout(400)
        await c.evaluate(RECV)
        await c.evaluate("""async () => { const obj = {app:'stufenweise', kind:'move', v:1, data:{profiles:[{id:'p-alt', name:'Alt', created:1, updated:1}], log:{'p-alt':[{ts:5, mode:'add', task:'1 + 1', ok:true}]}, matrix:{}, mhist:{}, skips:{}}};
          const z = await qrZip(new TextEncoder().encode(JSON.stringify(obj))), h = new Uint8Array(8 + z.bytes.length); h.set([83, 87, 1, 0, 7, 0, 1, z.flag]); h.set(z.bytes, 8); qrGot(h); }""")
        await c.wait_for_selector('#qr-take'); await c.click('#qr-take'); await c.wait_for_timeout(200)
        check('Format 1 lesbar', await c.evaluate("JSON.stringify(data.log['p-alt'])") == '[{"ts":5,"mode":"add","task":"1 + 1","ok":true}]')
        # 4. Neueres Format: Hinweis statt Fehler
        await c.evaluate(RECV); await c.evaluate("qrGot(new Uint8Array([83, 87, 3, 0, 1, 0, 1, 1, 0, 0]))")
        check('neueres Format: Hinweis', 'neuere Version' in await c.evaluate("document.querySelector('#qr-state').textContent"))

        # 5. Schalter in der Ansicht
        await a.evaluate("() => { settings.qrSmall = false; }")
        await send(a, ids); n1 = await a.evaluate("QRX.parts.length")
        await a.click('#qr-size'); await a.wait_for_function("document.querySelector('#qr-size') && document.querySelector('#qr-size').textContent.includes('Große')")
        n2 = await a.evaluate("QRX.parts.length")
        check('Schalter Kleine Codes', await a.evaluate("settings.qrSmall") is True and n2 > n1, f'{n1} → {n2}')
        await a.click('#qr-size'); await a.wait_for_timeout(300)
        check('Schalter zurück', await a.evaluate("settings.qrSmall") is False)
        await br.close()
    print('FERTIG', 'Fehler: ' + ', '.join(ERR) if ERR else 'alles ok')

asyncio.run(main())
