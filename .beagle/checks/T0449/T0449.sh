#!/bin/bash
# T0449: the own-copy refusal names only the functions the test computes results with (audit 2026-10-12)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_own_copy_refusal_names_only_the_computing_functions
uv run pytest -q $T
uv run ruff check $F $T
