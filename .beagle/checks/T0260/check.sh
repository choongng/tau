#!/bin/bash
# R29 classes 1,3: locks root-relative; cases-first plans never repeat the task title
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_step_locks_made_root_relative" \
  "$T::test_amend_accepts_check_naming_lock_given_absolute" \
  "$T::test_pending_locks_deduplicated_and_relative" \
  "$T::test_cases_first_carried_lock_matches_absolute_entry" \
  "$T::test_cases_first_on_known_answers_task_says_drop_code_from_scope" \
  "$T::test_cases_first_plan_never_repeats_task_title" \
  "$T::test_cases_on_disk_route_plan_never_repeats_task_title"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
