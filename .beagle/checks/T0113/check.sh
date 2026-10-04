#!/bin/bash
# R12 class 2 (a, b): cases first is enforced at open; key-only json checks are refused.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_opening_a_new_source_module_before_a_locked_cases_test_is_refused" \
  "$T::test_opening_the_module_a_locked_cases_test_imports_is_allowed" \
  "$T::test_cases_first_gate_is_off_without_references" \
  "$T::test_key_only_json_done_when_is_refused"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
