#!/bin/bash
# T0567: a Slice: task may save its sources under references/ and is told how to name one
# for contract add (S01: the worker could not save the spec and wrote contract.json by hand).
set -e
cd /home/choong/tautest/tau
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "slice_scope_admits_references or slice_worker_saves_a_source" | grep -qE '^[1-9][0-9]* passed(,| in)'
X | grep -qE '^[0-9]+ passed( in|,)'
