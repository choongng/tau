#!/bin/bash
# T0527: a turn cut off at the output limit is replayed with its reasoning,
# and the nudge says so; a turn the reasoning-loop guard cut is not, and its
# nudge says that. R91: a q35 encode worker's next reply restarted a trace
# whose 16k tokens of reasoning had been dropped.
set -e
cd /home/choong/tautest/tau
timeout 540 uv run --quiet pytest -q -p no:cacheprovider \
  "tests/test_coding_session.py::test_session_continues_a_turn_cut_off_at_the_output_limit" \
  tests/test_session_output_limit.py tests/test_session_output_limit_nudge.py 2>&1 \
  | tail -1 | tee /dev/stderr | grep -qE '^[0-9]+ passed in'
