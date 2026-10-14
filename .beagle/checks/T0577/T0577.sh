#!/bin/bash
# T0577: the unnamed-source refusal also offers saving references/<name>.txt and citing the stem,
# the route tau's Slice: examples text teaches (T0567).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "unnamed_source_refusal_offers_references" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
