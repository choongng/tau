#!/bin/bash
# T0572: seal runs a right-answer (oracle) stand-in and refuses any example, limit or invalid
# entry that fails under it (S01: ex-015..017 crashed on KeyError under every stand-in and sealed).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "oracle_standin" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
