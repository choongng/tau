#!/bin/bash
# Worked example in the known-answers brief: one example case the source judge accepts and one counter-example it flags by result
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_known_answers_brief_has_worked_example test_worked_example_agrees_with_the_source_judge
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
