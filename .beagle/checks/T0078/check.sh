#!/bin/bash
# T0078: dead waits on an abandoned leaf and an abandoned non-container heir, on R08's shape.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_dead_wait_on_an_abandoned_leaf_in_r08_shape \
  test_dead_wait_on_an_abandoned_non_container_heir_in_r08_shape
.venv/bin/ruff check tests/test_beagle_example_extension.py
