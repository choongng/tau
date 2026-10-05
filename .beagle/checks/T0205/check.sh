#!/bin/bash
# T0205: R22 classes 1-2
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_pursuit_runs_beagle_under_the_memory_cap" \
  "$T::test_pursuit_timeout_kills_the_whole_process_group" \
  "$T::test_open_refuses_when_the_pre_run_was_killed_for_memory" \
  "$T::test_worker_killed_by_cap_says_so_after_a_nonempty_report"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
