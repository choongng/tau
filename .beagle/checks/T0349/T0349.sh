#!/bin/bash
# R40 class 3: the data-only bind keeps the driver's absent in-scope test when the rewrite already passes; a refusal after a rewrite names it
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_absent_test_kept_when_data_test_already_passes \
  test_already_passes_refusal_names_the_rewritten_check
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
