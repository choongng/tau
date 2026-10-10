#!/bin/bash
# R39 class 2: the brief's command bound sits below the worker's bash timeout; exit 124 is explained as a hang
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 3 \
  test_command_bound_is_below_worker_bash_timeout \
  test_habit_line_explains_exit_124_as_a_hang \
  test_retry_note_after_check_timeout_names_a_hang
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
