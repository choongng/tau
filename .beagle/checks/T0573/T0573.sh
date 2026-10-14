#!/bin/bash
# beagle pursuit contract run --operation <op> (S01: milestones were checked by pytest alone).
set -e
cd /home/choong/tautest/tau
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "milestone_check_runs_contract_operation" | grep -qE '^[1-9][0-9]* passed(,| in)'
X | grep -qE '^[0-9]+ passed( in|,)'
