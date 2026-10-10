#!/bin/bash
# R44 fix: the source rule judges a structured result whole
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_result_unquoted_requires_a_nested_result_not_one_scalar test_keep_sourced_omits_a_case_with_no_searchable_result
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
