#!/bin/bash
# T0061: a python -c check importing a project module that is neither in scope nor on disk is refused.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_check_importing_a_module_outside_scope_and_disk_is_refused \
  test_check_importing_stdlib_or_an_existing_module_is_accepted
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
