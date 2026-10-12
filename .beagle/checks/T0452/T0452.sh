#!/bin/bash
# T0452: the step keeps the last non-empty worker report; the brief's Scope line is the call's scope (R52)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_step_result_keeps_last_nonempty_report test_brief_scope_line_is_call_scope
uv run pytest -q $T
uv run ruff check $F $T
