#!/bin/bash
# T0201: R21 classes 1 and 3
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_check_running_a_waiting_siblings_file_is_refused_at_open" \
  "$T::test_check_running_a_waiting_siblings_file_is_refused_at_amend_and_new_route" \
  "$T::test_not_workable_names_the_escalated_workable_tasks_working_call"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
