#!/bin/bash
# R42 fix: the scorecard counts tau's reasoning-loop cuts apart from output-limit cut-offs, and the driver's re-prefill time
set -eu
H=/home/choong/tautest/itc-harness
out=/tmp/claude-1000/t0379
mkdir -p $out
for r in R41 R42; do
  s=$(python3 -c "import json;print(json.load(open('$H/runs/$r/meta.json'))['session'])")
  repo=$(python3 -c "import json;print(json.load(open('$H/runs/$r/meta.json'))['cwd'])")
  python3 $H/scorecard.py --session "$s" --repo "$repo" --exit-json $H/runs/$r/exit.json --meta $H/runs/$r/meta.json --json > $out/$r.json
done
python3 - $out <<'PY'
import json, sys
d = sys.argv[1]
r42 = json.load(open(f"{d}/R42.json")); r41 = json.load(open(f"{d}/R41.json"))
lc = r42.get("loop_cuts")
assert isinstance(lc, dict) and lc.get("driver") == 10, lc          # all 10 driver length stops were reasoning_loop_cut
assert r42.get("driver_reprocess_seconds", 0) > 300, r42.get("driver_reprocess_seconds")
w41 = r41["workers"]
assert w41["reasoning_cut_offs"] == 12 and w41["cut_off_killed"] == 6, w41   # R41's output-limit counts unchanged (T0371)
assert r42["workers"]["reasoning_cut_offs"] + r42["workers"].get("loop_cuts", 0) >= 3, r42["workers"]
print("OK")
PY
python3 -m py_compile $H/scorecard.py
