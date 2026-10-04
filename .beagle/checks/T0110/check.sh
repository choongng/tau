#!/bin/bash
# R12 class 1: a tests-only task proves through the module its tests import.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_tests_only_task_proves_by_mutating_the_imported_module" \
  "$T::test_tests_only_witness_in_test_file_names_the_imported_module_and_is_not_unproven" \
  "$T::test_new_route_passing_only_on_own_uncommitted_work_is_opened"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
