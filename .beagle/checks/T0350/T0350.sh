#!/bin/bash
# R40 class 4: open refuses a check whose test file is absent and outside scope; not-done names it; the brief's scope line says outside writes are refused
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 3 \
  test_open_refuses_check_running_absent_file_outside_scope \
  test_not_done_names_absent_check_file_outside_scope \
  test_brief_scope_line_says_outside_writes_are_refused
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
