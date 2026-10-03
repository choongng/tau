#!/bin/bash
# T0075: the scorecard tells the breaker's stop from a provider error, and counts only raw reports tau passed through.
set -eu
cd /home/choong/tautest/itc-harness
card() { python3 scorecard.py --session "$(python3 -c "import json;print(json.load(open('runs/$1/meta.json'))['session'])")" --repo "$2" --exit-json runs/$1/exit.json --meta runs/$1/meta.json --json; }
card R09 /home/choong/itc | python3 -c "
import json,sys; d=json.load(sys.stdin)
assert d['last_stop_by'] == 'breaker', d.get('last_stop_by')
assert d['workers']['raw_tool_call_reports'] == 0, d['workers']
assert d['workers']['raw_reports_replaced'] == 4, d['workers']
"
card R08 /home/choong/itc.r08 >/dev/null
echo OK
