#!/bin/bash
# T0224: cases first names existing task
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_cases_first_names_the_live_task_holding_the_data_file"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
