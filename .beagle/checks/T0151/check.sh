#!/bin/bash
# R17 classes 2-3: an amend replaced a data-reading check with collect-only.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_amend_refuses_a_check_that_already_passes" \
  "$T::test_amend_refuses_a_collect_only_check" \
  "$T::test_amending_a_known_answers_check_to_one_that_reads_no_locked_file_is_refused" \
  "$T::test_not_done_names_a_missing_locked_file_as_the_work" \
  "$T::test_shell_operator_refusal_on_amend_says_the_bound_check_stands"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
