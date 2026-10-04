#!/bin/bash
# R16 classes 3 and 5: plans put implementation before known answers; the cases-first hint nests a duplicate; waiting tasks don't name what they wait on.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_plan_refuses_implementation_before_known_answers" \
  "$T::test_cases_first_hint_points_to_existing_known_answers_sibling" \
  "$T::test_cases_first_hint_names_data_test_done_when" \
  "$T::test_step_on_waiting_task_names_what_it_waits_on"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
