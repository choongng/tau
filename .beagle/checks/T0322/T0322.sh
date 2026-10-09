#!/bin/bash
# R37 class 1: step-cap refusals give a broken check one notes rerun and point at the escalation
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_unchanged_route_escalation_says_the_last_check_failed" \
  "$T::test_check_broken_after_passing_steps_earns_one_notes_rerun" \
  "$T::test_regression_rerun_is_offered_once" \
  "$T::test_scope_read_refusal_names_the_escalation_when_split_or_stop" \
  "$T::test_stop_gate_names_escalated_task_options"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
