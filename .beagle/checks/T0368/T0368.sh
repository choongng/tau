#!/bin/bash
# Audit 13: progress.py's repo chain counts baseline runs, which move a repo aside too; baselines.md's two slips fixed
set -eu
H=/home/choong/tautest/itc-harness
python3 - "$H" <<'PY'
import pathlib, sys
sys.path.insert(0, sys.argv[1])
import progress
P = pathlib.Path
want = {  # runs ordered by start time across R and B: R39 B01 R40 B02 B03 R41
    "R39": P("/home/choong/cobs.r39"), "B01": P("/home/choong/cobs.b01"),
    "B03": P("/home/choong/cobs.b03"), "R41": P("/home/choong/cobs"),
    "R40": P("/home/choong/itc.r40"), "B02": P("/home/choong/itc"),
    "R38": P("/home/choong/itc.r38"),
}
got = {r: progress.repo_of(r) for r in want}
bad = {r: str(got[r]) for r in want if got[r] != want[r]}
assert not bad, f"repo_of wrong: {bad}"
print("repos OK")
PY
bash .beagle/checks/T0353/T0353.sh >/dev/null
f=dev-notes/itc-runs/baselines.md
grep -q "still running" $f && { echo "baselines.md still says R41 is running"; exit 1; }
grep -q "5-7 of 42-44" $f && { echo "baselines.md ceiling ignores gemma's 4/44"; exit 1; }
echo OK
