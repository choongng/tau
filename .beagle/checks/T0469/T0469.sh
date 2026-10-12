#!/bin/bash
# T0469: a cut-off kill note is not briefed as reference notes (R58)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_cut_off_kill_note_is_not_briefed_as_reference_notes
uv run pytest -q $T
uv run ruff check $F $T
