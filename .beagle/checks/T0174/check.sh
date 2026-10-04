#!/bin/bash
# Audit 9 defect on T0171.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_an_implementation_task_naming_the_cases_cannot_hold_a_locked_file" \
  "$T::test_amend_refuses_a_scope_that_names_a_locked_file"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
