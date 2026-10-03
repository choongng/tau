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
python3 - "$H/scorecard.json" "$f" <<'PY'
import json, re, sys
c = json.load(open(sys.argv[1])); md = open(sys.argv[2]).read()
block = md.split("## Scorecard", 1)[1].split("```")[1]
for key in ("tasks_total", "tasks_done", "commits", "founded", "uncommitted_files"):
    m = re.search(rf"^{key}\s+(\S+)", block, re.M)
    assert m, f"no {key} in the Scorecard block"
    assert m.group(1) == str(c.get(key)), f"Scorecard {key} {m.group(1)} != scorecard.json {c.get(key)}"
g = json.load(open(sys.argv[1].replace("scorecard.json", "grade.json")))
m = re.search(r"^grader: (\d+)/(\d+)", md, re.M)
assert (int(m.group(1)), int(m.group(2))) == (g["passed"], g["total"]), f"grader line {m.group(0)} != grade.json {g['passed']}/{g['total']}"
PY
echo OK
