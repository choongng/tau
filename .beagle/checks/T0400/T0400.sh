#!/bin/bash
# Audit 14 fix: the argument-leak scan keeps its own pattern
set -e
T=tests/test_session_template_tokens.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_argument_scan_accepts_unopened_call_markup_in_a_write test_text_tool_call_without_opening_tag_is_followed_up
uv run pytest -q $T
uv run ruff check src/tau_coding/session.py $T
