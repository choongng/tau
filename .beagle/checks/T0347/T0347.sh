#!/bin/bash
# R40 class 1: the known-answers verdict says to replace a case no reference gives a result for, and names result lines
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_known_answers_unsourced_result_says_replace_the_case \
  test_known_answers_unsourced_result_names_reference_result_lines
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
