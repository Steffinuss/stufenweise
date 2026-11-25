# Schrift „Stufenfibel“

Die Schrift ist abgeleitet von **Andika** (© SIL International, https://software.sil.org/andika/), lizenziert unter der SIL Open Font License 1.1 (`OFL.txt`).

Änderungen gegenüber Andika:

- Das kleine **l** hat als Grundform unten einen Bogen (Andika-Variante `cv39`). So ist es klar vom großen **I** zu unterscheiden. Das ist für das Lesen- und Schreibenlernen wichtig.
- Das große **I** ist ein einfacher senkrechter Strich ohne Querstriche oben und unten, die Ziffer **1** hat unten keinen Querstrich (so, wie in der Schule geschrieben wird). Andika hat dafür keine Variante; `schlichte_formen.py` zeichnet beide Formen um (25.11.2026). Vom l bleibt das I durch den Bogen am l klar verschieden.
- Die Schrift enthält nur die Zeichen für Deutsch und Westeuropa (Basis-Latein, Latin-1, €, Anführungszeichen, Gedankenstrich).
- Keine Ligaturen (zum Beispiel kein verbundenes „fi“), damit jeder Buchstabe einzeln erkennbar bleibt.

Weil die OFL den Namen „Andika“ für veränderte Fassungen reserviert, heißt die Schrift „Stufenfibel“. Sie ist als WOFF direkt in `index.html` eingebettet. `build-stufenfibel.py` erzeugt die Dateien (mit `schlichte_formen.py`) aus `Andika-Regular.ttf` und `Andika-Bold.ttf` (Google-Fonts-Ausgabe) mit fontTools.
