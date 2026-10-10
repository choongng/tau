#!/bin/bash
# R40 class 2: a judge-only escalation offers a notes-only step naming cases and result lines, not a per-file split
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_judge_only_escalation_offers_no_split \
  test_judge_only_escalation_names_cases_and_result_lines
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
