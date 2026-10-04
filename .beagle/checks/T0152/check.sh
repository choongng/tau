#!/bin/bash
# R17 class 4: T0008 closed done with its locked cases.json never written, proved by deleting code.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_close_refused_when_a_lock_is_not_on_disk" \
  "$T::test_prove_takes_away_locked_data_for_a_known_answers_task"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
