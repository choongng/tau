#!/bin/bash
# T0475: retry notes say 'read the references' only when the attempt read them (R59)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_retry_notes_say_read_the_references_only_when_the_attempt_read_them
uv run pytest -q $T
uv run ruff check $F $T
