#!/bin/bash
# T0539: when the driver drafts the founding criteria itself, the extension tells it
# to name what must pass and leave exact values to the contract (R94: a size bound
# written into the criteria contradicted the sealed contract).
set -e
cd /home/choong/tautest/tau
timeout 300 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "found_criteria_leave_values_to_the_contract" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed'
