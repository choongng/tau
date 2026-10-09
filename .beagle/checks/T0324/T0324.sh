#!/bin/bash
# R37 class 3: a reply that writes a tool call as text gets a bounded follow-up
set -e
T=tests/test_session_template_tokens.py
uv run pytest -q -x \
  "$T::test_text_reply_with_tool_call_markup_is_followed_up" \
  "$T::test_text_tool_call_follow_ups_are_bounded" \
  "$T::test_reply_naming_the_tag_in_prose_is_not_followed_up"
uv run pytest -q tests/test_session_template_tokens.py tests/test_session_output_limit.py tests/test_session.py
uv run ruff check src/tau_coding/session.py "$T"
