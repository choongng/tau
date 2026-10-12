#!/bin/bash
# T0453: done-by refusal of a scope-less call points back to the offered scope (R53)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_done_by_without_scope_offers_the_committed_source_the_check_targets_miss
uv run pytest -q $T
uv run ruff check $F $T
