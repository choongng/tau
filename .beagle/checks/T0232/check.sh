#!/bin/bash
# T0232: brief states turn cap and reference sizes
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_brief_states_worker_turn_cap" \
  "$T::test_references_brief_states_line_counts_and_read_cost"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
