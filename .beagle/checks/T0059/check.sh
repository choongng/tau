#!/bin/bash
# T0059: a step may not write known-answer data and source code together.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_step_refuses_a_scope_mixing_known_answer_data_with_source \
  test_step_accepts_known_answer_data_with_its_tests_only
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
