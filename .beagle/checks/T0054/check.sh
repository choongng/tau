#!/bin/bash
# T0054: a milestone list that is only setup is seeded from the criteria, not refused.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 3 \
  test_founding_seeds_milestones_from_criteria_when_every_one_is_setup \
  test_r07_setup_only_milestone_founds_from_its_criterion \
  test_found_drops_setup_milestone_and_says_so
! grep -q "def test_founding_refuses_when_every_milestone_sets_the_pursuit_up" tests/test_beagle_example_extension.py
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
