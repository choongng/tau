#!/bin/bash
# R30 classes 2 and 5: worker test commands bounded below the worker cap; a cases test must compare the answers
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_habit_bounds_command_memory_below_worker_cap" \
  "$T::test_unreported_run_names_kill_during_own_command" \
  "$T::test_cases_test_refused_when_answers_never_compared"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
