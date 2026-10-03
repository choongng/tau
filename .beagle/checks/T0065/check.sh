#!/bin/bash
# T0065
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 test_already_passes_on_a_container_part_names_the_done_sibling test_already_passes_on_a_root_child_keeps_the_abandon_hint
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
