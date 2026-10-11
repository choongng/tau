#!/bin/bash
# T0437: data-only known-answers tasks get a sound witness
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_data_only_task_witness_in_cases_data_is_accepted test_absence_fallback_never_takes_away_a_file_the_check_names test_witness_resting_on_the_checks_own_script_is_refused
uv run pytest -q $T
uv run ruff check $F $T
