#!/bin/bash
# R36 fix: a tool call whose arguments carry chat-template tool-call tokens is refused
set -e
T=tests/test_session_template_tokens.py
uv run pytest -q -x \
  "$T::test_tool_args_with_template_tokens_refused" \
  "$T::test_tool_args_with_spilled_qwen_call_refused" \
  "$T::test_extension_tool_args_with_template_tokens_refused" \
  "$T::test_tool_args_with_ordinary_angle_brackets_run"
uv run pytest -q "$T" tests/test_coding_session.py tests/test_session_output_limit.py
uv run ruff check src/tau_coding/session.py "$T"
