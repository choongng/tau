#!/bin/bash
# T0066: pursuit_plan refuses a part that only re-runs or confirms a check.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_plan_refuses_a_part_that_only_reruns_a_check \
  test_plan_accepts_a_part_that_verifies_by_writing_a_test
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
