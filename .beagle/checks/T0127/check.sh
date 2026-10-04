#!/bin/bash
# audit 6 defects 1-3: guard clauses no test covered.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_open_refuses_a_check_whose_command_is_missing" \
  "$T::test_open_refuses_a_check_that_prints_usage" \
  "$T::test_locked_test_imports_skips_a_test_that_reads_no_locked_data" \
  "$T::test_cases_test_reads_requires_the_read_to_name_the_file" \
  "$T::test_part_abandon_refusal_offers_done_by" \
  "$T::test_done_by_closes_a_pending_milestone"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
