#!/bin/bash
# R14 class 1: the locked cases test must read the cases file.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_known_answers_task_whose_test_never_opens_the_cases_file_stays_open" \
  "$T::test_cases_test_naming_the_file_only_in_a_docstring_stays_open" \
  "$T::test_cases_test_that_json_loads_the_cases_file_is_locked"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
