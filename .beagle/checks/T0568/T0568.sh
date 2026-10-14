#!/bin/bash
# T0568: workers may run --help and read-only beagle verbs (contract status/refs/check/run, doctor);
# mutating verbs stay refused (S01: --help and doctor were refused while add ran).
set -e
cd /home/choong/tautest/tau
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "worker_runs_help_and_read_only_verbs or worker_mutating_beagle_refused" | grep -qE '^[1-9][0-9]* passed(,| in)'
X | grep -qE '^[0-9]+ passed( in|,)'
