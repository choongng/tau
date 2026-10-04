#!/bin/bash
# T0200: R21 class 2 — escalation after an unproven pass
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_escalation_after_unproven_pass_keeps_the_bound_check_and_adds_the_data_file" \
  "$T::test_working_call_never_contains_a_placeholder" \
  "$T::test_proof_note_for_a_data_test_scoped_without_its_data_names_the_data_file"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
