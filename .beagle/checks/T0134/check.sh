#!/bin/bash
# R15 class 3: plan parts reach beagle with one multi-line 423-char title.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_plan_of_one_part_with_three_lines_is_split_into_parts" \
  "$T::test_plan_drops_a_rerun_only_line_with_a_note" \
  "$T::test_plan_of_one_part_on_a_leaf_is_refused_before_beagle" \
  "$T::test_plan_part_over_the_title_cap_is_cut_at_the_dash"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
