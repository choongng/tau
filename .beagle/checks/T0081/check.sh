#!/bin/bash
# T0081: the setup detector catches R10's dash-titled setup milestone.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_setup_milestone_titled_with_a_dash_and_naming_beagle_is_dropped \
  test_founding_r10_milestones_drops_only_the_setup_one
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
