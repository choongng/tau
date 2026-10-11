#!/bin/bash
# T0440: the cases-test own-algorithm rule does not fire on data loaders
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_cases_test_with_only_a_data_loader_is_not_an_own_copy test_cases_test_computing_results_with_own_function_is_still_an_own_copy
uv run pytest -q $T
uv run ruff check $F $T
