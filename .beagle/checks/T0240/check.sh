#!/bin/bash
# T0240: pre-founding guard; clash covers the split task
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_dot_beagle_write_before_founding_names_pursuit_found" \
  "$T::test_plan_refuses_part_titled_as_the_split_task"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
