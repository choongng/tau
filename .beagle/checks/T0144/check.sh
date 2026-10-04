#!/bin/bash
# Audit 7 defect 1: multi-line parts split only in one-part plans.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_plan_splits_a_multi_line_part_among_others" \
  "$T::test_plan_drops_rerun_only_line_in_a_multi_part_plan"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
