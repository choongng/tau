#!/bin/bash
# T0464: cut-off kill note omits 'without acting' when the worker made calls (R56)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_cut_off_kill_note_omits_without_acting_when_the_worker_made_calls
uv run pytest -q $T
uv run ruff check $F $T
