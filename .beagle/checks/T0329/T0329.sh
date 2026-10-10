#!/bin/bash
# R38 class 2: arguments that are only _raw_arguments raise a ToolInputError naming the cut-off
set -e
T=tests/test_tool_cut_off_arguments.py
uv run pytest -q -x \
  "$T::test_cut_off_write_names_the_cut_off_not_the_path" \
  "$T::test_cut_off_bash_does_not_run" \
  "$T::test_parsed_arguments_still_reach_the_tool"
uv run pytest -q tests/test_coding_tools.py tests/test_tool_buffers.py tests/test_tool_history.py
uv run pytest -q tests/test_beagle_example_extension.py -k "cut_off or truncated"
uv run ruff check src/tau_coding/tools.py "$T"
