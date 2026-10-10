#!/bin/bash
# R39 class 4: a call missing a required string argument is told the argument is missing
set -e
T=tests/test_tool_missing_argument.py
bash .beagle/checks/fix/named_tests.sh $T 3 \
  test_missing_path_names_the_missing_argument \
  test_missing_argument_lists_the_keys_the_call_carried \
  test_non_string_path_still_says_must_be_a_string
uv run pytest -q tests/test_coding_tools.py tests/test_tool_cut_off_arguments.py tests/test_tool_buffers.py
uv run ruff check src/tau_coding/tools.py $T
