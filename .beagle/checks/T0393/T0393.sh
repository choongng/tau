#!/bin/bash
# R44 fix: a text tool call without its opening tag is followed up
set -e
T=tests/test_session_template_tokens.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_text_tool_call_without_opening_tag_is_followed_up test_text_tool_call_follow_ups_are_bounded
uv run pytest -q $T tests/test_session_output_limit_nudge.py tests/test_tool_history.py
uv run ruff check src/tau_coding/session.py $T
