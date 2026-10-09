#!/bin/bash
# R35 fix: workers may not write tau's store under .git/beagle
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_scope_guard_refuses_writes_into_beagle_store" \
  "$T::test_worker_scope_guard_allows_task_log_named_in_brief"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
