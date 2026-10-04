#!/bin/bash
# R17 classes 5 and 8: workers claimed files they never wrote; a preamble-only report was carried as notes.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_step_result_flags_report_paths_not_on_disk" \
  "$T::test_retry_note_flags_claimed_files_not_on_disk" \
  "$T::test_retry_note_skips_a_preamble_only_report"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
