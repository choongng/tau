#!/bin/bash
# T0229: reference text line breaks
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_pdf_text_has_no_line_breaks_besides_newline" \
  "$T::test_fetched_reference_line_numbers_agree_for_split_and_splitlines"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
