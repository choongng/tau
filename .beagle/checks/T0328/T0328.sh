#!/bin/bash
# R38 class 1: before founding, the found-first gate refuses agent whatever the setup-call count
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_found_first_gate_refuses_agent_before_founding" \
  "$T::test_found_first_gate_allows_agent_once_founded"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
