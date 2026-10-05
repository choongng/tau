#!/bin/bash
# T0222: misplaced rule
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_long_helper_in_data_test_is_not_misplaced" \
  "$T::test_misplaced_on_disk_close_does_not_count_a_step"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
