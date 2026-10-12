#!/bin/bash
# T0461: raw report with closing tool-call tags gets the stub (R55)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_raw_report_with_closing_tool_call_tags_gets_the_stub
uv run pytest -q $T
uv run ruff check $F $T
