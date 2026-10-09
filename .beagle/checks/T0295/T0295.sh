#!/bin/bash
# T0295: gemma4-12b-q4 joins the rotation; each run records the driver's provider, model and thinking.
set -eu
H=/home/choong/tautest/itc-harness
d=$(bash $H/launch.sh --dry-run R99 gemma itc)
echo "$d" | grep -qF -- "--model gemma4-12b-q4"
echo "$d" | grep -qF "BEAGLE_TAU_DISPATCH_MODEL=gemma4-12b-q4"
# the dry run says what thinking the driver will get, and whether tau will actually send it
echo "$d" | grep -qE '^driver thinking: medium \(sent\)$'
d=$(bash $H/launch.sh --dry-run R99 qwen cobs)
echo "$d" | grep -qE '^driver thinking: [a-z]+ \((sent|NOT sent[^)]*)\)$'
if bash $H/launch.sh --dry-run R99 nope itc >/dev/null 2>&1; then echo "unknown model accepted"; exit 1; fi
# launch.sh writes the same facts into meta.json
grep -q '"driver_thinking' $H/launch.sh
grep -q '"provider"' $H/launch.sh
# scorecard reports the driver's thinking level and its reasoning volume (R35: level medium, nothing sent)
python3 $H/scorecard.py --session /home/choong/.tau/sessions/home-cobs-1460ee/551998c9d98b485c9c7e688d1ddc325a.jsonl \
  --repo /home/choong/cobs --meta $H/runs/R35/meta.json --json > /tmp/claude-1000/t0295.sc.json
python3 - <<'PY'
import json; s = json.load(open("/tmp/claude-1000/t0295.sc.json"))
assert s["driver_thinking_level"] == "medium", s.get("driver_thinking_level")
assert s["driver_reasoning_chars"] == 0, s.get("driver_reasoning_chars")
PY
# scored.sh v6 knows gemma and still refuses a wrong task/model (its selftest)
grep -qF 'gemma=gemma4-12b-q4' .beagle/checks/runs/v6/scored.sh
bash .beagle/checks/runs/v6/selftest.sh
echo OK
