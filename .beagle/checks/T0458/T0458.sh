#!/bin/bash
# T0458: under lean no driver text promises locks (R55)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_lean_switch_drops_lock_promises_from_driver_texts
uv run pytest -q $T
uv run ruff check $F $T
