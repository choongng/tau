#!/bin/bash
# Audit 7 defect 2: the python -c judge is skipped for uv run python, for pytest named in a string, and counts any sys.exit argument.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_check_refuses_uv_run_python_c_that_judges_nothing" \
  "$T::test_check_refuses_python_c_naming_pytest_only_in_a_string" \
  "$T::test_check_refuses_sys_exit_of_a_call_without_comparison"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
