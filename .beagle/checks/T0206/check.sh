#!/bin/bash
# T0206: R22 classes 3-4
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_cases_test_indexing_the_top_level_key_is_not_an_absent_case" \
  "$T::test_known_answers_close_locks_the_cases_test_beside_explicit_locks" \
  "$T::test_cases_first_offers_to_lock_a_committed_cases_test_instead_of_a_new_split" \
  "$T::test_cases_first_never_plans_known_answers_over_locked_data"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
