#!/bin/bash
# T0223: kept done_when, new scope
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_step_with_same_done_when_names_the_scope_it_kept" \
  "$T::test_pending_locks_hold_only_tests_and_data"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
