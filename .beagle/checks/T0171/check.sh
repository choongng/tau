#!/bin/bash
# R20 class 2: locked test in task scope; no exit for a wrong locked test.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_step_refuses_a_scope_that_names_a_locked_file" \
  "$T::test_known_answers_fix_task_may_hold_locked_files_and_relocks_them" \
  "$T::test_put_back_of_a_failing_locked_test_names_the_known_answers_route"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
