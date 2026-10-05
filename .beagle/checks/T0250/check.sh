#!/bin/bash
# T0250: the data test imports no code, in brief and scope guard
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_known_answers_first_brief_says_data_test_imports_nothing" \
  "$T::test_known_answers_brief_omits_code_witness_note" \
  "$T::test_scope_guard_out_of_scope_import_from_data_test_says_remove_import" \
  "$T::test_not_run_call_does_not_carry_notes_restoring_self_import"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
