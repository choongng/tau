#!/bin/bash
# R43 fix: a check that selects no tests is not accepted as failing now
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_open_refuses_a_check_whose_selection_deselects_every_test test_collected_none_note_names_a_k_that_matched_nothing
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
