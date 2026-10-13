#!/bin/bash
# T0519: a close that seals the contract closes Reconcile done by the task that
# sealed it, and a contract milestone's done-by close takes the milestone's own
# scope and check, so it is proven to refuse with the second taken away (R85).
set -e
cd /home/choong/tautest/tau
uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "reconcile or seals_the_contract_once" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^4 passed'
echo "T0519: the seal closes Reconcile, and its done-by close is on its own check"
