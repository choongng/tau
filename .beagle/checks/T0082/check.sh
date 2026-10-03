#!/bin/bash
# T0082: the driver may not hand-edit .beagle files, and a long non-pursuit streak after founding is refused.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 4 \
  test_driver_write_or_edit_under_dot_beagle_is_refused \
  test_driver_bash_writing_dot_beagle_toml_is_refused \
  test_driver_reading_dot_beagle_is_allowed \
  test_driver_non_pursuit_streak_after_founding_is_refused
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
