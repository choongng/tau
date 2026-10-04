#!/bin/bash
# R16 classes 4 and 6: case runner called implementation; not-done result swamped by the worker report.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_implementation_in_tests_lead_names_case_runner_not_implementation" \
  "$T::test_not_done_result_caps_last_report"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
