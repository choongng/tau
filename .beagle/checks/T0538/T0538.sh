#!/bin/bash
# T0538: with no WITNESS from the worker, the extension's prove takes a file in
# the task's scope that changed since the task opened (not only one new since
# then) and puts back its content at the open, so a check an earlier, killed
# attempt made pass is still proven (R95: Reconcile superseded after 29 min).
set -e
cd /home/choong/tautest/tau
timeout 540 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "reverts_a_scope_file_changed_since_open or no_witness_and_no_change" 2>&1 \
  | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
