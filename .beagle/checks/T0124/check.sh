#!/bin/bash
# R14 class 2: a done-by route for a part an earlier commit made pass; consistent refusals.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_part_whose_check_passes_on_a_done_tasks_commit_closes_done_by_it" \
  "$T::test_done_by_abandon_without_that_tasks_commit_is_refused" \
  "$T::test_already_passes_on_the_cases_test_offers_done_by_not_the_same_test" \
  "$T::test_pending_milestone_abandon_refusal_offers_no_new_route" \
  "$T::test_step_with_done_when_but_no_criteria_says_criteria_is_missing"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
