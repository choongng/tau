#!/bin/bash
# T0062: founding commits beagle's setup files, so workspace-clean starts green.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_founding_commits_beagle_setup_files \
  test_founding_setup_commit_leaves_the_users_files_alone
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
