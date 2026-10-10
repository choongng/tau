#!/bin/bash
# R41 fix: the scorecard counts output-limit cut-off kills apart from wall timeouts
set -eu
H=/home/choong/tautest/itc-harness
s=$(python3 -c "import json;print(json.load(open('$H/runs/R41/scorecard.json'))['session'])")
python3 $H/scorecard.py --session "$s" --repo /home/choong/cobs --exit-json $H/runs/R41/exit.json --meta $H/runs/R41/meta.json --json > /tmp/claude-1000/t0371.sc.json
python3 - <<'PY'
import json
w = json.load(open("/tmp/claude-1000/t0371.sc.json"))["workers"]
assert w.get("reasoning_cut_offs") == 12, w.get("reasoning_cut_offs")   # turns at the limit with reasoning and no text or call
assert w.get("cut_off_killed", 0) >= 5, w.get("cut_off_killed")
assert w["cut_off_killed"] + w["wall_timeouts"] + w["cap_killed"] == 7, (w["cut_off_killed"], w["wall_timeouts"], w["cap_killed"])  # R41 7 re-filed, not lost
assert w.get("cut_off_seconds", 0) > 1200, w.get("cut_off_seconds")   # the cut-off turns took ~30 min
print("OK")
PY
python3 -m py_compile $H/scorecard.py
