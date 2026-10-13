#!/bin/bash
# T0541: seal runs the acceptance with no code; an entry that fails for a reason other
# than the code being absent never reached the code, and seal refuses naming it
# (R96: three invalid entries had prose inputs that eval could not parse).
set -e
cd /home/choong/beagle-wt/rotation-fixes/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "seal_names_an_entry_failing_codeless_for_another_reason" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed'
