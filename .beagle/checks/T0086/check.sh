#!/bin/bash
# T0086: a failed setup commit unstages only what founding staged.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 1 \
  test_failed_setup_commit_keeps_the_users_own_staging
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
