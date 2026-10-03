#!/bin/bash
# T0088: founding drops a milestone that only re-runs a check, with a note.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 1 \
  test_founding_drops_a_rerun_only_milestone_with_a_note
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
