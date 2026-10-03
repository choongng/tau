#!/bin/bash
# T0069: a closed-done result marks a worker report that claims failures as superseded.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_closed_done_step_marks_a_failing_report_superseded \
  test_closed_done_step_leaves_a_passing_report_alone
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
