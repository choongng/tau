#!/bin/bash
# T0465: under lean the ruff-over-root refusal names no locked tests (R57)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_ruff_over_root_refusal_names_no_locked_tests_when_none_are_locked
uv run pytest -q $T
uv run ruff check $F $T
