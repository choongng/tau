#!/bin/bash
# R36 fix: worker-report markup check knows the pipe-delimited template forms
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_tool_call_markup_matches_channel_tokens" \
  "$T::test_report_before_markup_cuts_at_pipe_tool_call"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
