"""Wie heft_seiten_passen.py, aber mit dem Häkchen „Große Aufgaben“ im Heft-Assistenten (Backlog N, Stefan 26.11.2026):
Alle Seitenarten aller Stufen passen, große Aufgaben werden nie verkleinert; passt groß nicht einmal eine Aufgabe, wird die Seite normal groß."""
import os, runpy, pathlib
os.environ['HEFT_GROSS'] = '1'
runpy.run_path(str(pathlib.Path(__file__).with_name('heft_seiten_passen.py')), run_name='__main__')
