#!/bin/bash
set -e
bash .beagle/checks/runs/v8/scored.sh R44 mimo itc
# the audit (10-10) found scored.sh checks neither thinking level
python3 - <<'PY'
import json, re, sys
m = json.load(open('/home/choong/tautest/itc-harness/runs/R44/meta.json'))
d = m.get('driver_thinking') or {}
if d.get('level') != 'medium' or not d.get('sent'): sys.exit(f"driver thinking not medium/sent: {d}")
if m.get('worker_thinking') != 'medium': sys.exit(f"worker thinking not medium: {m.get('worker_thinking')}")
note = open('dev-notes/itc-runs/R44.md').read()
if not re.search(r'driver_thinking\S*\s+medium|driver thinking\S*\s+medium', note, re.I): sys.exit("R44.md does not record the driver's thinking level")
if not re.search(r'worker\S* thinking\S*\s+medium|worker_thinking\S*\s+medium', note, re.I): sys.exit("R44.md does not record the workers' thinking level")
print("OK thinking")
PY
