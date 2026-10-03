#!/bin/bash
# T0087: the implementation-under-tests lead is tested on every not-done branch.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 3 \
  test_not_done_step_names_implementation_written_under_tests \
  test_worker_problem_step_names_implementation_written_under_tests \
  test_prove_refused_step_names_implementation_written_under_tests
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
