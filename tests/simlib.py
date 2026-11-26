import asyncio, json, sys
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
ZRS=[10,20,100,1000]; NL=['I','II','III','IV','V']
def math_skill(maxlvl_by_zr, smax, umax=2, rmax=0):
    def f(key):
        p=key.split('|')
        if p[0]=='R': return int(p[1][1]) <= rmax
        if p[0]=='G': return False
        if p[0]=='U': return int(p[1][1]) <= umax
        if p[0]=='M': return NL.index(p[2]) < maxlvl_by_zr.get(int(p[1]),0)
        if p[0]=='S': return int(p[1][1]) <= smax
    return f
def read_skill(lmax, pmax):
    def f(key):
        p=key.split('|')
        return int(p[1][1]) <= (lmax if p[0]=='L' else pmax)
    return f
KIDS = {
 'Ben': ('M', math_skill({10:5,20:5,100:2,1000:0},1,2,3)),
 'Mia': ('M', math_skill({10:1,20:0,100:0,1000:0},0)),
 'Kai': ('M', math_skill({10:5,20:5,100:5,1000:5},4,6,7)),
 'Ida': ('M', math_skill({10:5,20:3,100:0,1000:0},0,2,2)),
 'Leo': ('L', read_skill(4,2)),
 'Ela': ('L', read_skill(1,0)),
 'Tim': ('L', read_skill(7,4)),
 'Wil': ('W', lambda k: int(k.split('|')[1][1])<=3),
 'Wen': ('W', lambda k: int(k.split('|')[1][1])<=0),
 'Wan': ('W', lambda k: True),
}
async def answer(pg, correct):
    it = await pg.evaluate("(()=>{const d=app.diag,it=d.items[d.idx];return {type:it.type,fields:it.fields||null,correct:it.correct??null,nopt:it.options?it.options.length:0,target:it.target??null,pairs:it.pairs||null,label:it.label,zr:it.zr||null}})()")
    t = it['type']
    if t=='flash':
        await pg.wait_for_timeout(4300)
    if t in ('input','flash','scatter','seq'):
        vals = it['fields'] if correct else [f+1 for f in it['fields']]
        ins = pg.locator('#stage .dg-in, #controls .dg-in')
        n = await ins.count(); assert n==len(vals), (n, vals, it)
        # seit 0.35.1 sind Ziffernfelder bei offener Zifferntastatur readOnly → Wert per JS setzen (wie in antwortfeld.py)
        for i,v in enumerate(vals): await ins.nth(i).evaluate("(e,v)=>{e.focus(); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true}))}", str(v))
        await ins.nth(n-1).press('Enter')
    elif t=='clockset':
        await pg.evaluate("(c)=>{const it=app.diag.items[app.diag.idx];app.diag.resp={h:c?it.target.h:(it.target.h+3)%12,m:it.target.m,moved:true}}", correct); await pg.click('#d-next')
    elif t=='write':
        await pg.evaluate("(c)=>{const it=app.diag.items[app.diag.idx];app.diag.resp={text:c?it.target:(it.max?'x':'Qxq'),used:[]}}", correct); await pg.click('#d-next')
    elif t=='sent':
        await pg.evaluate("(c)=>{const it=app.diag.items[app.diag.idx];const o=it.words.map((_,i)=>i); if(!c) o.reverse(); app.diag.resp={order:o}}", correct); await pg.click('#d-next')
    elif t=='choice':
        idx = it['correct'] if correct else (it['correct']+1)%it['nopt']
        await pg.click(f'[data-dgc="{idx}"]'); await pg.click('#d-next')
    elif t=='pairs':
        for i,p in enumerate(it['pairs']):
            j = p.index(max(p)) if correct else p.index(min(p))
            await pg.click(f'[data-dgp="{i},{j}"]')
        await pg.click('#d-next')
    elif t=='line':
        v = it['target'] if correct else (it['target']+it['zr']*0.4)%it['zr']
        await pg.evaluate(f"app.diag.resp={{guess:{int(v)}}}"); await pg.click('#d-next')
    elif t=='money':
        await pg.evaluate("(c)=>{const it=app.diag.items[app.diag.idx];let r=it.target,out=[];for(const d of it.denoms){while(r>=d){out.push(d);r-=d;}} if(!c) out.push(it.denoms[it.denoms.length-1]); app.diag.resp={items:out}}", correct); await pg.click('#d-next')
    elif t=='build':
        await pg.evaluate("(c)=>{const it=app.diag.items[app.diag.idx]; const ok=(Z,E)=>it.exact?(Z===it.exact[0]&&E===it.exact[1]):Z*10+E===it.target; let m=[0,0]; outer: for(let z=0;z<=10;z++)for(let e=0;e<=30;e++){ if(ok(z,e)===c){m=[z,e];break outer;} } app.diag.resp={mat:m}}", correct); await pg.click('#d-next')
    return it
