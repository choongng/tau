#!/bin/bash
# T0477: the locked-test refusal offers both files in one check (R60)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_locked_test_refusal_with_a_new_failing_test_in_scope_offers_both_files_in_one_check
uv run pytest -q $T
uv run ruff check $F $T
