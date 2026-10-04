#!/bin/bash
# R19 class 1: Found-the-pursuit milestone survived founding.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_founding_drops_a_found_the_pursuit_milestone"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
