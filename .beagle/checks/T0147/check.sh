#!/bin/bash
# Audit 7 defect 6: a labelled verbatim quote is not found in the references.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_quoted_source_with_a_leading_label_is_found" \
  "$T::test_r15_cases_all_quote_the_reference"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
