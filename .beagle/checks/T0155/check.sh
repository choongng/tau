#!/bin/bash
# R17 classes 7 and 9: a docs milestone was retitled as known answers; a split left the parent's pending locks behind.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_founding_does_not_retitle_a_docs_milestone_mentioning_design" \
  "$T::test_founding_does_not_retitle_when_a_known_answers_milestone_exists" \
  "$T::test_plan_split_moves_parent_pending_locks_to_first_part"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
