#!/bin/bash
# Audit 11: a narrow result is not found by coincidence in the line after its quote
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_narrow_result_inside_a_larger_token_on_next_line_is_not_found" \
  "$T::test_result_unquoted_flags_all_four_r36_wrong_cases"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
