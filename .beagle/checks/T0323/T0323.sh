#!/bin/bash
# R37 class 2: the unsourced-case verdict points at the reference lines holding each case's values
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_unquoted_verdict_points_at_the_lines_holding_case_values" \
  "$T::test_unquoted_verdict_says_when_no_line_holds_the_values"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
