#!/bin/bash
# T0177: the harness runs and grades a second task (cobs) beside itc.
set -eu
H=/home/choong/tautest/itc-harness
# a COBS grader: reference adapter passes every case, a broken one fails some
python3 $H/grade_cobs.py --adapter $H/adapters/cobs_reference.py --json > /tmp/claude-1000/t0177.ref.json
python3 - <<'PY'
import json; g = json.load(open("/tmp/claude-1000/t0177.ref.json"))
assert g["total"] >= 40 and g["passed"] == g["total"], g
PY
if python3 $H/grade_cobs.py --adapter $H/adapters/cobs_broken.py --json > /tmp/claude-1000/t0177.bad.json; then echo "broken adapter passed"; exit 1; fi
python3 -c "import json; g=json.load(open('/tmp/claude-1000/t0177.bad.json')); assert 0 < g['passed'] < g['total'], g"
# launch.sh: third argument picks the task; default stays itc
d=$(bash $H/launch.sh --dry-run R99 qwen cobs)
echo "$d" | grep -q "empty /home/choong/cobs"
echo "$d" | grep -qF "Consistent_Overhead_Byte_Stuffing"
d=$(bash $H/launch.sh --dry-run R99 mimo)
echo "$d" | grep -q "empty /home/choong/itc"
echo "$d" | grep -qF "itc2008.pdf"
if bash $H/launch.sh --dry-run R99 mimo nope >/dev/null 2>&1; then echo "unknown task accepted"; exit 1; fi
# scored.sh v4 takes the task and refuses a wrong one (selftest)
bash .beagle/checks/runs/v4/selftest.sh
grep -q 'cobs' .beagle/checks/runs/v4/scored.sh
echo OK
