#!/bin/bash
# T0560: a Slice: task's worker cannot read the code under test; a due re-read is offered as a
# `Slice: reread <source> <lines>` task; an upheld dispute opens a superseding slice (and is
# refused without the corrected value); the amend path is gone (incremental-contract.md task 7).
set -e
cd /home/choong/tautest/tau
E=examples/extensions/beagle.py
if grep -nE 'AMEND_TITLE|def _amend_check' "$E"; then echo "amend path still present"; exit 1; fi
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "slice_worker_refused_code_read or reread_due_offers_slice or upheld_dispute_supersedes or upheld_dispute_without_value_refused" | grep -qE '^[1-9][0-9]* passed(,| in)'
X | grep -qE '^[0-9]+ passed( in|,)'
