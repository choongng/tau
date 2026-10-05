#!/bin/bash
# T0230: amend keeps data-only bind
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_amend_binds_data_test_when_cases_test_not_on_disk" \
  "$T::test_amend_rebinds_data_test_when_cases_test_imports_unwritten_module"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
