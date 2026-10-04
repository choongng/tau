#!/bin/bash
# R13 class 1: a check that cannot run (usage error, missing command, SyntaxError) is refused before any worker.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_step_refuses_a_check_that_exits_with_a_git_usage_error" \
  "$T::test_amend_refuses_a_check_with_a_python_syntax_error" \
  "$T::test_step_opens_a_check_that_fails_by_assertion"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
