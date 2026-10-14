#!/bin/bash
# T0528: the worker wall does not count turns cut off at the output limit, and
# a worker is ended at its third cut-off, not its second. R91: 8d863128 was
# ended at its second 16384-token turn; 4dea9856 walled with two ~5 min turns.
set -e
cd /home/choong/tautest/tau
timeout 540 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "wall_does_not_count_cut_off_turns or not_ended_at_its_second_cut_off or cut_off_kill or reasoning_only_cut_off or second_output_cap or thinking_off_after_reasoning" 2>&1 \
  | tail -1 | tee /dev/stderr | grep -qE '^[0-9]+ passed, [0-9]+ deselected'
