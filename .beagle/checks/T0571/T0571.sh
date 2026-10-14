#!/bin/bash
# T0571: a Slice: task's seal on close is committed (slices added, draft removed), so the
# workspace stays clean after it (S01: the gate went red and its repair was refused).
set -e
cd /home/choong/tautest/tau
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "slice_seal_is_committed" | grep -qE '^[1-9][0-9]* passed(,| in)'
X | grep -qE '^[0-9]+ passed( in|,)'
