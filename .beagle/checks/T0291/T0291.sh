#!/bin/bash
# R35 fix: a data test importing unwritten code through a sibling test is seen by the import checks
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_imports_unwritten_follows_sibling_test_import" \
  "$T::test_self_import_note_names_chain_through_sibling_test" \
  "$T::test_kept_data_check_not_kept_when_data_test_imports_code_transitively"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
