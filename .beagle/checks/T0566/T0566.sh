#!/bin/bash
# T0566: `Slice: supersede <id>` is a slice kind with its own brief (one entry superseding a
# retired entry, at its cite, with the judged value), not the "names no slice kind" fallback.
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "supersede_slice_kind" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
