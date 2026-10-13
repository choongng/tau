#!/bin/bash
# T0537: the acceptance is asked to load each operation on its own and print the
# exception it caught, and `contract run` says when every failing entry fails
# for one reason (R94: 44 entries "module not found" sent the driver after pip).
set -e
cd /home/choong/beagle-wt/rotation-fixes/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "names_one_reason_every_entry_fails_for or asks_for_one_import_per_operation" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
