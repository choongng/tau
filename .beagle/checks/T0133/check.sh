#!/bin/bash
# R15 class 2: escalation refusal names what the call lacks.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_escalation_names_the_missing_new_route_flag" \
  "$T::test_escalation_says_criteria_must_be_left_out_when_they_differ" \
  "$T::test_escalation_on_a_check_importing_an_unwritten_module_names_the_data_test"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
