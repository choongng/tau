#!/bin/bash
# R34 fix: a known-answer source must hold its expected result; a fix to a locked data file is provable; close and _already_passes agree
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_known_answer_source_must_hold_expected_result" \
  "$T::test_locked_data_fix_proved_by_putting_back_committed" \
  "$T::test_close_next_step_agrees_with_already_passes"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
