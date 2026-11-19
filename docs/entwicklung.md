# Wie an Stufenweise weitergearbeitet wird

Seit dem 17.11.2026 ist der Funktionsumfang eingefroren: Die App wird an Schulen genutzt. Damit Neues die Nutzer*innen nicht stört, gibt es zwei Zweige.

| Zweig | Wofür | Wo zu sehen |
| --- | --- | --- |
| `main` | Stand für alle. Nur Fehlerbehebungen (0.28.6, 0.28.7 …). | steffinuss.github.io/stufenweise |
| `entwicklung` | Neue Funktionen (Basis-Test, Lage im Raum, Sachunterricht …). | steffinuss.github.io/stufenweise-test (Testversion) |

## Abläufe

- **Fehler beheben:** in `main` ändern, testen, Version erhöhen, veröffentlichen. Danach `main` in `entwicklung` zusammenführen, damit beide Zweige gleich bleiben.
- **Neue Funktion:** in `entwicklung` bauen und testen. Dann denselben Stand in das Repository `stufenweise-test` übertragen: `sh tests/testversion.sh /pfad/zu/stufenweise-test`, danach dort committen und pushen. Das Skript ersetzt alle Dateien durch den Stand von `entwicklung`; die Geschichte bleibt im Haupt-Repository. Im Test-Repository wird nie direkt gearbeitet; es ist nur das Schaufenster.
- **Freigabe:** Wenn Stefan die Testversion ausprobiert hat und einverstanden ist, wird `entwicklung` in `main` zusammengeführt. Das ist die nächste Nebenversion (z. B. 0.29.0). Freigegebene Stände bekommen in GitHub ein Release (`v0.29.0`).
- **Mitarbeit von außen** (z. B. Sachunterricht): eigener Zweig oder Fork, Änderungen als Pull Request an `entwicklung`.

## Testversion und Daten

Beide Versionen laufen unter derselben Adresse `steffinuss.github.io` und teilen sich damit den Speicher des Browsers. Die Testversion erkennt ihren Pfad (`/stufenweise-test/`) und setzt vor alle gespeicherten Schlüssel `test:`. So berührt sie die Daten der richtigen App nie. Oben steht in Rot „Testversion – nicht für den Unterricht“.

## Planung und Stand

- `BACKLOG.md`: geplante Aufgaben mit Status, offenen Fragen und vorgeschlagener Reihenfolge
- `IN_PROGRESS.md`: was gerade begonnen ist und was bis zur Freigabe noch fehlt
- `CHANGELOG.md`: abgeschlossene Änderungen je Version

Wer eine Aufgabe beginnt, verschiebt sie vom Backlog nach `IN_PROGRESS.md`; nach der Freigabe kommt sie ins `CHANGELOG.md`.
