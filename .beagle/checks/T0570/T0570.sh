#!/bin/bash
# T0570: every acceptance runs from the project root with BEAGLE_PROJECT_ROOT set, and seal
# runs it from its sealed place before accepting (S01: a draft-relative root broke once sealed).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "acceptance_runs_from_project_root or seal_runs_acceptance_where_sealed" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
