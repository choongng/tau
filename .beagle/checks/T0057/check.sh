#!/bin/bash
# T0057: waits routed through a dead heir are released on abandon and named with depend --drop.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_abandon_releases_a_wait_routed_through_its_heir \
  test_nothing_ready_names_the_drop_for_a_wait_on_a_stalled_heir
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
