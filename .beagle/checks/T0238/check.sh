#!/bin/bash
# T0238: data test rebind and script-run tests
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_data_test_route_does_not_propose_the_importing_test_itself" \
  "$T::test_runs_test_file_sees_python_script_run"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
