#!/bin/bash
# R17 class 1: scopeless opens ran every worker unguarded.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_opening_a_task_with_no_scope_is_refused" \
  "$T::test_known_answers_open_with_locks_and_no_scope_names_the_scope_to_pass" \
  "$T::test_worker_of_a_known_answers_task_is_refused_a_write_to_source"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
