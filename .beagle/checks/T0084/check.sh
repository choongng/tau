#!/bin/bash
# T0084: the post-compaction note carries the last pursuit_step result, and `next` is steered.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 3 \
  test_state_after_compaction_repeats_last_step_result \
  test_state_after_compaction_without_a_step_result_is_unchanged \
  test_bash_pursuit_next_is_steered_to_pursuit_step
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
