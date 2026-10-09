#!/bin/bash
# Audit 10: short or input-equal known-answer results are checked in their quoted context
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_short_result_checked_against_quoted_reference_line" \
  "$T::test_input_equal_result_checked_against_quoted_reference_line" \
  "$T::test_short_result_with_no_quoted_context_is_not_flagged"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
