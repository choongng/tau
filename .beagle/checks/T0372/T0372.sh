#!/bin/bash
# R41 fix: a worker killed for reasoning-only cut-offs says so, and the task's next worker runs thinking-off (owner 2026-10-10: off on retry)
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_reasoning_only_cut_off_named_in_worker_note test_next_attempt_runs_thinking_off_after_reasoning_cut_offs
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
