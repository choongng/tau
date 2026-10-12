#!/bin/bash
# T0454: retry note never says a killed worker reported back (R53)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_retry_note_after_killed_attempt_does_not_say_reported_back
uv run pytest -q $T
uv run ruff check $F $T
