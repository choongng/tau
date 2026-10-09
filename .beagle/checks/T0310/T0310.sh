#!/bin/bash
# R36 fix: a new_route with rewritten criteria keeps the bound criteria and moves the new text to notes
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_new_route_changed_criteria_kept_and_moved_to_notes" \
  "$T::test_new_route_changed_criteria_with_bound_check_gets_unchanged_route_refusal"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
