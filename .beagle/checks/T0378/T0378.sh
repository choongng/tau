#!/bin/bash
# R42 fix: a nudge after a reasoning-loop cut keeps the session's thinking level
set -e
T=tests/test_session_output_limit_nudge.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_loop_cut_nudge_keeps_the_session_provider test_output_limit_cut_nudge_still_uses_the_thinking_off_twin
uv run pytest -q $T tests/test_session_output_limit.py tests/test_session_thinking_off_twin.py tests/test_coding_session.py
uv run ruff check src/tau_coding/session.py $T
