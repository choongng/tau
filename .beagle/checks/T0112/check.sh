#!/bin/bash
# R12 class 4: a split commits the open task's passing uncommitted work first.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_split_commits_passing_uncommitted_work_before_the_parts" \
  "$T::test_split_keeps_the_note_for_uncommitted_work_whose_check_failed"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
