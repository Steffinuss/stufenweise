#!/bin/sh
# Überträgt den Stand des Zweigs „entwicklung“ in das Schaufenster-Repository stufenweise-test.
# Aufruf: sh tests/testversion.sh /pfad/zur/kopie/von/stufenweise-test
# Dort wird nie direkt gearbeitet: Jeder Aufruf ersetzt alle Dateien durch den Stand von „entwicklung“
# und macht daraus einen neuen Commit (die Geschichte bleibt im Haupt-Repository).
set -e
ZIEL="$1"; QUELLE="$(cd "$(dirname "$0")/.." && pwd)"
[ -d "$ZIEL/.git" ] || { echo "Keine Git-Kopie: $ZIEL"; exit 1; }
STAND=$(git -C "$QUELLE" rev-parse --short entwicklung)
find "$ZIEL" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
git -C "$QUELLE" archive entwicklung | tar -x -C "$ZIEL"
{ printf '> **Testversion von Stufenweise** – Stand aus [Steffinuss/stufenweise](https://github.com/Steffinuss/stufenweise), Zweig `entwicklung` (%s). Nicht für den Unterricht. Hier nicht direkt arbeiten.\n\n' "$STAND"; cat "$ZIEL/README.md"; } > "$ZIEL/README.tmp" && mv "$ZIEL/README.tmp" "$ZIEL/README.md"
git -C "$ZIEL" add -A
git -C "$ZIEL" diff --cached --quiet && { echo "Keine Änderung."; exit 0; }
echo "Bereit zum Commit: Testversion aus entwicklung ($STAND)"
