#!/bin/bash
# R12 class 2(c), recurred R14: cases.json sources must quote references/.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_close_keeps_cases_open_when_most_sources_quote_nothing" \
  "$T::test_close_accepts_cases_whose_sources_quote_references" \
  "$T::test_known_answers_guidance_asks_for_a_quoted_source"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
