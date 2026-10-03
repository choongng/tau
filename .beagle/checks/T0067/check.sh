#!/bin/bash
# T0067: the data-with-code guard expands directory scopes against disk.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_step_refuses_directory_scopes_holding_unlocked_data_and_source \
  test_step_accepts_a_source_directory_alone
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
