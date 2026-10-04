#!/bin/bash
# Audit 8 defect on T0147.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_r15_full_cases_file_all_quote_the_reference"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
