#!/bin/bash
# R18 harness class: a breaker stop surfaced as a provider stream error, exit 1.
set -e
uv run pytest -q -x tests/test_agent_loop.py::test_cancel_between_turns_issues_no_further_request \
  tests/test_coding_session.py::test_breaker_stop_ends_as_aborted_with_its_reason
uv run pytest -q tests/test_agent_loop.py tests/test_agent_harness.py tests/test_coding_session.py tests/test_repeat_breaker_reset.py tests/test_agent_loop_turn_cap.py
uv run ruff check src/tau_agent src/tau_coding/session.py tests/test_agent_loop.py tests/test_coding_session.py
