#!/bin/bash
# Audit 11: the no-source-quoting verdict names each flagged case's searched source
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_unquoted_cases_verdict_shows_flagged_source_text" \
  "$T::test_unquoted_cases_verdict_shows_each_named_case_source"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
