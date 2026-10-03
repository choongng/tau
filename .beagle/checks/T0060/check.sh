#!/bin/bash
# T0060: a head-windowed read of a source file lists its def/class lines in the marker.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_tool_buffers.py 2 \
  test_cut_read_of_python_lists_definitions_with_line_numbers \
  test_cut_read_outline_is_bounded
.venv/bin/ruff check src/tau_coding/tool_buffers.py tests/test_tool_buffers.py
