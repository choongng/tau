#!/bin/bash
# R33 class 3: escalation offers a notes-only call when only the close judge kept the task open
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_escalation_after_judge_only_stays_open_offers_notes_only_call" \
  "$T::test_escalation_does_not_offer_check_rewritten_to_bound" \
  "$T::test_repeated_escalation_refusal_names_notes_only_call"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
