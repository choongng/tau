#!/bin/bash
# T0550: a task whose check passed on its first worker is proven and closed without a
# second worker being sent (R97 T0005: the first worker passed in 1.2 min, a second
# spent 9.5 min over a WITNESS).
set -e
cd /home/choong/tautest/tau
timeout 300 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "passed_check_is_proven_without_a_second_worker" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed'
