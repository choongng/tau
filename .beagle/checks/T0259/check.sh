#!/bin/bash
# audit 13: T0255's done-by ImportError-only branch tested
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_done_by_import_error_only_witness_is_released"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
