#!/bin/bash
# R18 class 3: known answers abandoned as duplicate of a superseded task; Cases first re-split with a passing check.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_abandon_of_a_known_answers_successor_as_duplicate_of_a_superseded_task_is_refused" \
  "$T::test_cases_first_names_cases_already_on_disk_instead_of_a_new_split"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
