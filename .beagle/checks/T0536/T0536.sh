#!/bin/bash
# T0536: `contract seal` runs the acceptance in a scratch tree that holds only
# the contract and the references, and refuses while an entry passes there:
# an entry that passes with no project code does not test the code (an
# 'invalid' entry expecting an error passes on the ImportError).
set -e
cd /home/choong/beagle-wt/rotation-fixes/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "passes_with_no_code or fails_every_entry_with_no_code" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
