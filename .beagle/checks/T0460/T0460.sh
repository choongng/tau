#!/bin/bash
# T0460: import-only prove asks for a witness, not a new check (R55)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_import_only_not_proof_next_asks_for_a_witness_not_a_new_check
uv run pytest -q $T
uv run ruff check $F $T
