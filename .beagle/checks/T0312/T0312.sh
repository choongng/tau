#!/bin/bash
# R36 fix: a whole-tree scope does not get past the cases-first rule
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_cases_first_refuses_whole_tree_scope_on_known_answers_task" \
  "$T::test_worker_scope_guard_known_answers_refuses_new_source_module" \
  "$T::test_worker_scope_guard_known_answers_allows_test_helper"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
