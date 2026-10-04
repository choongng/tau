#!/bin/bash
# R20 class 1: known answers locked with a cases test that could never pass.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_known_answers_close_refuses_a_cases_test_naming_absent_cases" \
  "$T::test_known_answers_close_refuses_a_cases_test_that_never_reads_expected" \
  "$T::test_known_answers_close_refuses_an_attribute_used_as_method_and_value"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
