# Ein neues Fach anlegen

Seit Version 0.26.0 baut Stufenweise alle Oberflächen aus zentralen Listen. Ein weiteres Fach (zum Beispiel „Basis“ oder Sachthemen) ist deshalb vor allem neuer Inhalt.

Alles steht in `index.html` im Abschnitt **„Fächer und Tests: zentrale Listen“**. Ein Beispiel, das alle Teile zeigt, ist der Test `tests/drittes_fach.py`: Er meldet ein Probe-Fach an und prüft, dass es überall erscheint.

## Die drei Listen

| Liste | Was hinein gehört | Anmelden mit |
| --- | --- | --- |
| `SUBJECTS` | ein Fach: Name, Bild, Leiste, Kacheln auf der Startseite, Einstieg | `addSubject(id, {...})` |
| `TESTS` | ein Test eines Fachs: Name, Achsen der Kompetenzmatrix, Testplan, Lernstand-Texte | `addTest(id, {...})` |
| `AXES` | eine neue Achse der Kompetenzmatrix: Stufen, Beschreibungen, Aufgaben | `AXES.X = {...}` |

Ein Schlüssel der Kompetenzmatrix sieht so aus: `Achse|Stufe`, zum Beispiel `V|V3`. Der erste Buchstabe ist die Achse. Er sagt, zu welchem Test und welchem Fach der Schlüssel gehört.

## Fach (`addSubject`)

- `name`, `long`: kurzer Name für die Fachwahl oben, langer Name für Berichte.
- `tests`: wird von `addTest` gefüllt.
- `guideAxes`: Achsen, nach deren Test die geführte Oberfläche greift.
- `ill()`: Bild für die Startseite (SVG, 120 × 70).
- `rail(g, lvOk)`: Knöpfe der Leiste links.
- `areas(g, lvOk)`: Kacheln auf der Startseite („Was möchtest du üben?“).
- `enter()`: was beim Wechsel ins Fach passiert (z. B. erste Übung öffnen).
- `axes`: Achsen des Fachs, solange es noch keinen Test hat (sonst kommen sie aus den Tests).
- `optional: true`: Kinder sehen das Fach nur, wenn es für sie eingeschaltet ist (`p.subjOn[id]`) oder ein Test des Fachs eine Förderzone zeigt. Ohne gewähltes Kind und in der Lehrkraft-Ansicht ist es immer sichtbar.

## Test (`addTest`)

- `subj`, `name`, `long`, `axes`, `cap` (höchstens so viele Aufgaben).
- `plan(d)`, `rePlan(d)`: Generatoren, die nacheinander Matrix-Schlüssel liefern (wie `mathPlan`).
- `title(d)`: Überschrift im Test. Mehrere Teile: `diagStart('X1')` startet Teil 1 (`d.part = 1`).
- `sections(d)`: Abschnitte für den Fortschrittsbalken (sonst nur der Testname).
- `keys()`: alle Schlüssel in Anzeige-Reihenfolge (Tabelle, Bericht).
- `zoneCells(m, first)`: Förderzonen aus der Matrix.
- `kann(m)`: „kann …“-Sätze für den ILEB-Vorschlag; `start`: Satz, wenn noch nichts erreicht ist.
- `matrix(m)`, `mxTable(m, sym)`: Kompetenzmatrix im Lernstand und im gedruckten Bericht.
- `infer(m, put, line)`: welche Stufen sich aus höheren ableiten lassen.
- `log(e)`: welche Übungen zum Test zählen („seit dem letzten Test …“).
- `buttons()`: eigene Start-Knöpfe im Lernstand (sonst einer).
- `secName(k)`: Name des Abschnitts im Fortschrittsbalken für einen Schlüssel.

Weitere Haken (seit dem Basis-Test, alle freiwillig):

- `cellItems(d, key)`: Aufgaben einer Zelle (sonst je ein Generator aus `itemsFor`). Aufgaben mit `demo:true` werden im Test vorgemacht und nicht gewertet; „Jetzt du“ geht zur nächsten Aufgabe.
- `decide(d)`: Einstufung der Zelle nach jeder Antwort (sonst `cellDecision`). Gibt `'erreicht'`, `'teilweise'`, `'nicht'` oder `null` (weiter) zurück und darf `d.items` hinter `d.idx` ergänzen, zum Beispiel einen zweiten Block. Antworten tragen `blk` der Aufgabe.
- `ziel(z)`, `why(z)`: eigener Zielsatz bzw. Zusatz zur Begründung einer Förderzone; `noTeil: true` lässt „Teilweise gelingt …“ im ILEB weg.
- `intro` (HTML) und `doneNote(d)`: zusätzlicher Text vor und nach dem Test.

Beispiel: `TESTS.B` (Basis-Test) in `index.html` mit drei Teilen, Blöcken a und b und `tests/basis_test.py`.

## Achse (`AXES`)

- `place`: Name des Bereichs („Vergleichen und Ordnen“).
- `levels`: Stufen, z. B. `['V1', 'V2']`.
- `info[Stufe]`: `name`, `short`, `kann`, `ziel`, `bp` (Bezug zum Bildungsplan), `analog` (Ideen für zu Hause), `ich` (Satz für die Lernlandkarte), `offer` (`{text, set:{mode:'read', lvl}}`).
- `items[Stufe]`: Liste von Aufgaben-Generatoren (mindestens 3 je Stufe; siehe `tests/test_nie_haengen.py`).
- `mode`: Name im Übungsprotokoll.

Für Aufgaben mit Bildern gibt es seit 0.28.0 die Typen `pick` (ein oder alle passenden Bilder antippen), `sort` (Ding, dann Kiste), `match` (oben, unten verbinden; optional mit „Reicht es? ja/nein“), `order` (der Reihe nach antippen) und `glance` (kurz zeigen, dann wählen). Beispiele: `AXES.V.items` in `index.html`.

Arbeitsblätter eines neuen Fachs kommen in `SHEET_SETS[Kürzel]` und `SHEET_INFO[Kürzel]`. Den Weg am Material trägt man in `MAT_WAY` ein.

## Prüfen

1. `sh tests/run_all.sh lang` muss grün bleiben.
2. Einen eigenen Test nach dem Vorbild von `tests/drittes_fach.py` anlegen.
3. Bestehende Lernstände und Datensicherungen dürfen sich nicht ändern.
