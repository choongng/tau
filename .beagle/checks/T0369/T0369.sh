#!/bin/bash
# Audit 13: the cases-test close note never names the data test, even when the scope holds only it
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_cases_test_close_note_never_names_the_data_test_without_room
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
