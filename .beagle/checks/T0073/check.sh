#!/bin/bash
# T0073: a worker stopped by tau's breaker reports why, not "worker error".
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 1 \
  test_worker_stopped_by_the_breaker_reports_the_refused_call
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
