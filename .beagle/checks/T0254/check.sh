#!/bin/bash
# T0254: locked files stay as locked; the known-answers note only when true
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_split_commit_restores_locked_file" \
  "$T::test_done_by_check_runs_on_locked_content" \
  "$T::test_step_restores_drifted_lock" \
  "$T::test_known_answers_note_not_said_when_test_imports_code" \
  "$T::test_known_answers_note_keeps_existing_import" \
  "$T::test_fix_task_brief_has_no_imports_none_note"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
