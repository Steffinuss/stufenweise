# Schrift „Stufenfibel“

Die Schrift ist abgeleitet von **Andika** (© SIL International, https://software.sil.org/andika/), lizenziert unter der SIL Open Font License 1.1 (`OFL.txt`).

Änderungen gegenüber Andika:

- Das kleine **l** hat als Grundform unten einen Bogen (Andika-Variante `cv39`). So ist es klar vom großen **I** zu unterscheiden. Das ist für das Lesen- und Schreibenlernen wichtig.
- Die Schrift enthält nur die Zeichen für Deutsch und Westeuropa (Basis-Latein, Latin-1, €, Anführungszeichen, Gedankenstrich).
- Keine Ligaturen (zum Beispiel kein verbundenes „fi“), damit jeder Buchstabe einzeln erkennbar bleibt.

Weil die OFL den Namen „Andika“ für veränderte Fassungen reserviert, heißt die Schrift „Stufenfibel“. Sie ist als WOFF direkt in `index.html` eingebettet. `build-stufenfibel.py` erzeugt die Dateien aus `Andika-Regular.ttf` und `Andika-Bold.ttf` (Google-Fonts-Ausgabe) mit fontTools.
