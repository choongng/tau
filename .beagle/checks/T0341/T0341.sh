#!/bin/bash
# R39 class 3: one pursuit_step is bounded by one step budget across its attempts
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_second_attempt_gets_remaining_step_budget \
  test_second_attempt_skipped_when_step_budget_spent
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
