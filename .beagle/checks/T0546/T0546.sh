#!/bin/bash
# T0546: beagle has a contract dispute verb: the judge brief holds the entry, its cited
# lines and its acceptance lines only; a verdict is recorded, an entry that did not FAIL is
# refused, and a re-seal keeps its reason (R96: a sealed test invented 319 for 81664).
set -e
cd /home/choong/beagle-wt/rotation-fixes/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "dispute_brief_holds_the_entry_its_cite_and_its_test or dispute_refuses_an_entry_that_did_not_fail or reseal_keeps_its_reason" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^3 passed'
