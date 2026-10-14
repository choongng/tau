#!/bin/bash
# T0588: after the same refusal twice, beagle's refusal names one route that works; a milestone
# can be abandoned as a duplicate of another (R98 T0003: 13 refusals; T0585 cut 2).
set -eo pipefail
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 600 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/ \
  -k "repeated_refusal_route" \
  2>&1 | tail -1 | tee /dev/stderr | grep -E '^[1-9][0-9]* passed(,| in)' | grep -qv error
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
