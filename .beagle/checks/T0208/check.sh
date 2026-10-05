#!/bin/bash
# T0208: R22 classes 6 and 8
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_done_by_does_not_leave_the_task_open_when_close_fails" \
  "$T::test_no_worker_for_an_open_task_with_empty_scope" \
  "$T::test_no_worker_when_the_check_passes_and_was_unproven" \
  "$T::test_sibling_check_ignores_a_path_named_only_in_a_title" \
  "$T::test_sibling_check_ignores_files_committed_by_a_done_task"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
