#!/bin/bash
# R15 classes 1 and 7: known-answers check importing unwritten code; cwd-relative cases load.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_amending_a_known_answers_check_to_run_the_cases_test_is_refused" \
  "$T::test_opening_with_a_check_that_imports_an_unwritten_module_outside_scope_is_refused" \
  "$T::test_not_done_on_a_missing_scoped_test_file_does_not_offer_a_new_done_when" \
  "$T::test_cases_first_note_says_to_open_the_data_beside_the_test" \
  "$T::test_not_done_with_a_cwd_relative_data_open_names_the_fix"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
