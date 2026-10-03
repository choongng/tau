#!/bin/bash
set -eu
H=/home/choong/tautest/itc-harness
S=$(python3 -c "import json;print(json.load(open('$H/runs/R02/meta.json'))['session'])")
python3 $H/scorecard.py --session "$S" --repo /home/choong/itc --meta $H/runs/R02/meta.json --json > /tmp/claude-1000/sc-T0030.json
python3 - <<'P'
import json; s=json.load(open('/tmp/claude-1000/sc-T0030.json'))
w=s['workers']; assert w['count']==17, w
for k in ('turns_max','capped','timed_out','reasoning_chars','empty_reports'): assert k in w, k
assert s['ended_with_abandoned'] is True, s.get('ended_with_abandoned')
print('OK')
P
