#!/bin/bash
# T0077: a failed setup commit leaves nothing tau staged; both founding-failure tests run.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_founding_without_identity_says_setup_is_uncommitted \
  test_failed_setup_commit_leaves_nothing_staged
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
