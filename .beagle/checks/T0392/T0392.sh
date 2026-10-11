#!/bin/bash
# R44 fix: an open refuses a check whose exit code is a bool expression
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_open_refuses_a_python_c_check_with_a_bool_exit test_kept_bound_note_refuses_an_inverted_bound_check test_retry_note_omits_fix_the_work_when_the_output_names_no_failure
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
