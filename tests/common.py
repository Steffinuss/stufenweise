"""Gemeinsame Einstellungen für die Testprogramme.

Umgebungsvariablen (alle optional):
  STUFENWEISE_URL   Adresse der App (Standard: http://localhost:8766/index.html)
  STUFENWEISE_OUT   Ordner für Bildschirmfotos und PDFs (Standard: tests/out)
  CHROME            Pfad zu Chrome/Chromium; sonst wird ein vorhandenes Chrome gesucht
"""
import os, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = os.environ.get('STUFENWEISE_URL', 'http://localhost:8766/index.html')
OUT = pathlib.Path(os.environ.get('STUFENWEISE_OUT', ROOT / 'tests' / 'out'))
for sub in ('', 'lege', 'sheets', 'anleitung/final'):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
os.chdir(OUT)  # alle Programme schreiben ihre Bilder relativ hierher


def _chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    for c in ('/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
              '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
        if os.path.exists(c):
            return c
    return shutil.which('google-chrome') or shutil.which('chromium')


async def launch(p, **kw):
    """Startet Chrome über Playwright: erst ein vorhandenes Chrome, sonst den Browser von Playwright."""
    exe = _chrome()
    if exe:
        try:
            return await p.chromium.launch(executable_path=exe, **kw)
        except Exception:
            pass
    return await p.chromium.launch(**kw)


# Konzentrationsmodus (seit Backlog H Standard „an“) für Tests ausschalten, die die volle Oberfläche
# mit Leiste und Einstellleiste bedienen. Vor pg.goto(URL) mit pg.add_init_script(FOKUS_AUS) setzen.
FOKUS_AUS = ("try{const k='stufenweise.settings',s=JSON.parse(localStorage.getItem(k)||'{}');"
             "if(!s.fokus){s.fokus='off';localStorage.setItem(k,JSON.stringify(s))}}catch(e){}")
