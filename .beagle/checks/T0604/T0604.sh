#!/bin/bash
# T0604: the S02 smoke ran on the port (tau beagle-0.48 at or past fb3823e5,
# beagle 0.48.0 pinned), ended (exit.json), was graded (grade.json), and
# eval.md on the branch records it: an S02 table row and an "## S02" section.
set -euo pipefail
R=/home/choong/tautest/itc-harness/runs/S02
W=/home/choong/tautest/tau-wt-048
[ -f $R/exit.json ] && [ -f $R/grade.json ] || { echo "S02 not ended and graded" >&2; exit 1; }
python3 - $R/meta.json <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
assert m["task"] == "wrenfold" and m["mode"] == "pursuit", m
assert m["beagle_version"] == "beagle 0.48.0", m["beagle_version"]
assert m.get("tau_dirty_code_files") == 0, "dirty tau"
assert "/tau-harness/" in (m.get("tau_bin") or ""), m.get("tau_bin")
print(m["tau_sha"])
PY
sha=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tau_sha"])' $R/meta.json)
git -C $W merge-base --is-ancestor fb3823e5 "$sha" || { echo "S02 not on the port" >&2; exit 1; }
grep -qE '^\| S02 \|' $W/dev-notes/contract-first/eval.md
grep -qE '^## S02' $W/dev-notes/contract-first/eval.md
