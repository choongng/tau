#!/bin/bash
# T0466: an amended check passing on disk briefs the witness note, not the old demand (R57)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_amended_check_passing_on_disk_briefs_witness_note_not_old_demand
uv run pytest -q $T
uv run ruff check $F $T
