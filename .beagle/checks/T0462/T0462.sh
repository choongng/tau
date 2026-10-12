#!/bin/bash
# T0462: under lean no remaining driver text recommends locks= (audit of T0458)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_lean_uncommitted_note_and_oracle_hints_recommend_no_locks
uv run pytest -q $T
uv run ruff check $F $T
