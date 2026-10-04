#!/bin/bash
# R14 class 4: construct-and-call checks; cases-module scope must run the locked cases test; no --absent for a pre-existing source.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_python_c_that_only_constructs_and_calls_is_refused" \
  "$T::test_python_c_with_an_assert_is_allowed" \
  "$T::test_part_scoping_the_cases_module_must_run_the_locked_cases_test" \
  "$T::test_prove_does_not_offer_absent_for_a_source_that_predates_the_task"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
