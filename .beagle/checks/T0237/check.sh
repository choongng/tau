#!/bin/bash
# T0237: known-answers close
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_known_answers_task_closes_done_when_proven_by_data_absence" \
  "$T::test_misplaced_gate_ignores_test_file_the_check_does_not_run"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
