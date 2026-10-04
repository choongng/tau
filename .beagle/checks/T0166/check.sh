#!/bin/bash
# R19 class 2: setup task's .beagle refusal names no exit.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_beagle_dir_refusal_on_a_setup_task_says_abandon_it" \
  "$T::test_setup_task_can_be_abandoned_as_done_by_founding"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
