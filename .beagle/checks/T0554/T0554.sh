#!/bin/bash
# T0554: beagle's contract is sealed in slices: a draft is checked and moved into
# contract/slices/NN-name append-only, a fix supersedes only an entry judged wrong, open
# refuses a milestone over an operation no slice has sealed, and the single-file
# [contract] path/second mode is gone (incremental-contract.md, task 1).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "seal_slice_moves_draft or sealed_slice_edit_altered or add_after_seal_writes_draft or supersedes_needs_wrong or open_refuses_unsealed_operation or duplicate_statement_across_slices" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^6 passed'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
