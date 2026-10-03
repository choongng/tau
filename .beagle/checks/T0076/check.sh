#!/bin/bash
# T0076: the T0060 outline is tested through CodingSession and on prefixed read text.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_tool_buffers.py 2 \
  test_cut_read_through_session_outline_carries_file_line_numbers \
  test_outline_reads_line_numbers_from_a_prefixed_read
