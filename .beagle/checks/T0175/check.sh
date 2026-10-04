#!/bin/bash
# Audit 9 defect on T0167: R17 docs clause unasserted.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_design_fold_keeps_r17_docs_milestone_beside_known_answers"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
