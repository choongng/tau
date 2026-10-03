#!/bin/bash
# T0072: bare-label titles take their title from the intent; a .beagle criterion is dropped at founding.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 3 \
  test_founding_milestone_with_a_bare_label_takes_its_title_from_the_intent \
  test_plan_part_with_a_bare_label_takes_its_title_from_the_intent \
  test_founding_drops_a_criterion_about_beagle_setup_with_a_note
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
