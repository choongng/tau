#!/bin/bash
# R35 fix: the close's file and defect reach the rerun brief; not-done lead names the breaking import; brief no longer calls ImportError the goal
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_rerun_brief_carries_close_file_and_defect" \
  "$T::test_not_done_lead_names_failing_import" \
  "$T::test_known_answers_brief_import_error_is_a_defect"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
