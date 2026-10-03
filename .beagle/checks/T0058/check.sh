#!/bin/bash
# T0058: abandoning a container's part as a duplicate is refused, with the move that keeps the container live.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 1 \
  test_duplicate_abandon_of_a_part_is_refused_because_it_stalls_its_container
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
