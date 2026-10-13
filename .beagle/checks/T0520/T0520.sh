#!/bin/bash
# T0520: workers and task workers may run `contract status`, `diff` and
# `run --operation` (the milestone check T0510 names), and the brief says so.
set -e
cd /home/choong/tautest/tau-wt-ops
uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "worker_guard_refuses_beagle_commands_and_beagle_reads or may_read_the_pursuit_but_not_change" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^17 passed'
