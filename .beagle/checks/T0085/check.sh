#!/bin/bash
# T0085: the stale-report detector needs a non-zero failure count and knows Error: lines.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_report_with_zero_failed_is_not_a_failure_report \
  test_report_naming_an_error_is_a_failure_report
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
