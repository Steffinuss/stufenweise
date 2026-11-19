# In Arbeit

Was gerade begonnen ist. Erledigtes wandert nach `CHANGELOG.md`, Geplantes steht in `BACKLOG.md`.
Arbeitsweise mit zwei Zweigen: `docs/entwicklung.md`.

Stand: 19.11.2026

## Basis-Test (Basis, Schritt 4)

| | |
| --- | --- |
| Zweig | `entwicklung`, Commit 329ab57 (gepusht) |
| Testversion | steffinuss.github.io/stufenweise-test (Commit ceba845 im Repository `stufenweise-test`) |
| Tests | `tests/basis_test.py` neu; `sh tests/run_all.sh lang` am 17.11.2026 komplett grün (38 Tests) |
| Anleitung | `docs/anleitung.md` (Abschnitt „Basis-Test“), `docs/neues-fach.md` (neue Test-Haken) |
| Status | **fertig gebaut, wartet auf Ausprobieren durch Stefan** |

Umgesetzt:
- Drei kurze Teile (Entscheidung Stefan, 17.11.2026): Teil 1 V1–V4, Teil 2 V5–V8, Teil 3 O2–O4.
- Je Stufe Block a (leicht), nur wenn a klappt Block b (schwerer). Jeder Block: einmal vormachen (nicht gewertet, nichts antippbar), dann 2–3 Aufgaben derselben Art. Ergebnis: a und b → erreicht, nur a → teilweise, a nicht → nicht erreicht.
- Kompetenzmatrix mit zwei Bereichszeilen (keine Treppe, nichts abgeleitet), Förderzone in der empfohlenen Reihenfolge, ILEB-Sätze, Elterninfo, Lernlandkarte, Kurztest, Re-Diagnose.
- Hinweis im Lernstand, wenn Mathe „Zahlen bis 10, Stufe I“ oder Lesen L1 nicht erreicht ist; Basis wird bei offener Förderzone automatisch sichtbar.
- Texte V3 und V6 an das angepasst, was der Test prüft (V3: Farbe bei gleichen bzw. verschiedenen Dingen; V6 b: vier Dinge ordnen).

Noch offen, bevor der Basis-Test freigegeben wird:
1. Stefan probiert den Test in der Testversion aus (am besten am Schul-iPad) und sieht sich die geänderten Texte V3/V6 an.
2. Rückmeldung einarbeiten, `sh tests/run_all.sh lang`, Testversion aktualisieren.
3. Nach Stefans OK: `entwicklung` in `main` zusammenführen, Version 0.29.0, `CHANGELOG.md` ergänzen, Release anlegen (Stefan, GitHub-Oberfläche).
4. Bildschirmfotos der Anleitung erneuern (dafür zuerst `tests/anleitung_bilder.py` reparieren, bricht seit 0.24.0 ab).

Achtung: Backlog-Punkt C (Progression in Basis) betrifft dieselben Aufgabenarten, auf denen der Test aufbaut. Siehe `BACKLOG.md`.
