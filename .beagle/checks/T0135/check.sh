#!/bin/bash
# R15 class 4: founding guidance names read-and-design milestones.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_found_first_note_names_known_answers_not_read_and_design" \
  "$T::test_founding_read_and_design_milestone_is_retitled_known_answers"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
