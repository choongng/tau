#!/bin/bash
# R36 fix: the not-done escalation offers the notes rerun when only the close kept the task open
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_not_done_escalation_offers_notes_rerun_when_only_close_kept_open" \
  "$T::test_escalated_calls_offers_notes_rerun_when_only_close_kept_open" \
  "$T::test_not_done_escalation_text_matches_step_refusal"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
