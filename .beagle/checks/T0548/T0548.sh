#!/bin/bash
# T0548: the contract check refuses an entry whose operation is an entry id, and a
# statement that duplicates another entry's (R97: Reconcile copied 56 entries with
# operation = their own id; the worker made `semver-NNN` importable to pass).
set -e
cd /home/choong/beagle-wt/rotation-fixes/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "check_refuses_an_operation_named_as_an_entry_id or check_refuses_a_duplicated_statement" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
