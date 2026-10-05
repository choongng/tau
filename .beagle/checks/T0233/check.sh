#!/bin/bash
# T0233: pursuit_plan repairs bare part labels; upstream note for amend --scope
set -e
T=tests/test_beagle_example_extension.py
grep -q "amend has no --scope" dev-notes/itc-runs/upstream.md
uv run pytest -q -x \
  "$T::test_plan_split_repairs_bare_label_titles" \
  "$T::test_plan_under_nonroot_refuses_part_duplicating_pending_task"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
