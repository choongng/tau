#!/bin/bash
# T0255: done-by closes only what the done task proves; pytest-form import-only checks refused
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_done_by_refuses_fix_of_done_task" \
  "$T::test_done_by_refuses_task_created_after_done_with_same_passing_check" \
  "$T::test_done_by_unwitnessed_does_not_offer_unrelated_data_file" \
  "$T::test_import_only_guard_catches_pytest_node_not_using_import" \
  "$T::test_witness_import_error_only_is_not_proof"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
