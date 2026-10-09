#!/bin/bash
# R36 fix: a repeating reasoning stream is cut early; the nudge sends thinking off
set -e
T=tests/test_session_output_limit.py
uv run pytest -q -x \
  "$T::test_reasoning_repetition_stops_turn_as_output_limit" \
  "$T::test_reasoning_without_repetition_is_not_cut" \
  "$T::test_output_limit_nudge_request_sends_thinking_off" \
  "$T::test_per_run_nudge_bound_skips_nudges_whose_reply_acted"
uv run pytest -q "$T" tests/test_coding_session.py
uv run ruff check src/tau_coding/session.py "$T"
