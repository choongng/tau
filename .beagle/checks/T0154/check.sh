#!/bin/bash
# R17 class 6: pytest exit 5 shown raw.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_not_done_explains_pytest_exit_5_no_tests_collected" \
  "$T::test_retry_note_explains_pytest_exit_5"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
