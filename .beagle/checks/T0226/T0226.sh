#!/bin/bash
# T0226: audit 11 follow-ups
set -e
T=tests/test_beagle_example_extension.py
if grep -q "18 of 20 hit the 31-turn cap" dev-notes/itc-runs/R24.md; then echo "R24.md still says 18 of 20"; exit 1; fi
grep -q "17 of 20 hit the 31-turn cap" dev-notes/itc-runs/R24.md
uv run pytest -q -x \
  "$T::test_unproven_refusal_first_line_is_a_complete_call_within_the_quote" \
  "$T::test_cases_first_names_a_holder_when_the_data_file_is_not_on_disk" \
  "$T::test_cases_first_holder_found_by_pending_locks"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
