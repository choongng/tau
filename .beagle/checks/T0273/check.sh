#!/bin/bash
# R32 classes 1 and 4: data-route refusal runs the close's own checks, never re-proposes the bound check, keeps the notes; refusals lead with their call
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_data_route_open_task_names_unread_cases_instead_of_closing" \
  "$T::test_data_route_says_leave_done_when_out_when_equal_to_bound_check" \
  "$T::test_open_task_rejected_done_when_still_runs_notes" \
  "$T::test_data_route_refusal_leads_with_its_call"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
