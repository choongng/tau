#!/bin/bash
# T0582: contract run --operation X is refused until a sealed X limits-and-invalid slice exists
# (R98 closed validation/rejection milestones on the examples slice alone); tau plans it from the refusal.
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "limits_slice_gate" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
cd /home/choong/tautest/tau && env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT -u UV_RUN_RECURSION_DEPTH \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed in'
env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT uv run --quiet pytest -q -p no:cacheprovider \
  tests/test_beagle_example_extension.py -k "limits_slice_gate" 2>&1 | tail -1 | grep -qE '^[1-9][0-9]* passed'
