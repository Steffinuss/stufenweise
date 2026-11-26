"""Raten im Test begrenzen (Backlog Q1, Prüfung vom 22.11.2026, Stefan 26.11.2026):
Sind die ersten beiden Aufgaben einer Stufe Auswahlaufgaben, gilt sie erst bei 3 von 3 als erreicht
(nach 2 von 2 kommt eine dritte Aufgabe, 2 von 3 = teilweise). Andere Stufen und der Basis-Test bleiben, wie sie sind.
Simulation: Ein Kind, das nur rät, durchläuft den ganzen Test. Vorher stand im Lese-Test in etwa 69 % der Tests
mindestens eine Stufe auf „erreicht“ (im Mittel 2 Stufen), im Mathe-Test Teil 2 in etwa 49 %."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

SIM = r"""
([subj, N]) => {
  const pOf = it => it.type === 'choice' ? 1/it.options.length : it.type === 'pick' ? (it.single ? 1/it.cells.length : 0) : it.type === 'pairs' ? Math.pow(.5, it.pairs.length) : 0;
  const ev = evalItem, rd = renderDiag; evalItem = it => ({ok: Math.random() < pOf(it), given:'?', obs:[]}); renderDiag = () => {};
  let any = 0, sum = 0;
  try {
    for(let t = 0; t < N; t++){
      const id = newId('p-'); data.profiles.push({id, name:'R' + t, created:1, updated:1, world:'HS'}); data.current = id;
      diagStart(subj); const d = app.diag; let g = 0;
      while(app.diag && !d.done && g++ < 300){ if(d.items[d.idx]?.demo){ d.idx++; continue; } diagAnswer(false); }
      const m = matrixOf(id), n = Object.keys(m).filter(k => isOk(m[k].status)).length; if(n) any++; sum += n;
      data.profiles = data.profiles.filter(p => p.id !== id); delete data.matrix[id]; delete data.mhist?.[id]; delete data.log[id];
    }
  } finally { evalItem = ev; renderDiag = rd; }
  return [any/N, sum/N];
}"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page()
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.add_init_script("Storage.prototype.setItem = function(){}")   # Simulation: nichts speichern
        await pg.goto(URL); await pg.wait_for_timeout(500)

        # Regel
        r = await pg.evaluate("""() => { const A = (...xs) => xs.map(([ok, ch, kern]) => ({ok, ...(ch ? {ch:true} : {}), kern:!!kern}));
          return {
            ch22: cellDecision(A([1, 1, 1], [1, 1])), ch12: cellDecision(A([1, 1, 1], [0, 1])), ch02: cellDecision(A([0, 1, 1], [0, 1])),
            ch33: cellDecision(A([1, 1, 1], [1, 1], [1, 1])), ch23: cellDecision(A([1, 1, 1], [0, 1], [1, 1])), ch23k: cellDecision(A([1, 1, 1], [1, 1], [0, 1])),
            ch13: cellDecision(A([1, 1, 1], [0, 1], [0, 1])), ch3n: cellDecision(A([1, 1, 1], [1, 1], [1, 0])), chk0: cellDecision(A([0, 1, 1], [1, 1], [1, 1])),
            in22: cellDecision(A([1, 0, 1], [1, 0])), in23: cellDecision(A([1, 0, 1], [0, 0], [1, 0])), mix23: cellDecision(A([1, 1, 1], [0, 0], [1, 1])) }; }""")
        exp = {'ch22': None, 'ch12': None, 'ch02': 'nicht', 'ch33': 'erreicht', 'ch23': 'teilweise', 'ch23k': 'teilweise', 'ch13': 'teilweise',
               'ch3n': 'erreicht', 'chk0': 'teilweise', 'in22': 'erreicht', 'in23': 'erreicht', 'mix23': 'erreicht'}
        bad = {k: (r[k], v) for k, v in exp.items() if r[k] != v}
        check('Regel: Auswahl 3 von 3, sonst wie bisher', not bad, str(bad))

        # echter Ablauf: Lese-Stufe mit 2 richtigen Antworten verlangt eine dritte
        r = await pg.evaluate("""() => { const id = newId('p-'); data.profiles.push({id, name:'K', created:1, updated:1, world:'HS'}); data.current = id;
          const ev = evalItem; evalItem = () => ({ok:true, given:'', obs:[]});
          try { diagStart('L'); const d = app.diag, key = d.key; diagAnswer(false); diagAnswer(false);
            const after2 = d.key === key && d.answers.length === 2; diagAnswer(false);
            return {key, after2, st: matrixOf(id)[key]?.status, sum: matrixOf(id)[key]?.sum}; } finally { evalItem = ev; } }""")
        check('Lesen: nach 2 von 2 eine dritte Aufgabe, dann erreicht', r['after2'] and r['st'] == 'erreicht' and r['sum'] == '3 von 3 richtig', str(r))

        # Simulation: Kind rät nur
        for subj, lim, lim_mean in [('L', .35, .8), ('M2', .32, .6)]:
            any_, mean = await pg.evaluate(SIM, [subj, 300])
            check(f'{subj}: Raten führt selten zu „erreicht“', any_ <= lim and mean <= lim_mean, f'{any_*100:.0f} % der Tests, im Mittel {mean:.2f} Stufen')
        any_, mean = await pg.evaluate(SIM, ['B2', 300])
        check('Basis Teil 2 unverändert (Blöcke a und b)', any_ <= .32, f'{any_*100:.0f} %')
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
