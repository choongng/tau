#!/bin/bash
# Audit 10: a rejected done_when on an open task still runs the notes against the bound check
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_open_task_rejected_done_when_already_passes_runs_notes_on_bound_check" \
  "$T::test_open_task_rejected_done_when_amend_problem_runs_notes_on_bound_check" \
  "$T::test_open_task_rejected_done_when_unwritten_runs_notes_on_bound_check" \
  "$T::test_open_task_rejected_done_when_without_runnable_bound_check_still_refuses"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
