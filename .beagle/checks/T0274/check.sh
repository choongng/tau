#!/bin/bash
# R32 classes 2 and 3: a rerun after a stays-open close carries the reason; known-answers brief names the right check file and the cases test's close requirement
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_rerun_after_stays_open_close_brief_carries_reason" \
  "$T::test_not_workable_after_stays_open_names_call_with_notes" \
  "$T::test_known_answers_note_names_check_file_not_yet_on_disk" \
  "$T::test_known_answers_brief_states_cases_test_must_load_data"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
