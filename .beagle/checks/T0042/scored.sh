#!/bin/bash
# usage: scored.sh RNN — the run ran, exited, and its scorecard + grade are written.
set -eu
R=$1; H=/home/choong/tautest/itc-harness/runs/$R; f=dev-notes/itc-runs/$R.md
test -s "$H/exit.json"
python3 -c "import json; m=json.load(open('$H/meta.json')); assert m.get('session'), 'no session recorded'; assert m.get('tau_sha'), 'not launched by launch.sh'"
test -s "$H/scorecard.json"
test -s "$H/grade.json"
python3 -c "import json; c=json.load(open('$H/scorecard.json')); assert 'workers' in c, 'scorecard made without --meta'"
test -s "$f"
grep -q '^## Scorecard' "$f"
grep -qE '^grader: [0-9]+/[0-9]+' "$f"
echo OK
