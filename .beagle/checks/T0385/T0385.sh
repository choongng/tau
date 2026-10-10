#!/bin/bash
# R43 fix: the source hold offers only quotes its rule accepts, and names the cases already sourced
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_source_hold_offers_only_quotes_that_pass_the_rule test_source_hold_names_the_cases_already_sourced
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
