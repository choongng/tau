#!/bin/bash
# T0558: pursuit.md teaches the incremental contract: §1.5 runs gather, the examples
# slice, the work, later slices sealed just ahead of it, coverage; the ethos table has a
# row for sealing late; the contract brief gives each slice kind its own inventory
# (incremental-contract.md task 5).
set -e
W=/home/choong/beagle-wt/rotation-fixes
P=$W/plugins/beagle-pursuit/commands/pursuit.md
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "brief_slice_inventory_by_kind" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed'
if grep -niE 'second extraction|reconcile' "$P"; then echo "forbidden text present"; exit 1; fi
for w in 'contract seal --slice' 'standin/' 'contract coverage' 'REREAD due' 'supersedes'; do
  grep -qF -- "$w" "$P" || { echo "pursuit.md does not name: $w"; exit 1; }
done
grep -E '^\| *Sealing' "$P" | grep -qiE 'append-only' || { echo "no ethos-table row for sealing late"; exit 1; }
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
