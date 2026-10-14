#!/bin/bash
# T0493: the tau extension no longer carries cases-first (the known-answer cases file,
# its locks, the cases-first split refusals, the source judge), which the contract
# replaced and _cases_off already switched off whenever [contract] is declared.
set -e
cd /home/choong/tautest/tau
E=examples/extensions/beagle.py
! grep -nE '_cases_off|_cases_first_problem|CASES_DATA_SUFFIXES|_is_cases_data|_unread_cases|_cases_test_reads|Cases first: part' "$E"
env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[0-9]+ passed( in|,)' 
