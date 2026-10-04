#!/bin/bash
# R19 class 3: design-only milestone kept as its own task when known answers exist.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_founding_folds_a_design_milestone_into_the_next_when_known_answers_exist"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
