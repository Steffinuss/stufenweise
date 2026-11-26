#!/bin/sh
# Startet einen lokalen Webserver für die App und führt die wichtigsten Tests nacheinander aus.
# Aufruf aus dem Repository-Ordner:  sh tests/run_all.sh        (schnell)
#                                    sh tests/run_all.sh lang   (mit allen Arbeitsblättern und simulierten Kindern)
cd "$(dirname "$0")/.." || exit 1
PORT=${STUFENWEISE_PORT:-8766}
export STUFENWEISE_URL=${STUFENWEISE_URL:-http://localhost:$PORT/index.html}
if ! curl -s -o /dev/null "http://localhost:$PORT/version.json"; then
  python3 -m http.server "$PORT" --directory . >/dev/null 2>&1 &
  SERVER=$!; sleep 1.5
fi
FAST="fehler smoke einstellungen runden gefuehrt hinweis_neu springen antwortfeld feld_ueben ueberspringen update_hinweis wochenuebersicht lernort_material legeblaetter tausenderbuch_nachspuren arbeitsheft doppelte_zeilen grosse_aufgaben arbeitsblatt_optionen zehnerpartner_ueben durchsicht_0_21 oberflaeche_details test_fortschritt test_nie_haengen test_passt handy drittes_fach basis_grundlagen basis_blaetter basis_ueben basis_test zwanzigerfeld_zahl plusminus_ueben blatt_auswahl mehrere_fenster materialkiste qr_umzug druck_seiten hundertertafel_blaetter heft_zone_optionen konzentrationsmodus deutsch_optimierung mathe_material tafel_rueckmeldung satz_ziehen frei_stift heft_assistent"
SLOW="sweep zufallsklicks kinder_sim arbeitsblaetter heft_seiten_passen"
LIST=$FAST; [ "$1" = "lang" ] && LIST="$FAST $SLOW"
FAIL=0
for t in $LIST; do
  OUTP=$(timeout 600 python3 "tests/$t.py" 2>&1)
  if echo "$OUTP" | grep -q "Traceback\|ERR \[.\+\]"; then echo "FEHLER  $t"; echo "$OUTP" | tail -5; FAIL=1; else echo "ok      $t"; fi
done
# Zwanzigerfeld braucht die Fenstergröße als Argument
for size in "1180 820" "390 844"; do
  OUTP=$(python3 tests/zwanzigerfeld.py $size 2>&1)
  if echo "$OUTP" | grep -q "Traceback\|ERR \[.\+\]"; then echo "FEHLER  zwanzigerfeld $size"; FAIL=1; else echo "ok      zwanzigerfeld $size"; fi
done
[ -n "$SERVER" ] && kill "$SERVER"
exit $FAIL
