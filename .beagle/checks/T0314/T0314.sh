#!/bin/bash
# R36 fix: a case's known-answer check requires each changed result field, not any one
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_case_results_drops_fields_equal_to_nested_inputs" \
  "$T::test_result_unquoted_requires_each_changed_field" \
  "$T::test_result_unquoted_passes_when_each_changed_field_quoted"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
