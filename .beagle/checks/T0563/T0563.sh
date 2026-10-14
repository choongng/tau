#!/bin/bash
# T0563: R71's and R73's real contracts (kept under .beagle/checks/T0498) are beagle test
# fixtures as sealed slices, so the anchor, short-quote, stand-in and coverage rules run on a
# real contract in beagle's own suite, not only in a retired check.
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
test -d tests/r71_itc && test -d tests/r73_itc
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "real_contract_slices_check_clean or real_contract_anchor_drift_refused or real_contract_coverage_counts" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
