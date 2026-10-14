#!/bin/bash
# T0557: a section is re-read only on evidence: an entry failing on 3 acceptance runs over
# distinct trees, an upheld dispute, or two live entries with one operation and input but
# different expects (refused by check); a re-read's listing is confined to its section's
# range; the second extraction (`contract diff`, `check --file`) is gone (incremental-contract.md task 4).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "reread_due_after_three_trees or reread_due_on_upheld_dispute or conflicting_expects_refused or reread_listing_outside_range_refused" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^4 passed'
! grep -nE 'sub == "diff"|_second_problems' src/beagle/contract.py src/beagle/cli.py
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
