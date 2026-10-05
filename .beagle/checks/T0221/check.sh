#!/bin/bash
# T0221: module home
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_non_test_py_under_tests_is_refused_as_scope_with_a_root_module_call" \
  "$T::test_stub_beside_the_tests_is_not_a_written_module"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
