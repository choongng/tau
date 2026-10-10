#!/bin/bash
# R43 fix: a known-answers test that passes without the code it imports is held
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_known_answers_close_holds_a_cases_test_that_passes_without_the_code test_open_on_a_locked_test_passing_without_its_module_offers_the_fix_split
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
