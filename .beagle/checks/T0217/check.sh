#!/bin/bash
# T0217: escalation working call
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_escalation_first_line_holds_the_working_call" \
  "$T::test_escalation_keeps_a_failing_bound_check_in_the_working_call" \
  "$T::test_working_call_names_scope_when_it_differs_from_the_record"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
