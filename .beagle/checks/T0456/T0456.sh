#!/bin/bash
# T0456: locked-test refusal advice never names the refused call (R54)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_locked_test_refusal_for_a_lint_check_offers_a_scope_without_the_judged_module
uv run pytest -q $T
uv run ruff check $F $T
