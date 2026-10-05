#!/bin/bash
# R30 class 1: a check killed at the cap on uncommitted scope code opens as a hang to find
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_open_proceeds_when_check_killed_on_uncommitted_scope_code" \
  "$T::test_new_route_does_not_rerun_killed_check" \
  "$T::test_check_timeout_scaled_from_recorded_duration" \
  "$T::test_guard_names_working_route_when_ready_task_cannot_open" \
  "$T::test_killed_note_names_non_finishing_code_when_earlier_run_was_fast"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
