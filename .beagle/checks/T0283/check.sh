#!/bin/bash
# R34 fix: lock refusal offers the scope minus locked files; call-scope rerun applies the lock check; fix tasks recognised by scope not title; nonexistent pytest node in an unwritable test file refused
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_locked_scope_refusal_offers_scope_without_locked" \
  "$T::test_call_scope_rerun_applies_lock_check" \
  "$T::test_known_answers_fix_recognised_by_scope" \
  "$T::test_missing_pytest_node_in_unwritable_file_refused"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
