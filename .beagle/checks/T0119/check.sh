#!/bin/bash
# R13 class 2: a bare-&& check gets a move the driver can make; bash -c scripts are checked per segment.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_and_chain_refusal_quotes_the_one_segment_left" \
  "$T::test_and_chain_of_file_existence_tests_gets_the_file_objection" \
  "$T::test_bash_c_script_is_checked_segment_by_segment" \
  "$T::test_and_chain_of_real_checks_binds_as_bash_c" \
  "$T::test_operator_refusal_says_the_worker_writes_the_test"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
