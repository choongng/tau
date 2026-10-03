#!/bin/bash
# T0070
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_tool_buffers.py 3 test_cut_read_marker_names_file_lines_and_next_offset test_read_with_explicit_limit_fills_the_char_window test_cut_read_through_session_outline_carries_file_line_numbers
.venv/bin/ruff check src/tau_coding/tool_buffers.py src/tau_coding/session.py tests/test_tool_buffers.py
