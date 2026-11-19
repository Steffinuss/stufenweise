# Backlog

Geplante Entwicklungsaufgaben für Stufenweise. Begonnenes steht in `IN_PROGRESS.md`, Erledigtes in `CHANGELOG.md`.

Regeln (Stand 17.11.2026): Der Funktionsumfang von `main` ist eingefroren, weil die App an Schulen genutzt wird. Neues entsteht nur im Zweig `entwicklung`, wird in der Testversion gezeigt und erst nach Stefans OK freigegeben (`docs/entwicklung.md`). Didaktische Entscheidungen trifft Stefan.

Stand: 19.11.2026

## Vorgeschlagene Reihenfolge

| Nr. | Aufgabe | Größe | Warum an dieser Stelle |
| --- | --- | --- | --- |
| 0 | Basis-Test abschließen (`IN_PROGRESS.md`) | klein | fertig gebaut, braucht nur Ausprobieren und Freigabe |
| 1 | **C** Basis: bessere Progression | mittel | betrifft dieselben Aufgabenarten wie der Basis-Test; besser jetzt klären, bevor viele Kinder mit dem Test eingestuft werden |
| 2 | ~~**B** Unterricht: Zahl im Zwanzigerfeld~~ | klein | erledigt 19.11.2026 (Testversion), siehe `CHANGELOG.md` |
| 3 | **A** Plus und Minus aufteilen | groß | größter Nutzen beim Üben, aber Umbau eines zentralen Mathe-Moduls; zuerst Konzept mit Stefan |

Alternative: B zuerst als schneller Gewinn, während Stefan den Basis-Test ausprobiert.

---

## A: Modul Plus und Minus aufteilen

**Status:** aufgenommen 19.11.2026 · nicht begonnen · Konzept nötig

**Ausgangslage:** Im Schülermodus bietet Plus/Minus zu viele Wahlmöglichkeiten: Zufallsaufgabe, eigene Aufgabe eingeben, Darstellung wählen (Zahlenstrahl, Material, Hundertertafel). Das kann Schüler*innen mit Förderschwerpunkt geistige Entwicklung überfordern.

**Wunsch:** zwei Bereiche.
- **A1 Rechenhilfe** (Arbeitsname, auch „Taschenrechner“ möglich): „Ich habe eine Aufgabe und brauche Unterstützung.“ Eigene Plus- und Minusaufgaben eingeben und mit Zahlenstrahl, Material oder Hundertertafel lösen.
- **A2 Üben:** „Ich möchte Plus und Minus trainieren und bekomme Aufgaben gestellt.“ Nur Zufallsaufgaben, keine eigene Eingabe. Die Darstellungen kommen nacheinander, ohne dass das Kind wählen muss: 1. Material, 2. Hundertertafel, 3. Zahlenstrahl.

**Heute im Code:** Plus/Minus läuft über `MODES` (`app.mode` `add`/`sub`). Die Ansicht wählt man mit `viewButtons()` (`data-view`): Material, Zahlenstrahl, Tafel (Hundertertafel, ab Zahlenraum 100; bei 1000 Tausenderbuch) und bis 20 Zehner-/Zwanzigerfeld. Knopf „Zufallsaufgabe“ und eigene Aufgaben (ins Feld tippen bzw. Zahlen eingeben) im selben Bildschirm; Einstellungen „Zufallsaufgaben (Plus und Minus)“. Die geführte Oberfläche und die Förderzonen R1–R6 führen ebenfalls dorthin.

**Vor der Umsetzung zu klären (Stefan):**
- Wann wechselt die Darstellung? Vorschlag: wie bei Basis nach einer Anzahl richtiger Aufgaben (z. B. 8), nach Fehlern zurück zur vorigen Darstellung.
- Reihenfolge je Zahlenraum: Die Hundertertafel gibt es erst ab dem Zahlenraum 100. Bis 20 also Material → Zwanzigerfeld → Zahlenstrahl? Bis 100 Material → Hundertertafel → Zahlenstrahl? Bis 1000 mit Tausenderbuch statt Hundertertafel?
- Folgt die Darstellung auch der Förderzone (z. B. R3 „über die 10“ zuerst am Zwanzigerfeld)?
- Wer sieht die Rechenhilfe: alle Kinder, nur auf Freigabe der Lehrkraft, oder nur im Unterrichtsmodus?
- Name und Symbol der beiden Bereiche in der Leiste; was passiert mit Lernständen und Statistik (Übungen bleiben unter „Plus“/„Minus“ gezählt?).
- Bleibt der heutige Bildschirm für Lehrkräfte erhalten (alle Wahlmöglichkeiten)?

**Risiko:** zentrales Modul, betrifft Startseite, geführte Oberfläche, „Heute für dich“, Förderzonen-Angebote, Arbeitsblatt-Verweise und viele Tests. Nur in `entwicklung`, mit vollständigem Testlauf.

---

## B: Unterricht – Zahlen im Zwanzigerfeld darstellen

**Status:** erledigt 19.11.2026 in `entwicklung` (Testversion), wartet auf Freigabe

**Ausgangslage:** Das Zwanzigerfeld (Unterricht, Tafelwerkzeug) wird vor allem mit Rechnungen genutzt.

**Wunsch:** Zahlen als eigener Lerngegenstand, unabhängig von einer Rechnung.
- Die Lehrkraft gibt eine Zahl vor, z. B. 14; sie erscheint als Material im Zwanzigerfeld.
- Die Zahl kann unabhängig von einer Rechnung ein- und ausgeblendet werden.
- Die Schüler*innen erkennen und benennen die Menge.
- Die bisherigen Funktionen bleiben erhalten.

**Heute im Code** (`app.tf`, `renderTfield`, Abschnitt „Zehner- und Zwanzigerfeld (Unterricht)“): Plättchen werden zeilenweise gelegt, auch mit Schnellknöpfen (`data-tfk`). Liegt nur eine Farbe, steht oben die Anzahl (z. B. „14“) – immer sichtbar. Der Schalter „Ergebnis verdecken“ (`app.tf.hide`, `?` zum Aufdecken) wirkt nur auf das Ergebnis einer Rechnung. Eine Zahl direkt eingeben kann man nicht.

**Umsetzungsidee (zur Abstimmung):** Eingabe „Zahl legen“ (Zifferntastatur), die das Feld neu füllt; Verdecken gilt auch für die Anzahl allein („?“ antippen zeigt sie). Optional: Zahl kurz zeigen und abdecken (wie Blitzblick). Kleine Änderung, keine neue Architektur.

---

## C: Basis – bessere Progression der Schwierigkeitsstufen

**Status:** aufgenommen 19.11.2026 · nicht begonnen · Konzept nötig

**Ausgangslage:** Die Stufen in Basis sollen systematischer aufeinander aufbauen. Heute steigt die Schwierigkeit innerhalb einer Aufgabenart vor allem über die Anzahl der Bilder (`st` 0–2: 2–3, dann mehr Bilder) und über den Wechsel zu einer anderen Aufgabenart.

**Wunsch:** zwei Dimensionen der Schwierigkeit.
1. **Quantitativ:** mehr Auswahl, mehr Elemente, größere Mengen.
2. **Qualitativ:** größere Ähnlichkeit, feinere Unterschiede, abstraktere Kategorien.

Möglichst dieselben Inhalte und Kategorien über mehrere Stufen, damit die Anforderung steigt und nicht der Lerngegenstand wechselt.

Beispiel „Was passt nicht?“:
- leicht: Hammer, Schraube, Mutter, Gabel (deutlich verschieden)
- mittel: Hammer, Schraubendreher, Schraubenschlüssel, Gabel (mehr Gemeinsamkeiten)
- schwer: verschiedene Hämmer, Schraubendreher, Schraubenschlüssel und ein Ding, das nicht passt (feine Unterschiede)

**Heute im Code:** 17 Alltagsgegenstände in `B_OBJ` (Gruppen `B_GRP`, z. B. Küche, Werkstatt), je in 4 Farben und beliebiger Größe; Aufgabenarten je Stufe in `AXES.V.arts` / `AXES.O.arts`, Schwierigkeit `st` 0–2. Es gibt keine Varianten eines Gegenstands (z. B. verschiedene Hämmer).

**Was es dafür braucht:**
- Ein Raster je Stufe: Zeilen = Ähnlichkeit (deutlich – ähnlich – fein), Spalten = Menge (wenige – mehr). Für jede Aufgabenart festlegen, welche Felder sinnvoll sind.
- Neue Bilder: Varianten innerhalb einer Art (Hammerarten, Schraubendreher, Schraubenschlüssel …) und vermutlich Ober- und Unterkategorien (Werkzeug → Schlagwerkzeug …). Das ist der größte Aufwand.
- Ähnlichkeit als Eigenschaft der Bilder (z. B. Gruppe, Untergruppe, Form), damit Generatoren gezielt „ähnlich“ oder „deutlich anders“ wählen können.

**Zusammenhang mit dem Basis-Test:** Der Test nutzt je Stufe eine leichte und eine schwerere Aufgabenart (`B_TEST`, `B_ST`). Ändert C die Aufgabenarten oder ihre Schwierigkeit, müssen Test, Lernstand-Texte und Arbeitsblätter nachgezogen werden. Mit Stefan klären, ob C vor oder nach der Freigabe des Basis-Tests kommt.

**Vor der Umsetzung zu klären (Stefan):** Welche Stufen zuerst (Vorschlag: V1 Gleiches, V2 Was passt nicht?, V3 Sortieren – dort wirkt Ähnlichkeit am stärksten)? Welche Gegenstände und Varianten? Soll „mittel“ eine eigene Aufgabenart werden oder eine weitere Schwierigkeit `st` innerhalb der Art? Gilt die neue Progression auch für die Arbeitsblätter?
