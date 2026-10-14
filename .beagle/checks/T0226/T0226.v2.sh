#!/bin/bash
# T0226: audit 11 follow-ups (v2: the cases-first holder tests went with cases-first in T0493;
# the whole suite is left to the checks that own it, so this one fits amend's 120 s)
set -e
T=tests/test_beagle_example_extension.py
if grep -q "18 of 20 hit the 31-turn cap" dev-notes/itc-runs/R24.md; then echo "R24.md still says 18 of 20"; exit 1; fi
grep -q "17 of 20 hit the 31-turn cap" dev-notes/itc-runs/R24.md
uv run pytest -q -x \
  "$T::test_unproven_refusal_first_line_is_a_complete_call_within_the_quote"
uv run ruff check examples/extensions/beagle.py "$T"
