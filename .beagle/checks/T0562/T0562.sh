#!/bin/bash
# T0562 (point in time): the harness runs choong-dev's slice-flow extension against merged
# contract-first, and a short smoke (S01, q35, semver) founded, sealed the examples slice
# and reached code under it.
set -e
H=/home/choong/tautest/tau-harness
git -C $H merge-base --is-ancestor 040a2b33 HEAD
git -C $H diff --quiet choong-dev -- examples/extensions/beagle.py
R=/home/choong/tautest/itc-harness/runs/S01
python3 - "$R" <<'PY'
import json, sys
m = json.load(open(f"{sys.argv[1]}/meta.json"))
s = json.dumps(m)
assert "cde3fbd" in s or "contract-first" in s, "smoke did not run merged contract-first"
assert m.get("task") == "semver" or "semver" in s, "smoke was not semver"
PY
ls -d /home/choong/semver/contract/slices/01-* >/dev/null
git -C /home/choong/semver log --format=%H -- src | grep -q .
