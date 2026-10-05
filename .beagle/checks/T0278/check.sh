#!/bin/bash
# R33 classes 1 and 2: close judge counts path.open and with-as handles as reads; refuses a cases test with nothing to collect or a name it never imports
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_cases_test_reads_counts_path_open_and_with_as_handle" \
  "$T::test_cases_test_problem_names_no_collectable_test" \
  "$T::test_cases_test_problem_names_unimported_module_name"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
