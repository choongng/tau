#!/bin/bash
# R36 fix: the source-quote check reads a parenthesised quote after a file:line label
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_quotes_reference_finds_parenthesised_quote_after_file_line_label" \
  "$T::test_quoted_context_finds_parenthesised_quote" \
  "$T::test_unquoted_cases_verdict_shows_flagged_source_text" \
  "$T::test_bare_file_line_source_still_flagged_unquoted"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
