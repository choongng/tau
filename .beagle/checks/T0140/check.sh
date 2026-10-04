#!/bin/bash
# R16 classes 1-2: an unpassable known-answers check is re-run, and the escalation refuses its own proposed done_when.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_step_resend_of_open_task_refuses_check_importing_unwritten_module" \
  "$T::test_step_skips_second_attempt_when_check_imports_unwritten" \
  "$T::test_not_done_leads_with_unwritten_import_and_data_test_check" \
  "$T::test_escalation_takes_its_proposed_data_test_done_when_as_new_route" \
  "$T::test_escalation_refusal_repeats_the_full_working_call" \
  "$T::test_data_test_fallback_is_added_to_scope"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
