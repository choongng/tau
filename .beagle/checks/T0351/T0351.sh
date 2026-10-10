#!/bin/bash
# R40 class 5: the cases-test close note never names the data test; the cases-test judge flags an in-file implementation
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_cases_test_close_note_never_names_the_data_test \
  test_cases_test_problem_flags_in_file_implementation
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
