#!/bin/bash
# Harness check: launcher, hidden grader, scorecard extractor.
set -eu
H=/home/choong/tautest/itc-harness
echo "== 1. grader accepts the reference ITC and refuses a broken one"
python3 "$H/grade.py" --adapter "$H/adapters/reference.py" --json > /tmp/grade-ref.$$.json
python3 -c "import json,sys; d=json.load(open('/tmp/grade-ref.$$.json')); assert d['passed']==d['total'] and d['total']>=20, d"
if python3 "$H/grade.py" --adapter "$H/adapters/broken_join.py" --json > /tmp/grade-bad.$$.json; then
  echo "grader passed a broken join"; exit 1
fi
python3 -c "import json; d=json.load(open('/tmp/grade-bad.$$.json')); assert d['passed']<d['total'], d"
rm -f /tmp/grade-ref.$$.json /tmp/grade-bad.$$.json
echo "== 2. launcher dry-run names the model, the cap and the memory limit"
out=$("$H/launch.sh" --dry-run R98 mimo)
echo "$out" | grep -q -- '--model mimo-v2.6-9b-q4'
echo "$out" | grep -q 'MemoryMax='
echo "$out" | grep -q '3600'
out=$("$H/launch.sh" --dry-run R99 qwen)
echo "$out" | grep -q -- '--model qwen3.5-9b-q4-mtp-thinking-coding'
echo "== 3. scorecard extracts every field from the run-11e session"
python3 "$H/scorecard.py" --session /home/choong/.tau/sessions/home-itc-bf8992/65de1e87107c464695e78ee08e5640aa.jsonl --repo /home/choong/itc --json \
 | python3 -c "
import json,sys
d=json.load(sys.stdin)
need={'model','founded','found_attempts','tasks_done','tasks_abandoned','tasks_stalled','witnessed','commits','breaker_refusals','length_stops','compactions','ended','wall_minutes','tool_calls'}
missing=need-set(d)
assert not missing, missing
assert d['model'].startswith('qwen'), d['model']
assert d['founded'] is True, d
"
echo OK
