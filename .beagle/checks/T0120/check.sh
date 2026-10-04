#!/bin/bash
# R13 class 3: a task's deliverable scoped under the git-ignored references/ is refused.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_step_refuses_a_scope_under_references" \
  "$T::test_step_opens_a_scope_under_docs"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
