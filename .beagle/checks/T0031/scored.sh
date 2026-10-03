#!/bin/bash
# usage: scored.sh RNN — the run ran, exited, and its scorecard + grade are written.
set -eu
R=$1; H=/home/choong/tautest/itc-harness/runs/$R; f=dev-notes/itc-runs/$R.md
test -s "$H/exit.json"
python3 -c "import json; m=json.load(open('$H/meta.json')); assert m.get('session'), 'no session recorded'"
test -s "$H/scorecard.json"
test -s "$H/grade.json"
test -s "$f"
grep -q '^## Scorecard' "$f"
grep -qE '^grader: [0-9]+/[0-9]+' "$f"
echo OK
