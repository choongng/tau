#!/bin/bash
# T0083: a never-opened setup milestone can be abandoned, and the .beagle refusal names how.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 3 \
  test_never_opened_setup_milestone_can_be_abandoned \
  test_worked_or_goal_milestone_abandon_is_still_refused \
  test_dot_beagle_scope_refusal_names_the_abandon_route
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
