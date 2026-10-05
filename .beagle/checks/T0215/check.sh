#!/bin/bash
# T0215: absolute scope
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_absolute_scope_under_root_is_matched_root_relative"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
