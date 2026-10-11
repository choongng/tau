#!/bin/bash
# T0438: a split keeps its parts provable and hands each lock to the part that writes it
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_part_after_split_commit_proves_against_the_parents_opened_commit test_split_hands_each_lock_to_the_part_that_names_it test_split_lock_with_no_naming_part_goes_to_the_first
uv run pytest -q $T
uv run ruff check $F $T
