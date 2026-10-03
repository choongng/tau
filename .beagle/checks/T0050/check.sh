#!/bin/bash
# T0050: each run's .md Scorecard agrees with its scorecard.json on the counts.
set -eu
for R in R04 R05 R06; do
  H=/home/choong/tautest/itc-harness/runs/$R; f=dev-notes/itc-runs/$R.md
  python3 - "$H/scorecard.json" "$f" <<'P'
import json, re, sys
c = json.load(open(sys.argv[1])); md = open(sys.argv[2]).read()
block = md.split("## Scorecard", 1)[1].split("```")[1]
for key in ("tasks_total", "tasks_done", "commits", "founded", "uncommitted_files"):
    m = re.search(rf"^{key}\s+(\S+)", block, re.M)
    assert m, f"{sys.argv[2]}: no {key} in the Scorecard block"
    assert m.group(1) == str(c.get(key)), f"{sys.argv[2]}: {key} {m.group(1)} != json {c.get(key)}"
P
done
grep -q 'tasks_total' .beagle/checks/runs/scored.sh
echo OK
