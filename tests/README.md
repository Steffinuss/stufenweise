# Tests für Stufenweise

Automatische Tests, die die App in einem echten Chrome-Browser bedienen (mit [Playwright](https://playwright.dev/python/)). Sie klicken die Bereiche durch, prüfen auf JavaScript-Fehler, lassen simulierte Kinder üben und erzeugen Arbeitsblätter als PDF. Bildschirmfotos und PDFs landen in `tests/out/` (nicht im Repository).

## Voraussetzungen

- Python 3 mit `pip install playwright pillow`
- Chrome oder Chromium (sonst `playwright install chromium`)
- für die PDF-Prüfung der Legeblätter: `pdfinfo` und `pdftoppm` (Paket poppler-utils)

## Alles auf einmal

```sh
sh tests/run_all.sh        # schnelle Tests, etwa 10 Minuten
sh tests/run_all.sh lang   # dazu alle Arbeitsblätter, simulierte Kinder, Zufallsklicks (etwa 25 Minuten)
```

Das Skript startet selbst einen Webserver auf Port 8766. „ok“ heißt: keine JavaScript-Fehler und kein Absturz. Viele Tests geben zusätzlich Messwerte aus; die stehen in der Beschreibung unten.

## Einzelne Tests

Zuerst den Server starten: `python3 -m http.server 8766` im Repository-Ordner. Dann zum Beispiel `python3 tests/legeblaetter.py`.

| Test | Prüft |
| --- | --- |
| `fehler.py` | App lädt ohne JavaScript-Fehler |
| `smoke.py` | Startseite, PIN, Einstellungen, Schreiben: einmal durchklicken |
| `sweep.py` | alle Aufgabentypen aller Stufen erzeugen und darstellen (über 4.500) |
| `kinder_sim.py` (mit `simlib.py`) | 10 simulierte Kinder machen Tests und üben; Förderzonen plausibel |
| `zufallsklicks.py` | viele zufällige Klicks, die App darf nicht abstürzen |
| `arbeitsblaetter.py` | jedes Arbeitsblatt-Thema: passt auf die Seite, genug Aufgaben (`PRÜFEN` = ansehen) |
| `arbeitsblatt_optionen.py` | Materialbilder „1. Aufgabe vorgegeben, dann selbst zeichnen“, Zehnerpartner, Rechnen über die 10 (Beispiel ausgefüllt), Geld mit Cent, Einmaleins-Reihen |
| `basis_grundlagen.py` | Basis, Schritt 1: alle Bilder (Gegenstände, Farben, Größen, Formen, Pfeile, Spiegel-Zeichen, Punktbilder, Symbole) und vollständige Stufentexte V1–V8, O1–O5 |
| `basis_blaetter.py` | Basis, Schritt 2: alle Basis-Arbeitsblätter (V1–V7, O2–O4) in allen Varianten, Lösungen passend, Vorgemachtes nur in der ersten Aufgabe jeder Art, Schwarz-Weiß mit Mustern; Legeblätter Sortierunterlage, Zuordnungsleiste, Musterstreifen |
| `basis_ueben.py` | Basis, Schritt 3: alle Übungs-Generatoren V1–V8, O2–O4 (Lösung richtig, falsche Antwort falsch), jede Aufgabenart mit echten Klicks gelöst (Bild wählen, Sortieren, Verbinden, Reihenfolge, kurz zeigen), Fach für Gast sichtbar, für Kinder erst nach Einschalten, Statistik; Ablauf: Vormachen vor jeder neuen Aufgabenart, bei einer Art bleiben, nach 8 richtigen „Nächste Aufgabe“, nach 3 Fehlern leichter; Ziehen mit der Maus (in die Kiste, zurück in den Vorrat, unter das Bild, auf die Plätze 1, 2, 3) |
| `basis_test.py` | Basis-Test (Schritt 4): drei Teile (V1–V4, V5–V8, O2–O4), je Stufe Block a mit Vormachen (nicht gewertet, nichts antippbar), Block b nur nach a; Einstufung erreicht / teilweise / nicht, keine Ableitung; Förderzone in empfohlener Reihenfolge, ILEB, Lernstand mit Matrix und Hinweis bei Mathe I / L1, Elterninfo, Lernlandkarte, automatische Sichtbarkeit, „Heute für dich“ mit Basis zuerst, Re-Diagnose, Kurztest, Abbrechen |
| `blatt_auswahl.py` | Arbeitsblätter: Auswahl Fach → Bereich → Blatt, jedes Blatt genau einmal, Legeblätter beim Fach, zuletzt gewähltes Blatt beim Zurückwechseln, „Zuletzt benutzt“, Kind mit Förderzone stellt das Fach ein, Arbeitsheft über Fächer |
| `drittes_fach.py` | Mehr als zwei Fächer: ein Probe-Fach wird angemeldet und erscheint in Fachwahl, Startseite, Üben, Test, Lernstand, Klassenübersicht und Berichten; optional nur für eingeschaltete Kinder |
| `handy.py` | Handy hochkant: Startseite, Leiste, Aufgaben ohne Überlappung, Zifferntastatur unten; quer Hinweis zum Drehen; iPad unverändert |
| `test_passt.py` | Jede Testaufgabe passt auf kleinere iPads (1080 × 740 und Hochformat); nur lange Lesetexte scrollen mit Hinweis |
| `test_nie_haengen.py` | Jede Stufe hat mindestens 3 Aufgaben; Test läuft auch bei vielen falschen Antworten durch |
| `test_fortschritt.py` | Fortschritt im Test: Abschnitte in fester Reihenfolge, Balken läuft nur vorwärts, keine Bewertung |
| `oberflaeche_details.py` | Fachwahl Mathe/Deutsch mittig; Lineal-Gegenstände mit realistischen Längen |
| `durchsicht_0_21.py` | Randfälle: kaputte gemerkte Blatt-Einstellungen, geführte Oberfläche mit Zehnerpartnern, Ableitung aus R3, Klassenübersicht, Wiederholungstest |
| `zehnerpartner_ueben.py` | Üben „Zehnerpartner“ Z1–Z3 lösbar, Statistik; Blitzblick „Neue Aufgabe“ zählt als übersprungen |
| `grosse_aufgaben.py` | „Große Aufgaben“: nichts zu breit, alles größer; Minus „Umtausch schon im Bild zeigen“: Bild stimmt, Tausch reicht zum Wegstreichen |
| `doppelte_zeilen.py` | keine Zeile doppelt in einer Aufgabe (z. B. zweimal „7 = 4 + □“), keine gleichen Aufgaben direkt nacheinander |
| `legeblaetter.py` | alle Legeblätter als PDF: genau 1 Seite, nichts abgeschnitten (`scroll` ≤ verfügbare Höhe) |
| `arbeitsheft.py` | Arbeitsheft mit mehreren Blättern |
| `heft_assistent.py` | Arbeitshefte (Backlog J): Fach, 12/24/36/48 Seiten (gedruckt genau so viele), Vorgriff, Kapitel mit Einstieg/Üben/„Das kann ich schon“, Wiederholung, Hilfen, Lösungsheft, Mathe-Feinstufen, Fortsetzungsgeschichte, neue Deutsch-Formate, Broschürendruck |
| `heft_seiten_passen.py` | (lang) Arbeitsheft: für jede Stufe Einstieg, Üben, „Das kann ich schon“ und Wiederholung bauen – keine Seite läuft über, gedruckt genau so viele Blätter, A5-Broschüre ohne abgeschnittene Seiten |
| `plaene_sinnvoll.py` | Erzeugte Inhalte ergeben Sinn: Stundenplan je Stufe (Fächer nach BP GENT, kein Fach jeden Tag in derselben Stunde), „Stimmt das?“-Sätze eindeutig, Stehendes nicht unter dem Tisch |
| `tausenderbuch_nachspuren.py` | Tausenderbuch-Seiten wählen, ganzes Buch, Nachspur-Buchstaben |
| `einstellungen.py` | Einstellungen mit Registerkarten |
| `runden.py`, `ueberspringen.py` | Übungsrunden; Überspringen zählt mit |
| `gefuehrt.py` | geführte Oberfläche zeigt die richtigen Bereiche |
| `antwortfeld.py`, `feld_ueben.py` | Antwortfeld in der Rechnung, Zwanzigerfeld beim Üben |
| `zwanzigerfeld.py BREITE HÖHE` | Tafelwerkzeug Zwanzigerfeld (Legen, Wegstreichen, Verdecken) |
| `springen.py` | nichts springt: Zwanzigerfeld bleibt beim ersten Tippen an seiner Stelle |
| `hinweis_neu.py` | „Richtig“ verschwindet bei der nächsten Aufgabe |
| `lernort_material.py` | Weg am Material für jede Stufe, Legeblatt-Knopf, ILEB-Maßnahmen |
| `materialkiste.py` | Materialkiste: Ablauf, alle Werkzeuge, Zählen, Taschenrechner, Lernstand/ILEB |
| `mehrere_fenster.py` | Zwei Fenster derselben App: nichts geht verloren, Löschen gilt weiter |
| `wochenuebersicht.py`, `update_hinweis.py` | Wochenübersicht; Update-Hinweis nur auf der Startseite |
| `shot.py BILD.png "js" "CLICK selektor" …` | Hilfsprogramm: Schritte ausführen und Bildschirmfoto speichern |

## Bilder für die Anleitung

```sh
python3 tests/anleitung_bilder.py                     # nimmt alle Bilder neu auf (Querformat 1180 × 820, „Testkind A“)
python3 tests/anleitung_markieren.py                  # umrandet den wichtigen Knopf orange
python3 tests/anleitung_markieren.py --uebernehmen    # kopiert die Bilder nach docs/bilder
```

Vorher die Bilder in `tests/out/anleitung/final/` ansehen. Ändert sich die Oberfläche stark, müssen die Klickschritte in `anleitung_bilder.py` angepasst werden.
