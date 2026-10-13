#!/bin/bash
# T0555: each sealed slice ships standin/, code with every answer wrong; the seal refuses an
# contract/slices/NN-name append-only, a fix supersedes only an entry judged wrong, open
# entry that passes under every stand-in, fails for the load reason, is invalid yet passes,
# or a stand-in that names a contract file (incremental-contract.md task 2; T0549 option a).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "standin_pass_refused or standin_load_reason_refused or standin_invalid_pass_refused or standin_naming_contract_refused or standin_r97_fixture_refused" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^5 passed'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
