#!/bin/bash
# R41 fix: a not-done step names a known-answers data test that imports code the tree does not have, and points at notes, not a new check
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_not_done_names_data_test_importing_unwritten_module test_data_test_import_next_is_notes_not_done_when
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
