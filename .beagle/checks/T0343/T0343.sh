#!/bin/bash
# R39 [harness]: the scorecard splits workers that ended without a reply by cause
set -eu
H=$HOME/tautest/itc-harness
want() {  # want RUN timed_out wall refusals cap
  local card
  card=$(python3 -c "import json;c=json.load(open('$H/runs/$1/scorecard.json'));print(c['session']);print(c['repo'])")
  python3 $H/scorecard.py --session "$(sed -n 1p <<<"$card")" --repo "$(sed -n 2p <<<"$card")" \
    --exit-json $H/runs/$1/exit.json --meta $H/runs/$1/meta.json --json | python3 -c "
import json, sys
w = json.load(sys.stdin)['workers']
got = [w.get(k) for k in ('timed_out', 'wall_timeouts', 'stopped_by_refusals', 'cap_killed')]
assert got == [$2, $3, $4, $5], f'$1: timed_out/wall/refusals/cap {got} != [$2, $3, $4, $5]'
"
}
want R39 6 1 4 1
want R35 4 1 3 0
echo OK
