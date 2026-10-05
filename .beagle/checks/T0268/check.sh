#!/bin/bash
# R31 class 1 (+3 beagle.py part): oracle-with-code judges only imported or named code, honours pending locks, names the narrowed-scope call
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_oracle_with_code_ignores_unimported_helper_under_tests_dir" \
  "$T::test_oracle_with_code_counts_pending_locks_of_same_task" \
  "$T::test_open_task_mixed_scope_refusal_names_narrowed_scope_call" \
  "$T::test_open_task_mixed_scope_narrowed_scope_runs_worker" \
  "$T::test_repeated_mixed_scope_refusal_says_locks_do_not_change_it"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
