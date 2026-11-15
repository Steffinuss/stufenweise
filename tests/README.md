# Tests für Stufenweise

Automatische Tests, die die App in einem echten Chrome-Browser bedienen (mit [Playwright](https://playwright.dev/python/)). Sie klicken die Bereiche durch, prüfen auf JavaScript-Fehler, lassen simulierte Kinder üben und erzeugen Arbeitsblätter als PDF. Bildschirmfotos und PDFs landen in `tests/out/` (nicht im Repository).

## Voraussetzungen

- Python 3 mit `pip install playwright pillow`
- Chrome oder Chromium (sonst `playwright install chromium`)
- für die PDF-Prüfung der Legeblätter: `pdfinfo` und `pdftoppm` (Paket poppler-utils)

## Alles auf einmal

```sh
sh tests/run_all.sh        # schnelle Tests, etwa 3 Minuten
sh tests/run_all.sh lang   # dazu alle Arbeitsblätter, simulierte Kinder, Zufallsklicks (etwa 15 Minuten)
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
| `grosse_aufgaben.py` | „Große Aufgaben“: nichts zu breit, alles größer; Minus „Umtausch schon im Bild zeigen“: Bild stimmt, Tausch reicht zum Wegstreichen |
| `doppelte_zeilen.py` | keine Zeile doppelt in einer Aufgabe (z. B. zweimal „7 = 4 + □“), keine gleichen Aufgaben direkt nacheinander |
| `legeblaetter.py` | alle Legeblätter als PDF: genau 1 Seite, nichts abgeschnitten (`scroll` ≤ verfügbare Höhe) |
| `arbeitsheft.py` | Arbeitsheft mit mehreren Blättern |
| `tausenderbuch_nachspuren.py` | Tausenderbuch-Seiten wählen, ganzes Buch, Nachspur-Buchstaben |
| `einstellungen.py` | Einstellungen mit Registerkarten |
| `runden.py`, `ueberspringen.py` | Übungsrunden; Überspringen zählt mit |
| `gefuehrt.py` | geführte Oberfläche zeigt die richtigen Bereiche |
| `antwortfeld.py`, `feld_ueben.py` | Antwortfeld in der Rechnung, Zwanzigerfeld beim Üben |
| `zwanzigerfeld.py BREITE HÖHE` | Tafelwerkzeug Zwanzigerfeld (Legen, Wegstreichen, Verdecken) |
| `springen.py` | nichts springt: Zwanzigerfeld bleibt beim ersten Tippen an seiner Stelle |
| `hinweis_neu.py` | „Richtig“ verschwindet bei der nächsten Aufgabe |
| `lernort_material.py` | Weg am Material für jede Stufe, Legeblatt-Knopf, ILEB-Maßnahmen |
| `wochenuebersicht.py`, `update_hinweis.py` | Wochenübersicht; Update-Hinweis nur auf der Startseite |
| `shot.py BILD.png "js" "CLICK selektor" …` | Hilfsprogramm: Schritte ausführen und Bildschirmfoto speichern |

## Bilder für die Anleitung

```sh
python3 tests/anleitung_bilder.py                     # nimmt alle Bilder neu auf (Querformat 1180 × 820, „Testkind A“)
python3 tests/anleitung_markieren.py                  # umrandet den wichtigen Knopf orange
python3 tests/anleitung_markieren.py --uebernehmen    # kopiert die Bilder nach docs/bilder
```

Vorher die Bilder in `tests/out/anleitung/final/` ansehen. Ändert sich die Oberfläche stark, müssen die Klickschritte in `anleitung_bilder.py` angepasst werden.
